from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Person, Corren, Corren_euro
import requests
from bs4 import BeautifulSoup
import time
import schedule
import smtplib


class Currency:
    EURO = 'https://www.google.ru/search?newwindow=1&client=opera&sxsrf=ALeKk01z7Zv71DCVUExCLz-JPIXtDRGvvQ%3A1585302666167&ei=isx9XoDPCeGAk74Pi9-Q8Ag&q=курс+евро&oq=курс+евро&gs_l=psy-ab.1.0.0i131i70i258j0i131i20i263l2j0j0i131j0j0i67j0l3.1288827.1291879..1293667...1.3..0.220.1561.0j7j2......0....1..gws-wiz.....10..0i71j35i362i39j35i39j0i131i67j35i39i70i258j0i20i263.05SlAWaayuc'
    DOLLAR = 'https://www.google.ru/search?newwindow=1&client=opera&hs=7Mo&sxsrf=ALeKk009g0zJ8nOlsPbtQCZb4XwvdSa2oQ%3A1585300321696&ei=YcN9XtCRKsHh6QTYwraYBQ&q=доллар+к+рублю&oq=доллар+к+рублю&gs_l=psy-ab.3..0i131i70i258j0j0i131l2j0l6.2325305.2342192..2342552...14.1..0.226.3774.0j24j1......0....1..gws-wiz.....10..0i71j35i362i39j0i10i1j0i10i1i42j0i10j0i13i30.jG-yUAz0h7s&ved=0ahUKEwiQxqX0p7roAhXBcJoKHVihDVMQ4dUDCAo&uact=5'
    user = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97'}

    def get_price_doll(self):
        fullPage_dollar = requests.get(self.DOLLAR, headers=self.user)
        soup_dollar = BeautifulSoup(fullPage_dollar.content, 'html.parser')
        convert_dollar = soup_dollar.findAll("span", {"class": "DFlfde", "class": "SwHCTb"})
        return convert_dollar[0].text

    def get_price_euro(self):
        fullPage_euro = requests.get(self.EURO, headers=self.user)
        soup_euro = BeautifulSoup(fullPage_euro.content, 'html.parser')
        convert_euro = soup_euro.findAll("span", {"class": "DFlfde", "class": "SwHCTb"})
        return convert_euro[0].text

    def check_doll(self):
        currency_doll = float(self.get_price_doll().replace(",", "."))
        return currency_doll

    def check_euro(self):
        currency_euro = float(self.get_price_euro().replace(",", "."))
        return currency_euro

    def mail(self, email):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        subject = 'Курс валют'
        body = 'курс валют на сегодня: 1$ = {0} , 1€ = {1}'.format(self.check_doll(), self.check_euro())
        message = f'Subject: {subject}\n\n{body}'
        server.sendmail('example.com', email, message)

        server.quit()


currency = Currency()


def create_currency_in_bd(dol=currency.check_doll(), euro=currency.check_euro()):
    Corren.objects.create(doll=dol)
    Corren_euro.objects.create(euro=euro)


def index(request):
    create_currency_in_bd()

    people = Person.objects.all()
    doll_all = Corren.objects.all()
    euro_all = Corren_euro.objects.all()

    doll_list = [i for i in doll_all]
    euro_list = [i for i in euro_all]

    ans_doll = doll_list[-1].doll
    ans_euro = euro_list[-1].euro

    return render(request, "index.html", {"currency_doll": ans_doll, "currency_euro": ans_euro, "people": people})


def create_email(request):
    if request.method == "POST":
        peo = Person()
        peo.email = request.POST.get("email")
        peo.time = request.POST.get("time")
        peo.save()
    return HttpResponseRedirect("/")


def send_email():
    people = Person.objects.all()
    if people.count:
        for person in people:
            schedule.every().day.at(person.time).do(currency.mail(person.email))

            schedule.run_pending()
            time.sleep(1800)
