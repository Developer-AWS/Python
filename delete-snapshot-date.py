import boto3
import datetime
client = boto3.client('ec2',region_name='us-east-1')
snapshots = client.describe_snapshots(OwnerIds=['ID ACCOUNT HERE'])

def lambda_handler(event, context):
   for snapshot in snapshots['Snapshots']:
       a=snapshot['StartTime']
       b=a.date()
       c=datetime.datetime.now().date()
       d=c-b
       f=a.day
       excludeDate=datetime.datetime.strptime('2019-10-09', '%Y-%m-%d').date()
       try:
           if d.days>30 and f!=1 and b!=excludeDate:
               id = snapshot['SnapshotId']
               client.delete_snapshot(SnapshotId=id)
       except Exception,e:
           if 'InvalidSnapshot.InUse' in e.message:
               print "skipping this snapshot"
               continue
