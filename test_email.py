import os
import smtplib
from email.message import EmailMessage

username = os.getenv("TMS_MAIL_USERNAME")
password = os.getenv("TMS_MAIL_PASSWORD")

if not username or not password:
    raise RuntimeError("Set 'TMS_MAIL_USERNAME' and 'TMS_MAIL_PASSWORD' environment variables first.")

msg = EmailMessage()
msg["Subject"] = "HikeHorizon SMTP Test"
msg["From"] = username
msg["To"] = username
msg.set_content(
    "This is a test email from Aggarwal HikeHorizon."
)

with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:
    smtp.login(username, password)
    smtp.send_message(msg)

print("Test email submitted successfully.")
