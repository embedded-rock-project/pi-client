import json


# with open('/'.join(__file__.split('/')[:-2]) + "/config.json") as f:
with open('/'.join(__file__.split('/')[:-1]) + "/config.json") as f:
    config = json.load(f)
    server_base_url = config['server_url']
    server_ws_endpoint = config['server_ws_endpoint']
    discord_base_url = config['discord_webhook']