from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# @app.route('/')
# def index():
   
    

#     return "Hello"
@app.route('/')
def index():
    return "Index for Messages API"


@app.route('/messages', methods=['GET','POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by('created_at').all()
        message_dict = []
        for message in messages:
            message_dict.append(message.to_dict())

        response = make_response(
            jsonify(message_dict),
            200
        )

        return response
    elif request.method == 'POST':
        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username']
        )

        db.session.add(message)
        db.session.commit()

        response = make_response(
            jsonify(message.to_dict()),
            201
        )

        return response

@app.route('/messages/<int:id>', methods=['GET','PATCH', 'DELETE'])
def messages_by_id(id):

    message = Message.query.filter_by(id=id).first()
    
    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()
        response = make_response(
            jsonify(message_dict),
            200
        )
        return response
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()

        response_message = {
            "delete_successful": True,
            'message' :"Record successfully deleted."
        }
        response = make_response(
            jsonify(response_message),
            200
        )
        return response
        
        
        


# @app.route('/messages')
# def messages():
#     return ''

# @app.route('/messages/<int:id>')
# def messages_by_id(id):
#     return ''

if __name__ == '__main__':
    app.run(port=5555)
