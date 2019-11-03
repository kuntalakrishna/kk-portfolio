import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
    build_bucket = s3.Bucket('portfoliobuild.futurecreations.net')
    portfolio_bucket = s3.Bucket('portfolio.futurecreations.net')
    
    portfolio_zip = StringIO.StringIO()
    build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)
    
    with zipfile.ZipFile(portfolio_zip) as myzip:
        for name in myzip.namelist():
            obj = myzip.open(name)
            portfolio_bucket.upload_fileobj(obj, name, ExtraArgs={'ContentType': mimetypes.guess_type(name)[0]})
            portfolio_bucket.Object(name).Acl().put(ACL='public-read')
    return 'Hello from deployment lambda . . .'
