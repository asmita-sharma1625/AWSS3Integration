from configChangeNotifier import ConfigChangeNotifier

class ConfigManager:

  def __init__(self):
    
    self.S3_BUCKET = "compute-config"
    self.s3Dao = S3Dao()
    self.s3Dao.setBucket(self.S3_BUCKET)

  def reportAllConfigChange(self):
    objects = self.getAllS3Objects()
    for obj in objects:
      self.reportOrApplyConfigChange(obj)      

  def reportOrApplyConfigChange(self, objectKey, apply_flag = False):
    newConfig = "/tmp/newConfig.conf"
    self.getS3Object(objectKey, newConfig)
    OLD_CONFIG_PATH = self.getConfigPath(objectKey)
    OLD_CONFIG_NODE = self.getConfigNode(objectKey)
    oldConfig = "/tmp/oldConfig.conf"
    self.getConfig(OLD_CONFIG_NODE, OLD_CONFIG_PATH, oldConfig)
    configChangeDetector = ConfigChangeDetector(oldConfig, newConfig)
    if configChangeDetector.compareConfig():
      old_config_diff = configChangeDetector.getDiffInOldConfig()
      new_config_diff = configChangeDetector.getDiffInNewConfig()
      ''' notify any change to registered user along 
          with objectKey and diff files if apply_flag is False 
          else apply the change on the related node'''
      if apply_flag:
        self.applyChange(newConfig, OLD_CONFIG_NODE, OLD_CONFIG_PATH)
      else:
        self.notifyConfigChange(objectKey, old_config_diff, new_config_diff)
        #call mail server to send notification with diff files and objectKey and old config node and path.

  def getAllS3Objects(self):
    return self.s3Dao.listObjects()

  def getS3Object(self, objectKey, newConfig):
    self.s3Dao.downloadObject(objectKey, newConfig)

  def getConfigPath(self, objectKey):
    return Helper.mapToPath(objectKey)

  def getConfigNode(self, objectKey):
    return Helper.mapToNode(objectKey)

  def getConfig(self, node, src_path, dest_path = None):
    return Helper.copyConfigFromRemote(node, src_path, dest_path)
    
  def applyChange(self, newConfig, node, path):
    ConfigChangeApplier(newConfig, node, path).copyConfigToRemote()

  def notifyConfigChange(self, objectKey, oldConfigDiff, newConfigDiff):
    server = "smtp.mail.yahoo.com"
    sender = "s3.notifier@yahoo.com"
    password = "jio@1234"
    receiver = "itsmeasmi25@gmail.com"
    subject = "JCS_Config_Change_Notification : S3 Object Key" + objectKey 
    oldDiffContent = "On Node Configuration :\n" + Helper.getFileContents(oldConfigDiff)
    newDiffContent = "S3 Configuration :\n" + Helper.getFileContents(newConfigDiff)
    text = "Config Differences - \n " + oldDiffContent + "\n\n\n\n" + newDiffContent
    mailServer = MailServer(server, sender, password)
    mailServer.sendMessage(receiver, subject, text)



