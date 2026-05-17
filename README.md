# AWS Lambda + Boto3 Automation Assignments

This repository contains solutions for **6 AWS Lambda + Boto3** automation tasks as part of the assignment.

**Completed Assignments:**
- Assignment 1: Automated EC2 Start/Stop
- Assignment 2: S3 Old Files Cleanup
- Assignment 3: Unencrypted S3 Buckets Detection
- Assignment 4: EBS Snapshot Creation & Cleanup

---

## Architecture & Best Practices Followed

- Used Python 3.12 runtime
- Proper logging using `logging` module
- Least privilege considered (though FullAccess used for simplicity)
- Error handling and meaningful log messages
- Environment variable ready (for production)

---

## Assignment Details & Code

### 1. Automated Instance Management (EC2 Start/Stop)
**File:** `assignment1_ec2_start_stop.py`
```python
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
```

**Steps:**
1. Launched 2 t2.micro instances
2. Tagged them with `Action: Auto-Stop` and `Action: Auto-Start`
3. Created IAM Role + Lambda function
4. Manually invoked → Instances stopped/started successfully

---

### 2. Automated S3 Bucket Cleanup
**File:** `assignment2_s3_cleanup.py`

```python
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
```

---

### 3. Monitor Unencrypted S3 Buckets
**File:** `assignment3_s3_encryption_check.py`

```python
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
```

---

### 4. Automatic EBS Snapshot & Cleanup
**File:** `assignment4_ebs_snapshot.py`

```python
import boto3
from datetime import datetime, timedelta, timezone
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

VOLUME_ID = 'vol-XXXXXXXXXXXXXXXXX'   # Change this
RETENTION_DAYS = 30

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    now = datetime.now(timezone.utc)
    
    # Create new snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description=f"Automated backup of {VOLUME_ID} at {now}"
    )
    snapshot_id = snapshot['SnapshotId']
    logger.info(f"Created snapshot: {snapshot_id}")
    print(f"Created snapshot: {snapshot_id}")
    
    # Cleanup old snapshots
    snapshots = ec2.describe_snapshots(
        Filters=[{'Name': 'volume-id', 'Values': [VOLUME_ID]}]
    )['Snapshots']
    
    deleted = []
    threshold = now - timedelta(days=RETENTION_DAYS)
    
    for snap in snapshots:
        snap_time = snap['StartTime']
        if snap_time < threshold and snap['SnapshotId'] != snapshot_id:
            ec2.delete_snapshot(SnapshotId=snap['SnapshotId'])
            deleted.append(snap['SnapshotId'])
            logger.info(f"Deleted old snapshot: {snap['SnapshotId']}")
    
    print(f"Deleted {len(deleted)} old snapshots")
    return {
        'statusCode': 200,
        'new_snapshot': snapshot_id,
        'deleted_count': len(deleted)
    }
```

---

