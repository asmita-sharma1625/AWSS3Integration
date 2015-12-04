from configChangeNotifier import ConfigChangeNotifier
import time

class S3NotificationMonitor:

  '''
  Sample S3 Notification Mail Body:
        {"Records":[{"eventVersion":"2.0","eventSource":"aws:s3","awsRegion":"us-west-2","eventTime":"2015-12-03T11:47:40.428Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AIDAI3LQQTO4RURMDMETK"},"requestParameters":{"sourceIPAddress":"49.32.0.187"},"responseElements":{"x-amz-request-id":"EBA9BB89874EF559","x-amz-id-2":"C+xu0zv/OxCgO22mZ2PtN5ubNw5+doOW9vJnUIuyWszdt6/I3c4HboOPLQnUM4rz"},"s3":{"s3SchemaVersion":"1.0","configurationId":"MyEmailNotificationsForPut","bucket":{"name":"compute-config","ownerIdentity":{"principalId":"A2GX7JMHUJDOBN"},"arn":"arn:aws:s3:::compute-config"},"object":{"key":"subfolder/Compute-Read","size":106,"eTag":"1caf53f68ac7f0a4a84bd6b163d0a564","versionId":"63P9JdVgXKXJRLe235EeCqJZdrASwGdZ","sequencer":"0056602BDC5B063096"}}}]}
  '''

  def __init__(self, dirpath, ):
    self.dirpath = dirpath
    server = 'pop.mail.yahoo.com'
    user = 's3.notifier@yahoo.com'
    passwd = 'jio@1234'
    self.mailClient = MailClient(server, user, passwd)
    self.S3_BODY_KEY_1_LEVEL_1 = "Records"
    self.S3_BODY_KEY_1_LEVEL_2 = "s3"
    self.S3_BODY_KEY_1_LEVEL_3 = "object"
    self.S3_BODY_KEY_1_LEVEL_4 = "key"
    self.S3_BODY_KEY_2_LEVEL_4 = "versionId"
    self.S3_BUCKET = "compute-config"
    self.s3Dao = S3Dao()
    self.s3Dao.setBucket(self.S3_BUCKET)
    
    timestamp = time.time()
    s3NotifyMsg = self.getS3NotificationMailBody()
    if s3NotifyMsg is not None:
      objectKey = self.getS3ObjectKey(s3NotifyMsg)
      objectVersion = self.getS3ObjectVersion(s3NotifyMsg)
      OLD_CONFIG_PATH = self.getConfigPath(objectKey)
      OLD_CONFIG_NODE = self.getConfigNode(objectKey)
      newConfig = os.path.join(os.path.join(dirpath, os.path.join(timestamp, NEW_DIR),OLD_CONFIG_PATH)
      self.getS3Object(objectKey, newConfig)
      oldConfig = os.path.join(os.path.join(dirpath, os.path.join(timestamp, OLD_DIR),OLD_CONFIG_PATH)
      self.getConfig(OLD_CONFIG_PATH, OLD_CONFIG_NODE, oldConfig)
      ''' notify any change to registered user '''
      self.notifyChange(oldConfig, newConfig, timestamp)

    self.responseMailClient = MailClient(server, user, passwd) 
    self.applyChange(newConfig, OLD_CONFIG_PATH, OLD_CONFIG_NODE)

  def getS3NotificationMail(self):
    return self.mailClient.getMail(deleteRead = True, section = 'subject', regex = 'conf_put*')
  
  def getS3NotificationMailBody(self):
    mail = self.getS3NotificationMail()
    if mail is not None:
      return self.mailClient.getMailBody(mail)
    return None

  def getS3ObjectKey(self, message):
    return message[self.S3_BODY_KEY_1_LEVEL_1][self.S3_BODY_KEY_1_LEVEL_2][self.S3_BODY_KEY_1_LEVEL_3][self.S3_BODY_KEY_1_LEVEL_4]

  def getS3ObjectVersion(self, message):
    return message[self.S3_BODY_KEY_1_LEVEL_1][self.S3_BODY_KEY_1_LEVEL_2][self.S3_BODY_KEY_1_LEVEL_3][self.S3_BODY_KEY_2_LEVEL_4]
    
  def getS3Object(self, objectKey, newConfig):
    self.s3Dao.downloadObject(objectKey, newConfig)

  def getConfigPath(self, objectKey):
    return Helper.mapToPath(objectKey)

  def getConfigNode(self, objectKey):
    return Helper.mapToNode(objectKey)

  def getConfig(self, node, src_path, dest_path = None):
    return Helper.copyConfigFromRemote(node, src_path, dest_path)

  def notifyChange(self, oldConfig, newConfig, node):
    configChangeDetector = ConfigChangeDetector(oldConfig, newConfig)
    if configChangeDetector.compareConfig():
      old_config_diff = configChangeDetector.getDiffInOldConfig()
      new_config_diff = configChangeDetector.getDiffInNewConfig()
      #call mail server to send notification with diff in body and node info in subject
    
  def applyChange(self, node, path):
    mail = self.getResponseMail()
    if mail is not None:
      subject = self.responseMailClient.getMailSubject(mail)
      newConfig = Helper.getNewConfigPathFromResponseMailSubject(subject)
      timestamp = Helper.getTimestampFromPath(newConfig)
      ConfigChangeApplier(newConfig, node, path).copyConfigToRemote()
    Helper.deleteAllConfigsBeforeTime(self.dirpath, timestamp)

  def getResponseMail(self):
    return self.responseMailClient.getMail(deleteRead = True, section = 'subject', regex = '*conf_change_apply*')



