from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Amount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=False)
    amount = db.Column(db.String, unique=False)

    def __init__(self, email, amount):
      self.email = email
      self.amount = amount

class AmountSchema(ma.Schema):
    class Meta:
        fields = ('email', 'amount')

amount_schema = AmountSchema()
amounts_schema = AmountSchema(many=True)


@app.route('/amount', methods=["POST"])
def add_amount():
    email = request.json['email']
    amount = request.json['amount']

    new_amount = Amount(email, amount)

    db.session.add(new_amount)
    db.session.commit()

    damount = Amount.query.get(new_amount.id)

    return amount_schema.jsonify(damount)

   
@app.route('/amounts', methods=["GET"])
def get_amounts():
    all_amounts = Amount.query.all()
    result = amounts_schema.dump(all_amounts)
    return jsonify(result)


@app.route("/amount/<id>", methods=["GET"])
def get_amount(id):
    damount = Amount.query.get(id)
    return amount_schema.jsonify(damount)



@app.route("/amount/<id>", methods=["PUT"])
def amount_update(id):
    damount = Amount.query.get(id)
    email = request.json['email']
    amount = request.json['amount']

    damount.email = email
    damount.amount = amount

    db.session.commit()
    return amount_schema.jsonify(damount)   


@app.route("/amount/<id>", methods=["DELETE"])
def amount_delete(id):
    damount = Amount.query.get(id)
    db.session.delete(damount)
    db.session.commit()

    return amount_schema.jsonify(damount)



if __name__== '__main__':
    app.run(debug=True)