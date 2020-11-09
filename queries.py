import csv

"""

for campaign in campaigns:
	for event in campaign:
		if not event['email'] in deliveredEmail:
			deliveredEmail.append(email)
		if event['type'] in ['open', 'click']:
			openedEmail.append(email)


1.- if email in adherentes and email in older and not email in deliveredNotOpen:
		print

2.- if email in militantes and not email in openedEmail and email in deliveredNotOpen:
		print

5.- if email in adherentes and email in deliveredNotOpen and email not in openedEmail:
		print

6.- if email in adherentes and email in newer and not email in deliveredNotOpen:
		print

"""


adherentes = []
militantes = []
openedOrClicked = []
deliveredNotOpen = []
older = []
newer = []
contacted = []

with open('adherentes.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        adherentes.append(row[0])

print(len(adherentes))

with open('militantes.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        militantes.append(row[0])

print(len(militantes))

with open('deliveredNotOpen.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        deliveredNotOpen.append(row[0])

print(len(deliveredNotOpen))

with open('openedOrClicked.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        openedOrClicked.append(row[0])

print(len(openedOrClicked))

with open('older.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        older.append(row[0])
print(len(older))
with open('newer.csv', newline='') as inputfile:
    for row in csv.reader(inputfile):
        newer.append(row[0])
print(len(newer))

#  wether the contact openned the email or just received it, add to contacted
for email in openedOrClicked:
    contacted.append(email)
for email in deliveredNotOpen:
    contacted.append(email)
contacted = list(dict.fromkeys(contacted))  #  remove repeated

print("contacted: " , len(contacted) , " emails")

query1 = []
for adherente in adherentes:
    if adherente not in contacted:
        query1.append(adherente)

file_object = open('query1.csv', 'w')
for c in query1:
	file_object.write(c + "\n")
file_object.close()

query2 = []
for militante in militantes:
    if not militante in openedOrClicked:
        if militante in deliveredNotOpen:
            query2.append(militante)

file_object = open('query2.csv', 'w')
for c in query2:
	file_object.write(c + "\n")
file_object.close()

query5 = []
for adherente in adherentes:
    if not adherente in openedOrClicked:
        if adherente in deliveredNotOpen:
            if adherente in newer:
                query5.append(adherente)

file_object = open('query5.csv', 'w')
for c in query5:
	file_object.write(c + "\n")
file_object.close()


query6 = []
for adherente in adherentes:
    if not adherente in deliveredNotOpen:
        if adherente in newer:
            query6.append(adherente)

file_object = open('query6.csv', 'w')
for c in query6:
	file_object.write(c + "\n")
file_object.close()