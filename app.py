import os
import pytz
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, session

from database import save_user_request
from hostel_db import fetch_all_preview, fetch_details, find_owner_phone_number, find_hostel_name

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')  # Change this to a random secret key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/survey")
def survey():
    return render_template("survey.html")

@app.route("/hostels", methods=["GET", "POST"])
def hostels():
    if request.method == "POST":
        print(request.form)
    hostels = fetch_all_preview()
    return render_template("hostels.html", hostels=hostels)

@app.route("/hostel-details/<int:id>", methods=["GET", "POST"])
def details(id):
    return render_template("details.html", details=fetch_details(id))

@app.route("/client-request", methods=["GET", "POST"])
def request_info():
    if request.method == "POST":
        try:
            # Store user data in session
            session['name'] = request.form.get('fullName')
            session['semester'] = request.form.get('semester')
            session['department'] = request.form.get('department')
            session['college'] = request.form.get('college')
            session['user_ph'] = request.form.get('phone')
            session['email'] = request.form.get('email')
            session['hostel_id'] = request.form.get('hostel_id')

            # Define the IST timezone
            ist = pytz.timezone('Asia/Kolkata')
            # Get the current time in IST
            now_ist = datetime.now(ist)

            user = {
                "name": session['name'],
                "semester": session['semester'],
                "department": session['department'],
                "college": session['college'],
                "user_ph": session['user_ph'],
                "email": session['email'],

                "hostel_id": session['hostel_id'],
                "hostel_name": find_hostel_name(int(session['hostel_id'])),
                "owner_ph": find_owner_phone_number(int(session['hostel_id'])),

                "requested_date": now_ist.strftime("%Y-%m-%d"),  # YYYY-MM-DD format for better sorting
                "requested_time": now_ist.strftime("%I:%M %p"),  # 12-hour format with AM/PM

                "informed_owner": False,
                "informed_client": False,
            }
            code = save_user_request(user)
            # code status check
            # -2 -> daily request limit exceeded
            # -1 -> request for this already exists (you can request tomorrow).
            # 0  -> error :(
            # 1  -> request recorded successfully!
        except Exception as e:
            print(f"Error occurred: {e}")
            code = 0
    return render_template("success.html", code=code)

@app.route("/contactus")
def contact_us():
    return render_template("aboutus.html")

@app.route('/instructions')
def instructions():
    return render_template('instructions.html')

@app.route('/privacy-policy')
def privacy_policy():
    return redirect(url_for('instructions') + "#section2")

@app.route('/services')
def services():
    return redirect(url_for('index') + "#section2")

if __name__ == "__main__":
    app.run(debug=True)
