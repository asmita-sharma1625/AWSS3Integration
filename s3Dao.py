import boto3
import sys
import logging

logger = logging.getLogger("s3Integration")
logger.addHandler(logging.FileHandler("/tmp/s3Integration.log"))

class S3Dao:

  def __init__(self):
    try:
      self.s3 = boto3.resource('s3')
    except:
      logger.error("Cannot instantiate S3 resource")

  def getBucket(self):
    return self.bucket

  def setBucket(self, bucket_name):
    self.bucket = bucket_name 

  def downloadObject(self, key, pathname, bucket_name = None):
    if bucket_name == None:
      bucket_name = self.bucket
    try:
      s3object = self.getObjectIfExists(key, bucket_name)
      s3object.download_file(pathname)   
    except:
      logger.error("Cannot download object to file " + pathname + " from bucket " + bucket_name + " having key " + key)     

  def uploadObject(self, key, pathname, bucket_name = None):
    if bucket_name == None:
      bucket_name = self.bucket
    try:
      bucket = self.getBucketIfExists(bucket_name)
      bucket.upload_file(pathname, key)
    except:
      logger.error("Cannot upload file " + pathname + " to bucket " + bucket_name + " with key " + key)

  def getBuckets(self):
    listOfBuckets = []
    for bucket in self.s3.buckets.all():
        listOfBuckets.append(bucket.name) 
    return listOfBuckets

  def getObjectIfExists(self, key, bucket_name = None):
    if bucket_name == None:
      bucket_name = self.bucket
    return self.s3.Object(bucket_name, key)

  def getBucketIfExists(self, bucket_name):
    return self.s3.Bucket(bucket_name)
    
  def removeObject(self, key, bucket_name = None):
    if bucket_name == None:
      bucket_name = self.bucket
    try:
      s3object.delete()
    except:
      logger.error("Cannot delete object with key " + key + " from bucket " + bucket_name)

