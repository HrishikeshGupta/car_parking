from datetime import datetime, timedelta,timezone
from operator import itemgetter 
import random
import re

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.shortcuts import render
from django.template import loader

from .forms import ParkingsForm
from .models import Parking
import math



# CONSTANTS
VALID_APLPHABETS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
VALID_NUMBERS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
VALID_COLOURS = ['BLACK', 'BLUE', 'WHITE', 'RED']


def index(request):
    now = datetime.now(timezone.utc)
    latest_cars_list = Parking.objects.filter(in_use=1).order_by('slot')
    context = {'latest_cars_list': latest_cars_list,'today':now}
    return render(request, 'cars/index.html', context)


def detail(request, question_id):
    car = get_object_or_404(Parking, pk=question_id)
    return render(request, 'cars/detail.html', {'detail': car})    


def parking_create_view(request):
    form = ParkingsForm(request.POST or None)
    slot_list = []
    sorted_slot_list = []
    if form.is_valid():
        reg_number = form['reg_number'].value()
        validity_pattern = validate_reg_number(reg_number) 
        if validity_pattern:
            Parking_obj = Parking.objects.filter(reg_number = reg_number, in_use = 1)
            if Parking_obj:
                return render(request, 'cars/parking_create.html', {'error4': 'Invalid Registration Number(Allowed type colour: KA-23-JG-1345)'})
        else:
            return render(request, 'cars/parking_create.html', {'error1': 'Invalid Registration Number(Allowed type colour: KA-23-JG-1345)'})
        colour = form['colour'].value()
        if colour in VALID_COLOURS:
            pass
        else:
            return render(request, 'cars/parking_create.html', {'error2': 'Invalid colour(Allowed colour: BLACK,WHITE,BLUE,RED)'})
        Parking_obj = Parking.objects.filter(in_use=0, slot_used=0)
        if Parking_obj:
            print('existing slot')
            for each in Parking_obj:
                id = each.id
                slot = each.slot
                slot_list.append({'id':id, 'slot':slot})
   
            sorted_slot_list = sorted(slot_list, key=itemgetter('slot'))
            slot=int(sorted_slot_list[0]['slot'])
            #print(slot)
           # print('=====================')
            parking_slot_used = Parking.objects.filter(slot = slot)
            for each in parking_slot_used:
                Parking.objects.filter(id=each.id).update(slot_used=1)
            p = Parking(reg_number=reg_number, colour=colour, slot=slot, in_use=1, reg_date=datetime.now())
            p.save()
        else:
            f = open("slot.txt", "r")
            solt_size = f.read()
            Parking_obj = Parking.objects.filter(in_use=1).order_by('slot')
            for each in Parking_obj:
                slot_list.append(each.slot)
            latest_slot = max(slot_list)
            #print('new added')
            #print(slot_list)
            #print('-----------------------')
            if latest_slot + 1 <= int(solt_size):
                p = Parking(reg_number=reg_number, colour=colour, slot=int(latest_slot + 1), in_use=1, reg_date=datetime.now())
                p.save()
            else:
                return render(request, 'cars/parking_create.html', {'error3': 'OPPS!! All slots full'})
    form = ParkingsForm()  # rendering for clearing the data
    context = {'form': form}
    return render(request, 'cars/parking_create.html', context)


def validate_reg_number(reg_number):
    pattern = re.compile("(([A-Z]){2,2}(|-)(?:[0-9]){2,2}(|-)(?:[A-Z]){2}(|-)([0-9]){4,4})")
    return(pattern.match(reg_number))


def search_by_colour(request):
    context = {}
    return render(request, 'cars/search_by_colour.html', context)


def view_result(request):
    colour = request.GET.get("colour", "")
    latest_cars_list = Parking.objects.filter(in_use=1, colour=colour).order_by('slot')
    context = {'latest_cars_list': latest_cars_list}
    return render(request, 'cars/search_colour_result.html', context)
   
   
def auto_generate(request):
    slot_size = request.POST.get("slot_size", "")
    cars_already_present = request.POST.get("cars_already_present", "")
    
    f = open("slot.txt", "w+")
    f.write(slot_size)
    bool_validate = genetare_random_cars(slot_size, cars_already_present)
    if bool_validate == 1:
        context = {'cars_genereated': cars_already_present}
        return render(request, 'cars/auto_generate.html', context)
    else:
        context = {'invalid':'Invalid data'}
        return render(request, 'cars/auto_generate.html', context)

    
def genetare_random_cars(slot_size, cars_already_present):
    if int(cars_already_present) <= int(slot_size):
        for i in range(1, int(cars_already_present) + 1):
            reg_number, colour = validate_and_generate_reg_no_and_colour()
            p = Parking(reg_number=reg_number, colour=colour, slot=i, in_use=1, reg_date=datetime.now())
            p.save()
        return(1)
    else:
        return(0)
            
            
