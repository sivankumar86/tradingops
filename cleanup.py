import boto3

client = boto3.client('ec2', region_name='ap-southeast-2')

response = client.describe_instances(
    Filters=[
        {
            'Name': 'key-name',
            'Values': [
                'siva_local',
            ]
        },
    ]
)

print(response)
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        res=client.terminate_instances(InstanceIds=[instance["InstanceId"]])
        print(res)

