# Deploy EMR using Python with Boto3 Library
#### set the credentials for aws account

export AWS_ACCESS_KEY_ID='xxxxx'
export AWS_SECRET_ACCESS_KEY='xxxxxxx'

#### Setup the emr/configs with configuration for deploy
vi emr/configs.py

#### Run the deploy app with bootstraping and Step
python3 deploy_emr.py


#### If you needs to access cluster:

chmod 400
ssh -i rodrigo-emr-stack.pem hadoop@ec2-3-231-223-106.compute-1.amazonaws.com
