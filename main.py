import requests
import json
import urllib
from requests.exceptions import HTTPError

def getPhone(email, apikey):
    try:
        #print("- Downloading Contact from Hubspot API...")
        url= 'https://api.hubapi.com/contacts/v1/contact/email/' + email + '/profile?hapikey=' + apikey
        response = requests.get(url)
        response.raise_for_status()
        jsonResponse = response.json()
        phone = jsonResponse['properties']['phone']['value']
    except HTTPError as http_err:
        #print(f'HTTP error occurred: {http_err}')
        return "httpERROR"
    except Exception as err:
        #print(f'Other error occurred: {err}')
        return "ERROR"
    return phone

def processEvent(e, contactDict):
    #print(e)
    email = e['recipient']
    #print ("Event read for: " + email)
   
    if email in contactDict.keys():
        #print("- already in contactDict.keys")
        #  IF CURRENT EVENT TYPE IS  FINAL  OR  EQUAL TO CURRENT STATE, DO NOTHING.  ELSE, SAVE IT IF IT'S A MORE RECENT TYPE IN THE WORKFLOW
        if contactDict[email] == 'DROPPED' or contactDict[email] == 'BOUNCE' or contactDict[email] == 'SPAMREPORT' or contactDict[email] == e['type']:
            #print("--- already " + e['type'] + ". Nothing to do.")
            pass
        else:
            if e['type'] == 'CLICK':
                contactDict[email] = e['type']
            elif e['type'] == 'OPEN' and contactDict[email] not in ['CLICK']:
                contactDict[email] = e['type']
            elif e['type'] == 'DELIVERED' and contactDict[email] not in ['CLICK', 'OPEN']:
                contactDict[email] = e['type']
            elif e['type'] == 'PROCESSED' and contactDict[email] not in ['CLICK', 'OPEN', 'DELIVERED']:
                contactDict[email] = e['type']
            elif e['type'] == 'SENT' and contactDict[email] not in ['CLICK', 'OPEN', 'DELIVERED', 'PROCESSED']:
                contactDict[email] = e['type']
            elif e['type'] == 'STATUSCHANGE' or e['type'] == 'DEFERRED':
                contactDict[email] = e['type']   
    else:
        #  FIRST TYPE STATE IS THE FIRST RECEIVED
        #print("- NOT in contactDict.keys, adding contact and setting to " + e['type'])
        contactDict[email] = e['type']


def main():
    
    apikey = input('What\'s is your API Key? ')
    campaignId = input('What\'s the campaignId? ')
    contactDict =	{}

    try:
        print("- Downloading Events from Hubspot API for Campaign " + campaignId + " ...")
        url = 'https://api.hubapi.com/email/public/v1/events?hapikey=' + apikey + '&campaignId=' + campaignId
        #print( ">>> GET: " , url)
        response = requests.get(url)
        response.raise_for_status()
        jsonResponse = response.json()
        for e in jsonResponse['events']:
            processEvent(e, contactDict)
        
        hasMore = jsonResponse['hasMore']

        while hasMore:
            url = 'https://api.hubapi.com/email/public/v1/events?hapikey=' + apikey + '&campaignId=' + campaignId + '&offset=' + jsonResponse['offset']
            #print( ">>> GET: " , url)
            response = requests.get(url)
            response.raise_for_status()
            jsonResponse = response.json()
            for e in jsonResponse['events']:
                processEvent(e, contactDict)
            #print("<<<< Response: ")
            #print(jsonResponse)
            hasMore = jsonResponse['hasMore']

        print("")
        print("- All events read from API. Saving CSV with each Contact email,status for this campaign")
        print("")
        file_object = open('contactsCampaign.csv', 'w')
        for email in contactDict:
            phone = getPhone(email, apikey)
            print (email + "," + phone + "," + contactDict[email])
            file_object.write(email + "," + phone + "," + contactDict[email] + "\n")
        file_object.close()

    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    

if __name__ == '__main__':
    main()
