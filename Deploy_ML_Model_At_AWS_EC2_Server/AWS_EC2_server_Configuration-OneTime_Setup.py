import boto3

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

'''
Create an Amazon EC2 instance
## Make sure to Specify correct ImageId- AMI from the AWS Console

->> GO to AWS console AMI Catalog, Search Deep Learning -> and Seklect an image with Pytorch and  GPU support
copy the AMI ID - ami-05b1f2b5642f2ad75   and specify as ImageId
Verified provider
Deep Learning OSS Nvidia Driver AMI GPU PyTorch 2.8 (Ubuntu 24.04)
ami-05b1f2b5642f2ad75 (64-bit (x86)) / ami-0d5adcc9364262579 (64-bit (Arm))
Release notes: https://docs.aws.amazon.com/dlami/latest/devguide/appendix-ami-release-notes.html
'''
'''
Specify the correct Key Pair Created for the llm server EC2 instance  llmDeployKey1
'''
## check if the Instance available or not otherwise create the instance
if instance_id == "":
    response = ec2.run_instances(
        ImageId = 'ami-05b1f2b5642f2ad75',
        MinCount=1,
        MaxCount=1,
        InstanceType='t2.large',
        KeyName='llmDeployKey1',
        BlockDeviceMappings=[
            {
                "DeviceName": "/dev/xvda",
                'Ebs':{
                    'DeleteOnTermination': True,
                    'VolumeSize': 120
                }
            }
        ]

    )

    instance_id = response['Instances'][0]['InstanceId']

    ec2.create_tags(Resources=[instance_id], Tags=[
        {
            'Key':'Name',
            'Value':instance_name
        }
    ])
    print("EC2 Instance Created...")
else:
    print("Instance is already present")


'''
## Create Security Group and add rules to it

- Security groups control inbound and outbound traffic of the EC2 instance network interface.
- every EC2 instance must have at least one Security Group associated with it. If no Security Group has been specified during the EC2 instance launch, 
  the default Security Group of the default VPC is associated with the instance.
'''


group_name = 'secgroup-llmServer'

response = ec2.describe_security_groups()

security_group_id = [x['GroupId'] for x in response['SecurityGroups'] if x['GroupName']==group_name]

if security_group_id == []:
    response = ec2.create_security_group(
        GroupName = group_name,
        Description = "Security group for testing"
    )
    security_group_id = response['GroupId']
else:
    security_group_id = security_group_id[0]

print(security_group_id)


from botocore.exceptions import ClientError

def update_security_group(group_id, protocol, port, cidr):
    try:
        response = ec2.authorize_security_group_ingress(
            GroupId = group_id,
            IpPermissions=[
                {
                    'IpProtocol': protocol,
                    'FromPort': port,
                    'ToPort': port,
                    'IpRanges': [{'CidrIp': cidr}]
                }
            ]
        )
    except ClientError as e:
        if e.response['Error']['Code']=='InvalidPermission.Duplicate':
            print('This rule is already there')
        else:
            print("an error as occured!")
            print(e)

update_security_group(security_group_id, 'tcp', 22, '0.0.0.0/0')
update_security_group(security_group_id, 'tcp', 80, '0.0.0.0/0')
update_security_group(security_group_id, 'tcp', 8501, '0.0.0.0/0')
update_security_group(security_group_id, 'tcp', 8502, '0.0.0.0/0')


'''
Connect the Security Group  (secgroup-llmServer) with  EC2 Instance (ec2-mlops-llmServer)
'''

ec2.modify_instance_attribute(InstanceId=instance_id, Groups=[security_group_id])
print("Security Group Attached to EC2 Instance...")