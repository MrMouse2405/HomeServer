/* 
WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING 

This is purposefully written to be expoitable! Please do not use any of this code IRL!

WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING 
*/

console.log("[ChatApp] Ok I hackathon-level sped-run this codebase lmao. My bad if its trash.");
document.addEventListener('DOMContentLoaded',()=>{
    const connect_ip = '//'+location.host;
    var socket = io.connect(connect_ip);
    socket.on('connect',()=>
    {
        console.log(`[ChatApp] SocketIO Connected`)
        socket.emit('join',{})
        document.getElementById("conn-status").innerHTML = "CONNECTED!"
        document.getElementById("conn-status").style = "color: green;"
    })

    socket.on('disconnect',()=>
    {
        console.log(`[ChatApp] SocketIO Disconnected`)
        document.getElementById("conn-status").innerHTML = "DISCONNECTED!"
        document.getElementById("conn-status").style = "color: red;"
    })


    socket.on('message',data=>
    {
        console.log(`[ChatApp] Received Message from Server!`)        
        const p = document.createElement('p')
        p.innerHTML = `<span style="color:green">[${data.time_stamp}] &lt;<span style="color:${data.name_color}">${data.username}</span>&gt;</span> <span style="color:${data.text_color}">${data.message}</span>`
        // This is how it was originally implemented
        // document.querySelector('#display-message-section').append(p);

        // This stupid hack is here so that I can trick HTML into dynamically add script tags
        const scriptEl = document.createRange().createContextualFragment(p.outerHTML);
        document.querySelector('#display-message-section').append(scriptEl);

    })


    socket.on('update',data=>
    {
        console.log(`[ChatApp] Received Update from Server!`)
        document.getElementById("info-ip").innerHTML = connect_ip
        document.getElementById("info-servername").innerHTML = data.servername
        document.getElementById("info-servertime").innerHTML = data.servertime
        document.getElementById("info-uptime").innerHTML = data.uptime
        document.getElementById("info-connected").innerHTML = data.connected
        document.getElementById("info-version").innerHTML = data.version
        document.getElementById("info-security").innerHTML = data.security
        document.getElementById("serverconfig").innerHTML = JSON.stringify(data.serverconfig)
    })
    
    // Hack together an "enter" system
    document.querySelector('#user_message').addEventListener("keyup", event =>
    {
        if(event.key == "Enter")
        {
            event.preventDefault();
            document.querySelector('#send_message').click();
        }
    })

    //Send Message
    document.querySelector('#send_message').onclick = ()=>
    {
        const message = document.querySelector('#user_message').value
        if (message.trim() == ""){
            return;
        }
        
        console.log(`[ChatApp] Sending Message: ${message} `)
        socket.send( {'message':message, 'username': username, 'name_color':'black', 'text_color':'black'} )
        document.querySelector('#user_message').value = ""
    }
})
