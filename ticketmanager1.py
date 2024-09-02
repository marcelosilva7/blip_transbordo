import requests
import uuid


class TicketManager:
    def __init__(self):
        self.base_url = 'https://sicoobcressem.http.msging.net/commands'
        self.token = 'YXRlbmRpbWVudG82Mzg1OTE1NDk1MDQ2MDM5NjI6d2ZJa29ZUVdWM2lVcklJQnljblA='

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Key {self.token}'
        }

    def get_waiting_tickets(self):
        payload = {
            "id": str(uuid.uuid4()),
            "to": "postmaster@desk.msging.net",
            "method": "get",
            "uri": "/tickets?$filter=status%20eq%20'waiting'&$skip=0&$take=100"
        }
        response = requests.post(self.base_url, json=payload, headers=self._get_headers())
        if response.status_code == 200:
            return response.json().get('resource', {}).get('items', [])
        else:
            print(f"Failed to get tickets: {response.status_code}")
            return []

    def get_online_agents(self):
        payload = {
            "id": str(uuid.uuid4()),
            "to": "postmaster@desk.msging.net",
            "method": "get",
            "uri": "/teams/agents-online"
        }
        response = requests.post(self.base_url, json=payload, headers=self._get_headers())
        if response.status_code == 200:
            return response.json().get('resource', {}).get('items', [])
        else:
            print(f"Failed to get online agents: {response.status_code}")
            return []

    def close_ticket(self, ticket_id):
        payload = {
            "id": str(uuid.uuid4()),
            "to": "postmaster@desk.msging.net",
            "method": "set",
            "uri": "/tickets/change-status",
            "type": "application/vnd.iris.ticket+json",
            "resource": {
                "id": ticket_id,
                "status": "ClosedClient"
            }
        }
        response = requests.post(self.base_url, json=payload, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to close ticket: {response.status_code}")
            print("Response content:", response.content)
            return None

    def transfer_ticket(self, ticket_id, team_name):
        payload = {
            "id": str(uuid.uuid4()),
            "to": "postmaster@desk.msging.net",
            "method": "set",
            "uri": f"/tickets/{ticket_id}/transfer",
            "type": "application/vnd.iris.ticket+json",
            "resource": {
                "team": team_name
            }
        }
        response = requests.post(self.base_url, json=payload, headers=self._get_headers())
        if response.status_code == 200:
            print(f"Ticket {ticket_id} successfully transferred to {team_name}")
            return response.json()
        else:
            print(f"Failed to transfer ticket: {response.status_code}")
            return None

