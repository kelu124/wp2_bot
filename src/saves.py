from streamlit_javascript import st_javascript
import streamlit as st 
from datetime import datetime
import json, glob

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


def save_state(IP, STATE):
    to_save = {"IP": IP, 'content':{}}
    for k in STATE.keys():
        to_save["content"][k] = STATE[k]
    to_save["time"] = datetime.now().timestamp()
    txt = json.dumps(to_save)
    with open("cached_states/"+IP.replace(".","_")+"-"+str(int(datetime.now().timestamp()*1000))+".json", "w") as f:
        f.write(txt)



def load_state(IP):
    X = IP.replace(".","_")
    txt =  glob.glob("cached_states/*.json")
    print(X, txt)
    txt =  [x for x in txt if x.startswith("cached_states/"+X)]
    with open(sorted(txt)[-1], "r") as f:
        txt = f.read()
    A = json.loads(txt)
    # db.collection.find({key : 0}).sort({timestamp : -1}).limit(1)
    return A["content"]