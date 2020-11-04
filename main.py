import requests
import json
import urllib
from requests.exceptions import HTTPError

def getContact(email, apikey):
    contact = {}
    try:
        #print("- Downloading Contact from Hubspot API...")
        url= 'https://api.hubapi.com/contacts/v1/contact/email/' + email + '/profile?hapikey=' + apikey
        response = requests.get(url)
        response.raise_for_status()
        jsonResponse = response.json()
        #print(jsonResponse['properties'])
        if 'phone' in jsonResponse['properties']:
            contact['phone'] = jsonResponse['properties']['phone']['value']
        else:
            contact['phone'] = ""
        if 'firstname' in jsonResponse['properties']:
            contact['name'] = jsonResponse['properties']['firstname']['value']
        else:
            contact['name'] = ""
        if 'lastname' in jsonResponse['properties']:
            contact['lastname'] = jsonResponse['properties']['lastname']['value']
        else:
            contact['lastname'] = ""

    except HTTPError as http_err:
        if response.status_code == 404:
            print("------ ERROR: contact " + email + " might not exist. Maybe it was deleted ------")
        else:
            print(f"--- HTTP error occurred: {response}")
        contact['phone'] = 'error'
        contact['name'] = 'error'
        contact['lastname'] = 'error'
        return contact
    except Exception as err:
        print(f'------- Other error occurred: {err}')
        contact['phone'] = 'error'
        contact['name'] = 'error'
        contact['lastname'] = 'error'

    return contact

def processEvent(e, statusDict):
    #print(e)
    email = e['recipient']
    #print ("Event read for: " + email)
   
    if email in statusDict.keys():
        #print("- already in statusDict.keys")
        #  IF CURRENT EVENT TYPE IS  FINAL  OR  EQUAL TO CURRENT STATE, DO NOTHING.  ELSE, SAVE IT IF IT'S A MORE RECENT TYPE IN THE WORKFLOW
        if statusDict[email] == 'DROPPED' or statusDict[email] == 'BOUNCE' or statusDict[email] == 'SPAMREPORT' or statusDict[email] == e['type']:
            #print("--- already " + e['type'] + ". Nothing to do.")
            pass
        else:
            if e['type'] == 'CLICK':
                statusDict[email] = e['type']
            elif e['type'] == 'OPEN' and statusDict[email] not in ['CLICK']:
                statusDict[email] = e['type']
            elif e['type'] == 'DELIVERED' and statusDict[email] not in ['CLICK', 'OPEN']:
                statusDict[email] = e['type']
            elif e['type'] == 'PROCESSED' and statusDict[email] not in ['CLICK', 'OPEN', 'DELIVERED']:
                statusDict[email] = e['type']
            elif e['type'] == 'SENT' and statusDict[email] not in ['CLICK', 'OPEN', 'DELIVERED', 'PROCESSED']:
                statusDict[email] = e['type']
            elif e['type'] == 'STATUSCHANGE' or e['type'] == 'DEFERRED':
                statusDict[email] = e['type']   
    else:
        #  FIRST TYPE STATE IS THE FIRST RECEIVED
        #print("- NOT in statusDict.keys, adding contact and setting to " + e['type'])
        statusDict[email] = e['type']


def main():
    
    apikey = input('What\'s is your API Key? ')
    campaignId = input('What\'s the campaignId? ')
    statusDict =	{}

    try:
        print("- Downloading Events from Hubspot API for Campaign " + campaignId + " ...")
        url = 'https://api.hubapi.com/email/public/v1/events?hapikey=' + apikey + '&campaignId=' + campaignId
        #print( ">>> GET: " , url)
        response = requests.get(url)
        response.raise_for_status()
        jsonResponse = response.json()
        for e in jsonResponse['events']:
            processEvent(e, statusDict)
        
        hasMore = jsonResponse['hasMore']

        while hasMore:
            url = 'https://api.hubapi.com/email/public/v1/events?hapikey=' + apikey + '&campaignId=' + campaignId + '&offset=' + jsonResponse['offset']
            #print( ">>> GET: " , url)
            response = requests.get(url)
            response.raise_for_status()
            jsonResponse = response.json()
            for e in jsonResponse['events']:
                processEvent(e, statusDict)
            #print("<<<< Response: ")
            #print(jsonResponse)
            hasMore = jsonResponse['hasMore']

        print("")
        print("- All events read from API. Saving CSV with each Contact email,status for this campaign")
        print("")
        file_object = open('contactsCampaign.csv', 'w')
        for email in statusDict:
            contact = getContact(email, apikey)
            print (email + "," + contact['phone'] + "," + contact['name'] + "," + contact['lastname'] + "," + statusDict[email])
            file_object.write(email + "," + contact['phone'] + "," + contact['name'] + "," + contact['lastname'] + "," + statusDict[email] + "\n")
        file_object.close()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    

if __name__ == '__main__':
    main()
