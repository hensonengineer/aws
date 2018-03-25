import boto3, json, time, datetime, sys

client = boto3.client('iam')
sns = boto3.client('sns')


usernames = []

mylist = []


def lambda_handler(event, context):

    users = client.list_users()
    for key in users['Users']:
        a = str(key['UserName'])
        usernames.append(a)


    for username in usernames:

        try:
            res = client.list_access_keys(UserName=username)  
            accesskeydate = res['AccessKeyMetadata'][0]['CreateDate'] 
            accesskeydate = accesskeydate.strftime("%Y-%m-%d %H:%M:%S")
            currentdate = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

            accesskeyd = time.mktime(datetime.datetime.strptime(accesskeydate, "%Y-%m-%d %H:%M:%S").timetuple())
            currentd = time.mktime(datetime.datetime.strptime(currentdate, "%Y-%m-%d %H:%M:%S").timetuple())

            active_days = (currentd - accesskeyd)/60/60/24 ### We get the data in seconds. converting it to days

            if 90 < active_days:

                
                a = str(username)
                b = str(' has access keys that are ')
                c = int(int(round(active_days)))
                d = str(' days old!   ')

                mylist.append(a)
                mylist.append(b)
                mylist.append(c)
                mylist.append(d)
                mylist.append(e)

        except:
                e = str(username) + (' does not have an accesskey assigned')
                f = str('')

    print(mylist)
    mylist.insert(0, "**** User Accounts with Access Keys older than 90 days in AWS  Account ****                                 ") # replace with account name
    finallist = ''.join(str(mylist))
    finallist = finallist.replace('"', '').replace("'", '').replace(",", '')

    sns_message = (finallist)
    topic_arn = 'arn:aws:sns:ca-central-1:111111111111:Test' #replace with your ARN


    response = sns.publish(TopicArn=topic_arn, Message = sns_message)