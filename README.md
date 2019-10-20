# HackTheMidlands phoneline

This is a phoneline program to forward calls to organizers.

The number can be either called or texted and it will passed along to the
appropriate organizers.

## Development

After cloning the repository, install the dependencies into a virtual
environment:

    $ virtualenv .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt

Then run the app:

    $ python -m app

You should be able to see the generated conversation on
[localhost:8000](localhost:8000).

## Deployment

This repository contains a terraform script to deploy and manage the
phoneline using Google Cloud and Twilio (using
[terraform-provider-twilio](https://github.com/Preskton/terraform-provider-twilio))

First, create `config.yaml` to point to your target phone numbers.

```yaml
numbers:
  - 0XXXXXXXXXX
  - 0XXXXXXXXXX
```

Then, create `credentials/gcloud.json` to be the credentials of a Google
Cloud service account and `credentials/twilio.json` to contain your
appropriate Twilio details.

Finally, deploy the infrastructure:

    $ terraform init
    $ terraform apply

You can get the phone number to call:

    $ terraform output number
