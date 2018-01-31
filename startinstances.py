import boto3
ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
    filters = [{
            'Name': 'your tag name',
            'Values': ['your tag value']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
        }
    ]
    
    instances = ec2.instances.filter(Filters=filters)

    runningInstances = [instance.id for instance in instances]
    
    if len(runningInstances) > 0:
        shuttingDown = ec2.instances.filter(InstanceIds=runningInstances).start()
