###### FELIPE & GUSTAVO#####
import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    auto_scaling = boto3.client('autoscaling')
    
    
    today = datetime.today().strftime('%Y-%m-%d')
    images = ec2.describe_images(
        Filters=[
            {
                'Name':'tag:CreationDate',
                'Values':[today]
            }
        ]
    )
    print(json.dumps(images, indent=4, sort_keys=True, default=str))
    
    image_id = images['Images'][0]['ImageId']
    launch_conf_name = event['LaunchConfigurationName'] + today
        
    ref_launch_conf = auto_scaling.describe_launch_configurations(
        LaunchConfigurationNames=[event['LaunchConfigurationName']]
    )['LaunchConfigurations'][0]
    
    print ("Launch Configuration Raference")
    print (json.dumps(ref_launch_conf, sort_keys=True, indent=4, default=str))
        
    new_launch_conf = auto_scaling.create_launch_configuration(
        LaunchConfigurationName=launch_conf_name,
        ImageId=image_id,
        SecurityGroups=ref_launch_conf['SecurityGroups'],
        InstanceType=ref_launch_conf['InstanceType'],
        KeyName=ref_launch_conf['KeyName']
    )
    print ("New Launch Configuration:")
    print (json.dumps(new_launch_conf, sort_keys=True, indent=4, default=str))
    
    update_as = auto_scaling.update_auto_scaling_group(
        AutoScalingGroupName=event['AutoScalingGroupName'],
        LaunchConfigurationName=launch_conf_name
    )
    print ("Updated Auto Scalling Group")
    print (json.dumps(update_as, sort_keys=True, indent=4, default=str))

    return 'Ok'
    
    
    
    #Params
#{
#  "AutoScalingGroupName": "NameXXX",
#  "LaunchConfigurationName": "NameXXX"
#}
