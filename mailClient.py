import poplib
from email import parser
import sys, re

class MailClient:

  def __init__(self, server, user, passwd):
    self.server = server
    self.user = user
    self.passwd = passwd
    self.pop_conn = self.connect()

  def __del__(self):
    self.pop_conn.quit()

  def connect(self):
    pop_conn = poplib.POP3_SSL(self.server)
    print pop_conn.getwelcome()
    try:
      print "authenticating..."
      pop_conn.user(self.user)
      pop_conn.pass_(self.passwd)
    except poplib.error_proto, e:
      print "Login failed:", e
      raise Exception("Could not authenticate ")
    return pop_conn

  def getMail(self, deleteRead = False, section = None, regex = "*"):
    compiled_regex = re.compile(regex, re.IGNORECASE)
    messages = []
    ''' gets all messages from inbox '''
    for i in range(1, len(self.pop_conn.list()[1]) + 1):
      print "retrieving messages..."
      #Get messages from server:
      messages.append(self.pop_conn.retr(i))
    ''' convert mails to parsable email format'''
    #Concat message pieces:
    messages = ["\n".join(mssg[1]) for mssg in messages]
    #Parse message into an email object:
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]  
    ''' match each mail's specified section with specified regex and return first match. 
    Also delete matched mail if deleteRead flag is True'''
    msgNo = 1
    for message in messages:
      if re.match(regex, message[section]) is not None:
        print "*****************message " + section + "  matched*****************\n ", message[section]
        if deleteRead:
          self.pop_conn.dele(msgNo)
        return message
      msgNo = msgNo + 1
    return None

  def getMailBody(self, message):
    return message['body']

