import os
import stripe

from dotenv import load_dotenv
from flask import Flask, render_template, redirect

load_dotenv()
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

app = Flask(__name__)
YOUR_DOMAIN = 'http://127.0.0.1:5000'

@app.route("/")
def home():
	try:
		pricelists = stripe.Price.list(active='true', expand=['data.product'])
		return render_template("index.html",pricelists=pricelists)
	except Exception as e:
		return str(e)

@app.route("/checkout/<price_id>")
def checkout(price_id):
	try:
		checkout_session = stripe.checkout.Session.create(
			line_items=[{ 'price': price_id, 'quantity':1 }],
			mode='payment',
			success_url=YOUR_DOMAIN+'/success',
			cancel_url=YOUR_DOMAIN+'/cancel',
		)
		return redirect(checkout_session.url,code=303)
	except Exception as e:
		return str(e)

@app.route("/success")
def success():
	return "Thank you for your Purchase! Back to <a href='/'>Catalog</a>?"

@app.route("/cancel")
def cancel():
	return "Maybe next time! Back to <a href='/'>Catalog</a>?"