import requests
import json
import urllib
from datetime import datetime

hapikey = input('What\'s is your API Key? ')
max_results = 5000 
count = 100
contact_list = []
property_list = []
get_all_contacts_url = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all?"
parameter_dict = {'hapikey': hapikey, 'count': count}
headers = {}

# Paginate your request using offset
has_more = True
while has_more:
	print("Downloading contacts...")
	parameters = urllib.parse.urlencode(parameter_dict)
	get_url = get_all_contacts_url + parameters + "&property=fecha_inscripcion_servel&property=createdate"
	r = requests.get(url= get_url, headers = headers)
	response_dict = json.loads(r.text)
	has_more = response_dict['has-more']
	contact_list.extend(response_dict['contacts'])
	parameter_dict['vidOffset']= response_dict['vid-offset']
	if len(contact_list) >= max_results: # Exit pagination, based on whatever value you've set your max results variable to. 
		print('maximum number of results exceeded')
		break


print("Succesfully downloaded {} contact records and saved them to a list".format(len(contact_list)))

targetDate = 1601521200000 # 1601521200000 = 01/10/2020 00:00:00
dt_object = datetime.fromtimestamp(targetDate/1000)
older = []
newer = []
militantes = []
adherentes = []
for c in contact_list:
	#print(c)
	for identProf in c['identity-profiles']:
		identities = identProf['identities']
		for i in identities:
			if i['type'] == 'EMAIL':
				email= i['value']
	# Add to older or newer
	#print(c['properties']['createdate'])
	if 'createdate' in c['properties']:
		if int(c['properties']['createdate']['value']) < targetDate:
			#print(" -- " , c['addedAt'] , " older than " , targetDate)
			older.append(email)
		else:
			#print(" ** " ,c['addedAt'] , " newer than " , targetDate)
			newer.append(email)
	
	#  Add to Militantes or Adherentes
	if 'fecha_inscripcion_servel' in c['properties']:
		militantes.append(email)
	else:
		adherentes.append(email)


"""
TODO:

for campaign in campaigns:
	for event in campaign:
		if not event['email'] in deliveredEmail:
			deliveredEmail.append(email)
		if event['type'] in ['open', 'click']:
			openedEmail.append(email)


1.- if email in adherentes and email in older and not email in contacted:
		print

2.- if email in militantes and not email in openedEmail and email in contacted:
		print

5.- if email in adherentes and email in contacted and email not in openedEmail:
		print

6.- if email in adherentes and email in newer and not email in contacted:
		print

for campaign in campaigns:
	for event in campaign:
		if not event['email'] in deliveredEmail:
			deliveredEmail.append(email)



"""



#  Save csv files 
file_object = open('older.csv', 'w')
older = list(dict.fromkeys(older))
print("- - Contacts older than " , dt_object , " : " , len(older))
for c in older:
	print(c)
	file_object.write(c + "\n")
file_object.close()

file_object = open('newer.csv', 'w')
newer = list(dict.fromkeys(newer))
print("- - Contacts newer than " , dt_object , " : " , len(newer))
for c in newer:
	print(c)
	file_object.write(c + "\n")
file_object.close()

file_object = open('militantes.csv', 'w')
militantes = list(dict.fromkeys(militantes))
print("- - Militantes: ",len(militantes))
for c in militantes:
	print(c)
	file_object.write(c + "\n")
file_object.close()

file_object = open('adherentes.csv', 'w')
adherentes = list(dict.fromkeys(adherentes))
print("- - Adherentes: ",len(adherentes))
for c in adherentes:
	print(c)
	file_object.write(c + "\n")
file_object.close()