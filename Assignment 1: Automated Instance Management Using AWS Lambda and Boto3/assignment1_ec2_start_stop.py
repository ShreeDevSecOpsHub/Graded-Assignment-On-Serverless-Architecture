import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Find Auto-Stop instances
    stop_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}]
    )
    
    stop_instance_ids = []
    for reservation in stop_response['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] != 'stopped':
                stop_instance_ids.append(instance['InstanceId'])
    
    # Find Auto-Start instances
    start_response = ec2.describe_instances(
        Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}]
    )
    
    start_instance_ids = []
    for reservation in start_response['Reservations']:
        for instance in reservation['Instances']:
            if instance['State']['Name'] != 'running':
                start_instance_ids.append(instance['InstanceId'])
    
    # Perform actions
    if stop_instance_ids:
        ec2.stop_instances(InstanceIds=stop_instance_ids)
        logger.info(f"Stopped instances: {stop_instance_ids}")
        print(f"Stopped instances: {stop_instance_ids}")
    
    if start_instance_ids:
        ec2.start_instances(InstanceIds=start_instance_ids)
        logger.info(f"Started instances: {start_instance_ids}")
        print(f"Started instances: {start_instance_ids}")
    
    return {
        'statusCode': 200,
        'body': f"Processed {len(stop_instance_ids)} stops and {len(start_instance_ids)} starts"
    }
