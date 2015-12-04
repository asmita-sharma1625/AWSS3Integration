from s3Dao import S3Dao
import sys

if len(argv) == 4:
  bucket = sys.argv[1]
  key = sys.argv[2]
  path = sys.argv[3]
else:
  raise Exception("Invalid Arguments passed. Required : S3 bucket, Key and Filepath")

s3Dao = S3Dao()
s3Dao.uploadObject(key, path, bucket)

