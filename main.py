from flask import Flask, request
import json
from google.cloud import pubsub_v1
import os

app = Flask(__name__)

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(os.getenv("GCP_PROJECT"), "topic-a")

@app.route("/", methods=["POST"])
def index():
    envelope = request.get_json()
    if not envelope:
        return "No message received", 400

    name = envelope["name"]
    size = envelope["size"]
    content_type = envelope["contentType"]

    message = {
        "filename": name,
        "size": size,
        "type": content_type
    }

    publisher.publish(topic_path, json.dumps(message).encode("utf-8"))
    return "Message published", 200
