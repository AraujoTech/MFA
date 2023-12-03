import json
import pyotp
import os

def generate_mfa(event, context):
    try:
        # Retrieve parameters from the request
        service_name = event.get('queryStringParameters', {}).get('service_name')

        if not service_name:
            raise ValueError('Service name is a required parameter')

        # Retrieve the secret from environment variable
        service_secret_env_variable = f'{service_name.upper()}_SECRET'
        service_secret = os.environ.get(service_secret_env_variable)

        if not service_secret:
            raise ValueError(f'Secret for {service_name} not found in environment variables')

        # Generate a TOTP code based on the provided secret
        totp = pyotp.TOTP(service_secret)
        mfa_code = totp.now()

        response = {
            'statusCode': 200,
            'body': json.dumps({
                'service': service_name,
                'mfa_code': mfa_code,
            })
        }        
        return response
    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }