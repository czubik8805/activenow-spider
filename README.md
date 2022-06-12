# ActiveNow Spider 1.0

Spider app for keeping track of available swimming lessons dates.

# Getting started

Required Python 3.8.10

## Install requirements:

    pip install -r requirements.txt

## Add required environment variables

    ACTIVE_NOW_USERNAME=<username>
    ACTIVE_NOW_PASSWORD=<password>

    DEFAULT_FROM_EMAIL=<default_email>
    EMAIL_PASSWORD=<default_email_password>
    EMAIL_SMTP=<smtp_server>
    EMAIL_PORT=<smtp port, default:587>
    RECEIVER_EMAIL=<receiver_email>

**Note:** you can use _.env_ file

# Run the script

    scrapy crawl active_now
