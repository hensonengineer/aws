import boto3

# create an EC2 resource object using boto3
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):

    #filter using a list of dictionaries
    filters = [{
            'Name': 'tag:your-tag-name',
            'Values': ['your-tag-value']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    #ec2.instances.filter()  method is used to retrieve a list of instances that match the filter
    instances = ec2.instances.filter(Filters=filters)


    for instance in instances:
        print('Terminating', instance) # log which instances terminate to CloudWatch
        #instance.terminate() # uncomment when testing complete
   
