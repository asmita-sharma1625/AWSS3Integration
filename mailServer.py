import smtplib
from email.mime.text import MIMEText

class MailServer:

  def __init__(self, server, sender, password):
    self.server = server #'smtp.mail.yahoo.com'
    self.sender = sender #'s3.notifier@yahoo.com'
    self.password = password #'jio@1234'
    try:
      self.smtpObj = smtplib.SMTP(server, 587)
      self.smtpObj.ehlo()
      self.smtpObj.starttls()
      self.smtpObj.login(self.sender, self.password)
    except smtplib.SMTPException:
      print "Error: unable to connect to email"

  def __del__(self):
    try:
      self.smtpObj.quit()
    except smtplib.SMTPException:
      print "Error: unable to quit email session"

  def sendMessage(self, receiver, subject, message):
    msg = MIMEText(text)
    #receiver = 'itsmeasmi25@gmail.com'
    msg['Subject'] = subject #'JCS_Config_Change_Notification'
    msg['From'] = self.sender
    msg['To'] = receiver
    try:
      self.smtpObj.sendmail(sender, receiver, msg.as_string())
    except smtplib.SMTPException:
      print "Error: unable to send email"
      
