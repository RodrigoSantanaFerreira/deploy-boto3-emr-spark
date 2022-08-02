import boto3
import json
import configs

'''
-- Credentials directly in code isn't the practice

client = boto3.client(
    'emr', 
    region_name='us-east-1',
    aws_access_key_id='xxxxxxxxxxxxxx'
    aws_secret_access_key='bD8yLkxqXWoEzmvu5Qxxxxxxxxxxx'
)

'''
client = boto3.client(
    # Get the credentials from environment variables
    'emr',
    region_name = 'us-east-1'
)

response = client.run_job_flow (
    Name="Emr-Cluster-Stack",
    ReleaseLabel='emr-6.3.0',
    LogUri='s3://aws-logs-562248030452-us-east-1/elasticmapreduce/',
    
    # Setup the applications to install in Cluster.
    Applications=[{'Name': 'Hadoop'}, 
                  {'Name': 'Spark'},
                  {'Name':'Hive'}
                  ],
    
    # Set master and Slaves nodes 
    Instances = 
    {
        'InstanceGroups': [
            {
          
                'Name': "Master nodes",
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': 'r5.2xlarge',
                'InstanceCount': 1,
            },
            {
                'Name': "Slave nodes",
                'Market': 'ON_DEMAND',
                'InstanceRole': 'CORE',
                'InstanceType': 'r5.2xlarge',
                'InstanceCount': 2,
            },
            
        ],
        'TerminationProtected': False,
        'Ec2KeyName': configs.var_Ec2KeyName,
     },

    BootstrapActions=[
        # In order to descrompress the files from application in the same place in machines /home/hadoop                                                                                            
        {
            'Name': 'Download and Extract files on cluster',
            'ScriptBootstrapAction': {
                'Path': configs.var_script_extract
            }
        },
    ],  
    Steps=[
        # Setup user steps to run after bootstrap actions
        {
            'Name': 'Run Spark App',
            'ActionOnFailure': 'TERMINATE_CLUSTER',                                       
            'HadoopJarStep': {
                'Args': 
                ['sudo','spark-submit','/home/hadoop/job-1-spark.py'],
                'Jar': 'command-runner.jar'
            }
        }
    ],
  
    # The IAM role that Amazon EMR assumes in order to access Amazon Web Services resources on your behalf.
    
    VisibleToAllUsers=True,
    ServiceRole = configs.var_role_service,                                                 
    JobFlowRole = configs.var_instance_role,
    )

print (json.dumps(response, indent=4, sort_keys=True, default=str))