import smtplib
from datetime import datetime, timezone
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_FROM, EMAIL_TO, EMAIL_PASS
from logger import get_logger

log = get_logger(__name__)


def send_email(html_body: str) -> bool:
    subject = f"Trends Summary — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg.attach(MIMEText(html_body, 'html', 'utf-8'))
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
            s.login(EMAIL_FROM, EMAIL_PASS)
            s.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        log.info('Email sent successfully')
        return True
    except Exception as e:
        log.error(f'Failed to send email: {e}')
        return False
