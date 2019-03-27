from flask import Flask
app = Flask(__name__)

import tensorflow as tf

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

        return result.__repr__()

