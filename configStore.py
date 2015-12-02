from s3Dao import S3Dao
import logging
from configReader import ConfigReader
import os

logger = logging.getLogger("s3Integration")

class ConfigStore:
  
  def ConfigStore(self, bucket):
    self.dao = S3Dao()
    self.dao.setBucket(bucket)

  def NotifyConfigChanges(self, key, value, pathname):
    temp_file = "/tmp/temp.cfg"
    helper = Helper(pathname, temp_file)
    objectKey = helper.mapToKey(pathname)
    open(temp_file, "w").close()
    self.dao.downloadObject(objectKey, temp_file)
    if helper.compareConfig():
      #self.dao.uploadObject(pathname, objectKey)    
    os.remove(temp_file)

class Helper:

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
          
  def mapToKeySectionPair(self):
    pass
    
