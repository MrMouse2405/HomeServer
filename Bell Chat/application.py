# https://github.com/ahmishra/Flask-ChatApp
from flask import Flask, render_template, redirect, url_for, flash  # type: ignore
from wtforms_fields import *
from models import *
from passlib.hash import pbkdf2_sha512
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room
from time import localtime, strftime
from datetime import datetime, timedelta
from collections import defaultdict
from time import sleep
from threading import Thread
import os

MUTED = []
CHAT_PROCESSORS = []
SERVER_START_TIME = datetime.now()
CONF = {
    "SERVER_NAME": "main1",
    "CHAT_MUTED": False,
    "CHAT_TIMEOUT": 0,
    "MAX_CHAT_LEN": 512,
    "XSS_SEC_LEVEL": 3,
    "SERVER_VERSION": "1.0.0",
}
timeouts = {}
app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db = SQLAlchemy(app)
socketio = SocketIO(app)
login = LoginManager(app)
login.init_app(app)
mode = 0

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/bellchat/", methods=["GET"])
def index():
    print(f"[SERVE PAGE] / - {datetime.now()}")
    return redirect("/login")


@app.route("/bellchat/register", methods=["GET", "POST"])
def register():
    print(f"[SERVE PAGE] /register - {datetime.now()}")
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data
        hashed_pwd = pbkdf2_sha512.hash(password)
        user = User(username=username, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash("Registered Successfully. Please login.")
        return redirect(url_for('login'))
    return render_template("register.html", form=reg_form, admin_key=ADMIN_KEY)


@app.route('/bellchat/login', methods=["GET", "POST"])
def login():
    print(f"[SERVE PAGE] /login - {datetime.now()}")
    if current_user.is_authenticated:
        return redirect(url_for('chat'))
    
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(
            username=login_form.username.data).first()
        login_user(user_object)

        return redirect(url_for('chat'))

    return render_template("login.html", form=login_form)


@app.route("/bellchat/chat", methods=["GET", "POST"])
# @login_required
def chat():
    print(f"[SERVE PAGE] /chat - {datetime.now()}")
    if not current_user.is_authenticated:
        print(f"[AUTH ERR] No Perms, Redirecting...")
        flash("Please Login!")
        return redirect(url_for('login'))

    return render_template('chat.html', username=current_user.username)


@app.route("/bellchat/logout", methods=["GET"])
def logout():
    print(f"[SERVE PAGE] /logout - {datetime.now()}")
    if not current_user.is_authenticated:
        print(f"[AUTH ERR] No Perms, Redirecting...")
        flash("Please Login!")
        return redirect(url_for('login'))
    
    try:
        del timeouts[load_user(current_user.id).id]
    except Exception:
        pass
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))


def send_message(username, message, name_color="black", text_color="black"):
    payload = {
        'message': f"{message}",
        'username': f"{username}",
        'time_stamp': str(datetime.now()),
        'name_color': f"{name_color}",
        'text_color': f"{text_color}",
    }
    send(payload, room="general"
    )
    print(f"[SERVER -> ALL] {payload}")


def send_self_message(username, message, name_color="black", text_color="black"):
    payload = {
        'message': f"{message}",
        'username': f"{username}",
        'time_stamp': str(datetime.now()),
        'name_color': f"{name_color}",
        'text_color': f"{text_color}",
    }
    send(payload)
    print(f"[SERVER -> CLIENT] {payload}")


@socketio.on('message')  # I coded this in 5 mins please be kind
def message(data):
    print(f"[CLIENT -> SERVER ] {data}")
    # Check if user is allowed to chat
    if not current_user.is_authenticated:
        flash("Please Login!")
        return redirect(url_for('login'))
    
    # Get & Check Content
    user = load_user(current_user.get_id())
    content = data.get("message", "ERROR: NO MESSAGE CONTENT")
    name_color = data.get("name_color", "black")
    text_color = data.get("text_color", "black")
    if user.username != ADMIN_USER:
        if CONF['CHAT_MUTED']:
            return send_self_message("System", f"Chat is now muted. Pay attention to the front!", name_color="red", text_color="red")
        if user.username in MUTED:
            return send_self_message("System", f"You are muted!", name_color="red", text_color="red")
        if len(content) > CONF['MAX_CHAT_LEN']:
            return send_self_message("System", f"Your message is too long! (max {CONF['MAX_CHAT_LEN']} characters)", name_color="red", text_color="red")
        if len(content) == 0:
            return
        if datetime.now() - timeouts[user.id] < timedelta(seconds=CONF['CHAT_TIMEOUT']):
            return send_self_message("System", f"You are sending messages too fast!", name_color="red", text_color="red")

    print(f"{data}")
    if content[0] == "/":
        if user.username != ADMIN_USER:
            return send_self_message("System", f"You do not have permission to send commands.", name_color="red", text_color="red")
        try:
            return process_command(content)
        except Exception as e:
            return send_self_message("System", f"Error: {e}", name_color="red", text_color="red")
    timeouts[user.id] = datetime.now()
    print(f"[MESSAGE] {user.username} -> {content}")
    return CHAT_PROCESSORS[CONF["XSS_SEC_LEVEL"]](user.username, content, name_color=name_color, text_color=text_color)
    # emit('some-event','this is a custom event message')
    

# Very Basic message processing
def process_message(username, data, **kwargs):
    return send_message(username, data, **kwargs)

