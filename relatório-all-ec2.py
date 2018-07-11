import boto3
#Keys user
access_key = "keyxxx"
secret_key = "keyxxx"
#Autenticação
client = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key,
                                  region_name='us-east-1')

ec2_regions = [region['RegionName'] for region in client.describe_regions()['Regions']]

for region in ec2_regions:
    conn = boto3.resource('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key,
                   region_name=region)
    instances = conn.instances.filter()
    for instance in instances:
        if instance.state["Name"] == "Running":
            print(" (Id) ", instance.id," (Type) ", instance.instance_type ," (Public-IP) ", instance.public_ip_address," (Platform) ", instance.tags , " (VPC) ", instance.vpc_id, "(Subnet)" , instance.subnet_id ,  " (Region) ",  region)
