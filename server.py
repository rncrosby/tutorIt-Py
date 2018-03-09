import smtplib
from flask import Flask
app = Flask(__name__)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("tutorit.development@gmail.com", "1EstateDr")

@app.route("/")
def hello():
	return "<h1 style='color:black'><center>All Systems Operational</center></h1>"

@app.route("/verifyEmail/<email>/<code>")
def verifyEmail(email,code):
	print "sending email"
	msg = "Welcome to TutorTree, your code to get started is: " + code
	server.sendmail("tutorit.development@gmail.com", email, msg)
	server.quit()
	return "Success"

if __name__ == "__main__":
	app.run(host='0.0.0.0', threaded=True)
