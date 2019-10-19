import yaml

from twilio.twiml.voice_response import Dial, VoiceResponse, Say

with open("config.yaml") as config_file:
    CONFIG = yaml.safe_load(config_file)

VOICE_ARGS = {
    "voice": "alice",
    "language": "en-GB"
}

def voice(request):
    resp = VoiceResponse()

    resp.say("Connecting you to a safeguarding lead...", **VOICE_ARGS)
    resp.pause()

    for number in CONFIG["numbers"]:
        resp.say("Please hold.", **VOICE_ARGS)
        resp.dial(number)

    resp.say("Couldn't connect you to a member of our safeguarding team.", **VOICE_ARGS)
    resp.say("Please try again soon.", **VOICE_ARGS)

    return str(resp)
