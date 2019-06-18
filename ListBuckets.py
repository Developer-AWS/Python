import boto
from boto.s3.connection import S3Connection
s3 = boto.connect_s3()  
buckets = s3.get_all_buckets() 
for key in buckets:
    print key.name
