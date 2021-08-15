from flask import Flask
import Api.BackTest as BackTest
import Api.GetTechnicals as GetTechnicals
import Api.CompareStrategies as CompareStrategies
import Api.UpdateSeries as UpdateSeries
import Api.Scanner as Scanner
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

app.add_url_rule('/runBacktest', view_func=BackTest.run, methods=['GET'])
app.add_url_rule('/getTechnicals', view_func=GetTechnicals.getTechnicals, methods=['GET'])
app.add_url_rule('/compare/', view_func=CompareStrategies.compare, methods=['GET'])
app.add_url_rule('/updateSeries', view_func=UpdateSeries.update, methods=['POST'])
app.add_url_rule('/runScan/', view_func=Scanner.runScan, methods=['GET'])

if __name__ == '__main__':
    app.run(host="localhost", debug=True, use_reloader=True)
