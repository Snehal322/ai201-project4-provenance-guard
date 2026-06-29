import json
import os

LOG_FILE="audit_log.json"

def load_log():

    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE) as f:
        return json.load(f)

def save_entry(entry):

    log=load_log()
    log.append(entry)

    with open(LOG_FILE,"w") as f:
        json.dump(log,f,indent=2)

def get_log():
    return load_log()