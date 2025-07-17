# Email Sender Utility

This repository includes a simple command-line utility to construct and send email messages via SMTP, written in Python.

## Prerequisites

* Python 3.8+
* Internet connection with access to the desired SMTP server

> **Gmail users:** You might need to enable "Less secure app access" or create an App Password if you have 2-factor authentication enabled.

## Installation

Create a virtual environment (optional but recommended) and install the only runtime dependency, **Python itself** — the script exclusively uses the Python standard library.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

No external packages are required.

## Usage

```bash
python email_sender.py \
  --smtp-server smtp.gmail.com \
  --smtp-port 587 \
  --username your_email@gmail.com \
  --password your_password \
  --to recipient1@example.com recipient2@example.com \
  --subject "Weekly Report" \
  --body "Hi team, please find the weekly report attached." \
  --attachment ./report.pdf ./chart.png
```

You can omit `--password` and the script will securely prompt for it at runtime.  When using `--inline-image`, the script automatically generates a simple HTML body that embeds each inline image via `cid:` references so most modern email clients will render them inside the message.

### Flags

* `--smtp-server`: SMTP server hostname (default: `smtp.gmail.com`)
* `--smtp-port`: Port (default: `587` which uses STARTTLS)
* `--username`: Sender email / SMTP username (required)
* `--password`: SMTP password (optional; will prompt if omitted)
* `--to`: One or more recipient email addresses (required)
* `--subject`: Email subject line (required)
* `--body`: Plain-text email body (required)
* `--attachment`: Zero or more file paths to attach
* `--no-tls`: Disable STARTTLS (not recommended)
* `--save`: Path to save the raw email in RFC 5322 (.eml) format (optional)
* `--inline-image`: Paths to image files that should be embedded inline in the HTML body (optional)

## License

MIT