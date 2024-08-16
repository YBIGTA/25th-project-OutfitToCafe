import boto3
from django.conf import settings
import uuid

def upload_file_to_s3(upload_file, bucket_name, folder_name):
    s3 = boto3.resource(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

    unique_filename = str(uuid.uuid4()) + '.' + upload_file.name.split('.')[-1]
    s3_path = f'{folder_name}/{unique_filename}'

    s3.Bucket(bucket_name).put_object(
        Key=s3_path,
        Body=upload_file,
        ContentType=upload_file.content_type
    )

    return f"https://{bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_path}"
