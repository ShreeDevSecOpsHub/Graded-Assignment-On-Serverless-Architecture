# AWS Lambda + Boto3 Automation Assignments

This repository contains solutions for **6 AWS Lambda + Boto3** automation tasks as part of the assignment.

**Completed Assignments:**
- Assignment 1: Automated EC2 Start/Stop
- Assignment 2: S3 Old Files Cleanup
- Assignment 3: Unencrypted S3 Buckets Detection
- Assignment 4: EBS Snapshot Creation & Cleanup
- Assignment 5: Auto-Tagging EC2 Instances on Launch
- Assignment 7: DynamoDB Change Alert via SNS

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

*(Paste the code I gave you earlier)*

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

### 5. Auto-Tagging EC2 Instances on Launch
**File:** `assignment5_auto_tagging.py`

```python
import boto3
import logging
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    ec2 = boto3.client('ec2')
    
    # Get instance ID from CloudWatch Event
    instance_id = event['detail']['instance-id']
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Apply tags
    ec2.create_tags(
        Resources=[instance_id],
        Tags=[
            {'Key': 'AutoTagged', 'Value': 'True'},
            {'Key': 'LaunchDate', 'Value': current_date},
            {'Key': 'Environment', 'Value': 'Dev'}
        ]
    )
    
    logger.info(f"Successfully tagged instance {instance_id}")
    print(f"Instance {instance_id} tagged with LaunchDate: {current_date}")
    
    return {'statusCode': 200, 'message': f'Tagged instance {instance_id}'}
