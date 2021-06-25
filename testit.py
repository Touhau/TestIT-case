import re
from contextlib import suppress
from dataclasses import dataclass
from json import dumps, dump

import requests

ADDR = ""
KEY = ""
PROJECT_ID = ""  #IDшник откуда

@dataclass
class TestItProject:
    addr: str
    key: str
    id_: str

    def send_request(self, handler, data=None):
        headers = {"Authorization": f"PrivateToken {KEY}"}
        if data is None:
            headers["accept"] = "application/json"
            result = requests.get(f"{self.addr}/api/v2/{handler}", headers=headers)
        else:
            headers["Content-Type"] = "application/json"
            result = requests.post(
                f"{self.addr}/api/v2/{handler}", headers=headers, data=dumps(data)
            )
        try:
            result.raise_for_status()
        except Exception as e:
            
            print(result.text)
            raise Exception from e
        try:
            return result.json()
        except Exception:
            return result.text

    def create_test_case(self, section, case, positive: bool = True):
        return self.send_request(
            "workItems",
            data={
                "entityTypeName": "TestCases",
                "description": "",
                "state": "Ready",
                "priority": "Medium",
                "steps": [],
                "preconditionSteps": [],
                "postconditionSteps": [],
                "duration": 10,
                "attributes": {
                    # "c6f7a002-9429-48cc-b9c9-e06c1c96d3e8": "3c3b4d7b-37c6-471c-b795-6df3a08d0586"
                    # if positive
                    # else "f1548b37-acff-454d-bc5f-8e2a5ba169f3"
                    "c6f7a002-9429-48cc-b9c9-e06c1c96d3e8": "3c3b4d7b-37c6-471c-b795-6df3a08d0586"
                    if positive
                    else "f1548b37-acff-454d-bc5f-8e2a5ba169f3"
                },
                "tags": [],
                "attachments": [],
                "links": [],
                "name": case,
                "projectId": PROJECT_ID,
                "sectionId": section,
            },
        )

    def create_section(self, section, parent):
        parent = parent or "b96e6ce9-6aeb-419c-8e28-99032903222c"       
        return self.send_request(
            "sections",
            data={
                "name": section,
                "projectId": self.id_,
                "parentId": parent,
                "preconditionSteps": [],
                "postconditionSteps": [],
            },
        )


dci_project = TestItProject(ADDR, KEY, PROJECT_ID)


