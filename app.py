from flask import Flask, jsonify, request
from ariadne import load_schema_from_path, make_executable_schema, QueryType
from graphql_server.flask import GraphQLView

app = Flask(__name__)

stocks = [
    { 'name': 'Nasdaq', 'price': 13580.87, 'ticker': 'NDAQ' },
    { 'name': 'Dow Jones Industrial Average', 'price': 33658.77, 'ticker': 'DJIA' },
    { 'name': 'S&P 500 Index', 'price': 4352.70, 'ticker': 'SPX' }
]

detailedData = {
  'NDAQ': {
    'historical_price_data': [], 
    'highest_price': 1300, 
    'lowest_price': 800, 
    'trading_volume': 15
  },
  'DIJA': {
    'historical_price_data': [], 
    'highest_price': 1300, 
    'lowest_price': 800, 
    'trading_volume': 15
  },
  'SPX': {
    'historical_price_data': [], 
    'highest_price': 1300, 
    'lowest_price': 800, 
    'trading_volume': 15
  }
}

type_defs = load_schema_from_path("schema.graphql")

query = QueryType()

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

@query.field("stockData")
def resolve_get_historical_data(_, info, ticker):
    for stock in stocks:
        if stock[ticker] == ticker and detailedData[ticker]:
            return detailedData[ticker]
        
    return None

schema = make_executable_schema(type_defs, query)
app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)