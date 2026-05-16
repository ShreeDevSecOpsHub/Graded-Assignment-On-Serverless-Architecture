import boto3
from datetime import datetime, timedelta, timezone
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BUCKET_NAME = 'your-bucket-name-here'   # Change this

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    now = datetime.now(timezone.utc)
    threshold = now - timedelta(days=30)
    
    deleted = []
    paginator = s3.get_paginator('list_objects_v2')
    
    for page in paginator.paginate(Bucket=BUCKET_NAME):
        if 'Contents' not in page:
            continue
        for obj in page['Contents']:
            if obj['LastModified'] < threshold:
                s3.delete_object(Bucket=BUCKET_NAME, Key=obj['Key'])
                deleted.append(obj['Key'])
                logger.info(f"Deleted: {obj['Key']}")
    
    print(f"Deleted {len(deleted)} objects older than 30 days")
    return {'statusCode': 200, 'deleted_count': len(deleted)}
