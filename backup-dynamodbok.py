import boto3
import sys
from datetime import datetime, timedelta
import calendar
import json
import gc
from pprint import pprint
dynamo = boto3.client('dynamodb')
ses = boto3.client('ses')
sns = boto3.client('sns')
#email_from = 'suporte@ipsense.com.br'
#email_to = 'rodolfo.ribeiro@targetsistemas.com.br'
#email_cc = 'suporte@ipsense.com.br'
#emaiL_subject = 'O Backup do Dynamodb foi executado com sucesso (conta do cliente) '
#email_body = 'O Backup do Dynamodb foi executado com sucesso, em caso de dúvida portaldesuporte@ipsense.com.br o backup da table: '

current_time = datetime.now()

def make_backup(name):
    try:
        response = dynamo.create_backup(
            TableName=name,
            BackupName=name+'_bkp_'+ '%s-%s-%s_%s.%s.%s' % (current_time.year, current_time.month, current_time.day,current_time.hour, current_time.minute, current_time.second)
            
        )
        print(response)
        send_email(name)
        return 0
    except:
        send_sns()
        sys.exit("Erro ao realizar backup!")

#Delete bkp        
def delete_backup(name):
    try:
        print("Deleting")
        print(current_time)
        print(current_time - timedelta(days=30))
    
        check = dynamo.list_backups(
            TableName=name,
            Limit=100,
            #TimeRangeUpperBound lista determinadas tabelas / os atuais -1
            #TimeRangeUpperBound = current_time - timedelta(days=1)
            TimeRangeUpperBound = current_time - timedelta(minutes=5)
            
        )

        print(check)
        for backup in check['BackupSummaries']:
            arn = backup['BackupArn']
            print("ARN to delete: "+arn)
            deletedArn = dynamo.delete_backup(
                BackupArn=arn
            )
            print(deletedArn['BackupDescription']['BackupDetails']['BackupStatus'])
    except:
        sys.exit("Erro ao realizar a limpeza de backups !!")

#Function - Backup realizado mas algo deu errado no processo        
def send_sns():
    sns_message = sns.publish(
        TopicArn='arn:aws:sns:us-east-2:065274192387:dynamodb',
        Message='Dynamodb backup Realizado, porém houve uma falha em algum recurso!'
    )
    
#Function - Backup Sucesso
def send_email(name):
     sns_message = sns.publish(
        TopicArn='arn:aws:sns:us-east-2:065274192387:dynamodb',
        Message='Dynamodb backup Realizado! table:'+name
    )
    
# response is a function for dynamodb this develop the backup of table.
def lambda_handler(event, context):
    print(event['TableName'])
    if make_backup(event['TableName']) == 0:
        delete_backup(event['TableName'])