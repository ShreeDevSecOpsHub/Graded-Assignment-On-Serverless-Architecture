
Created two t2.micro EC2 instances.
Tagged first with Key=Action, Value=Auto-Stop; second with Auto-Start.
Created IAM role with AmazonEC2FullAccess.
Created Lambda function (Python 3.12), attached role, pasted code.
Manually invoked → verified states changed in EC2 console.
