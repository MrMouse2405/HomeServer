"""

    Automatic Cloudflare Dynamic DNS Updating Daemon

    You can run this Daemon in background to monitor
    changes to your Dynamic DNS and automatically update
    your new public IP address to cloud flare

"""
import json
import logging
import os
import requests
import time

# Make sure to set this environment variables. Read documentation to know what I am talking about:
# https://api.cloudflare.com/#dns-records-for-a-zone-update-dns-record
ZONE_IDENTIFIER = os.getenv('CLOUD_FLARE_ZONE_IDENTIFIER')
IDENTIFIER = os.getenv('CLOUD_FLARE_IDENTIFIER')
CLOUD_FLARE_AUTHENTICATION_EMAIL = os.getenv('CLOUD_FLARE_AUTHENTICATION_EMAIL')
CLOUD_FLARE_GLOBAL_AUTH_KEY = os.getenv('CLOUD_FLARE_GLOBAL_AUTH_KEY')

# REPLACE THIS WITH YOUR RECORD NAME!!!
RECORD_NAME = None

# Services
ICANHAZ_URL = "https://ipv4.icanhazip.com"
CLOUDFLARE_URL = f"https://api.cloudflare.com/client/v4/zones/{ZONE_IDENTIFIER}/dns_records/{IDENTIFIER}"

# Cloudflare param
CLOUDFLARE_HEADERS = {
    'Content-type': 'application/json',
    'Accept': 'text/plain',
    'X-Auth-Email': CLOUD_FLARE_AUTHENTICATION_EMAIL,
    'X-Auth-Key': CLOUD_FLARE_GLOBAL_AUTH_KEY,
}
CLOUDFLARE_PARAMS = {
    'type': 'A',
    'name': RECORD_NAME,
    'content': None,
    'ttl': '3600',  # every hour
    'proxied': True,  # Cloud Flare proxy?
}

# Variables
LAST_PUBLIC_IP = ""


def get_current_public_ip():
    return requests.get(url=ICANHAZ_URL).text


def publish_public_ip(current_public_ip):
    CLOUDFLARE_PARAMS['content'] = current_public_ip
    r = requests.put(url=CLOUDFLARE_URL, data=json.dumps(CLOUDFLARE_PARAMS), headers=CLOUDFLARE_HEADERS)
    logging.info('CLOUD FLARE DNS RECORD UPDATE RESPONSE:', r.json())


while True:

    CurrentPublicIP = get_current_public_ip()

    if CurrentPublicIP != LAST_PUBLIC_IP:
        publish_public_ip(CurrentPublicIP)

    time.sleep(3600)
