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
from email.utils import make_msgid
from pathlib import Path
from typing import List


def build_email(
    sender: str,
    recipients: List[str],
    subject: str,
    body: str,
    attachments: List[Path] | None = None,
    inline_images: List[Path] | None = None,
    cc_recipients: List[str] | None = None,
    bcc_recipients: List[str] | None = None,
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
    cc_recipients = cc_recipients or []
    bcc_recipients = bcc_recipients or []

    if cc_recipients:
        msg["Cc"] = ", ".join(cc_recipients)
    if bcc_recipients:
        msg["Bcc"] = ", ".join(bcc_recipients)
    msg["Subject"] = subject
    # Plain-text part
    msg.set_content(body)

    # ------------------------------------------------------------------
    # HTML + inline images
    # ------------------------------------------------------------------
    inline_images = inline_images or []
    cid_map: dict[Path, str] = {}

    if inline_images:
        html_body = [f"<p>{body.replace('\n', '<br>')}</p>"]

        # Reserve content-IDs first so we can reference them in HTML before attaching.
        for p in inline_images:
            cid = make_msgid()[1:-1]  # strip <>
            cid_map[p] = cid
            html_body.append(f'<img src="cid:{cid}" alt="{p.name}">')
        html = "\n".join(html_body)

        # add alternative HTML part
        msg.add_alternative(f"<html><body>{html}</body></html>", subtype="html")

        # Last payload is the HTML part we just added
        html_part = msg.get_payload()[-1]

        for img_path in inline_images:
            if not img_path.exists():
                print(f"Warning: inline image {img_path} does not exist and will be skipped.", file=sys.stderr)
                continue
            ctype, _ = mimetypes.guess_type(img_path)
            maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
            with img_path.open("rb") as fp:
                data = fp.read()
            # cid must be enclosed in angle brackets per RFC
            html_part.add_related(
                data,
                maintype=maintype,
                subtype=subtype,
                cid=f"<{cid_map[img_path]}>",
                filename=img_path.name,
            )

    # ------------------------------------------------------------------
    # Regular file attachments (not inline)
    # ------------------------------------------------------------------
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
    recipients: List[str],
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
        server.send_message(msg, from_addr=username, to_addrs=recipients)
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
    parser.add_argument(
        "--cc",
        nargs="*",
        default=[],
        help="CC (carbon copy) recipient email addresses",
    )
    parser.add_argument(
        "--bcc",
        nargs="*",
        default=[],
        help="BCC (blind carbon copy) recipient email addresses",
    )
    parser.add_argument("--body", required=True, help="Plain text email body")
    parser.add_argument(
        "--attachment",
        nargs="*",
        default=[],
        type=Path,
        help="Paths to files to attach (optional)",
    )
    parser.add_argument(
        "--inline-image",
        nargs="*",
        default=[],
        type=Path,
        help="Paths to images to embed inline in the HTML body (optional)",
    )
    parser.add_argument(
        "--save",
        type=Path,
        help="Optional path to save the raw email (.eml) before sending",
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
        inline_images=args.inline_image,
        cc_recipients=args.cc,
        bcc_recipients=args.bcc,
    )

    # Combine recipients for SMTP envelope
    all_recipients = args.to + args.cc + args.bcc

    # Optionally save the email to disk
    if args.save:
        try:
            args.save.parent.mkdir(parents=True, exist_ok=True)
            with args.save.open("wb") as fp:
                fp.write(msg.as_bytes())
            print(f"Email saved to {args.save}")
        except Exception as exc:
            print(f"Warning: Could not save email to {args.save}: {exc}", file=sys.stderr)

    try:
        send_email(
            msg=msg,
            smtp_server=args.smtp_server,
            smtp_port=args.smtp_port,
            username=args.username,
            password=password,
            recipients=all_recipients,
            use_tls=args.use_tls,
        )
    except Exception as exc:
        print(f"Error sending email: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()