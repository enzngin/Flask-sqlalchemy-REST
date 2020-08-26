from flask import Flask, jsonify,request,json
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/enes.zengin/Desktop/Users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

@app.route('/')
def index():
    return "-------"


#Create and add User
@app.route('/user', methods=['POST'])
def add_user():
  username = request.json['username']
  user = User(username)
  db.session.add(user)
  db.session.commit()
  
  users = User.query.all()
  return user_schema.jsonify(users)

  
#Get all Users
@app.route('/user')
def get_users():
    users = User.query.all()
    return user_schema.jsonify(users)


#Get single User
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.filter_by(id=id)
    return user_schema.jsonify(user)


#Update User
@app.route('/user/<id>',methods=['PUT'])
def update_user(id):
    user = User.query.filter_by(id=id).first()
    username = request.json['username']
    user.username = username
    db.session.commit()

    users = User.query.all()
    return user_schema.jsonify(users)


#Delete user
@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    users = User.query.all()
    return user_schema.jsonify(users)


#Filter by name
@app.route('/users/filter/<name>', methods=['GET'])
def filter_user(name):
    user = User.query.filter_by(username=name)
    return user_schema.jsonify(user)



class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))

    def __init__(self, username):
        self.username = username


#User Schema
class UserSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username')

#Init schema
user_schema = UserSchema()
user_schema = UserSchema(many=True)


#Driver function
if __name__ == '__main__':
    app.run(debug=True)
