__author__ = 'Alex'

from twilio.rest import TwilioRestClient

account_sid = "AC9db62ba6a34d28f94bfc9753e3988dfc"
auth_token = "9b41675f991fa8decf69921169a725e7"
client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(to="6049285414", from_="2028366058", body="Beep")
