import boto3
import sys
import logging

logger = logging.getLogger("s3Integration")

class s3Access:

  def s3Access(self):
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
      self.s3.Bucket(bucket_name).download_file(key, pathname)   
    except:
      logger.error("Cannot download object to file " + pathname + " from bucket " + bucket_name + " having key " + key)     

  def uploadObject(self, bucket_name, key, pathname):
    try:
      self.s3.Bucket(bucket_name).upload_file(pathname, key)
    except:
      logger.error("Cannot upload file " + pathname + " to bucket " + bucket_name + " with key " + key)

  def getBuckets(self):
    for bucket in self.s3.buckets.all():
        print(bucket.name)  
