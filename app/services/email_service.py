import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_password_reset_otp(email: str, otp: str) -> None:
    if not settings.smtp_host or not settings.smtp_from_email:
        print(f"Password reset OTP for {email}: {otp}")
        return

    message = EmailMessage()
    message["Subject"] = "Your password reset code"
    message["From"] = settings.smtp_from_email
    message["To"] = email
    message.set_content(
        f"Your password reset code is {otp}. "
        f"It expires in {settings.password_reset_otp_expire_minutes} minutes."
    )

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as smtp:
        if settings.smtp_use_tls:
            smtp.starttls()
        if settings.smtp_username and settings.smtp_password:
            smtp.login(settings.smtp_username, settings.smtp_password)
        smtp.send_message(message)
