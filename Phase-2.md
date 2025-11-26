<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>PHASE 2 – Lambda Event Automation</title>
</head>
<body>

<h1>🟩 PHASE 2 – Lambda Event Automation (README.md)</h1>

<p>This phase implements serverless automation using AWS Lambda.  
When a file is uploaded to S3, Lambda will:</p>

<ul>
  <li>✔ Capture S3 event metadata</li>
  <li>✔ Store the event in DynamoDB</li>
  <li>✔ Send notification via SNS</li>
  <li>✔ Push a message into SQS</li>
  <li>✔ Log full details to CloudWatch Logs</li>
</ul>


<h2>🧠 1. Create Lambda Function (cloudops-event-handler)</h2>

<h3>Step 1: Open Lambda Console</h3>
<ol>
  <li>Go to AWS Console → Lambda</li>
  <li>Click <strong>Create Function</strong></li>
</ol>

<h3>Step 2: Configure Function</h3>
<ul>
  <li>Author from scratch</li>
  <li>Function name: <strong>cloudops-event-handler</strong></li>
  <li>Runtime: Python 3.10</li>
  <li>Architecture: x86_64</li>
  <li>Permissions: Use existing role → <strong>CloudOpsLambdaRole</strong></li>
</ul>

<h3>Step 3: Create Function</h3>
<p>Click <strong>Create Function</strong></p>

<hr/>

<h2>🧠 2. Add S3 Trigger (ObjectCreated Event)</h2>

<h3>Step 1: Open Lambda → Triggers</h3>
<ol>
  <li>Open the Lambda function page</li>
  <li>Under “Function overview” click <strong>Add trigger</strong></li>
</ol>

<h3>Step 2: Configure Trigger</h3>
<ul>
  <li>Trigger: S3</li>
  <li>Bucket: <strong>cloudops-event-bucket</strong></li>
  <li>Event Type: All object create events</li>
  <li>Prefix: (leave blank)</li>
  <li>Suffix: (leave blank)</li>
  <li>Enable trigger: ✔ Checked</li>
</ul>

<h3>Step 3: Save</h3>
<p>Click <strong>Add</strong></p>

<p>This allows S3 uploads to invoke your Lambda function.</p>

<hr/>

<h2>🧠 3. Configure Environment Variables (Recommended)</h2>

<p>Lambda → Configuration → Environment variables → Add:</p>

<table border="1" cellpadding="4" cellspacing="0">
  <tr><th>Key</th><th>Value</th></tr>
  <tr><td>DDB_TABLE</td><td>cloudops_events</td></tr>
  <tr><td>SNS_TOPIC_ARN</td><td>arn:aws:sns:us-east-1:784154679353:cloudops-alerts</td></tr>
  <tr><td>SQS_QUEUE_URL</td><td>https://sqs.us-east-1.amazonaws.com/784154679353/cloudops-job-queue</td></tr>
</table>

<p>(Environment variables allow easy updates without editing code.)</p>

<hr/>

<h2>🧠 4. Add IAM Permissions (CloudOpsLambdaRole)</h2>

<p>Role: <strong>CloudOpsLambdaRole</strong></p>

<p>Attach these AWS-managed policies:</p>
<ul>
  <li>✔ AmazonDynamoDBFullAccess</li>
  <li>✔ AmazonSNSFullAccess</li>
  <li>✔ AmazonSQSFullAccess</li>
  <li>✔ AWSLambdaBasicExecutionRole</li>
</ul>

<p>(Later replace with least-privilege policy in Phase 3.)</p>

<hr/>

<h2>🧠 5. Write Lambda Python Code</h2>

<p>Open Lambda → Code → <strong>lambda_function.py</strong>  
Replace code with:</p>

<pre>
import json
import os
import time
import uuid
import boto3
from botocore.exceptions import ClientError

REGION = os.environ.get("AWS_REGION", "us-east-1")
DDB_TABLE = os.environ.get("DDB_TABLE", "cloudops_events")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN", "")
SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL", "")

dynamo = boto3.resource("dynamodb", region_name=REGION)
ddb_table = dynamo.Table(DDB_TABLE)
sns = boto3.client("sns", region_name=REGION)
sqs = boto3.client("sqs", region_name=REGION)

def lambda_handler(event, context):
    print("EVENT RECEIVED:", json.dumps(event))
    timestamp = int(time.time())
    try:
        records = event.get("Records", [])
        for r in records:
            if r.get("eventSource") == "aws:s3":
                bucket = r["s3"]["bucket"]["name"]
                key = r["s3"]["object"]["key"]
                event_id = str(uuid.uuid4())

                item = {
                    "event_id": event_id,
                    "bucket": bucket,
                    "object_key": key,
                    "timestamp": str(timestamp)
                }

                print("Putting item to DynamoDB:", item)
                ddb_table.put_item(Item=item)

                if SNS_TOPIC_ARN:
                    sns.publish(
                        TopicArn=SNS_TOPIC_ARN,
                        Subject="S3 Upload Event",
                        Message=f"File uploaded: {bucket}/{key}"
                    )

                if SQS_QUEUE_URL:
                    sqs.send_message(
                        QueueUrl=SQS_QUEUE_URL,
                        MessageBody=json.dumps(item)
                    )

        return {"status": "OK"}

    except Exception as e:
        print("Error:", str(e))
        raise
</pre>

<p>Click <strong>Deploy</strong></p>

<hr/>

<h2>🧠 6. Enable CloudWatch Logs</h2>

<p>CloudWatch logging is enabled via:</p>
<ul>
  <li>✔ AWSLambdaBasicExecutionRole</li>
</ul>

<p>Verify logs:</p>
<p>AWS Console → CloudWatch → Logs → <strong>/aws/lambda/cloudops-event-handler</strong></p>

<hr/>

<h2>🧠 7. End-to-End Testing</h2>

<h3>Step 1: Upload a file to S3</h3>
<p>Bucket: <strong>cloudops-event-bucket</strong></p>
<p>Example file: <strong>test.jpg</strong></p>

<h3>Step 2: Verify Lambda Runs</h3>
<p>Check CloudWatch logs for:</p>
<ul>
  <li>EVENT RECEIVED</li>
  <li>Putting item to DynamoDB</li>
  <li>SNS publish response</li>
  <li>SQS send_message response</li>
</ul>

<h3>Step 3: Verify DynamoDB</h3>
<p>Go to DynamoDB → Tables → <strong>cloudops_events</strong> → Items</p>

<p>You should see entries like:</p>

<pre>
{
  "event_id": "uuid",
  "bucket": "cloudops-event-bucket",
  "object_key": "test.jpg",
  "timestamp": "...."
}
</pre>

<h3>Step 4: Verify SNS</h3>
<p>Check your email inbox for alert message.</p>

<h3>Step 5: Verify SQS</h3>
<p>SQS → Your Queue → Send and receive messages → Poll messages  
You should see messages generated by Lambda.</p>

<hr/>

<h2>🧠 8. Verification Summary (Copy to Notion Table)</h2>

<table border="1" cellpadding="4" cellspacing="0">
  <tr><th>Step</th><th>Verification</th></tr>
  <tr><td>Lambda Created</td><td>AWS Console → Lambda Dashboard</td></tr>
  <tr><td>S3 Trigger Working</td><td>Upload file → Lambda invoked</td></tr>
  <tr><td>DynamoDB Working</td><td>Items shown in cloudops_events</td></tr>
  <tr><td>SNS Working</td><td>Email received</td></tr>
  <tr><td>SQS Working</td><td>Queue shows messages</td></tr>
  <tr><td>CloudWatch Logs</td><td>Logs show detailed processing</td></tr>
  <tr><td>End-to-End Tested</td><td>All components responded correctly</td></tr>
  <tr><td>Documentation Done</td><td>Phase 2 README ready</td></tr>
</table>

<hr/>

<h2>🎉 PHASE 2 Completed Successfully</h2>

<p>You have implemented:</p>
<ul>
  <li>✔ S3 Event Trigger</li>
  <li>✔ Lambda Automation</li>
  <li>✔ DynamoDB Logging</li>
  <li>✔ SNS Alerts</li>
  <li>✔ SQS Queue Messaging</li>
  <li>✔ CloudWatch Observability</li>
</ul>

</body>
</html>
