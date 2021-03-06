from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt
import io


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://pcscbtvlgotbgr:50ddfceac3807eeb54429acb0afff0f27fb56d75fd16e8dc7430dc015c9bd24c@ec2-34-193-117-204.compute-1.amazonaws.com:5432/ddqn9iuu1258id"

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
  
    def __init__(self, username, password):
      self.username = username
      self.password = password
        
class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username", "password")

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/user/create", methods=["POST"])
def create_user():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    username_check = db.session.query(User.username).filter(User.username == username).first()
    user_id = db.session.query(User.id).filter(User.username == username).first()
    if user_id is not None:
      return jsonify("Username Taken")
    else:
      hashed_password = bcrypt.generate_password_hash(password).decode("utf8")

      record = User(username, hashed_password)
      db.session.add(record)
      db.session.commit()
      return jsonify("Successful")



@app.route("/user/get", methods=["GET"])
def get_all_users():
    all_users = db.session.query(User).all()
    return jsonify(users_schema.dump(all_users))

@app.route("/user/get/<id>", methods=["GET"])
def get_user_by_id(id):
    user = db.session.query(User).filter(User.id == id).first()
    return jsonify(user_schema.dump(user))

@app.route("/user/verification", methods=["POST"])
def verify_user():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    stored_password = db.session.query(User.password).filter(User.username == username).first()

    if stored_password is None:
        return jsonify("User has no paossword Verified")

    valid_password_check = bcrypt.check_password_hash(stored_password[0], password)

    if valid_password_check == False:
        return jsonify("User Passowrd Wrong Verified")

    return jsonify("User Verified")


if __name__ == "__main__":
    app.run(debug=True)