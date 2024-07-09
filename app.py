from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    cf = fetch_conversion_factor(source_currency, target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount, 2)
    response = {
        "fulfillmentText": f"{amount} {source_currency} is {final_amount} {target_currency}"
    }
    return jsonify(response)

def fetch_conversion_factor(source, target):
    api_key = 'c36fea12f9bd825c1923be2a'  # Replace with your actual API key
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/pair/{source}/{target}'
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()['conversion_rate']

@app.route('/', methods=['GET'])
def home():
    return "Currency conversion service is running. Use POST method to convert currency."

if __name__ == '__main__':
    app.run(debug=True)