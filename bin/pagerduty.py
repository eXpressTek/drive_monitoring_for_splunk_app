#!/usr/bin/env python
import json
import requests


SUBDOMAIN='pdt-dank'
API_ACCESS_KEY='i8KrMBvvJbhsyh24nxGx'


def trigger_incident(incident_key, drive, description="Drive Monitor Drive Failure", client="guardant", clientURL="corp.guardant.com"):
    headers = {
        'Authorization': 'Token token={0}'.format(API_ACCESS_KEY),
        'Content-type': 'application/json',
    }
    payload = json.dumps({
      "service_key": "19d91bda718c4cfabdbdcaeac3cd7fd6",
      "incident_key": incident_key,
      "event_type": "trigger",
      "description": description,
      "client": client,
      "client_url": clientURL,
      "details": {
        "drive": drive
      }
    })
    r = requests.post(
                    'https://events.pagerduty.com/generic/2010-04-15/create_event.json',
                    headers=headers,
                    data=payload,
    )
    print r.status_code
    print r.text
#trigger_incident()