from flask import Flask
app = Flask(__name__)

import tensorflow as tf
import json

@app.route("/")
def hello():
    with tf.Session() as sess:
        x = tf.constant([[37.0, -23.0], [1.0, 4.0]])
        w = tf.Variable(tf.random_uniform([2, 2]))
        y = tf.matmul(x, w)
        output = tf.nn.softmax(y)
        init_op = w.initializer

        sess.run(init_op)

        result = sess.run(y)

        return json.dumps({
            "a": result.__repr__(),
            "b": [1,2,3],
            "c": {
                "A": "hello",
            }
        })

from flask import Flask, request, jsonify

@app.route('/api/', methods=['GET', 'POST'])
def add_message():
    content = request.json
    print("old speed:", content['speed'])
    return jsonify({"new_speed":content["speed"] * 2})

import requests
res = requests.post('http://localhost:5000/api/', json={"speed":10})
if res.ok:
    print(res.json())
