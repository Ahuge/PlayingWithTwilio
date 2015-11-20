__author__ = 'Alex'

from flask import Flask, request, redirect
import twilio.twiml
from base64 import b64decode, b64encode
import re

app = Flask(__name__)

numbers = {
    'KzE2MDQ5Mjg1NDE0': "Alex"
}

RECENT_TOLERANCE = 2
recent_numbers = {}

MY_NAME_IS_REGEX = re.compile(r"\w+name\sis\s([a-zA-Z]+).*")

DEFAULT_MESSAGE = "Wow %s, Thanks for the message!"
UNKNOWN_USER_MESSAGE = "Thanks for the message but I don't know your name. What is it?"
COULDNT_GET_NAME_MESSAGE = "Sorry I think you just told me your name but I couldn't catch it. Could you just send " \
                           "your name back to me?"

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """
    Respond to incomming calls with a simple text message.
    """

    from_number = request.values.get("From", None)

    body = request.values.get("Body", None)
    if b64encode(from_number) in numbers:
        message = DEFAULT_MESSAGE % numbers[b64encode(from_number)]
    else:
        if from_number in recent_numbers:
            # Assume they are replying to my question.
            if recent_numbers[from_number] in [UNKNOWN_USER_MESSAGE, COULDNT_GET_NAME_MESSAGE]:
                if len(body.split(" ")) == 1:
                    # Assume they just sent back their name.
                    numbers[b64encode(from_number)] = body
                    message = DEFAULT_MESSAGE % body + " Try to send me another message and see if I remember it!"
                elif MY_NAME_IS_REGEX.search(body):
                    # Assume they said something like "My name is Alex" and catch Alex.
                    name = MY_NAME_IS_REGEX.search(body)
                    numbers[b64encode(from_number)] = name

                    message = DEFAULT_MESSAGE % name + " Try to send me another message and see if I remember it!"
                else:
                    message = COULDNT_GET_NAME_MESSAGE
            else:
                message = "Haha I don't know what you are saying!"

        else:
            message = UNKNOWN_USER_MESSAGE

    recent_numbers[from_number] = message

    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