# Lets just remove all script tags. ezpz
def process_message_v2(username, data, **kwargs):
    data = data.replace("<script>", "[SCRIPT DISABLED]")
    return send_message(username, data, **kwargs)

# Replace all places where "script" is used. That should fix it!
def process_message_v2_better(username, data, **kwargs):
    import re
    data = re.sub("script", "s crpt", data, flags=re.I)
    return send_message(username, data, **kwargs)

# Screw this! No tags at all!
def process_message_v2_better_final(username, data, **kwargs):
    data = data.replace("<", "[").replace(">", "]")
    return send_message(username, data, **kwargs)

# Here is one of the proper ways of doing this.
def process_message_proper_way(username, data, name_color="black", text_color="black"):
    from jinja2 import utils
    username = utils.escape(username)
    data = utils.escape(data)
    name_color = utils.escape(name_color)
    text_color = utils.escape(text_color)
    return send_message(username, data, name_color=name_color, text_color=text_color)

# Here is one of the proper ways of doing this.
def process_message_alternative_way(username, data, name_color="black", text_color="black"):
    import bleach
    username = bleach.clean(username)
    data = bleach.clean(data)
    name_color = bleach.clean(name_color)
    text_color = bleach.clean(text_color)
    return send_message(username, data, name_color=name_color, text_color=text_color)

def process_command(data):
    global CONF
    send_message("Admin", f"Command Sent By Admin Executed By Server", name_color="orange", text_color="orange")
    cmd, *args, key = data[1:].split(" ")
    if cmd == "whatisthekey":
        return send_self_message("KEY", f"{ADMIN_KEY}", name_color="gray", text_color="gray")
    if key != ADMIN_KEY:
        return send_self_message("System", f"Admin Check Failed", name_color="red", text_color="red")
    if cmd == "help":
        return send_self_message("System", f"help, stop, mutechat, muteuser, settimeout, setdifficulty", name_color="red", text_color="red")
    elif cmd == "stop":
        send_message("System", f"SERVER SHUTTING DOWN...", name_color="red", text_color="red")
    elif cmd == "mutechat":
        if not CONF["CHAT_MUTED"]:
            send_message("System", f"Chat is now muted. Pay attention to the front!", name_color="red", text_color="red")
            CONF["CHAT_MUTED"] = True
        else:
            send_message("System", f"Chat is now unmuted.", name_color="red", text_color="red")
            CONF["CHAT_MUTED"] = False
    elif cmd == "muteuser":
        mute_user = args[0]
        send_message("System", f"Toggled Mute for {mute_user}!", name_color="red", text_color="red")
        if mute_user in MUTED:
            MUTED.remove(mute_user)
        else:
            MUTED.append(mute_user)
    elif cmd == "settimeout":
        new_timeout = args[0]
        send_message("System", f"Global Chat Timeout Is Now {new_timeout} Seconds!", name_color="red", text_color="red")
        CONF["CHAT_TIMEOUT"] = int(new_timeout)
    elif cmd == "setdifficulty":
        new_diff = args[0]
        send_message("System", f"XSS Protection Is Now Set To {new_diff}", name_color="red", text_color="red")
        CONF["XSS_SEC_LEVEL"] = int(new_diff)

@socketio.on('join')
def join(data):
    user = load_user(current_user.get_id())
    print(f"{user.username} Connected")
    join_room("general")
    # Set up user
    if user.username == ADMIN_USER:
        send_self_message("System", f"Logged In As Admin!", name_color="red", text_color="red")
    timeouts[user.id] = datetime.now()
    send_self_message("BruinChat", f"Welcome to BruinChat, world's best chatting app!", name_color="olive", text_color="black")
    send_self_message("BruinChat", f"Look around and say hello! Make sure you do not hack ;)", name_color="olive", text_color="black")
    send_message("System", f"User [{user.username}] has joined the chat", name_color="red", text_color="blue")
    
def send_server_info_task():
    while True:
        socketio.sleep(1)
        # print("[UPDATE PING] sending...")
        try:
            with app.test_request_context('/'):
                emit('update', {
                    "servername": CONF["SERVER_NAME"], 
                    "servertime": str(datetime.now()),
                    "uptime": str(datetime.now()-SERVER_START_TIME),
                    "connected": len(timeouts),
                    "version": CONF["SERVER_VERSION"],
                    "security": CONF["XSS_SEC_LEVEL"],
                    "serverconfig": CONF
                }, room="general", namespace='/')
        except Exception as e:
            print(f"[UPDATE PING] Error: {e}")

if __name__ == "__main__":
    CHAT_PROCESSORS.append(process_message)
    CHAT_PROCESSORS.append(process_message_v2)
    CHAT_PROCESSORS.append(process_message_v2_better)
    CHAT_PROCESSORS.append(process_message_v2_better_final)
    CHAT_PROCESSORS.append(process_message_proper_way)
    CHAT_PROCESSORS.append(process_message_alternative_way)
    # CHAT_PROCESSORS.append(process_message_alternative_way)
    # CONF["XSS_SEC_LEVEL"] = len(CHAT_PROCESSORS) - 1
    print("Starting Server", os.environ.get('PORT', 8001))
    socketio.start_background_task(send_server_info_task)
    socketio.run(app, debug=False, port=int(os.environ.get('PORT', 8001)), host='0.0.0.0')
    # app.run(debug=True)
