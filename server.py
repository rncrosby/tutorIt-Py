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
	server.login("tutorit.development@gmail.com", "1EstateDr")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	return "Success"

@app.route("/sendPush")
def sendPush():
	client = APNSClient(certificate='cert/apns-pro.pem',
                    default_error_timeout=10,
                    default_expiration_offset=2592000,
                    default_batch_size=100,
                    default_retries=5)

	token = 'a152e60af7ac27a080c788ae4fac1ae36b462d17f79b37e75bceba32af71ccfd'
	alert = 'Hello world.'
	res = client.send(token,
	                  alert,
	                  badge='badge count',
	                  sound='sound to play',
	                  category='category',
	                  content_available=True,
	                  title='Title',
	                  title_loc_key='t_loc_key',
	                  title_loc_args='t_loc_args',
	                  action_loc_key='a_loc_key',
	                  loc_key='loc_key',
	                  launch_image='',
	                  extra={'custom': 'data'})

	return "Success"

if __name__ == "__main__":
	app.run(host='0.0.0.0', threaded=True)
