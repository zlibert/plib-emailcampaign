TODO:
- Create an easier way to execute

REQUIRES:
- Python 3
- Requests library, to install: pip install requests

OUTPUTS:
main.py
- Provide a csv output (contactsCampaign.csv) with contacts classified by status in order to make calls if necessary.
- Provides shell output (same as csv file but with more process and error details)
getMilitAdherent.py
- Provides a csv output (older.csv, newer.csv, adherentes.csv, militantes.csv) based createdate and fecha_inscripcion_servel

Script reads the HubSpot campaign events from the API and associated contact info, and stores the relevant status (type) where status priority is as follows:

	CLICK > OPEN > DELIVERED > PROCESSED > SENT | DROPPED | BOUNCE | SPAMREPORT | STATUSCHANGE or DEFERRED
Status can be in 5 blocks described above. The first block has priority, if status is CLICK implies it was sent, processed, delivered and also open, ergo if it's on click the rest of the statuses of that block is ignored. If it's dropped, bounce, spamreport it's not going to update it's status anymore because the workflow is stopped there. Statuschange or deferred is currently irrelevant.

LIMITATIONS:
- This info is by campaign, therefore it might repeat contacts that are already contacted before. A persistent database is needed to avoid this and store further info like labels, notes, differnet status.
