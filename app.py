from flask import Flask, request, render_template
from scripts.predict import predict
from scripts.model import *
from scripts.raw import get_raw
from sklearn.ensemble import GradientBoostingClassifier


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/score/', methods = ['POST'])
def predict_page():

    prediction, proba = predict()
    proba0 = np.around(proba[0][0], decimals=5)
    proba1 = np.around(proba[0][1], decimals=5)

    return render_template('predict.html', prediction=prediction[0], proba0=proba0, proba1=proba1)

@app.route('/report/', methods = ['GET'])
def report_page():
    return render_template('workflow.html')

@app.route('/image/', methods = ['GET'])
def report_page():
    return render_template('image.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
