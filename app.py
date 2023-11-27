from flask import Flask,jsonify,request
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/search/*": {"origins": "http://localhost:3000"}})
app.config["MONGO_URI"] = "mongodb://localhost:27017/new"
mongo = PyMongo(app)
paintings_collection = mongo.db.paintings

@app.route('/submit', methods=['GET','POST','DELETE'])
def submit_form():
    global data
    data = request.json
    painting_name = data.get('paintingName')
    painting_id = data.get('paintingId')
    painter = data.get('painter')
    year = data.get('year')
    style = data.get('style')
    medium = data.get('medium')
    dimensions = data.get('dimensions')
    description = data.get('description')        

    new_painting = {
        'paintingName': painting_name,
        'paintingId': painting_id,
        'painter' : painter,
        'year' : year,
        'style' : style,
        'medium' : medium,
        'dimensions' : dimensions,
        'description' : description
    }

    try:
        inserted = mongo.db.paintings.insert_one(new_painting)
        if inserted:
            return jsonify({'message': 'Form data successfully inserted into MongoDB'}), 200
        
        else:
            return jsonify({'message': 'Failed to insert data into MongoDB'}), 500
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

# @app.route('/find/<search_term>',methods=['GET'])
# def get_result(search_term):
#     painting = mongo.db.paintings.find({'paintingID':search_term}, {'paintingName': 1})
#     if painting:
#         return jsonify(painting)
#     else:
#         return jsonify({'paintingName': None})
@app.route('/search/<painting_id>', methods=['GET'])
def get_painting_by_id(paintingId):
    try:
        # Find the painting in MongoDB based on the provided ID
        painting = paintings_collection.find_one({'paintingId': paintingId})
        
        if painting:
            # Return painting data as JSON response
            return jsonify(painting), 200
        else:
            return jsonify({'error': 'Painting not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500
# @app.route('/search/<painting_id>', methods=['GET'])
# def search_painting_by_id(painting_id):
#     painting = mongo.db.paintings.find_one({'paintingId': painting_id})
#     if painting:
#         return jsonify({
#             'paintingName': painting['paintingName'],
#             'year': painting['year']
#         })
#     else:
#         return jsonify({'message': 'Painting not found'}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method Not Allowed'}), 405
    
@app.route("/") #website URL
def hello_world():
     return "<p>sup!</p>"

if __name__ == '__main__':
    app.run(debug=True)

