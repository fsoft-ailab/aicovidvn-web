import boto3
import logging
from botocore.exceptions import ClientError
from instance import environment

from utils import log_service

S3_BUCKET = environment.S3_BUCKET
S3_REGION = environment.S3_REGION

s3 = boto3.client('s3',
                  aws_secret_access_key=environment.AWS_SECRET_ACCESS_KEY,
                  aws_access_key_id=environment.AWS_ACCESS_KEY_ID)


def get_presigned_url_from_original_url(url, expiration=environment.AWS_GET_EXPIRED):
    """Get key object name from URL

      :param url: string
      :param expiration: int
      :return:  Presigned URL as string. If error, returns None.
    """
    try:
        object_name = get_key_from_url(url)
        if object_name is not None or object_name != '':
            presigned_url = create_get_presigned_url(object_name, expiration)
            return presigned_url
        else:
            return None
    except:
        return None


def get_key_from_url(url):
    """Get key object name from URL

    :param url: string
    :return: Object name as string. If error, returns None.
    """

    try:
        split_arr = str(url).split('/')
        object_name = ""
        for item in split_arr[3:]:
            object_name += item + "/"
        return object_name[:-1]
    except Exception as e:
        logging.error(e)
        return None


def create_get_presigned_url(object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object

    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """

    try:
        response = s3.generate_presigned_url('get_object',
                                             Params={'Bucket': S3_BUCKET,
                                                     'Key': object_name},
                                             ExpiresIn=expiration,
                                             HttpMethod='GET')
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def upload_object(fileobj, key, extra_args=None):
    if extra_args is None:
        extra_args = {'ACL': 'private', "ContentType": 'audio/wav'}

    try:
        s3.put_object(Body=fileobj, Bucket=S3_BUCKET, Key=str(key), ExtraArgs=extra_args)
        log_service.warning('upload file to s3 ok')
    except Exception as ex:
        print(ex)
        log_service.warning('upload file to s3 fail')


def upload_file(fileobj, key, extra_args=None):
    if extra_args is None:
        extra_args = {'ACL': 'private', "ContentType": 'audio/wav'}

    try:
        s3.upload_file(fileobj, S3_BUCKET, str(key), ExtraArgs=extra_args)
        log_service.warning('upload file to s3 ok')
    except Exception as ex:
        print(ex)
        log_service.warning('upload file to s3 fail')


def download_file(key, des):
    try:
        s3.download_file(S3_BUCKET, key, des)
        return True
    except:
        return False


def generate_url(file_dir):
    url = 'https://{}.s3-{}.amazonaws.com/{}'.format(S3_BUCKET, S3_REGION, file_dir)
    return url
