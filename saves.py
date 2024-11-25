from streamlit_javascript import st_javascript
import streamlit as st 
from datetime import datetime


def get_remote_ip():
    print("Getting IP")
    url = 'https://api.ipify.org?format=json'
    script = (f'await fetch("{url}").then('
                'function(response) {'
                    'return response.json();'
                '})')
    try:
        result = st_javascript(script)
        
        if isinstance(result, dict) and 'ip' in result:
            print("IP:" +result['ip'])
            return result['ip']
        else: return str(None)
    except: return str(None)


def save_state(IP, STATE, DB):
    to_save = {"IP": IP, 'content':{}}
    for k in STATE.keys():
        to_save["content"][k] = STATE[k]
    to_save["time"] = datetime.now().timestamp()
    DB.insert_one(to_save)
    print("STATE SAVED")

def load_state(IP, DB):
    # https://www.mongodb.com/community/forums/t/mongodb-query-select-all-documents-with-latest-timestamp/200064
    A = DB.find({"IP" : IP}).sort({"time" : -1}).limit(1)[0]
    # db.collection.find({key : 0}).sort({timestamp : -1}).limit(1)
    return A["content"]