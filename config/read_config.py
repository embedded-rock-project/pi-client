import json


with open('/'.join(__file__.split('/')[:-2]) + "/config.json") as f:
    config = json.load(f)
    server_base_url = config['server_url']
    discord_base_url = config['discord_webhook']