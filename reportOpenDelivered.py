import requests
import json
import urllib
from requests.exceptions import HTTPError



def processEvent(e, openedEmail, deliveredEmail):
    #print(e)
    email = e['recipient']
    #print ("Event read for: " + email)
    if e['type'] in ['CLICK', 'OPEN']:
        openedEmail.append(email)
    if e['type'] in ['DELIVERED']:
        deliveredEmail.append(email)


def main():
    
    apikey = input('What\'s is your API Key? ')

    openedEmail = []
    deliveredEmail = []

    for campaignId in ['97978544' , '98253928', '98302875', '98598107', '98687858', '98838609', '98838609']:
        try:
            print("- Downloading Events from Hubspot API for Campaign " + campaignId + " ...")
            url = 'https://api.hubapi.com/email/public/v1/events?hapikey=' + apikey + '&campaignId=' + campaignId
            #print( ">>> GET: " , url)
            response = requests.get(url)
            response.raise_for_status()
            jsonResponse = response.json()
            for e in jsonResponse['events']:
                processEvent(e, openedEmail, deliveredEmail)
            
            hasMore = jsonResponse['hasMore']

            while hasMore:
                url = 'https://api.hubapi.com/email/public/v1/events?hapikey=' + apikey + '&campaignId=' + campaignId + '&offset=' + jsonResponse['offset']
                #print( ">>> GET: " , url)
                response = requests.get(url)
                response.raise_for_status()
                jsonResponse = response.json()
                for e in jsonResponse['events']:
                    processEvent(e, openedEmail, deliveredEmail)
                #print("<<<< Response: ")
                #print(jsonResponse)
                hasMore = jsonResponse['hasMore']
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
    
    openedEmail = list(dict.fromkeys(openedEmail))
    
    print("Contacts that opened the email or clicked a link in the email")
    for email in openedEmail:
        print(email)

    deliveredNotOpen = []  #  emails that received emails but never opened one
    for email in deliveredEmail:
        if not email in openedEmail:
            deliveredNotOpen.append(email)
    print("Contacts that received -delivered- but didn't open the email")
    deliveredNotOpen = list(dict.fromkeys(deliveredNotOpen))
    for email in deliveredNotOpen:
        print(email)

if __name__ == '__main__':
    main()
