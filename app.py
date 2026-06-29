from flask import Flask,request,jsonify

from detector import llm_signal
from audit import save_entry,get_log

import uuid
from datetime import datetime
import json

from stylometric import stylometric_score
from confidence import combine_scores,get_label

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app=Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://"
)

@limiter.limit("10 per minute;100 per day")


@app.route("/submit",methods=["POST"])
def submit():

    data=request.get_json()

    text=data["text"]
    creator=data["creator_id"]

    # result=json.loads(llm_signal(text))

    llm = json.loads(llm_signal(text))

    llm_score = llm["score"]

    style_score = stylometric_score(text)

    confidence = combine_scores(
        llm_score,
        style_score
    )

    attribution, label = get_label(confidence)

    content_id = str(uuid.uuid4())

    entry={
        
        "content_id": content_id,
        "creator_id": creator,
        "timestamp": datetime.utcnow().isoformat(),

        "attribution": attribution,
        "confidence": confidence,

        "llm_score": llm_score,
        "stylometric_score": style_score,

        "label": label,

        "status": "classified",

        "appeal_reasoning": None
    }

    save_entry(entry)

    # return jsonify({

    #     "content_id":content_id,

    #     "attribution":result["attribution"],

    #     "confidence":0.0,

    #     "label":"Placeholder label"

    # })

    return jsonify({

    "content_id":content_id,

    "attribution":attribution,

    "confidence":confidence,

    "label":label,

    "signals":{

        "llm_score":llm_score,

        "stylometric_score":style_score

    }

})

@app.route("/log")
def log():

    return jsonify({

        "entries":get_log()

    })

@app.route("/appeal", methods=["POST"])
def appeal():

    data = request.get_json()

    content_id = data["content_id"]
    reason = data["creator_reasoning"]

    log = get_log()

    found = False

    for entry in log:
        if entry["content_id"] == content_id:

            entry["status"] = "under_review"
            entry["appeal_reasoning"] = reason

            found = True
            break

    if not found:
        return jsonify({"error": "Content ID not found"}), 404

    with open("audit_log.json", "w") as f:
        json.dump(log, f, indent=2)

    return jsonify({
        "message": "Appeal submitted successfully.",
        "content_id": content_id,
        "status": "under_review"
    })



if __name__=="__main__":
    app.run(debug=True)


    '''

    user1:
    attribution": "likely_human",
  "confidence": 0.0,
  "content_id": "07305a9b-d73e-4004-b7f2-a7be75092ab2",
  "label": "Placeholder label"

user 2:
  "attribution": "likely_ai",
  "confidence": 0.0,
  "content_id": "864d4f8c-898b-4da5-b81d-c61f467158ad",
  "label": "Placeholder label"
  '''