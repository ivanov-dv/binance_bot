import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import *


class EmailSMTP:
    """
        :param server: SMTP server
        :param port: SMTP port
        :param sender: Sender email address
        :param recipient: Recipient email address
    """

    def __init__(self, server, port, sender, recipient, password):
        self.server = server
        self.port = port
        self.sender = sender
        self.recipient = recipient
        self.password = password

    def send_email_message(self, subject, text_message) -> bool:
        msg = MIMEMultipart()
        msg['From'], msg['To'], msg['Subject'] = self.sender, self.recipient, subject
        msg.attach(MIMEText(text_message))
        smtp_server = smtplib.SMTP_SSL(self.server, self.port)
        try:
            smtp_server.login(self.sender, self.password)
            smtp_server.sendmail(self.sender, self.recipient, msg.as_string())
        except Exception as e:
            logger.error(f'Ошибка отправки email: {e}')
            return False
        else:
            return True
        finally:
            smtp_server.quit()
