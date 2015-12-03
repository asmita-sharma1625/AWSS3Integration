import poplib
from email import parser
import sys

host = 'pop.mail.yahoo.com'
user = 's3.notifier@yahoo.com'
passwd = 'jio@1234'

pop_conn = poplib.POP3_SSL(host)
print pop_conn.getwelcome()
try:
  print "authenticating..."
  pop_conn.user(user)
  pop_conn.pass_(passwd)
except poplib.error_proto, e:
  print "Login failed:", e
  sys.exit(1)

print "retrieving messages..."
#Get messages from server:
messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
# Concat message pieces:
messages = ["\n".join(mssg[1]) for mssg in messages]
#Parse message intom an email object:
messages = [parser.Parser().parsestr(mssg) for mssg in messages]
for message in messages:
  print "message subject :: ", message['subject']

pop_conn.quit()

