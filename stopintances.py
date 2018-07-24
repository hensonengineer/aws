import boto3
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):

    filters = [{
            'Name': 'tag:your-tag-name',
            'Values': ['your-tag-value']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running']
        }
    ]
    
    instances = ec2.instances.filter(Filters=filters)


    for instance in instances:
        print('stopping', instance) #console logging so you can see which instances were stopped in CloudWatch
        #instance.stop() #uncomment this once you've tested
   
