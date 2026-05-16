import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    unencrypted = []
    
    # List all buckets
    buckets = s3.list_buckets()['Buckets']
    
    for bucket in buckets:
        bucket_name = bucket['Name']
        try:
            encryption = s3.get_bucket_encryption(Bucket=bucket_name)
            # If it reaches here, encryption is configured
            logger.info(f"Bucket {bucket_name} is encrypted")
        except s3.exceptions.ClientError as e:
            if 'ServerSideEncryptionConfigurationNotFoundError' in str(e):
                unencrypted.append(bucket_name)
                logger.warning(f"Unencrypted bucket found: {bucket_name}")
            else:
                logger.error(f"Error checking {bucket_name}: {str(e)}")
    
    if unencrypted:
        print(f"Unencrypted buckets: {unencrypted}")
    else:
        print("All buckets have encryption enabled.")
    
    return {
        'statusCode': 200,
        'unencrypted_buckets': unencrypted
    }
