# Custom-Federation-Broker-access-AWS-Console for China region

Python 3.6, Authored by James Huang

## 说明
该示例是在AWS中国区委派一个Role给临时用户，不需要为该用户建IAM User，也不用登录
可以直接通过以下代码生成的URL link直接访问console，权限由委派的Role控制

参考官方文档：
https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_roles_providers_enable-console-custom-url.html#STSConsoleLink_programPython

原文档是针对AWS Global区的，以下示例修改为针对AWS 北京区，endpoint和console/signin的URL不同
(如果是宁夏区，则把37行enpoint_url修改为sts.cn-nortwest-1.amazonaws.com.cn)

原文档是Python2+老的boto，现在修改为Python3.6+boto3

## 注意：
运行本代码的本机需要配置有credential和默认region，可以通过AWS CLI配置：
aws configure
或者配置~/.aws下的config和credentials文件

assume的role不要是Role里面那个默认的Admin，要Admin也自己建一个，因为信任实体不同

## 创建Role示例
aws iam create-role --role-name stsassume --assume-role-policy-document file://trust-policy.json
aws iam put-role-policy --role-name stsassume --policy-name stsassume --policy-document file://role-policy.json
