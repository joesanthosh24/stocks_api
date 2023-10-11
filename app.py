from flask import Flask, jsonify, request

app = Flask(__name__)

stocks = [
    { 'name': 'Nasdaq', 'price': 13580.87, 'ticker': 'NDAQ' },
    { 'name': 'Dow Jones Industrial Average', 'price': 33658.77, 'ticker': 'DJIA' },
    { 'name': 'S&P 500 Index', 'price': 4352.70, 'ticker': 'SPX' }
]

@app.route('/')
def welcome():
    return '''
        <h1>Welcome to the Stocks API</h1>
        <a href="/stocks">View Stocks</a>
    '''

@app.route('/stocks')
def get_stocks():
    return jsonify(stocks)

@app.route('/stock', methods=['POST'])
def add_stock():
    data = request.json
    
    if data.get('name') and data.get('ticker') and data.get('price'):
        stocks.append(
            { 
                'name': data.get('name'), 
                'ticker': data.get('ticker'), 
                'price': data.get('price')
            }
        )

        return jsonify({'new_stock': stocks[len(stocks) - 1]})
    
    return jsonify("Missing Data")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)