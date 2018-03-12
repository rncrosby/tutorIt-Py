import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time
from apns import APNs, Frame, Payload
from flask import Flask

app = Flask(__name__)

apns = APNs(use_sandbox=True, cert_file='cert/apns-dev.pem', key_file='cert/apns-dev-key.pem')

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

@app.route("/sendPush")
def sendPush():
    token_hex = 'a152e60af7ac27a080c788ae4fac1ae36b462d17f79b37e75bceba32af71ccfd'
    payload = Payload(alert="Hello World!", sound="default", badge=1, mutable_content=True)
    apns.gateway_server.send_notification(token_hex, payload)

if __name__ == "__main__":
	app.run(host='0.0.0.0', threaded=True)
