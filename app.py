from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency'][0]['currency']
    amount = data['queryResult']['parameters']['unit-currency'][0]['amount']
    target_currency = data['queryResult']['parameters']['currency-name'][0]


    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount, 2)
    print(final_amount)
    response = {
        "fulfillmentText": "{} {} is {} {}".format(amount, source_currency, final_amount, target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source, target):
    # logic to fetch conversion factor from a database or API
    url = 'https://v6.exchangerate-api.com/v6/c36fea12f9bd825c1923be2a/pair/{}/{}'.format(source, target)
    response = requests.get(url)
    response = response.json()
    return response['conversion_rate']


if __name__ == '__main__':
    app.run(debug=True)