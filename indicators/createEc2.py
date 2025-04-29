import boto3

client = boto3.client('ec2', region_name='ap-southeast-2')

response = client.run_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/xvda',
            'Ebs': {

                'DeleteOnTermination': True,
                'VolumeSize':20,
                'VolumeType': 'gp3'
            },
        },
    ],
    ImageId='ami-0e8fd5cc56e4d158c',
    InstanceType='t3.micro',
    MaxCount=1,
    MinCount=1,
    KeyName= "siva_local",
    # NetworkInterfaces=[
    #     {
    #         'AssociatePublicIpAddress': True
    #     }
    # ],
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Team',
                    'Value': 'Data-eng'
                },
                {
                    'Key': 'Name',
                    'Value': 'Siva-Data-eng'
                },
            ]
        },
    ]
    # Monitoring={
    #     'Enabled': False
    # },
    # SecurityGroupIds=[
    #     'sg-1f39854x',
    # ],
)

print(response)