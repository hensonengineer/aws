import boto3
# import json

denyPolicyArn = 'arn:aws:iam::330311450122:policy/lab1-stack-DenyIAMAccessManaged-LNBPWWKD5J00'
adminGroup = 'admin'

iam = boto3.resource('iam')

def handler( event, context ):

	# print("Event data:")
	# print( json.dumps( event, sort_keys=True, indent=4, separators=(',', ': ') ) )

	# Test if the user type is IAM:
	if event["detail"]["userIdentity"]["type"] != 'IAMUser':
		print('User is not an IAMUser. Done.')
		return

	else:
		# Get the userName of the user:
		userName = event["detail"]["userIdentity"]["userName"]
		print("userName is {}".format(userName))
		
		# Loop through the user's group memberships
		user = iam.User(userName)
		group_iterator = user.groups.all()

		# If the user is a member of the 'admin' group all is good.
		for group in group_iterator:
			if group.name == adminGroup:
				print("User {} is a member of the admin group '{}'. Done.".format( userName, adminGroup ))
				return
			
		# The user is not a member of the 'admin' group...
		# Revoke users access to IAM
		print ("User '{}' is not a member of the admin group '{}'".format( userName, adminGroup ))
		revokeIamAccess(userName)

# Attach the 'revoke' managed policy to the user.		
def revokeIamAccess(userName):
	
	policy = iam.Policy(denyPolicyArn)

	try:
		print("Attaching revoke policy '{}' to user '{}'.".format( denyPolicyArn, userName ))
		policy.attach_user( UserName=userName )
	except Exception as e:
		print("{}".format(e) )
		revokeIamAccessInline( userName )

# Or add an inline policy to the user (if max managed policies reached.
def revokeIamAccessInline(userName):		
		
	policyDocument = ('{'
        '"Version": "2012-10-17",'
        '"Statement": ['
        '{'
        '"Effect": "Deny",'
        '"Action": "iam:*",'
        '"Resource": "*"'
        '}'
        ']'
        '}')

	try:
		print("Attching inline policy for user '{}'.".format( userName ))
		client = boto3.client('iam')
		
		response = client.put_user_policy(
    		UserName=userName,
    		PolicyName='denyIamBlockedByEventSecurity',
    		PolicyDocument = policyDocument
		)	
	except:
		print("Error: Unable to add inline policy to user '{}'.".format( userName ))

