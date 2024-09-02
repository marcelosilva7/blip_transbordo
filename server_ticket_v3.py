from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timezone, timedelta
from ticketmanager1 import TicketManager

app = FastAPI()


ticket_manager = TicketManager()


def email_automatico(para, corpo, assunto):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import datetime

    data_atual = datetime.datetime.now()
    dia_atual = data_atual.strftime("%d/%m/%Y")
    host = "smtp.office365.com"
    port = "587"
    login = "no-reply@sicoobcressem.com.br"
    senha = "KDkcxSWuJ!u&H57"
    server = smtplib.SMTP(host, port)
    server.ehlo()
    server.starttls()
    server.login(login, senha)

    recive = para
    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = recive
    email_msg['Subject'] = assunto
    email_msg.attach(MIMEText(corpo, "html"))

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string().encode("utf-8"))
    server.quit()



# @app.get("/monitor_tickets")
# def monitor_tickets():
#     waiting_tickets = ticket_manager.get_waiting_tickets()
#     now = datetime.now(timezone.utc)
#     for ticket in waiting_tickets:
#         if ticket.get('team') == 'Atendimento Geral':
#             continue
#         storage_date = datetime.fromisoformat(ticket['storageDate'].replace('Z', '+00:00'))
#         if (now - storage_date) > timedelta(minutes=10):
#             print(f"Ticket {ticket['id']} has been waiting since {storage_date}, transferring to 'Atendimentos Atrasados'")
#             ticket_manager.transfer_ticket(ticket['id'], 'Atendimentos Atrasados')
#     return {"status": "Monitoring complete"}

emails_enviados = {}

@app.get("/monitor_tickets")
def monitor_tickets():
    waiting_tickets = ticket_manager.get_waiting_tickets()
    now = datetime.now(timezone.utc)

    toggle_fila = ""

    minutos_espera = 10

    # Lista de setores que queremos monitorar
    setores = ["Atendimento Sede", "Agência Sede", "Seguro", "Cadastro", "Financeiro",
               "Centro de Convivência", "Sul"]

    setores_cidades = ["Campos do Jordão", "Jacareí", "Santa Branca",
                       "São Bento do Sapucaí", "Monteiro Lobato", "Caraguatatuba",
                       "Cachoeira Paulista", "Cruzeiro", "Caçapava", "Ilhabela",
                       "Santo Antônio do Pinhal", "Ubatuba", "São Sebastião"]

    atraso_cidades = "Atraso Atendimento Cidades"

    for ticket in waiting_tickets:
        storage_date = datetime.fromisoformat(ticket['storageDate'].replace('Z', '+00:00'))

        # Verificar se o ticket pertence à localidade 'Jambeiro'
        if ticket.get('team') == 'Jambeiro':
            if (now - storage_date) > timedelta(minutes=minutos_espera):
                print(
                    f"Ticket {ticket['id']} has been waiting since {storage_date}, transferring to Atraso Jambeiro")
                ticket_manager.transfer_ticket(ticket['id'], 'Atraso Jambeiro')
            continue  # Ir para o próximo ticket, pois já tratamos esse caso

        # Verificar se o ticket pertence à localidade 'Paraibuna'
        if ticket.get('team') == 'Paraibuna':
            if (now - storage_date) > timedelta(minutes=minutos_espera):
                print(
                    f"Ticket {ticket['id']} has been waiting since {storage_date}, transferring to Atraso Paraibuna")
                ticket_manager.transfer_ticket(ticket['id'], 'Atraso Paraibuna')
            continue  # Ir para o próximo ticket, pois já tratamos esse caso

        # Verificar se o ticket pertence à localidade 'Salesópolis'
        if ticket.get('team') == 'Salesópolis':
            if (now - storage_date) > timedelta(minutes=minutos_espera):
                if toggle_fila:
                    fila_atraso = 'Atraso Paraibuna'
                else:
                    fila_atraso = 'Atraso Jambeiro'

                print(f"Ticket {ticket['id']} has been waiting since {storage_date}, transferring to '{fila_atraso}'")
                ticket_manager.transfer_ticket(ticket['id'], fila_atraso)

                # Alternar a fila para a próxima vez
                toggle_fila = not toggle_fila
            continue  # Ir para o próximo ticket, pois já tratamos esse caso

        # Verificar se o ticket pertence a um dos setores que estamos monitorando
        if ticket.get('team') in setores_cidades:
            if (now - storage_date) > timedelta(minutes=minutos_espera):
                setor_atraso = "Atraso Atendimento Cidades"
                print(
                    f"Ticket {ticket['id']} has been waiting since {storage_date}, transferring to '{setor_atraso}'")
                ticket_manager.transfer_ticket(ticket['id'], setor_atraso)

        # Verificar se o ticket pertence a um dos setores que estamos monitorando
        if ticket.get('team') in setores:
            if (now - storage_date) > timedelta(minutes=minutos_espera):
                setor_atraso = "Atraso Atendimento Sede"
                print(f"Ticket {ticket['id']} has been waiting since {storage_date}, transferring to '{setor_atraso}'")
                ticket_manager.transfer_ticket(ticket['id'], setor_atraso)

        # Verificar se o ticket pertence a um dos setores que estamos monitorando
        if ticket.get('team') == "Pessoa Juridica":
            if (now - storage_date) > timedelta(minutes=10):
                # Verificar se já enviamos um e-mail para este ticket
                if ticket['id'] not in emails_enviados:
                    # Construir o corpo do e-mail
                    setor = "Pessoa Juridica"
                    subject = f"Alerta de Atraso no Blip"
                    body = f"O ticket {ticket['id']} está aguardando há mais de 10 minutos no Blip. Por favor, verifique."
                    to_address = "marcelo.silva@sicoobcressem.com.br"
                    email_real = "helton.coelho@sicoobcressem.com.br"

                    # Enviar o e-mail
                    email_automatico(to_address, body, subject)

                    # Registrar que o e-mail foi enviado
                    emails_enviados[ticket['id']] = True

                    print(f"E-mail enviado para {setor} sobre o ticket {ticket['id']}.")


    return {"status": "Monitoring complete"}


def schedule_monitoring():
    scheduler = BackgroundScheduler()
    scheduler.add_job(monitor_tickets, 'interval', minutes=1)
    scheduler.start()
    print("estou checando")

@app.on_event("startup")
def on_startup():
    schedule_monitoring()

@app.on_event("shutdown")
def on_shutdown():
    scheduler = BackgroundScheduler()
    scheduler.shutdown()
