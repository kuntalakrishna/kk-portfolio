import boto3
from botocore.client import Config
import StringIO
import zipfile
import mimetypes


def lambda_handler(event, context):
    location = {
        'bucketName': 'portfoliobuild.futurecreations.net',
        'objectKey': 'portfoliobuild.zip'
    }
    
    job = event.get('CodePipeline.job')
    
    if job:
        for artifact in job['data']['inputArtifacts']:
            print(str(artifact))
            if(artifact['name'] == 'MyPortfolioBuild'):
                location = artifact['location']['s3Location']
                
    print('Building portfolio from: ' + str(location))
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
    build_bucket = s3.Bucket(location['bucketName'])
    portfolio_bucket = s3.Bucket('portfolio.futurecreations.net')
    
    portfolio_zip = StringIO.StringIO()
    build_bucket.download_fileobj(location['objectKey'], portfolio_zip)
    
    with zipfile.ZipFile(portfolio_zip) as myzip:
        for name in myzip.namelist():
            obj = myzip.open(name)
            portfolio_bucket.upload_fileobj(obj, name, ExtraArgs={'ContentType': mimetypes.guess_type(name)[0]})
            portfolio_bucket.Object(name).Acl().put(ACL='public-read')
    print('Deployment done . . .')
    
    if job:
        codepipeline = boto3.client('codepipeline')
        codepipeline.put_job_success_result(jobId=job['id'])
    return 'Hello from deployment lambda . . .'
