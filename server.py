import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from flask import Flask
app = Flask(__name__)

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
	server.login(fromaddr, "1EstateDr")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	return "Success"

if __name__ == "__main__":
	app.run(host='0.0.0.0', threaded=True)
