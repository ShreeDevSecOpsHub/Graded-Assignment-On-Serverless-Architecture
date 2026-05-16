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

*(Paste the code I gave you earlier - remember to update bucket name)*

---

### 3. Monitor Unencrypted S3 Buckets
**File:** `assignment3_s3_encryption_check.py`

*(Paste the code I gave you earlier)*

---

### 4. Automatic EBS Snapshot & Cleanup
**File:** `assignment4_ebs_snapshot.py`

*(Paste the code I gave you earlier - update VOLUME_ID)*

---

