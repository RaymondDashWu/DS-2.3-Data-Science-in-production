# from flask_restplus import Api, Resource, fields, reqparse
from flask import Flask, jsonify, request
import pandas as pd
from functools import reduce

application = app = Flask(__name__)
# api = Api(app, version='1.0', title='MNIST Classification', description='CNN for Mnist')
# ns = api.namespace('Make_School', description='Methods')

df = pd.read_csv('multiTimeline.csv', skiprows = 1)
df.columns = ['month', 'diet', 'gym', 'finance']

@app.route('/', methods = ['GET'])
def get_trend():
    ls_year = request.args.getlist('n')
    ls_col = request.args.getlist('m')

    df_new = df[(reduce(lambda a, b: a | b, (df['month'].str.contains(s) for s in ls_year)))][['month'] + ls_col]

    df_new['month'] = pd.to_datetime(df_new['month'])
    df_new = df_new.sort_values(by = ['month'])

    return jsonify(df_new.to_json())
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)