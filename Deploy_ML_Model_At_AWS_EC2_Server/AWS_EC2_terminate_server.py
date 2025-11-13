import boto3
import time
ec2 = boto3.client('ec2')

response = ec2.describe_instances()

''' 
Check if EC2 Instance is Present
'''
## EC2 Instance Name
instance_name = "ec2-mlops-llmServer"

instance_id = ""

for resp in response['Reservations']:
    resp = resp['Instances'][0]
    tags = resp.get('Tags', [])

    for tag in tags:
        if tag.get("Key", "") == "Name" and tag.get("Value", "") == instance_name:
            instance_id = resp['InstanceId']

if instance_id == "":
    print(f"No instance found with name {instance_name}")
    # raise("Stop here!!!")

print(instance_id)

def wait_for_status(instance_id, target_status):
    while True:
        response = ec2.describe_instances(InstanceIds=instance_id)

        status = response['Reservations'][0]['Instances'][0]['State']['Name']

        if status == target_status:
            print("Instance is in {} state".format(target_status))
            break

        time.sleep(10)


def terminate_instances(instance_id):
    print("EC2 Instance Termination")
    ec2.terminate_instances(InstanceIds=instance_id)

    wait_for_status(instance_id, 'terminated')

terminate_instances([instance_id])