'''
## Start, Stop and Delete Amazon EC2 instances
'''

import boto3

ec2 = boto3.client('ec2')
'''
Check if the EC2 Instance Available or not
'''
response = ec2.describe_instances()

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
    raise ("Stop here!!!")

print("Instance ID", instance_id);

'''
Check  of Running Status
# status -> running, stopped, terminated, pending etc.
'''



import time


def wait_for_status(instance_id, target_status):
    while True:
        response = ec2.describe_instances(InstanceIds=instance_id)

        status = response['Reservations'][0]['Instances'][0]['State']['Name']

        if status == target_status:
            print("Instance is in {} state".format(target_status))
            break

        time.sleep(10)


'''
Stop the  EC2 Instance
'''

def stop_instances(instance_id):
    print("EC2 Instance Stop")
    ec2.stop_instances(InstanceIds=instance_id)

    wait_for_status(instance_id, 'stopped')

stop_instances([instance_id])

'''
Start the  EC2 Instance
'''
def start_instances(instance_id):
    print("EC2 Instance Start")
    ec2.start_instances(InstanceIds=instance_id)

    wait_for_status(instance_id, 'running')

start_instances([instance_id])

response = ec2.describe_instances(InstanceIds=[instance_id])
public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

print("EC2 Server PublicIP:",public_ip)
