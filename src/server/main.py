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

    old_speed = content['speed']

    with tf.Session() as sess:
        x = tf.constant([[old_speed, -23.0], [1.0, 4.0]])
        w = tf.Variable(tf.random_uniform([2, 2]))
        y = tf.matmul(x, w)
        init_op = w.initializer
        sess.run(init_op)

        result = sess.run(y)

        print("old speed:", old_speed)
        return jsonify({
            "new_speed": old_speed * 2,
            "result": result.__repr__(),
        })
