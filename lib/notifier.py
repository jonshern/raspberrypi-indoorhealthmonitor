

import boto3
import json


class Notifier(object):
    snsarn = ''
    sns = ''
    topic = ''

    def __init__(self, arn):
        self.arn = arn
        sns = boto3.resource('sns')
        topic = sns.Topic(arn)

    def sendnotification(self, message, subject):
        response = topic.publish(
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )