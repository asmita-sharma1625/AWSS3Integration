import unittest
from  s3Dao import S3Dao
import boto3

class TestS3Dao(unittest.TestCase):

  BUCKET = "compute-config"
  KEY = "demo_file"

  def setUp(self):
    self.s3Dao = S3Dao()
    self.s3Dao.setBucket(TestS3Dao.BUCKET)

  def test_getBucket(self):
    self.assertEquals(TestS3Dao.BUCKET, self.s3Dao.getBucket())

  def test_bucketExists(self):
    self.assertFalse(self.s3Dao.getBucketIfExists(TestS3Dao.BUCKET) == None)

  def test_uploadObjectIfNotExists(self):
    self.s3Dao.removeObject(TestS3Dao.KEY)
    self.assertTrue(self.s3Dao.getObjectIfExists(TestS3Dao.KEY) == None)
    open("/tmp/foo.txt", "a").close()
    self.s3Dao.uploadObject(TestS3Dao.KEY, "/tmp/foo.txt")
    self.assertFalse(self.s3Dao.getObjectIfExists(TestS3Dao.KEY) == None)

if __name__ == '__main__':
  unittest.main()
   
