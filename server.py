from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1 style='color:black'><center>All Systems Operational</center></h1>"

@app.route("/verifyEmail/<email>/<code>")
def verifyEmail(email,code):
	return "<h1 style='color:black'><center>" + email + ", " + code + "</center></h1>"

if __name__ == "__main__":
	app.run(host='0.0.0.0', threaded=True)
