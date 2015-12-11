import configChangeNotifier 
import mailServer
import s3Dao
import helper
import configReader
import logging, os

logger = logging.getLogger("s3Integration")
logger.addHandler(logging.FileHandler("/tmp/s3Integration.log"))

class ConfigManager:

  def __init__(self, config_file):
    self.SECTION = "Manager"
    self.CONF_DIR = "ConfDir"#"/tmp"
    self.MAIL_SERVER = "mailServer"#"smtp.mail.yahoo.com"
    self.MAIL_SENDER = "mailSender"#"s3.notifier@yahoo.com"
    self.MAIL_PASSWORD = "mailPassword"#"jio@1234"
    self.MAIL_RECEIVER = "mailReceiver"#"itsmeasmi25@gmail.com"
    self.MAIL_SUBJECT = "mailSubject"#"JCS_Config_Change_Notification"
    self.BUCKET = "s3Bucket"#"compute-config"
    
    try:
      self.configReader = configReader.ConfigReader(config_file)#("/tmp/Config_Manager_config.conf")
      self.S3_BUCKET = self.configReader.getValue(self.SECTION, self.BUCKET) 
    except Exception:
      logger.error("Invalid config file")
    self.s3Dao = s3Dao.S3Dao()
    self.s3Dao.setBucket(self.S3_BUCKET)

  def reportAllConfigChange(self):
    objects = self.getAllS3Objects()
    for obj in objects:
      self.reportOrApplyConfigChange(obj)      

  def reportOrApplyConfigChange(self, objectKey, apply_flag = False):
    newConfig = "/tmp/newConfig.conf"
    self.getS3Object(objectKey, newConfig)
    try:
      OLD_CONFIG_PATH = self.getConfigPath(objectKey)
      OLD_CONFIG_NODE = self.getConfigNode(objectKey)
    except Exception:
      logger.error("Config corresponding to s3 object - " + objectKey + " not found")
      return
    oldConfig = "/tmp/oldConfig.conf"
    self.getConfig(OLD_CONFIG_NODE, OLD_CONFIG_PATH, oldConfig)
    configChangeDetector = configChangeNotifier.ConfigChangeDetector(oldConfig, newConfig)
    print "before check****"
    if not configChangeDetector.compareConfig():
      config_diff = configChangeDetector.getDiff()
      print "config_diff : ", open(config_diff, 'r').readlines()
      ''' notify any change to registered user along 
          with objectKey and diff files if apply_flag is False 
          else apply the change on the related node'''
      if apply_flag:
        self.applyChange(newConfig, OLD_CONFIG_NODE, OLD_CONFIG_PATH)
      else:
        '''call mail server to send notification with diff files and objectKey and old config node and path.'''
        self.notifyConfigChange(objectKey, config_diff)

  def getAllS3Objects(self):
    return self.s3Dao.getAllObjects()

  def getS3Object(self, objectKey, newConfig):
    self.s3Dao.downloadObject(objectKey, newConfig)

  def getConfigPath(self, objectKey):
    return helper.Helper.mapToPath(objectKey)

  def getConfigNode(self, objectKey):
    return helper.Helper.mapToNode(objectKey)

  def getConfig(self, node, src_path, dest_path = None):
    return helper.Helper.copyConfig(os.path.join(self.configReader.getValue(self.SECTION, self.CONF_DIR), src_path), dest_path)
    #return helper.Helper.copyConfigFromRemote(node, src_path, dest_path)
    
  def applyChange(self, newConfig, node, path):
    configChangeNotifier.ConfigChangeApplier(newConfig, node, path).copyConfigToRemote()

  def notifyConfigChange(self, objectKey, ConfigDiff):
    server = self.configReader.getValue(self.SECTION, self.MAIL_SERVER)
    sender = self.configReader.getValue(self.SECTION, self.MAIL_SENDER)
    password = self.configReader.getValue(self.SECTION, self.MAIL_PASSWORD)
    receiver = self.configReader.getValue(self.SECTION, self.MAIL_RECEIVER)
    subject = self.configReader.getValue(self.SECTION, self.MAIL_SUBJECT) + ":S3 Object Key:" + objectKey 
    text = helper.Helper.getFileContents(ConfigDiff)
    
    mail = mailServer.MailServer(server, sender, password)
    mail.sendMessage(receiver, subject, text)
    return subject + "\001" + text

