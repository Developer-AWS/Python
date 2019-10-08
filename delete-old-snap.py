# Delete snapshots older than retention period

import boto3
from botocore.exceptions import ClientError

from datetime import datetime,timedelta

def delete_snapshot(snapshot_id, reg):
    print "Deleting snapshot %s " % (snapshot_id)
    try:  
        ec2resource = boto3.resource('ec2', region_name=reg)
        snapshot = ec2resource.Snapshot(snapshot_id)
        snapshot.delete()
    except ClientError as e:
        print "Caught exception: %s" % e
        
    return
    
def lambda_handler(event, context):
    
    # Get current timestamp in UTC
    now = datetime.now()

	# AWS Account ID    
	account_id = '1234567890'
    
    # Define retention period in days
    retention_days = 10
    
    # Create EC2 client
    ec2 = boto3.client('ec2')
    
    # Get list of regions
    regions = ec2.describe_regions().get('Regions',[] )

    # Iterate over regions
    for region in regions:
        print "Checking region %s " % region['RegionName']
        reg=region['RegionName']
        
        # Connect to region
        ec2 = boto3.client('ec2', region_name=reg)
        
        # Filtering by snapshot timestamp comparison is not supported
        # So we grab all snapshot id's
        result = ec2.describe_snapshots( OwnerIds=[account_id] )
    
        for snapshot in result['Snapshots']:
            print "Checking snapshot %s which was created on %s" % (snapshot['SnapshotId'],snapshot['StartTime'])
       
            # Remove timezone info from snapshot in order for comparison to work below
            snapshot_time = snapshot['StartTime'].replace(tzinfo=None)
        
            # Subtract snapshot time from now returns a timedelta 
            # Check if the timedelta is greater than retention days
            if (now - snapshot_time) > timedelta(retention_days):
                print "Snapshot is older than configured retention of %d days" % (retention_days)
                delete_snapshot(snapshot['SnapshotId'], reg)
            else:
                print "Snapshot is newer than configured retention of %d days so we keep it" % (retention_days)          
  
