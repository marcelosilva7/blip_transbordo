from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone, timedelta
from ticketManager import TicketManager

app = FastAPI()


ticket_manager = TicketManager()

@app.get("/monitor_tickets")
def monitor_tickets():
    waiting_tickets = ticket_manager.get_waiting_tickets()
    now = datetime.now(timezone.utc)
    for ticket in waiting_tickets:
        storage_date = datetime.fromisoformat(ticket['storageDate'].replace('Z', '+00:00'))
        if (now - storage_date) > timedelta(minutes=2):
            print(f"Ticket {ticket['id']} has been waiting since {storage_date}, transferring to 'Atendimento Geral'")
            ticket_manager.transfer_ticket(ticket['id'], 'Atendimento Geral')
    return {"status": "Monitoring complete"}

def schedule_monitoring():
    scheduler = BackgroundScheduler()
    scheduler.add_job(monitor_tickets, 'interval', minutes=1)
    scheduler.start()
    print("Scheduler started.")


@app.on_event("startup")
def on_startup():
    schedule_monitoring()


@app.on_event("shutdown")
def on_shutdown():
    scheduler = BackgroundScheduler()
    scheduler.shutdown()
    print("Scheduler shut down.")

