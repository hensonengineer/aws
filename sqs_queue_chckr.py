import boto3
import csv

# Initialize a boto3 client
sqs = boto3.client('sqs', region_name='us-east-1')

# Fetch the list of all SQS queue URLs in the specified region
queues = sqs.list_queues()
queue_urls = queues.get('QueueUrls', [])

# Prepare to write to CSV
with open('queues_and_keys.csv', 'w', newline='') as csvfile:
    fieldnames = ['QueueURL', 'KmsMasterKeyId']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    # For each queue URL, fetch its encryption status or associated KMS Key
    for queue_url in queue_urls:
        attributes = sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['KmsMasterKeyId']
        )
        kms_master_key_id = attributes.get('Attributes', {}).get('KmsMasterKeyId', 'Not Encrypted')
        
        # Write the queue URL and its KMS Master Key ID to the CSV
        writer.writerow({'QueueURL': queue_url, 'KmsMasterKeyId': kms_master_key_id})

print("CSV file 'queues_and_keys.csv' created successfully.")
