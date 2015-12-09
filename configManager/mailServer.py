import smtplib
from email.mime.text import MIMEText
import logging

logger = logging.getLogger("s3Integration")

class MailServer:

  def __init__(self, server, sender, password):
    self.server = server
    self.sender = sender
    self.password = password 
    try:
      self.smtpObj = smtplib.SMTP(server, 587)
      self.smtpObj.ehlo()
      self.smtpObj.starttls()
      self.smtpObj.login(self.sender, self.password)
    except smtplib.SMTPException:
      logger.error("Unable to login to email server " + self.server + " with [username, password] = [" + self.sender + "," + self.password + "]")
      raise Exception("Unable to login to email server " + self.server + " with [username, password] = [" + self.sender + "," + self.password + "]") 

  def __del__(self):
    try:
      self.smtpObj.quit()
    except smtplib.SMTPException:
      logger.error("Unable to quit email session")
      pass

  def sendMessage(self, receiver, subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject 
    msg['From'] = self.sender
    msg['To'] = receiver
    try:
      self.smtpObj.sendmail(self.sender, receiver, msg.as_string())
    except smtplib.SMTPException:
      logger.error("Unable to send email with subject - " + subject + " to receiver - " + receiver)
      raise Exception("Unable to send email with subject - " + subject + " to receiver - " + receiver)
      
