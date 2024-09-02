import requests
from datetime import datetime, timedelta
import uuid

BASE_URL = 'https://sicoobcressem.http.msging.net/commands'
TOKEN = 'YXRlbmRpbWVudG82Mzg1OTE1NDk1MDQ2MDM5NjI6d2ZJa29ZUVdWM2lVcklJQnljblA='

def get_waiting_tickets():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Key {TOKEN}'
    }
    payload = {
        "id": "{{$guid}}",
        "to": "postmaster@desk.msging.net",
        "method": "get",
        "uri": "/tickets?$filter=status%20eq%20'waiting'&$skip=0&$take=100"
    }
    response = requests.post(BASE_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get('resource', {}).get('items', [])
    else:
        print(f"Failed to get tickets: {response.status_code}")
        return []


def get_online_agents():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Key {TOKEN}'
    }

    payload = {
      "id": "{{$guid}}",
      "to": "postmaster@desk.msging.net",
      "method": "get",
      "uri": "/teams/agents-online"
    }

    response = requests.post(BASE_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get('resource', {}).get('items', [])
    else:
        print(f"Failed to get online agents: {response.status_code}")
        return []


def close_ticket(ticket_id):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Key {TOKEN}'
    }

    payload = {
        "id": "{{$guid}}",
        "to": "postmaster@desk.msging.net",
        "method": "set",
        "uri": "/tickets/change-status",
        "type": "application/vnd.iris.ticket+json",
        "resource": {
            "id": ticket_id,
            "status": "ClosedClient"
        }
    }

    response = requests.post(BASE_URL, json=payload, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        print("Response JSON:", response_json)
        return response_json
    else:
        print(f"Failed to close ticket: {response.status_code}")
        print("Response content:", response.content)
        return None


def transfer_ticket(ticket_id, team_name):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Key {TOKEN}'
    }

    guid = str(uuid.uuid4())

    payload = {
        "id": guid,
        "to": "postmaster@desk.msging.net",
        "method": "set",
        "uri": f"/tickets/{ticket_id}/transfer",
        "type": "application/vnd.iris.ticket+json",
        "resource": {
            "team": team_name
        }
    }

    response = requests.post(BASE_URL, json=payload, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        print("Response JSON:", response_json)
        return response_json
    else:
        print(f"Failed to transfer ticket: {response.status_code}")
        print("Response content:", response.content)
        return None


def get_metricas_atendentes():
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Key {TOKEN}'
    }

    payload = {
  "id": "{{$guid}}",
  "to": "postmaster@desk.msging.net",
  "method": "get",
  "uri": "/analytics/reports/attendants/productivity?beginDate=2019-04-15&endDate=2024-07-29"
}
    response = requests.post(BASE_URL, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get('resource', {}).get('items', [])
    else:
        print(f"Failed to get tickets: {response.status_code}")
        return []



def transfer_ticket_directly(ticket_id, team_name, agent_identity):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Key {TOKEN}'
        }

        guid = str(uuid.uuid4())

        payload = {
            "id": f"{guid}",
            "to": "postmaster@desk.msging.net",
            "method": "set",
            "uri": f"/tickets/{ticket_id}/transfer",
            "type": "application/vnd.iris.ticket+json",
            "resource": {
                "agentIdentity": f"{agent_identity}",
                "team": f"{team_name}"
            }
        }

        response = requests.post(BASE_URL, json=payload, headers=headers)
        if response.status_code == 200:
            response_json = response.json()
            print("Response JSON:", response_json)
            return response_json
        else:
            print(f"Failed to transfer ticket: {response.status_code}")
            print("Response content:", response.content)
            return None

# ticket_id = '99e73614-6eff-4dbc-9586-0190db727865'
# team_name = 'Gerencia'
# transfer_ticket(ticket_id, team_name)


# ticket_id = '4c2a9d0f-883c-4d28-ba81-0190fffd863d'
# team_name = 'Atendimento sede'
# agent_identity = 'autoti%40sicoobcressem.com.br@blip.ai'
# transfer_ticket_directly(ticket_id, team_name, agent_identity)


# ticket_id = '3cb24c74-7679-4764-834c-0190db69f7f4'
# close_ticket(ticket_id)

#
tickets = get_waiting_tickets()
print(tickets)

# agents = get_online_agents()
# print(agents)
