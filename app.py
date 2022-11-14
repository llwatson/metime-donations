from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Amount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=False)
    content = db.Column(db.Float, unique=False)

    def __init__(self, title, content):
      self.title = title
      self.content = content

class AmountSchema(ma.Schema):
    class Meta:
        fields = ('title', 'content')

amount_schema = AmountSchema()
amounts_schema = AmountSchema(many=True)



@app.route('/amount', methods=["POST"])
def add_amount():
    title = request.json['title']
    content = request.json['content']

    new_amount = Amount(title, content)

    db.session.add(new_amount)
    db.session.commit()

    amount = Amount.query.get(new_amount.id)

    return amount_schema.jsonify(amount)

   
@app.route('/amounts', methods=["GET"])
def get_amounts():
    all_amounts = Amount.query.all()
    result = amounts_schema.dump(all_amounts)
    return jsonify(result)


@app.route("/amount/<id>", methods=["GET"])
def get_amount(id):
    amount = Amount.query.get(id)
    return amount_schema.jsonify(amount)



@app.route("/amount/<id>", methods=["PUT"])
def amount_update(id):
    amount = Amount.query.get(id)
    title = request.json['title']
    content = request.json['content']

    amount.title = title
    amount.content = content

    db.session.commit()
    return amount_schema.jsonify(amount)   


@app.route("/amount/<id>", methods=["DELETE"])
def amount_delete(id):
    amount = Amount.query.get(id)
    db.session.delete(amount)
    db.session.commit()

    return amount_schema.jsonify(amount)


if __name__== '__main__':
    app.run(debug=True)