import boto3
import sys, os
import logging
import traceback 

logger = logging.getLogger("s3Integration")

class S3Dao:

  def __init__(self):
    try:
      self.s3 = boto3.resource('s3')
    except:
      logger.error("Cannot instantiate S3 resource")
      raise Exception("Cannot instantiate S3 resource")

  def getBucket(self):
    return self.bucket

  def setBucket(self, bucket_name):
    self.bucket = bucket_name 

  def downloadObject(self, key, pathname, bucket_name = None):
    print "pathname =======", pathname
    if bucket_name == None:
      bucket_name = self.bucket
    try:
      s3object = self.getObjectIfExists(key, bucket_name)
      print "dirname ====", os.path.dirname(pathname)
      if not os.path.exists(os.path.dirname(pathname)):
        print "dirname ====", os.path.dirname(pathname)
        os.makedirs(os.path.dirname(pathname))
      s3object.download_file(pathname)   
    except:
      logger.error("Cannot download object to file " + pathname + " from bucket " + bucket_name + " having key " + key)     
      raise Exception("Cannot download object to file " + pathname + " from bucket " + bucket_name + " having key " + key + traceback.format_exc())

  def uploadObject(self, key, pathname, bucket_name = None):
    if bucket_name == None:
      bucket_name = self.bucket
    try:
      bucket = self.getBucketIfExists(bucket_name)
      bucket.upload_file(pathname, key)
    except:
      logger.error("Cannot upload file " + pathname + " to bucket " + bucket_name + " with key " + key)
      raise Exception("Cannot upload file " + pathname + " to bucket " + bucket_name + " with key " + key)

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
      raise Exception("Cannot delete object with key " + key + " from bucket " + bucket_name)

  def getAllObjects(self, bucket_name = None):
    if bucket_name == None:
      bucket_name = self.getBucket()
    listOfObjects = []  
    for obj in self.s3.Bucket(bucket_name).objects.all():
      listOfObjects.append(obj.key)
    return listOfObjects
