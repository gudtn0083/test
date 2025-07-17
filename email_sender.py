#!/usr/bin/env python3
"""email_sender.py

A simple utility to construct and send emails from the command line.

Example usage:
    python email_sender.py \
        --smtp-server smtp.gmail.com \
        --smtp-port 587 \
        --username your_email@gmail.com \
        --password your_password \
        --to recipient@example.com \
        --subject "Test Mail" \
        --body "Hello, this is a test email sent from Python!" \
        --attachment ./report.pdf ./image.png

Note: For Gmail accounts, you may need to enable "Less secure app access" or set up an App Password.
"""
from __future__ import annotations

import argparse
import getpass
import mimetypes
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path
from typing import List


def build_email(
    sender: str,
    recipients: List[str],
    subject: str,
    body: str,
    attachments: List[Path] | None = None,
) -> EmailMessage:
    """Construct an EmailMessage.

    Args:
        sender: Sender email address.
        recipients: List of recipient email addresses.
        subject: Email subject.
        body: Email body as plain text.
        attachments: Optional list of file paths to attach.

    Returns:
        A fully-formed EmailMessage object ready to be sent.
    """
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.set_content(body)

    for path in attachments or []:
        if not path.exists():
            print(f"Warning: attachment {path} does not exist and will be skipped.", file=sys.stderr)
            continue
        ctype, encoding = mimetypes.guess_type(path)
        maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
        with path.open("rb") as fp:
            data = fp.read()
        msg.add_attachment(data, maintype=maintype, subtype=subtype, filename=path.name)
    return msg


def send_email(
    msg: EmailMessage,
    smtp_server: str,
    smtp_port: int,
    username: str,
    password: str,
    use_tls: bool = True,
) -> None:
    """Send EmailMessage via SMTP.

    Args:
        msg: EmailMessage to send.
        smtp_server: SMTP server hostname.
        smtp_port: Port number.
        username: SMTP username (usually the sender email).
        password: SMTP password.
        use_tls: Whether to start TLS.
    """
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.ehlo()
        if use_tls:
            server.starttls()
            server.ehlo()
        server.login(username, password)
        server.send_message(msg)
        print("Email sent successfully.")


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:  # noqa: D401 – short description fine
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Construct and send an email with optional attachments.")
    parser.add_argument("--smtp-server", default="smtp.gmail.com", help="SMTP server hostname (default: smtp.gmail.com)")
    parser.add_argument("--smtp-port", type=int, default=587, help="SMTP server port (default: 587)")
    parser.add_argument("--username", required=True, help="SMTP username / sender email address")
    parser.add_argument("--password", help="SMTP password (will prompt if omitted)")
    parser.add_argument("--to", nargs="+", required=True, help="Recipient email addresses (space-separated)")
    parser.add_argument("--subject", required=True, help="Email subject")
    parser.add_argument("--body", required=True, help="Plain text email body")
    parser.add_argument(
        "--attachment",
        nargs="*",
        default=[],
        type=Path,
        help="Paths to files to attach (optional)",
    )
    parser.add_argument(
        "--no-tls",
        dest="use_tls",
        action="store_false",
        help="Disable STARTTLS (not recommended)",
    )
    parser.set_defaults(use_tls=True)
    return parser.parse_args(argv)


def main(argv: List[str] | None = None) -> None:
    args = parse_args(argv)
    password = args.password or getpass.getpass(prompt="SMTP password: ")

    msg = build_email(
        sender=args.username,
        recipients=args.to,
        subject=args.subject,
        body=args.body,
        attachments=args.attachment,
    )

    try:
        send_email(
            msg=msg,
            smtp_server=args.smtp_server,
            smtp_port=args.smtp_port,
            username=args.username,
            password=password,
            use_tls=args.use_tls,
        )
    except Exception as exc:
        print(f"Error sending email: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()