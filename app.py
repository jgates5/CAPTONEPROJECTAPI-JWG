from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt
import io


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://exxqadfxlgzanx:30c0270c0c2c28c62b51524fbacd51d0a8f1e8ce1e1a50ddbd2ce13c14a04985@ec2-18-214-119-135.compute-1.amazonaws.com:5432/d5fhhq1fhprqfc"

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)
bcrypt = Bcrypt(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
      

    def __init__(self, username, password):
      self.admin = username
      self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "admin", "password")


user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route("/admin/create", methods=["POST"])
def create_admin():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    admin = post_data.get("admin")
    password = post_data.get("password")
    
    if username_check is not None:
      return jsonify("Admin Taken")

    hashed_password = bcrypt.generate_password_hash(password).decode("utf8")

    record = User(username, hashed_password)
    db.session.add(record)
    db.session.commit()

    return jsonify("Admin Created Successfully")

    @app.route("/admin/get", methods=["GET"])
def get_all_admin():
    all_admin = db.session.query(User).all()
    return jsonify(users_schema.dump(all_users))

@app.route("/admin/get/<id>", methods=["GET"])
def get_dmain_by_id(id):
    user = db.session.query(User).filter(User.id == id).first()
    return jsonify(user_schema.dump(user))

@app.route("/admin/verification", methods=["POST"])
def verify_admin():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    post_data = request.get_json()
    username = post_data.get("username")
    password = post_data.get("password")

    stored_password = db.session.query(User.password).filter(Admin.admin == admin).first()

    if stored_password is None:
        return jsonify("User NOT Verified")

    valid_password_check = bcrypt.check_password_hash(stored_password[0], password)

    if valid_password_check == False:
        return jsonify("Admin NOT Verified")

    return jsonify("admin Verified")



if __name__ == "__main__":
    app.run(debug=True)