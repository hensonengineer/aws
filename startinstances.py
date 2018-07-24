
import boto3
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):

    filters = [{
            'Name': 'tag:your-tag-name',
            'Values': ['your-tag-value']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        }
    ]
    
    instances = ec2.instances.filter(Filters=filters)


    for instance in instances:
        print('starting', instance) #console log to Cloudwatch
        #instance.start() # uncomment after testing 
   
