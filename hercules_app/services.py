import requests

TMP_SERVERS_API = "https://api.truckersmp.com/v2/servers"
def get_servers_info():
    r = requests.get(TMP_SERVERS_API)
    servers = r.json()