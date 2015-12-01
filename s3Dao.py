import boto3
import sys
import logging

logger = logging.getLogger("s3Integration")

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

  def downloadObject(self, key, pathname):
    self.downloadObject(self.bucket, key, pathname)
 
  def uploadObject(self, key, pathname):
    self.uploadObject(self.bucket, key, pathname)

  def downloadObject(self, bucket_name, key, pathname):
    try:
      s3object = self.getObjectIfExists(bucket_name, key)
      if s3object == None:
        logger.error("Object with key " + key + " does not exist in bucket " + bucket_name)
        raise ValueError("Object with key " + key + " does not exist in bucket " + bucket_name)
      s3object.download_file(pathname)   
    except:
      logger.error("Cannot download object to file " + pathname + " from bucket " + bucket_name + " having key " + key)     

  def uploadObject(self, bucket_name, key, pathname):
    try:
      if self.getObjectIfExists(bucket_name, key) != None:
        logger.error("Object with key " + key + " already exists in bucket " + bucket_name)
        raise ValueError("Object with key " + key + " already exists in bucket " + bucket_name)
      self.s3.Bucket(bucket_name).upload_file(pathname, key)
    except:
      logger.error("Cannot upload file " + pathname + " to bucket " + bucket_name + " with key " + key)

  def getBuckets(self):
    listOfBuckets = []
    for bucket in self.s3.buckets.all():
        listOfBuckets.append(bucket.name) 
    return listOfBuckets

  def getObjectIfExists(self, key):
    return self.getObjectIfExists(self.bucket, key)

  def getObjectIfExists(self, bucket_name, key):
    if self.getBucketIfExists(bucket_name) == None:
        raise ValueError("Bucket " + bucket_name + " does not exist")
    return self.s3.Object(bucket_name, key)

  def getBucketIfExists(self, bucket_name):
    return self.s3.Bucket(bucket_name)
    
  def createBucket(self, bucket_name):
    if self.getBucketIfExists(bucket_name) != None:
      raise ValueError("Bucket with name " + bucket_name + " already exists")
    pass

  def removeObject(self, key):
    self.removeObject(self.bucket, key)

  def removeObject(self, bucket_name, key):
    try:
      s3object = self.getObjectIfExists(bucket_name, key)
      if s3object == None:
        logger.error("Object with key " + key + " does not exist in bucket " + bucket_name)
        raise ValueError("Object with key " + key + " does not exist in bucket " + bucket_name)
      s3object.delete()
    except:
      logger.error("Cannot delete object with key " + key + " from bucket " + bucket_name)

