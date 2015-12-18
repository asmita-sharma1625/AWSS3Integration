import smtplib
from email.mime.text import MIMEText
import logging
import traceback
import socks

logger = logging.getLogger("s3Integration")

class MailServer:

  def __init__(self, server, sender, password, http_proxy_addr, http_proxy_port):
    socks.setdefaultproxy(socks.PROXY_TYPE_HTTP, http_proxy_addr, int(http_proxy_port))
    socks.wrapmodule(smtplib)
    self.server = server
    self.sender = sender
    self.password = password 
    try:
      self.smtpObj = smtplib.SMTP(server, 587)
      self.smtpObj.ehlo()
      self.smtpObj.starttls()
      self.smtpObj.login(self.sender, self.password)
    except smtplib.SMTPException:
      logger.error("Unable to login to email server " + self.server + " with [username, password] = [" + self.sender + "," + self.password + "]" + ":" + traceback.format_exc())
      raise Exception("Unable to login to email server " + self.server + " with [username, password] = [" + self.sender + "," + self.password + "]" + ":" + traceback.format_exc()) 
    except Exception:
      logger.error("Unable to connect to server : " + server + ":" + traceback.format_exc())
      raise Exception("Unable to connect to server : " + server + ":" + traceback.format_exc())

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
      
