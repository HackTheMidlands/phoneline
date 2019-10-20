import json
import yaml

from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Dial, Say
from twilio.twiml.messaging_response import MessagingResponse

with open("config.yaml") as config_file:
    NUMBERS = yaml.safe_load(config_file)["numbers"]

with open("twilio.json") as credentials_file:
    CREDENTIALS = json.load(credentials_file)

VOICE_ARGS = {
    "voice": "alice",
    "language": "en-GB"
}

client = Client(CREDENTIALS["account_sid"], CREDENTIALS["auth_token"])

def voice(request):
    resp = VoiceResponse()

    resp.say("Connecting you to a safeguarding lead...", **VOICE_ARGS)
    resp.pause()

    for number in NUMBERS.values():
        resp.say("Please hold.", **VOICE_ARGS)
        resp.dial(number)

    resp.say("Couldn't connect you to a member of our safeguarding team.", **VOICE_ARGS)
    resp.say("Please try again soon.", **VOICE_ARGS)

    return str(resp)

def sms(request):
    content = request.values['Body']
    sender = request.values['From']
    master_number = request.values['To']

    if sender in NUMBERS.values():
        # extract sender name
        sender_name = [na for na, num in NUMBERS.items() if num == sender][0]

        # send help message if requested
        if content == "!help":
            resp = MessagingResponse()
            resp.message('\n'.join([
                "To message the group, simply send <message>",
                "To message an individual, send <number>: <message>"
            ]))
            return str(resp)

        # extract individual target if requested
        try:
            target, content = content.split(':', maxsplit=1)
            target_name = target
        except ValueError:
            target = None
            target_name = 'group'

        # send message to group
        for number in NUMBERS.values():
            if number == sender:
                continue

            message = client.messages.create(
                body=f"{sender_name} -> {target_name}: {content}",
                from_=master_number,
                to=number
            )

        # send message to target
        if target:
            message = client.messages.create(
                body=content,
                from_=master_number,
                to=target
            )
    else:
        # send message to group
        for number in NUMBERS.values():
            client.messages.create(
                body=f"{sender} -> group: {content}",
                from_=master_number,
                to=number
            )

    return ''
