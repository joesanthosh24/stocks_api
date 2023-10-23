from flask import Flask, jsonify, request
from ariadne import load_schema_from_path, make_executable_schema, QueryType
from graphql_server.flask import GraphQLView

app = Flask(__name__)

stocks = [
    { 
        'name': 'Nasdaq', 
        'price': 50.60, 
        'ticker': "NDAQ"
    },
    { 
        'name': 'Dow Jones Industrial Average', 
        'price': 33127.28, 
        'ticker': "DJIA"
    },
    { 
        'name': 'S&P 500 Index', 
        'price': 4224.16, 
        'ticker': "SPX"
    }
]

detailedData = [
  {
    'ticker': 'NDAQ',
    'historical_price_data': [
        13,018.33,
        12,983.81,
        13,186.18,
        13,314.30,
        13,533.75
    ],
    'highest_price': 68.97, 
    'lowest_price': 46.88, 
    'trading_volume': 4046593000
  },
  {
    'ticker': 'DIJA',
    'historical_price_data': [
        32,936.41,
        33,127.28,
        33,414.17,
        33,665.08,
        33,997.65
    ], 
    'highest_price': 36799.65, 
    'lowest_price': 59.93, 
    'trading_volume': 330150558
  },
  {
    'ticker': 'SPX',
    'historical_price_data': [
        4,217.04,
        4,224.16,
        4,278.00,
        4,314.60,
        4,373.20
    ], 
    'highest_price': 4796.56, 
    'lowest_price': 4.40, 
    'trading_volume': 2737578858
  }
]

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
                'price': data.get('price'),
            }
        )

        return jsonify({'new_stock': stocks[len(stocks) - 1]})
    
    return jsonify("Missing Data")

@query.field("stocks")
def resolve_get_stocks(*_):
    return stocks

@query.field("detailedData")
def resolve_get_detailedData(_, info, ticker):
    for data in detailedData:
        if data['ticker'] == ticker:
            return data
        
    return None

schema = make_executable_schema(type_defs, query)
app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)