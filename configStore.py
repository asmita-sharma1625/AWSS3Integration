from s3Dao import S3Dao
import logging
from configReader import ConfigReader
import os

logger = logging.getLogger("s3Integration")

class ConfigStore:
  
  def ConfigStore(self, bucket):
    self.dao = S3Dao()
    self.dao.setBucket(bucket)

  def updateConfig(self, key, value, pathname):
    temp_file = "/tmp/temp.cfg"
    keySectionPair = Helper.mapToKeySectionPair(pathname)
    objectKey = keySectionPair[0]
    section = keySectionPair[1] 
    open(temp_file, "w").close()
    self.dao.downloadObject(objectKey, temp_file)
    Helper.mergeConfig(pathname, temp_file, section)
    self.dao.uploadObject(pathname, objectKey)    
    os.remove(temp_file)

class Helper:
  
  @staticmethod
  def mergeConfig(oldConfig, newConfig, section):
    oldConfigReader = ConfigReader(oldConfig)
    newConfigReader = ConfigReader(newConfig)
    oldKeys = oldConfigReader.getKeys(section)
    newKeys = newConfigReader.getKeys(section)
    for key in oldKeys:
      if key in newKeys:
        oldConfigReader.setValue(section, key, newConfigReader.getValue(section, key))
          
  @staticmethod
  def mapToKeySectionPair(pathname):
    pass
    
