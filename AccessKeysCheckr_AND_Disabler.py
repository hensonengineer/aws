import boto3, json, time, datetime, sys, math


resource = boto3.resource('iam')
client = boto3.client("iam")
sns = boto3.client('sns')


KEY = 'LastUsedDate'

mywarnlist = []
mykilllist = []
finalwarnlist = []
finalkilllist = []

def lambda_handler(event, context):

    for user in resource.users.all():
        Metadata = client.list_access_keys(UserName=user.user_name)
        
        if Metadata['AccessKeyMetadata'] :
            for key in user.access_keys.all():
                AccessId = key.access_key_id
                Status = key.status
                LastUsed = client.get_access_key_last_used(AccessKeyId=AccessId)
                accesskeydate = Metadata['AccessKeyMetadata'][0]['CreateDate']
                accesskeydate = accesskeydate.strftime("%Y-%m-%d %H:%M:%S")
                currentdate = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
                
                accesskeyd = time.mktime(datetime.datetime.strptime(accesskeydate, "%Y-%m-%d %H:%M:%S").timetuple())
                currentd = time.mktime(datetime.datetime.strptime(currentdate, "%Y-%m-%d %H:%M:%S").timetuple())
                active_days = (currentd - accesskeyd)/60/60/24 ### We get the data in seconds. converting it to days
                active_days = math.ceil(active_days) # round up
                active_days = int(active_days) # change into integer for comparison
                warnage = 80
                killage = 90
                if (Status == "Active"):
                    if warnage < active_days:

                        a = user.user_name
                        b = str(' has access keys that are ')
                        c = active_days
                        d = str(' days old!   ')
                        e = str('                                        ')

                        mywarnlist.append(a)
                        mywarnlist.append(b)
                        mywarnlist.append(c)
                        mywarnlist.append(d)
                        mywarnlist.append(e)

                    else:
                        pass
                
                
                if (Status == "Active"):
                    if killage < active_days:
                        client.update_access_key(AccessKeyId=AccessId, Status='Inactive', UserName=user.user_name)

                    
                        e = str('Deactivated ')
                        f = AccessId
                        g = str(' for user ')
                        h = user.user_name
                        i = str(' because key age has exceed 90 days and was not rotated!')

                        mykilllist.append(e)
                        mykilllist.append(f)
                        mykilllist.append(g)
                        mykilllist.append(h)
                        mykilllist.append(i)
                    
                    else:
                        pass
                       
                else:
                    pass
        else:
            pass

    mywarnlist.insert(0, "**** User Accounts with API Access Keys older than 80 days in AWS Zoll Canada Account ****                                 ")
    finalwarnlist = ''.join(str(mywarnlist))
    finalwarnlist = finalwarnlist.replace('"', '').replace("'", '').replace(",", '')


    mykilllist.insert(0, "**** Users whose API Keys are now deactived AWS Zoll Canada Account ****      ")
    finalkilllist = ''.join(str(mykilllist))
    finalkilllist = finalkilllist.replace('"', '').replace("'", '').replace(",", '')



    sns_message = finalwarnlist + finalkilllist
    print(sns_message)
    topic_arn = 'arn:aws:sns:xxxxx:xxxxxx:xxxxxxxx'


    response = sns.publish(TopicArn=topic_arn, Message = sns_message)