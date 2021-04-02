"""Extensions module - Set up for additional libraries can go in here."""
import os
import boto3
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

s3 = boto3.client(
    's3',
    region_name=os.environ['LINODE_BUCKET_REGION'],
    endpoint_url=os.environ['AWS_S3_ENDPOINT_URL'],
    aws_access_key_id=os.environ['LINODE_BUCKET_ACCESS_KEY'],
    aws_secret_access_key=os.environ['LINODE_BUCKET_SECRET_KEY']
)
db = SQLAlchemy()
