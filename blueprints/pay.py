from flask import Blueprint, request, render_template, redirect, url_for, g
import stripe
from config import stripe_public_key, stripe_secret_key

bp = Blueprint("stripe", __name__)  #不加prefix为了能访问首页， 如果要加就加默认值 /

@bp.route("/pay")
def checkout():
    return render_template("indexStripe.html", public_key = stripe_public_key);

@bp.route("/thankyou")
def subscribe():
    return render_template("thankyou.html")

@bp.route('/payment', methods=['POST'])
def payment():
    stripe.api_key = config.stripe.api_key

    # CUSTOMER INFORMATION
    customer = stripe.Customer.create(email=request.form['stripeEmail'], source=request.form['stripeToken'])

    # CHARGE/PAYMENT INFORMATION
    charge = stripe.Charge.create(
        customer=customer.id,
        amount=1999,
        currency='usd',
        description='Donation'
    )

    return redirect(url_for('stripe_bp.thankyou'))