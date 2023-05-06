from flask import Flask, render_template, request, redirect, url_for
from enum import Enum
from datetime import date, timedelta

app = Flask(__name__)

class Language(Enum):
    ENGLISH = 1
    CHINESE = 2
    SPANISH = 3

class TicketSystem:
    def __init__(self, available_tickets=100):
        self.available_tickets = available_tickets
        self.language = Language.ENGLISH

    def set_language(self, language):
        self.language = language

    def get_text(self, key):
        translations = {
            "welcome": {
                Language.ENGLISH: "Welcome to the Beijing Resort Ticket System!",
                Language.CHINESE: "欢迎使用北京度假村门票系统！",
                Language.SPANISH: "¡Bienvenido al sistema de entradas del complejo turístico de Beijing!",
            },
            "tickets_left": {
                Language.ENGLISH: "Available tickets: ",
                Language.CHINESE: "可用门票：",
                Language.SPANISH: "Entradas disponibles: ",
            },
            "how_many_tickets": {
                Language.ENGLISH: "How many tickets do you want to grab?",
                Language.CHINESE: "您想抢多少张门票？",
                Language.SPANISH: "¿Cuántas entradas quieres conseguir?",
            },
            "not_enough_tickets": {
                Language.ENGLISH: "Sorry, there are not enough tickets available.",
                Language.CHINESE: "抱歉，没有足够的门票。",
                Language.SPANISH: "Lo siento, no hay suficientes entradas disponibles.",
            },
            "grab_success": {
                Language.ENGLISH: "You have successfully grabbed {} tickets.",
                Language.CHINESE: "您已成功抢到{}张门票。",
                Language.SPANISH: "Has conseguido con éxito {} entradas.",
            },
        }
        return translations[key][self.language]

    def grab_tickets(self, count):
        if count > self.available_tickets:
            return False, self.get_text("not_enough_tickets")
        self.available_tickets -= count
        return True, self.get_text("grab_success").format(count)

ticket_system = TicketSystem(100)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        date_selected = request.form['date']
        count = int(request.form['count'])
        success, message = ticket_system.grab_tickets(count)
        if success:
            return redirect(url_for('ticket', name=name, date=date_selected, count=count))
        return render_template('index.html', message=message, available_tickets=ticket_system.available_tickets)
    min_date = date.today()
    max_date = min_date + timedelta(days=60)
    return render_template('index.html', available_tickets=ticket_system.available_tickets, min_date=min_date, max_date=max_date)

@app.route('/ticket')
def ticket():
    name = request.args.get('name')
    date_selected = request.args.get('date')
    count = request.args.get('count')
    return render_template('ticket.html', name=name, date=date_selected, count=count)

if __name__ == '__main__':
    app.run(debug=True)
