import os
import socket
import json
import math
import time

# check if we have internet
def internet(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ).connect((host, port))
        return True
    except Exception as ex:
        return False
    
with open('speedtests.json', 'r') as log:
    past_data = json.load(log) or []
error_data = None

try:
    if internet():
        os.system('rm temp.json; touch temp.json')
        st_results = os.system('speedtest-cli --secure --json >> temp.json')
        with open('temp.json') as json_file:
            st_result_data = json.load(json_file)
        if st_result_data:
            st_result_data['download_mbps'] = math.floor(st_result_data['download'] / 1000000)
            st_result_data['upload_mbps'] = math.floor(st_result_data['upload'] / 1000000)
            st_result_data['local_timestamp'] = int(time.time())
            st_result_data['local_datetime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(st_result_data['local_timestamp']))
            with open('speedtests.json', 'w') as log:
                past_data.append(st_result_data)
                json.dump(past_data, log)
        else:
            error_data = {
                "status": "speedtest failed",
                "error_message": "no data returned from speedtest-cli"
            }
    else:
        error_data = {
            "status": "speedtest failed",
            "error_message": "no internet connection detected"
        }
except Exception as ex:
    error_data = {
        "status": "speedtest failed",
        "error_message": str(ex)
    }

message = "if you see this message, something went wrong"
if error_data:
    message = "internet speed test failed: " + error_data['error_message']
    with open('speedtests.json', 'w') as log:
        past_data.append(error_data)
        json.dump(past_data, log)

if (st_result_data):
    message = "download: " + \
    str(st_result_data['download_mbps']) + \
    " mbps, upload: " + \
    str(st_result_data['upload_mbps']) + \
    " mbps, datetime: " + \
    st_result_data['local_datetime']

with open('speedtests.log', 'a') as log:
    log.write(message + "\n")

print(message)