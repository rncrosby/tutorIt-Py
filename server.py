import smtplib
import random
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time
from apns import APNs, Frame, Payload
from flask import Flask

app = Flask(__name__)

apns_enhanced = APNs(use_sandbox=False, cert_file='cert/pro/apns-pro.pem', enhanced=True)
apns = APNs(use_sandbox=False, cert_file='cert/pro/apns-pro.pem', key_file='cert/pro/apns-pro-key-noenc.pem')

def response_listener(error_response):
	print ("client get error-response: " + str(error_response))

@app.route("/")
def hello():
	return "<h1 style='color:black'><center>All Systems Operational</center></h1>"

@app.route("/verifyEmail/<email>/<code>")
def verifyEmail(email,code):
	print "sending email"
	fromaddr = "<TutorTree Verification> tutorit.development@gmail.com"
	toaddr = email
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "TutorTree Verification Code"
	body = "Welcome to TutorTree,\nYour code is: " + code
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("tutorit.development@gmail.com", "1EstateDr")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	return "Success"

@app.route("/sendPush/<message>/<token>")
def sendPush(message,token):
	payload = Payload(alert=message, sound="default", badge=1)
	identifier = random.getrandbits(32)
	apns_enhanced.gateway_server.send_notification(token, payload, identifier=identifier)
	apns_enhanced.gateway_server.register_response_listener(response_listener)
	return "Success"


if __name__ == "__main__":
	app.run(host='0.0.0.0', threaded=True)
