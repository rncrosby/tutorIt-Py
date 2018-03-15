import smtplib
import random
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import time
from apns import APNs, Frame, Payload
from flask import Flask
import braintree

app = Flask(__name__)

gateway = braintree.BraintreeGateway(
  braintree.Configuration(
    environment=braintree.Environment.Production,
    merchant_id='j3thkst7k9j6mkvc',
    public_key='y77kkm6dvvjcswqr',
    private_key='5d0998038deb27cebd643b1c11a4bdf7'
  )
)

apns_enhanced = APNs(use_sandbox=False, cert_file='cert/pro/apns-pro.pem', enhanced=True)
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

@app.route("/getClientToken")
def client_token():
  return gateway.client_token.generate()

@app.route("/checkoutWithNonceAndAmount/<nonce>/<amount>")
def checkoutWithNonceAndAmount(nonce,amount):
	stringAmount = amount + '.00'
	result = gateway.transaction.sale({
		"amount": stringAmount,
		"payment_method_nonce": nonce,
		"options": {
			"submit_for_settlement": True
		}
	})

	if result.is_success:
		print result.transaction
		return "Success"
	# See result.transaction for details
	else:
		print result.message
		return "Error: " + result.message
	# Handle errors

if __name__ == "__main__":
	app.run(host='0.0.0.0', threaded=True, ssl_context='adhoc')
