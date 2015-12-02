from s3Dao import S3Dao
import logging
from configReader import ConfigReader

logger = logging.getLogger("s3Integration")

class ConfigStore:
  
  def ConfigStore(self, bucket):
    self.dao = S3Dao()
    self.dao.setBucket(bucket)

  def updateConfig(self, key, value, pathname):
    temp_file = "/tmp/temp.cfg"
    objectKey = Helper.mapToKey(pathname)
    open(temp_file, "w").close()
    self.dao.downloadObject(objectKey, temp_file)
    Helper.mergeConfig(pathname, temp_file)


class Helper:
  
  def mergeConfig(oldConfig, newConfig):
    oldConfigReader = ConfigReader(oldConfig)
    newConfigReader = ConfigReader(newConfig)
    
