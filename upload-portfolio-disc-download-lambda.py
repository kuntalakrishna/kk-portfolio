import boto3
from botocore.client import Config
import zipfile

def lambda_handler(event, context):
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))

    build_bucket = s3.Bucket('portfoliobuild.robinnorwood.info')
    portfolio_bucket = s3.Bucket('portfolio.robinnorwood.info')

    # On Windows, this will need to be a different location than /tmp
    build_bucket.download_file('portfolio.zip', '/tmp/portfolio.zip')

    with zipfile.ZipFile('/tmp/portfolio.zip') as myzip:
        for name in myzip.namelist():
            obj = myzip.open(name)
            target_bucket.upload_fileobj(obj, name)
            target_bucket.Object(name).Acl().put(ACL='public-read')
    print('Deployment done . . .')
    return 'Hello from deployment lambda . . .'
