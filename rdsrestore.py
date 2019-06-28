import boto3  
import botocore  
import datetime  
import re  
import logging

region='us-east-1'  
db_instance_class='db.t2.micro'  
db_subnet='default'  
instances = ['instance01', 'instance02']

print('Loading function')

def byTimestamp(snap):  
  if 'SnapshotCreateTime' in snap:
    return datetime.datetime.isoformat(snap['SnapshotCreateTime'])
  else:
    return datetime.datetime.isoformat(datetime.datetime.now())

  #Fuck função!!
def lambda_handler(event, context):  
    source = boto3.client('rds', region_name=region)
    for instance in instances:
        try:
            source_snaps = source.describe_db_snapshots(DBInstanceIdentifier = instance)['DBSnapshots']
            print "DB_Snapshots:", source_snaps
            source_snap = sorted(source_snaps, key=byTimestamp, reverse=True)[0]['DBSnapshotIdentifier']
            snap_id = (re.sub( '-\d\d-\d\d-\d\d\d\d ?', '', source_snap))
            print('Will restore %s to %s' % (source_snap, snap_id))
            response = source.restore_db_instance_from_db_snapshot(DBInstanceIdentifier=snap_id,                                                        DBSnapshotIdentifier=source_snap DBInstanceClass=db_instance_class, DBSubnetGroupName=db_subnet,MultiAZ=False,PubliclyAccessible=True)
            print(response)

        except botocore.exceptions.ClientError as e:
            raise Exception("Could not restore: %s" % e)
