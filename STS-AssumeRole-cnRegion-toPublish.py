'''
该示例是在AWS中国区临时委派一个Role给临时用户，不需要为该用户建IAM User，也不用登录
可以直接通过以下代码生成的URL link直接访问console
参考官方文档：
https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html#STSConsoleLink_programPython
原文档是针对AWS Global区的，以下示例修改为针对AWS 北京区，endpoint和console/signin的URL不同
(如果是宁夏区，则把37行enpoint_url修改为sts.cn-nortwest-1.amazonaws.com.cn)
原文档是Python2+老的boto，现在修改为Python3.6+boto3

注意：运行example的本机需要配置有credential和默认region，可以通过AWS CLI配置：
aws configure
或者配置~/.aws下的config和credentials文件

注意：assume的role不要是Role里面那个默认的Admin，要Admin也自己建一个，因为信任实体不同
'''
import boto3
import urllib
import json
import requests  # 'pip install requests'
# # AWS SDK for Python (Boto) 'pip install boto'
# from boto3.sts import STSConnection

# # Step 1: Authenticate user in your own identity system.

# # Step 2: Using the access keys for an IAM user in your AWS account,
# # call "AssumeRole" to get temporary access keys for the federated user

# # Note: Calls to AWS STS AssumeRole must be signed using the access key ID
# # and secret access key of an IAM user or using existing temporary credentials.
# # The credentials can be in EC2 instance metadata, in environment variables,
# # or in a configuration file, and will be discovered automatically by the
# # STSConnection() function. For more information, see the Python SDK docs:
# # http://boto.readthedocs.org/en/latest/boto_config_tut.html
# sts_connection = STSConnection()
sts = boto3.client(
    'sts', 
    endpoint_url="https://sts.cn-north-1.amazonaws.com.cn",
    )
# assumed_role_object = sts.get_federation_token(
#     Name='abctoken001'
# )
assumed_role_object = sts.assume_role(
    RoleArn="arn:aws-cn:iam::313497334385:role/s3fullaccess_self_account",
    RoleSessionName="AssumeRoleSession1"
)
print(assumed_role_object)

# Step 3: Format resulting temporary credentials into JSON
json_string_with_temp_credentials = '{'
json_string_with_temp_credentials += '"sessionId":"' + \
    assumed_role_object['Credentials']['AccessKeyId'] + '",'
json_string_with_temp_credentials += '"sessionKey":"' + \
    assumed_role_object['Credentials']['SecretAccessKey'] + '",'
json_string_with_temp_credentials += '"sessionToken":"' + \
    assumed_role_object['Credentials']['SessionToken'] + '"'
json_string_with_temp_credentials += '}'

# Step 4. Make request to AWS federation endpoint to get sign-in token. Construct the parameter string with
# the sign-in action request, a 12-hour session duration, and the JSON document with temporary credentials
# as parameters.
request_parameters = "?Action=getSigninToken"
request_parameters += "&SessionDuration=43200"
request_parameters += "&Session=" + \
    urllib.parse.quote_plus(json_string_with_temp_credentials)
request_url = "https://signin.amazonaws.cn/federation" + request_parameters
r = requests.get(request_url)
# Returns a JSON document with a single element named SigninToken.
signin_token = json.loads(r.text)

# Step 5: Create URL where users can use the sign-in token to sign in to
# the console. This URL must be used within 15 minutes after the
# sign-in token was issued.
request_parameters = "?Action=login"
request_parameters += "&Issuer=Example.org"
request_parameters += "&Destination=" + \
    urllib.parse.quote_plus("https://console.amazonaws.cn/")
request_parameters += "&SigninToken=" + signin_token["SigninToken"]
request_url = "https://signin.amazonaws.cn/federation" + request_parameters

# Send final URL to stdout
print (request_url)
