from  AWSS3Integration.s3Dao import S3Dao
import logging

logger = logging.getLogger("s3Integration")

class ConfigStore:
  
  def ConfigStore(self, bucket):
    self.dao = S3Dao()
    self.dao.setBucket(bucket)

  def writeToConfig(key, value,  
