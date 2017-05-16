import boto3
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt


class AWSIOT(object):
    host = ""
    rootCAPath = ""
    cognitoIdentityPoolID = ""

    accesskeyid = ""
    secretkeyid = ""
    sessiontoken = ""
    awsiotmqttclient = ""

    
    def __init__(self, host, rootCAPath, cognitoIdentityPoolID):
        
        self.host = host
        self.rootCAPath = rootCAPath
        self.cognitoIdentityPoolID = cognitoIdentityPoolID

        # Cognito auth
        identityPoolID = cognitoIdentityPoolID
        region = host.split('.')[2]
        cognitoIdentityClient = boto3.client('cognito-identity', region_name=region)
        # identityPoolInfo = cognitoIdentityClient.describe_identity_pool(IdentityPoolId=identityPoolID)
        # print identityPoolInfo

        temporaryIdentityId = cognitoIdentityClient.get_id(IdentityPoolId=identityPoolID)
        identityID = temporaryIdentityId["IdentityId"]

        temporaryCredentials = cognitoIdentityClient.get_credentials_for_identity(IdentityId=identityID)
        self.accesskeyid = temporaryCredentials["Credentials"]["AccessKeyId"]
        self.secretkeyid = temporaryCredentials["Credentials"]["SecretKey"]
        self.sessiontoken = temporaryCredentials["Credentials"]["SessionToken"]

        # Init AWSIoTMQTTClient
        myAWSIoTMQTTClient = AWSIoTMQTTClient("healthmonitoriot", useWebsocket=True)

        # AWSIoTMQTTClient configuration
        myAWSIoTMQTTClient.configureEndpoint(host, 443)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath)
        myAWSIoTMQTTClient.configureIAMCredentials(AccessKeyId, SecretKey, SessionToken)
        myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
        myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
        myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
        myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec


    def sendmessage(self, topic, message):

        # Connect and subscribe to AWS IoT
        myAWSIoTMQTTClient.connect()
        myAWSIoTMQTTClient.publish(topic, message, 1)
