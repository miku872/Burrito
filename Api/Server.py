from flask import Flask, make_response
import api.BackTest as BackTest
import api.GetTechnicals as GetTechnicals
import api.CompareStrategies as CompareStrategies
import api.UpdateSeries as UpdateSeries
import api.Scanner as Scanner
from flask_cors import CORS
import algo_trading.AlgoTrade as algotrader

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.add_url_rule('/runBacktest', view_func=BackTest.run, methods=['GET'])
app.add_url_rule('/getTechnicals', view_func=GetTechnicals.getTechnicals, methods=['GET'])
app.add_url_rule('/compare/', view_func=CompareStrategies.compare, methods=['GET'])
app.add_url_rule('/updateSeries', view_func=UpdateSeries.update, methods=['POST'])
app.add_url_rule('/runScan/', view_func=Scanner.runScan, methods=['GET'])

@app.route('/deployStrategy/', methods=['POST'])
def deployStrategy():
    # your logic here
    # response = {"result": []}
    response = make_response(algotrader.runAlgo())
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
    return response

if __name__ == '__main__':
    app.run(host="localhost", debug=True, use_reloader=True)

# @app.after_request
# def after_request(response):
#     header = response.headers
#     header['Access-Control-Allow-Origin'] = 'http://localhost:3000'
#     header['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
#     header['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,OPTIONS'
#     return response
#
# if __name__ == '__main__':
