from s3Dao import S3Dao
import logging
from configReader import ConfigReader
import os
from helper import Helper

logger = logging.getLogger("s3Integration")

class ConfigChangeNotifier:
  
  def __init__(self, bucket, objectKey):
    self.dao = S3Dao()
    self.dao.setBucket(bucket)
    self.objectKey = objectKey
    self.oldConfig = Helper.getConfigFromRemote(self.objectKey)

  def NotifyIfConfigChange(self):
    newConfig = "/tmp/newConfig.conf"
    configChangeDetector = ConfigChangeDetector(self.oldConfig, newConfig)
    open(newConfig, "w").close()
    self.dao.downloadObject(self.objectKey, newConfig)
    if configChangeDetector.compareConfig():
      #self.dao.uploadObject(pathname, objectKey)    
    os.remove(newConfig)

class ConfigChangeDetector:

  def __init__(self, oldConfig, newConfig):
    self.oldConfig = oldConfig
    self.newConfig = newConfig
    self.oldConfigReader = ConfigReader(self.oldConfig)
    self.newConfigReader = ConfigReader(self.newConfig)
    self.flag = False

  def compareConfig(self):
    oldSections = self.oldConfigReader.getSections()
    newSections = self.newConfigReader.getSections()
    for section in newSections:
      if section not in oldSections:
        oldConfigReader.addSection(section)
        self.flag = True  
      Helper.compareSection(oldConfig, newConfig, section)
    return self.flag

  def compareSection(self, section):
    oldKeys = self.oldConfigReader.getKeys(section)
    newKeys = self.newConfigReader.getKeys(section)
    for key in newKeys:
      if key not in oldKeys:
        self.flag = True
        # Trigger Notification
        #oldConfigReader.setValue(section, key, newConfigReader.getValue(section, key))
      oldValue = self.oldConfigReader.getValue(section, key)
      newValue = self.newConfigReader.getValue(section, key)
      if oldValue != newValue:
        self.flag = True
