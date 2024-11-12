#!/usr/bin/env python3

from flask import Flask, request, render_template, redirect, jsonify
from uuid import uuid4
from kopokopo.payment import Pesapal

app = Flask(__name__)


# Route for the home page
@app.route("/")
def home():
    return render_template("index.html", static_folder="static")


# Route for handling payment requests
@app.route("/pay", methods=["POST"], strict_slashes=False)
def pay():
    # Get phone number from form data
    phone = request.form.get("phone")
    package = request.form.get("package")
    price = request.form.get("price")
    new_id = str(uuid4())

    print(f"Purchasing {package} ,{phone}, {price}")

    # Initialize Pesapal object and create a payment request
    pesapal = Pesapal(new_id)
    pesapal.request_payment(price, phone, "Gad", "Nadolo")

    return redirect(pesapal.redirect)


# Route for the packages page (for users to choose a package)
@app.route("/packages", strict_slashes=False)
def packages():
    return render_template("packages.html")


# Payment callback route that PesaPal will call
@app.route("/payment-callback", methods=["POST"], strict_slashes=False)
def payment_callback():
    # Get the data sent by PesaPal
    payment_status = request.form.get("payment_status")
    transaction_id = request.form.get("transaction_id")
    phone_number = request.form.get(
        "phone_number"
    )  # PesaPal sends this in the callback

    # Handle the callback - Check if the payment was successful
    if payment_status == "SUCCESS":
        # Payment successful - update your records here (database, session, etc.)
        return jsonify(
            {
                "status": "success",
                "message": "Payment successful",
                "transaction_id": transaction_id,
            }
        )
    else:
        # Payment failed - handle accordingly
        return jsonify(
            {
                "status": "failure",
                "message": "Payment failed",
                "transaction_id": transaction_id,
            }
        )


# Run the app with debug mode enabled
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
