import boto3
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()


def get_secure_parameter(param_name):
    """ Gets a KMS encrypted param from AWS Parameter store
    """

    ssm = boto3.client(
        'ssm',
        region_name='us-east-2'
    )

    try:
        params = ssm.get_parameters(
            Names=[
                param_name,
            ],
            WithDecryption=True
        )

        return params['Parameters'][0]['Value']
    except ClientError as err:
        logger.error(
            'Received error when retrieving SSM parameters: {err}',
            exc_info=True
        )
        raise
