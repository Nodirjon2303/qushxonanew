import datetime

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse, HttpResponse
import json
from django.db.models import Q
import requests


from functools import wraps
def admin_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        profile = request.user
        if 'admin' in  profile.username :
            return function(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrap
def qushxona_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        profile = request.user
        if ('qushxona' in  profile.username) or ('admin' in profile.username) :
            return function(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrap


def bozor_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):

        profile = request.user
        if 'bozor' in  profile.username :
            return function(request, *args, **kwargs)
        else:
            return redirect('login')

    return wrap




@qushxona_only
def homeView(request):
    if request.method == 'POST':
        clients = Client.objects.filter(role='dehqon')
        data = []
        for i in clients:
            data.append({'name': i.full_name,
                         'id': i.id
                         })
        products = Product.objects.all()
        datap = []
        for i in products:
            datap.append({'name': i.name})
        return JsonResponse({'data': data, 'product': datap})
    kirim = ExpenseDehqon.objects.filter(created_date__date=datetime.date.today(),
                                         status='progress')
    data = []
    for i in kirim:
        summa = 0
        tulovlar = IncomeDehqon.objects.filter(dehqon_product=i,
                                               created_date__date=datetime.date.today())

        for j in tulovlar:
            summa += j.amount
        data.append({
            "name": i.dehqon.full_name,
            'product': i.product.name,
            'quantity': i.quantity,
            'weight': i.weight,
            'tulov': summa,
            'created_data': i.created_date.strftime("%d-%m-%Y %H:%M")
        })

    return render(request, 'main.html', {'data': data
                                         })

@qushxona_only
def saveView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = data['quantity']
        weight = data['weight']
        name = data['name']
        product = data['product']
        tulov = data['tulov']
        if quantity and weight and name and product:
            quantity, weight = int(quantity), int(weight)
            dehqon = Client.objects.get(full_name=name)
            product = Product.objects.get(name=product)
            expense = ExpenseDehqon.objects.create(dehqon=dehqon, product=product, quantity=quantity, weight=weight)
            expense.save()
            try:
                text = f"Qushxonaga Yangi mollar keldi!!!\n" \
                       f"Dehqon: {expense.dehqon.full_name}\n" \
                       f"Taxminiy Og'irligi: {expense.weight}kg\n" \
                       f"Soni: {expense.quantity}ta \n" \
                       f"Sanasi:{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}"
                requests.post(
                    f'https://api.telegram.org/bot5262072872:AAFdCPS5Ah7fJV8Qyl-rIxcfw8otYDI6Sr0/sendMessage?chat_id=-1001681426591&text={text}')
            except Exception as e:
                print(e)
            if tulov:
                expense = IncomeDehqon.objects.create(dehqon_product=expense, amount=int(tulov))
                expense.save()
                try:
                    text = f"Dehqonga to'lov!!!\n" \
                           f"Dehqonning ismi: {expense.dehqon_product.dehqon.full_name}\n" \
                           f"Tulov miqdori: {expense.amount}"
                    requests.post(
                        f'https://api.telegram.org/bot5262072872:AAFdCPS5Ah7fJV8Qyl-rIxcfw8otYDI6Sr0/sendMessage?chat_id=-1001591856875&text={text}')
                except Exception as e:
                    print(e)
            return JsonResponse({'data': 'ok'})
        else:
            return JsonResponse({'data': 'error'})

@qushxona_only
def saveIncomeView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        weight = data['weight']
        price = data['price']
        dehqon = data['dehqon']
        mijoz = data['mijoz']
        massa = 0
        ogirliki = weight
        data = weight.split('+')
        price = int(price)
        if weight[-1] == '+':
            quantity = len(data) - 1
        else:
            quantity = len(data)
        for i in data:
            try:
                a = float(i)
                massa += a
            except:
                return JsonResponse({'data': 'error'})
        mijoz = Client.objects.get(full_name=mijoz)
        dehqon = IncomeClient.objects.get(id=int(dehqon))
        product_dehqon = dehqon.product_dehqon
        text = f"Dehqon: {dehqon.product_dehqon.dehqon.full_name}\nMijoz: {mijoz.full_name}\nOg'irligi: {ogirliki} = {massa}kg\nSoni: {quantity}ta \nNarxi(1 kg) : {price}\nJami: {massa * price}\nSanasi:{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}"
        requests.post(
            f'https://api.telegram.org/bot5262072872:AAFdCPS5Ah7fJV8Qyl-rIxcfw8otYDI6Sr0/sendMessage?chat_id=-1001681426591&text={text}')
        if dehqon.quantity < quantity:
            return JsonResponse({'data': 'error'})
        elif dehqon.quantity == quantity:
            dehqon.delete()
            return JsonResponse({'data': 'ok'})
        else:
            dehqon.quantity -= quantity
            dehqon.save()
        IncomeClient.objects.create(client=mijoz, product_dehqon=product_dehqon, quantity=quantity, weight=massa,
                                    price=price)
        return JsonResponse({'data': 'ok'})

@qushxona_only
def incomeView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mijozlar = Client.objects.filter(role='client')
        # dehqonlar = ExpenseDehqon.objects.filter(status='progress')
        product = Product.objects.all()
        mijoz = []
        dehqon = []
        sanoq = 0
        for i in mijozlar:
            products = IncomeClient.objects.filter(status='bron', client=i)
            if len(products) > 0:
                mijoz.append({
                    'name': i.full_name
                })
                if sanoq == 0:
                    for i in products:
                        dehqon.append({
                            'name': f"{i.product_dehqon.dehqon.full_name}ning {i.quantity} ta {i.product_dehqon.product.name}lari",
                            'id': i.id
                        })
                sanoq += 1

        # for i in dehqonlar:
        #     miqdori = IncomeClient.objects.filter(product_dehqon=i)
        #     soni = 0
        #     for j in miqdori:
        #         soni += j.quantity
        #     dehqon.append({
        #         'name': f"{i.dehqon.full_name}ning {i.quantity - soni}ta  {i.product.name}lari",
        #         'id': i.id
        #     })
        products = []
        for i in product:
            products.append({'name': i.name})
        return JsonResponse({'mijoz': mijoz,
                             'dehqon': dehqon,
                             'product': products
                             })
    incomes = IncomeClient.objects.filter(status='progress')
    data = []

    for i in incomes:
        data.append({
            'id': i.client.id,
            'client': i.client.full_name,
            'dehqon': f"{i.product_dehqon.dehqon.full_name}ning {i.product_dehqon.quantity}ta {i.product_dehqon.product.name}lari",
            'product': i.product_dehqon.product.name,
            'quantity': i.quantity,
            'weight': i.weight,
            'price': i.price,
            'total_price': i.price * i.weight,
            'created_data': i.created_date.strftime("%d-%m-%Y %H:%M")

        })
    return render(request, 'IncomeClient.html', {'data': data})

@qushxona_only
def clientPageView(request, slug):
    client = Client.objects.get(id=slug)
    incomes = IncomeClient.objects.filter(client=client, status='progress').order_by('created_date')
    data = []
    for i in incomes:
        res = []
        tulovlar = ExpenseClient.objects.filter(income_client=i)
        all = 0
        for j in tulovlar:
            res.append({
                'data': f"{j.created_date.strftime('%d-%m-%Y %H:%M')}",
                'amount': j.amount,
                'id': i.id
            })
            all += j.amount
        data.append({
            'mijoz': i.client.full_name,
            'dehqon': i.product_dehqon.dehqon.full_name,
            'product': i.product_dehqon.product.name,
            'quantity': i.quantity,
            'weight': i.weight,
            'price': i.price,
            'total_price': i.weight * i.price,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M"),
            'payments': res,
            'Jami': all,
            'qarz': (i.weight * i.price) - all,
            'id': i.id
        })
    return render(request, 'ClientPage.html', {'data': data})

@qushxona_only
def clientPaymentView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        summa = data['miqdor']
        id = data['id']
        expense = ExpenseClient.objects.create(amount=summa, income_client_id=id)
        try:
            text = f"Optomchidan to'lov!!!\n" \
                   f"Optomchining ismi: {expense.income_client.client.full_name}\n" \
                   f"Tulov miqdori: {expense.amount}"
            requests.post(
                f'https://api.telegram.org/bot5262072872:AAFdCPS5Ah7fJV8Qyl-rIxcfw8otYDI6Sr0/sendMessage?chat_id=-1001591856875&text={text}')
        except Exception as e:
            print(e)
        tulovlar = sum([i.amount for i in ExpenseClient.objects.filter(income_client_id=id)])
        product = IncomeClient.objects.get(id=id)
        if (product.weight * product.price) <= tulovlar:
            product.status = 'completed'
            product.save()
        return JsonResponse({'data': 'ok'})

@qushxona_only
def incomeDehqonView(request):
    products = ExpenseDehqon.objects.filter(status='progress')
    data = []

    for i in products:
        sotilganlari = sum([i.quantity for i in IncomeClient.objects.filter(product_dehqon=i)])
        ogirligi = sum([i.weight for i in IncomeClient.objects.filter(product_dehqon=i)])

        data.append(
            {
                "dehqon": i.dehqon.full_name,
                "dehqon_id": i.dehqon.id,
                "product": i.product.name,
                'sotilganlar': sotilganlari,
                "weight": ogirligi,
                'tiriklari': i.quantity - sotilganlari,
                'price': i.price,
                'sanasi': i.created_date.strftime("%d-%m-%Y %H:%M"),
                'id': i.id
            }
        )

    return render(request, 'IncomeDehqon.html', {"data": data})

def SearchboxView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        dehqon = data['search']
        data = Client.objects.filter(Q(full_name__contains=f'{dehqon}')& (Q(role='dehqon')|Q(role='client')))
        print(data)
        context = []
        for i in data:
            context.append({
                'full_name': i.full_name,
                'id': i.id,
                'role': i.role
            })
        return  JsonResponse({'data': context})


@qushxona_only
def priceChangeView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        miqdor = data['miqdor']
        id = data['id']
        product = ExpenseDehqon.objects.get(id=id)
        product.price = miqdor
        product.save()
        return JsonResponse({'data': 'ok'})

@qushxona_only
def dehqonView(request, slug):
    dehqon = Client.objects.get(id=slug)
    products = ExpenseDehqon.objects.filter(dehqon=dehqon, status='progress')
    data = []
    for i in products:
        tulovlar = []
        summ = 0
        sanoq = 1
        for j in IncomeDehqon.objects.filter(dehqon_product=i):
            tulovlar.append(
                {
                    'amount': j.amount,
                    'id': sanoq,
                    'date': j.created_date.strftime("%d-%m-%Y %H:%M")
                }
            )
            sanoq += 1
            summ += j.amount
        sotilganlari = sum([i.quantity for i in IncomeClient.objects.filter(~Q(status='bron'), product_dehqon=i)])
        bronlari = sum([i.quantity for i in IncomeClient.objects.filter(status='bron', product_dehqon=i)])

        ogirligi = sum([i.weight for i in IncomeClient.objects.filter(product_dehqon=i)])
        data.append({
            'dehqon': i.dehqon.full_name,
            'product': i.product.name,
            'quantity': i.quantity,
            'sotilganlari': sotilganlari,
            'ogirligi': ogirligi,
            'price': i.price,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M"),
            'tulovlar': tulovlar,
            'bron': bronlari,
            'id': i.id,
            'deh_id': i.dehqon.id,
            'next': sanoq,
            'Summa': summ,
            'qarz': (ogirligi * i.price) - summ,
            'status': (i.quantity == sotilganlari and summ >= ogirligi * i.price)
        })
    return render(request, 'dehqon.html', {'data': data})

@qushxona_only
def dehqonIncomeView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        miqdor = data['miqdor']
        id = data['id']
        expense = IncomeDehqon.objects.create(dehqon_product_id=int(id), amount=int(miqdor))
        expense.save()
        try:
            text = f"Dehqonga to'lov!!!\n" \
                   f"dehqonning ismi: {expense.dehqon_product.dehqon.full_name}\n" \
                   f"Tulov miqdori: {expense.amount}"
            requests.post(
                f'https://api.telegram.org/bot5262072872:AAFdCPS5Ah7fJV8Qyl-rIxcfw8otYDI6Sr0/sendMessage?chat_id=-1001591856875&text={text}')
        except Exception as e:
            print(e)
        return JsonResponse({'data': 'ok'})

@qushxona_only
def dehqonCompleteView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        id = int(data['id'])
        expense = ExpenseDehqon.objects.get(id=id)
        expense.status = 'completed'
        expense.save()
        return JsonResponse({"data": 'ok'})

@qushxona_only
def teriView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        type = data['type']
        day = int(data['day'])
        if type == 'teri':
            objects = Teri.objects.filter(created_date__gte=(datetime.datetime.now() - datetime.timedelta(days=day)))
            mijozlar = Client.objects.filter(role='Teri')
        else:
            mijozlar = Client.objects.filter(role='kallahasb')
            objects = KallaHasb.objects.filter(
                created_date__gte=(datetime.datetime.now() - datetime.timedelta(days=day)))
        products = Product.objects.all()
        data = []
        for i in objects:
            data.append({
                'mijoz': i.mijoz.full_name,
                'product': i.product.name,
                'soni': i.soni,
                'created_date': i.created_date.strftime("%d-%m-%Y %H:%M")
            })
        mijoz = []
        for i in mijozlar:
            mijoz.append(
                {
                    'mijoz': i.full_name,
                    'id': i.id
                }
            )
        product = []
        for i in products:
            product.append({
                'name': i.name,
                'id': i.id
            })

        return JsonResponse({'data': data, 'mijozlar': mijoz, 'product': product})
    teris = Teri.objects.filter(created_date__date=datetime.date.today())
    id = 5
    mijozlar = Client.objects.filter(role='Teri')
    product = Product.objects.all()
    return render(request, 'teri.html', {'data': teris, 'id': id, 'mijoz': mijozlar, 'product': product})

@qushxona_only
def kallaHasbView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mijoz = int(data['mijoz'])
        product = int(data['product'])
        soni = int(data['soni'])
        type = data['type']
        if type == 'kallahasb':
            KallaHasb.objects.create(mijoz_id=mijoz, product_id=product, soni=soni).save()
        else:
            Teri.objects.create(mijoz_id=mijoz, product_id=product, soni=soni).save()
        return JsonResponse({'data': 'ok'})
    kallas = KallaHasb.objects.filter(created_date__date=datetime.date.today()).order_by('-id')
    id = "№"
    mijozlar = Client.objects.filter(role='kallahasb')
    product = Product.objects.all()
    return render(request, 'kallahasb.html', {'data': kallas, 'id': id, 'mijoz': mijozlar, 'product': product})

@qushxona_only
def kirimView(request):
    # kirimlar = ExpenseClient.objects.all()
    kirimlar = ExpenseClient.objects.filter(created_date__date=datetime.date.today())
    chiqimlar = IncomeDehqon.objects.filter(created_date__date=datetime.date.today())
    data = []
    sanoq = 1
    kirim = 0
    chiqim = sum([i.amount for i in chiqimlar])
    for i in kirimlar:
        data.append({
            'n': sanoq,
            'mijoz': i.income_client.client.full_name,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M"),
            'amount': i.amount
        })
        kirim += i.amount
        sanoq += 1
    return render(request, 'kirim.html', {'kirimlar': data, 'kassa': (kirim - chiqim)})

@qushxona_only
def chiqimView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        mijoz = Client.objects.get(id=int(data['mijoz']))
        product_dehqon = ExpenseDehqon.objects.get(id=int(data['dehqon']))
        soni = int(data['soni'])
        jami = sum([i.quantity for i in IncomeClient.objects.filter(product_dehqon=product_dehqon)])
        if jami + soni > product_dehqon.quantity:
            return JsonResponse({'data': "error"})
        IncomeClient.objects.create(client=mijoz, product_dehqon=product_dehqon, quantity=soni, status='bron').save()
        return JsonResponse({'data': 'ok'})
    kirimlar = ExpenseClient.objects.filter(created_date__date=datetime.date.today())
    chiqimlar = IncomeDehqon.objects.filter(created_date__date=datetime.date.today())
    # chiqimlar = IncomeDehqon.objects.all()
    data = []
    sanoq = 1
    chiqim = 0
    kirim = sum([i.amount for i in kirimlar])
    for i in chiqimlar:
        data.append({
            'n': sanoq,
            'mijoz': i.dehqon_product.dehqon.full_name,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M"),
            'amount': i.amount
        })
        chiqim += i.amount
        sanoq+=1
    datab = []
    xarajatlar = Xarajat.objects.filter(created_date__date=datetime.date.today(), choise='qushxona')
    sanoq = 1
    chiqimb = 0
    for i in xarajatlar:
        datab.append({
            'n': sanoq,
            'maqsad': i.comment,
            'miqdori': i.amount,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M")
        })
        chiqimb += i.amount
    return render(request, 'chiqim.html',
                  {'chiqimlar': data, 'kassa': (kirim - chiqim - chiqimb), 'dehqonjami': chiqim, 'data': datab,
                   'chiqimb': chiqimb})

@qushxona_only
def bronView(request):
    if request.method == 'POST':
        mijoz = []
        mijozlar = Client.objects.filter(role='client')
        for i in mijozlar:
            mijoz.append({
                'name': i.full_name,
                'id': i.id
            })
        product = []
        allproduct = ExpenseDehqon.objects.filter(status='progress')
        for i in allproduct:
            soni = sum([i.quantity for i in IncomeClient.objects.filter(product_dehqon=i)])
            if i.quantity > soni:
                product.append({
                    'name': f"{i.dehqon.full_name}ninf {i.quantity - soni}ta {i.product.name}lari",
                    'id': i.id
                })
        return JsonResponse({
            'mijoz': mijoz,
            'product': product
        })
    mijozlar = IncomeClient.objects.filter(status='bron')
    return render(request, 'bron.html', {'data': mijozlar})

@qushxona_only
def mijozchangeView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        bronlar = IncomeClient.objects.filter(status='bron', client__full_name=data['mijoz'])
        data = []
        # products = IncomeClient.objects.filter(status='bron', client=i)
        for i in bronlar:
            data.append({
                'name': f"{i.product_dehqon.dehqon.full_name}ning {i.quantity} ta {i.product_dehqon.product.name}lari",
                'id': i.id
            })
        return JsonResponse({'data': data})


def loginView(request):
    if request.POST:
        password = request.POST.get('password')
        username = request.POST.get('username')
        if request.user.username == '':
            user = authenticate(request, username=username, password=password)
            if user:
                login(request=request, user=user)
                if 'admin' in user.username:
                    return redirect('adminkirim')
                elif 'bozor' in request.user.username:
                    return redirect('bozorchiqim')
                else:
                    return redirect('home')
            else:
                return HttpResponse("username yoki password xato")
        else:
            if 'admin' in request.user.username:
                return redirect('adminkirim')
            elif 'bozor' in request.user.username:
                return redirect('bozorchiqim')
            else:
                return redirect('home')

    return render(request, 'login.html', {})

@admin_only
def adminkirimView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        type = data['type']
        days = int(data['day'])
        data = []
        sanoq = 1
        Jami = 0
        datab = []
        if type == 'kirim':
            kirimlar = ExpenseClient.objects.filter(
                created_date__gte=(datetime.datetime.now() - datetime.timedelta(days=days)))
            for i in kirimlar:
                data.append({
                    'dehqon': i.income_client.client.full_name,
                    'n': sanoq,
                    'summa': i.amount,
                    'date': i.created_date.strftime("%d-%m-%Y %H:%M")
                })
                sanoq += 1
                Jami += i.amount

        elif type == 'chiqim':
            chiqimlar = IncomeDehqon.objects.filter(
                created_date__gte=(datetime.datetime.now() - datetime.timedelta(days=days)))
            for i in chiqimlar:
                data.append({
                    'dehqon': i.dehqon_product.dehqon.full_name,
                    'n': sanoq,
                    'summa': i.amount,
                    'date': i.created_date.strftime("%d-%m-%Y %H:%M")
                })
                sanoq += 1
                Jami += i.amount
            chiqimother = Xarajat.objects.filter(
                created_date__gte=(datetime.datetime.now() - datetime.timedelta(days=days)), choise='qushxona')
            sanoq = 1
            for i in chiqimother:
                datab.append({
                    'n': sanoq,
                    'maqsad': i.comment,
                    'miqdori': i.amount,
                    'date': i.created_date.strftime("%d-%m-%Y %H:%M")
                })
                Jami += i.amount
                sanoq += 1

        return JsonResponse({'data': data, 'jami': Jami, 'datab': datab})
    kirimlar = ExpenseClient.objects.filter(created_date__date=datetime.date.today())
    sanoq = 1
    Jami = 0
    data = []
    for i in kirimlar:
        data.append({
            'dehqon': i.income_client.client.full_name,
            'n': sanoq,
            'summa': i.amount,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M")
        })
        sanoq += 1
        Jami += i.amount
    return render(request, 'adminkirim.html', {'kirimlar': data, 'jami': Jami})

@admin_only
def adminchiqimView(request):
    chiqimlar = IncomeDehqon.objects.filter(created_date__date=datetime.date.today())
    data = []
    sanoq = 1
    Jami = 0
    for i in chiqimlar:
        data.append({
            'dehqon': i.dehqon_product.dehqon.full_name,
            'n': sanoq,
            'summa': i.amount,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M")
        })
        sanoq += 1
        Jami += i.amount
    datab = []
    xarajatlar = Xarajat.objects.filter(created_date__date=datetime.date.today(), choise='qushxona')
    sanoq = 1
    for i in xarajatlar:
        datab.append({
            'n': sanoq,
            'maqsad': i.comment,
            'miqdori': i.amount,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M")
        })
        Jami += i.amount
        sanoq += 1
    return render(request, 'adminchiqim.html', {'chiqimlar': data, 'jami': Jami, 'data': datab})

@admin_only
def adduserView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        fullname = data['fullname']
        phone = data['phone']
        address = data['address']
        role = data['role']
        Client.objects.create(full_name=fullname, address=address, phone=phone, role=role).save()
        return JsonResponse({'data': 'ok'})
    users = Client.objects.all()
    return render(request, 'adminadduser.html', {'users': users})

@qushxona_only
def qarzView(request):
    clients = Client.objects.filter(role='client')
    data = []
    sanoq = 1
    for i in clients:
        savdolar = IncomeClient.objects.filter(status='progress', client=i)
        jamitulov = 0
        jamiqarz = sum([(i.weight * i.price) for i in savdolar])
        for j in savdolar:
            tulovlar = ExpenseClient.objects.filter(income_client=j)
            jamitulov += sum([k.amount for k in tulovlar])
        qarz = jamiqarz - jamitulov
        if qarz > 0:
            data.append({
                'Client': i.full_name,
                'id': i.id,
                'qarz': qarz,
                'n': sanoq
            })
            sanoq += 1

    return render(request, 'Qarzlar.html', {"data": data})

@qushxona_only
def otherexpenseView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment = data['comment']
        amount = data['amount']
        type = data['type']
        Xarajat.objects.create(comment=comment, amount=amount, choise=type).save()
        return JsonResponse({'data': 'ok'})
    data = []
    xarajatlar = Xarajat.objects.filter(created_date__date=datetime.date.today(), choise='qushxona')
    sanoq = 1
    for i in xarajatlar:
        data.append({
            'n': sanoq,
            'maqsad': i.comment,
            'miqdori': i.amount,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M")
        })
    return render(request, 'boshqa.html', {'data': data})

@bozor_only
def bozorchiqimView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sotuvchi = int(data['sotuvchi'])
        mahsulot = int(data['mahsulot'])
        weight = data['ogirligi']
        price = int(data['price'])
        tulov = data['tulov']
        massa = 0
        data = weight.split('+')
        if weight[-1] == '+':
            quantity = len(data) - 1
        else:
            quantity = len(data)
        for i in data:
            try:
                a = int(i)
                massa += a
            except:
                return JsonResponse({'data': 'error'})
        income = IncomeSotuvchi.objects.create(sotuvchi_id=sotuvchi, product_id=mahsulot, quantity=quantity, weight=massa,
                                      price=price)
        text = f"Sotuvchi: {income.sotuvchi.full_name}\nOg'irligi: {weight} = {massa}kg\nSoni: {quantity}ta \nNarxi(1 kg) : {price}\nJami: {massa * price}\nSanasi:{datetime.datetime.now().strftime('%d-%m-%Y %H:%M')}"
        requests.post(
            f'https://api.telegram.org/bot5262072872:AAFdCPS5Ah7fJV8Qyl-rIxcfw8otYDI6Sr0/sendMessage?chat_id=-1001610927804&text={text}')

        if tulov:
            ExpenseSotuvchi.objects.create(income_sotuvchi=income, amount=int(tulov))
        return JsonResponse({'data': 'ok'})

    client = Client.objects.filter(role='client', status_bozor=True).first()
    jami_gush = 0
    jami_soni = 0
    incomes = IncomeSotuvchi.objects.filter(status='progress')
    sanoq = 1
    data = []
    for i in incomes:
        data.append({
            'n': sanoq,
            'id': i.sotuvchi.id,
            'sotuvchi': i.sotuvchi.full_name,
            'mahsulot': i.product.name,
            "ogirligi": i.weight,
            'soni': i.quantity,
            'price': i.price,
            'tulov' : sum([j.amount for j in ExpenseSotuvchi.objects.filter(income_sotuvchi=i)]),
            'date': i.created_date.strftime("%d-%m-%Y %H:%M")
        })
        jami_gush += i.weight
        jami_soni += i.quantity
    sotuvchilar = Client.objects.filter(role='sotuvchi')
    products = Product.objects.all()
    datam = []
    jamiqolganson = 0
    jamiogirlik = 0

    for i in products:
        incomes = IncomeClient.objects.filter(~Q(status='bron'), client=client, product_dehqon__product=i)
        soni = sum([i.quantity for i in incomes])
        ogirligi = sum([i.weight for i in incomes])

        sotilganlari = sum([i.quantity for i in IncomeSotuvchi.objects.filter(product=i)])
        sotogirlik = sum([i.weight for i in IncomeSotuvchi.objects.filter(product=i)])
        if soni > sotilganlari:
            datam.append(
                {'name': i.name,
                 'id': i.id
                 }
            )
        jamiqolganson += (soni - sotilganlari)
        jamiogirlik += (ogirligi - sotogirlik)

    return render(request, 'bozorchiqim.html',
                  {'gush': jami_gush, 'soni': jami_soni, 'data': data, 'sotuvchilar': sotuvchilar, 'mahsulotlar': datam,
                   'bazadaqolganson': jamiqolganson, 'qolganogirlik': jamiogirlik})

@bozor_only
def bozorboshqachiqimView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        miqdor = data['miqdor']
        id = data['id']
        ExpenseSotuvchi.objects.create(income_sotuvchi_id=id, amount=miqdor).save()
        sotuvchi = IncomeSotuvchi.objects.get(id = id).sotuvchi
        try:
            text = f"Sotuvchidan to'lov!!!\n" \
                   f"Sotuvchining ismi: {sotuvchi.full_name}\n" \
                   f"Tulov miqdori: {str(miqdor)[:-3]+' '+str(miqdor)[-3:]}"
            requests.post(
                f'https://api.telegram.org/bot5262072872:AAFdCPS5Ah7fJV8Qyl-rIxcfw8otYDI6Sr0/sendMessage?chat_id=-1001610927804&text={text}')
        except Exception as e:
            print(e)
        return JsonResponse({'data': 'ok'})
    datab = []
    Jami = 0
    xarajatlar = Xarajat.objects.filter(created_date__date=datetime.date.today(), choise='bozor')
    sanoq = 1
    for i in xarajatlar:
        datab.append({
            'n': sanoq,
            'maqsad': i.comment,
            'miqdori': i.amount,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M")
        })
        Jami += i.amount
        sanoq += 1
    return render(request, 'bozorboshqaxarajat.html', {"data": datab})

@bozor_only
def sotuvchiView(request, slug):
    sotuvchi = Client.objects.get(id=slug)
    sotuvlar = IncomeSotuvchi.objects.filter(sotuvchi=sotuvchi)
    data = []
    sanoq = 1
    for i in sotuvlar:
        payments = []
        jami_tulov = 0
        n = 1
        for j in ExpenseSotuvchi.objects.filter(income_sotuvchi=i):
            jami_tulov += j.amount
            payments.append({'n': n,
                             'amount': j.amount,
                             'date': j.created_date.strftime("%d-%m-%Y %H:%M")
                             })
            n += 1
        data.append({
            'id': i.id,
            'n': sanoq,
            'sotuvchi': i.sotuvchi.full_name,
            'mahsulot': i.product.name,
            'soni': i.quantity,
            'ogirligi': i.weight,
            'narxi': i.price,
            'sanasi': i.created_date.strftime("%d-%m-%Y %H:%M"),
            'jamisumma': (i.weight * i.price),
            'jamitulov': jami_tulov,
            'qarz': i.weight * i.price - jami_tulov,
            'payments': payments
        })
        sanoq += 1

    return render(request, 'sotuvchi.html', {'data': data})

@bozor_only
def qushxonastatisticsView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        day = int(data['day'])
        client = Client.objects.filter(status_bozor=True, role='client').first()
        incomes = IncomeClient.objects.filter(client=client, created_date__gte=(datetime.datetime.now()-datetime.timedelta(days=day)))
        data = []
        sanoq = 1
        jamiqarz = 0
        jamitulovlar = 0
        for i in incomes:
            jamitulov = sum([i.amount for i in ExpenseClient.objects.filter(income_client=i)])
            data.append({
                'n': sanoq,
                'product': i.product_dehqon.product.name,
                'quantity': i.quantity,
                'weight': i.weight,
                'price': i.price,
                'jamisumma': i.weight * i.price,
                'jamitulov': jamitulov,
                'qarz': i.weight * i.price - jamitulov,
                'date': i.created_date.strftime("%d-%m-%Y %H:%M")
            })
            jamiqarz += i.weight * i.price - jamitulov
            sanoq+=1
            jamitulovlar+=jamitulov
        return JsonResponse({'data': data, 'jamiqarz': jamiqarz, 'jamitulov': jamitulovlar})
    client = Client.objects.filter(status_bozor=True, role='client').first()
    incomes = IncomeClient.objects.filter(client=client, created_date__date = datetime.date.today())
    data = []
    sanoq = 1
    jamiqarz = 0
    jamitulovlar = 0
    for i in incomes:
        jamitulov = sum([i.amount for i in ExpenseClient.objects.filter(income_client=i)])
        data.append({
            'n':sanoq,
            'product': i.product_dehqon.product.name,
            'quantity': i.quantity,
            'weight': i.weight,
            'price': i.price,
            'jamisumma': i.weight*i.price,
            'jamitulov': jamitulov,
            'qarz': i.weight*i.price- jamitulov,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M")
        })
        jamitulovlar+=jamitulov
        jamiqarz+=i.weight*i.price- jamitulov
        sanoq+=1
    return render(request, 'qushxonastatistics.html', {'data': data, 'jamiqarz': jamiqarz, 'jamitulov': jamitulovlar})

@bozor_only
def bozorstatisticsView(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        day = int(data['day'])
        jami_gush = 0
        jami_soni = 0
        incomes = IncomeSotuvchi.objects.filter(created_date__gte= (datetime.datetime.now() - datetime.timedelta(days=day)))
        sanoq = 1
        data = []
        jtulov = 0
        jsumma = 0
        for i in incomes:
            jamitulov = sum([j.amount for j in ExpenseSotuvchi.objects.filter(income_sotuvchi=i)])
            data.append({
                'n': sanoq,
                'id': i.sotuvchi.id,
                'sotuvchi': i.sotuvchi.full_name,
                'mahsulot': i.product.name,
                "ogirligi": i.weight,
                'soni': i.quantity,
                'price': i.price,
                'jamitulov': jamitulov,
                'jamisumma': i.price * i.weight,
                'qarz': i.price*i.weight - jamitulov,
                'date': i.created_date.strftime("%d-%m-%Y %H:%M")
            })
            jami_gush += i.weight
            jami_soni += i.quantity
            jtulov += jamitulov
            jsumma += i.price * i.weight
            sanoq+=1
        return JsonResponse({'gush': jami_gush, 'jtulov': jtulov,'jsumma': jsumma , 'soni': jami_soni, 'data': data})
    jami_gush = 0
    jami_soni = 0
    incomes = IncomeSotuvchi.objects.filter(created_date__date = datetime.datetime.today())
    sanoq = 1
    data = []
    jtulov = 0
    jsumma = 0
    for i in incomes:
        jamitulov = sum([j.amount for j in ExpenseSotuvchi.objects.filter(income_sotuvchi=i)])
        data.append({
            'n': sanoq,
            'id': i.sotuvchi.id,
            'sotuvchi': i.sotuvchi.full_name,
            'mahsulot': i.product.name,
            "ogirligi": i.weight,
            'soni': i.quantity,
            'price': i.price,
            'jamitulov': jamitulov,
            'jamisumma': i.price * i.weight,
            'qarz': i.price*i.weight - jamitulov,
            'date': i.created_date.strftime("%d-%m-%Y %H:%M")
        })
        jami_gush += i.weight
        jami_soni += i.quantity
        jtulov +=jamitulov
        jsumma += i.price *i.weight
        sanoq+=1
    return render(request, 'bozorstatistics.html',
                  {'gush': jami_gush,'jtulov': jtulov,'jsumma': jsumma , 'soni': jami_soni, 'data': data})

@bozor_only
def bozorqarzView(request):
    sotuvchilar = Client.objects.filter(role='sotuvchi')
    data = []
    sanoq=1
    for i in sotuvchilar:
        incomes = IncomeSotuvchi.objects.filter(sotuvchi = i)
        jamisumma = sum([j.weight*j.price for j in incomes])
        jamitulov = sum([j.amount for j in ExpenseSotuvchi.objects.filter(income_sotuvchi__sotuvchi=i)])
        data.append({
            'n': sanoq,
            'client': i.full_name,
            'id': i.id,
            'qarz':jamisumma-jamitulov
        })
        sanoq+=1
    return render(request, 'bozorqarz.html', {'data': data})
