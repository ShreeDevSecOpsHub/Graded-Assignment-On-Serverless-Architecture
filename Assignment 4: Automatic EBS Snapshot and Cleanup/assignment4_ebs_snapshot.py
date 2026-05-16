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
