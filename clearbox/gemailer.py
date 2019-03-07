
import smtplib
from email.mime.text import MIMEText
from clearbox.gemailer_config import *

def send_msg(subject, toAddr, msg):
        s = smtplib.SMTP(SMTP_SERVER, 587)
        s.set_debuglevel(0)
        s.ehlo()
        s.starttls()
        s.login(SMTP_USER, PW)

        msg = MIMEText(msg)

        msg['Subject'] = subject
        msg['From'] = "gemailer.py"

        msg['To'] = toAddr

        if ',' in toAddr:
                toAddr = toAddr.split(',')
        s.sendmail('mikesutton@gmail.com',toAddr,msg.as_string())
        s.close()
