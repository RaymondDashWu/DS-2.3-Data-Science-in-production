from keras.preprocessing.image import img_to_array
from keras.models import load_model
from flask_restplus import Api, Resource, fields
from flask import Flask, jsonify, request, make_response, abort, render_template, redirect, url_for
from firebase_admin import credentials, firestore, initialize_app
import datetime

import numpy as np
from werkzeug.datastructures import FileStorage
from PIL import Image
from keras.models import model_from_json
import tensorflow as tf

application = app = Flask(__name__)
api = Api(app, version='1.0', title='MNIST Classification', description='CNN for Mnist')
ns = api.namespace('Make_School', description='Methods')

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('mnist_responses')

single_parser = api.parser()
single_parser.add_argument('file', location='files', type=FileStorage, required=True)

# CNN model can be found here
# https://www.kaggle.com/raymonddashwu/ds2-2-hw2-mnist-mlp-cnn
model = load_model('mnist_cnn.h5')
graph = tf.get_default_graph()

@ns.route('/prediction')
class CNNPrediction(Resource):
    """Uploads your data to the CNN"""
    @api.doc(parser=single_parser, description='Upload an mnist image')
    def post(self):
        args = single_parser.parse_args()
        image_file = args.file
        image_file.save('img_1.jpg')
        img = Image.open('img_1.jpg')
        image_red = img.resize((28, 28))
        image = img_to_array(image_red)
        print(image.shape)
        x = image.reshape(1, 1, 28, 28)
        # x = image.reshape(1, 28, 28, 1)
        x = x/255
        # This is not good, because this code implies that the model will be
        # loaded each and every time a new request comes in.
        # model = load_model('my_model.h5')
        with graph.as_default():
            out = model.predict(x)
        print("out[0]", out[0])
        # print("out[1]", out[1])
        print(np.argmax(out[0]))

        # What will be shown in flask_restplus
        r = np.argmax(out[0])
        softmax_interval = np.around(model.predict(x)[0], decimals = 2)

        # id = request.json['id']
        # todo_ref.document(id).update(request.json)

        # Note: Sends response but only a random id
        # todo_ref.add(request.json)

        todo_ref.document().set({"Filename": str(image_file), "Time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "Prediction": int(r), "Activation": [float(x) for x in softmax_interval]})

        return jsonify({'prediction': "{} {}".format(r, softmax_interval)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)