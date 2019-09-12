import boto3
import json
from botocore.exceptions import ClientError

def lambda_handler(event, context):

    print ("Importing boto3 class for ec2 service")

    # Boto Version Check
    print(boto3.__version__)

    #define the connection
    client = boto3.resource('ec2')

    # Get state
    instanceState = event["instanceState"]
    filters = event["tags"]

    print(filters)

    print(instanceState)
    
    #filter the instances
    instance_iterator = client.instances.filter(Filters=filters)

    #Get IDs of all running and tagged instances
    instance_ids = [instance.id for instance in instance_iterator]

    #Print list of instances that will be stopped to logs
    print("instances ids : " + ', '.join(instance_ids))

    # Starting instances
    if (len(instance_ids) > 0 and instanceState == "on"):
        # Starting the instances
        print ('Trying to Start the EC2 instances : ' + ', '.join(instance_ids))
        try:
            starting_instances = client.instances.filter(InstanceIds=instance_ids).start()
            return starting_instances
        except ClientError as e:
            print(e)

    # Stopping instances
    if (len(instance_ids) > 0 and instanceState == "off"):
        # Stopping the instances
        print ('Trying to Stop EC2 instances : ' + ', '.join(instance_ids))
        try:
            stopping_instances = client.instances.filter(InstanceIds=instance_ids).stop()
            return stopping_instances
        except ClientError as e:
            print(e)

    # End
    return "Script execution completed. See Cloudwatch logs for complete output"