def validate_and_generate_reg_no_and_colour():
    reg_number = get_reg_number()
#     print(reg_number)
    colour = random.choices(VALID_COLOURS)
#     latest_cars_list = Parking.objects.filter(reg_number=reg_number, in_use = 0)
#     if latest_cars_list:
#         validate_and_generate_reg_no_and_colour()
#     else:
    return(reg_number, colour[0])


def get_reg_number():
    a = random.choices(VALID_APLPHABETS, k=2)
    a_str = list_to_str(a)
    b = random.choices(VALID_NUMBERS, k=2)
    b_str = list_to_str(b)
    c = random.choices(VALID_APLPHABETS, k=2)
    c_str = list_to_str(c)
    d = random.choices(VALID_NUMBERS, k=4)
    d_str = list_to_str(d)
    reg_number = a_str + '-' + b_str + '-' + c_str + '-' + d_str
#     validity_reg_number = validate_reg_number(reg_number)
#     if validity_reg_number:
#         return(reg_number)
#     else:
#         get_reg_number()
    return(reg_number)
        

def list_to_str(data_list):
    str_data = ''.join(map(str, data_list))
    return(str_data)

    
def exit_car(request):
    slot = request.POST.get("slot", "")
    reg_number = request.POST.get("reg_number", "")
    park_oj = Parking.objects.filter(reg_number=reg_number, slot=slot).first()
    now = datetime.now(timezone.utc)
    time_difference = (now -park_oj.reg_date)
    minutes = time_difference.seconds / 60
    park_oj = Parking.objects.filter(reg_number=reg_number, slot=slot).update(in_use=0)
    context = {'reg_number':reg_number, 'slot':slot, 'duration': minutes}
    return render(request, 'cars/car_exit.html', context)

    
def search_by_colour(request):
    context = {}
    return render(request, 'cars/search_by_colour.html', context)


def search_by_reg_number(request):
    context = {}
    return render(request, 'cars/search_by_reg_number.html', context)


def view_result_reg_source(request):
    reg_number = request.GET.get("reg_number", "")
    latest_cars_list = Parking.objects.filter(in_use=1, reg_number=reg_number).order_by('slot')
    context = {'latest_cars_list': latest_cars_list}
    return render(request, 'cars/search_reg_source_result.html', context)

def get_total_count_of_cars(request):
    total_cars = Parking.objects.all()
    now = datetime.now(timezone.utc)
    print('present time:' +str(now))
    for each in total_cars:
        print('entered time:'+str(each.reg_date))
        time_difference = (now -each.reg_date)
        minutes = time_difference.seconds / 60
        print('Duration: ', minutes) 
        print('-------------')
        
    context = {'total_count_of_cars': total_cars.count()}
    return render(request, 'cars/total_count_of_cars.html', context)

def get_total_income(request):
    amount = 0
    parking_obj = Parking.objects.all()
    for each in parking_obj:
        tepm_amount = 0
        tepm_amount,minutes = get_amount_for_car(each.reg_date)
        amount = amount + tepm_amount
    context = {'earned_till_now': amount}
    return render(request, 'cars/total_income.html', context)
    
def get_amount_for_car(reg_date):
    amount = 0
    now = datetime.now(timezone.utc)
    time_difference = (now -reg_date)
    minutes = time_difference.seconds / 60
    if minutes < 60:
        amount = 20
    else:
        temp = math.ceil(minutes /60)
        amount1 = 20
        amount2 = (temp-1) *10
        amount = amount1 +  amount2
    if amount > 200:
        amount =  200
    return(amount,minutes)

def get_slot_details(request):
    parking_obj = Parking.objects.filter(in_use = 1)
    used_slot = parking_obj.count()
    f = open("slot.txt", "r")
    solt_size = f.read()
    free = int(solt_size) - used_slot
    context = {'free_slot': free,'occupied_slot':used_slot, 'total_slots': int(solt_size) }
    return render(request, 'cars/slot_details.html', context)
        
def test(request):
#     now = datetime.now(timezone.utc)
#     latest_cars_list = Parking.objects.filter(in_use=1).order_by('slot')
#     context = {'latest_cars_list': latest_cars_list,'today':now}
#     return render(request, 'cars/test.html', context)
    list_of_dict = []
    amount = 0
    parking_obj = Parking.objects.all()
    for each in parking_obj:
        dict_data = {}
        tepm_amount = 0
        tepm_amount,minutes = get_amount_for_car(each.reg_date)
        amount = amount + tepm_amount
        dict ={'reg_number':each.reg_number,'minutes':minutes,'amount':tepm_amount}
        list_of_dict.append(dict)
         
    context = {'data': list_of_dict}
    print(context)
    return render(request, 'cars/test2.html', context)
    
    
    
    