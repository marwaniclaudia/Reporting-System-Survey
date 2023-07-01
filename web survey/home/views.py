from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from random import randrange
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User as U
from .forms import Createuser
from django.db.models import F
import csv as CSV
from django.db.models import Avg
import numpy as np
from .models import Question, SurveyQuestion, Survey, Responden,QuestionValue, ResponSurvey, User, Csv, CsvValue, Layanan
PDSI = "PDSI" #isi PDSI disini
# Create your views here.


def spilt(listA, n):
    for x in range(0, len(listA), n):
        chunck = listA[x: n+x]

        if len(chunck) < n:
            chunck = chunck + [None for y in range(n-len(chunck))]
        yield chunck

def auth(request):
    print("printed")
    if not request.user.is_authenticated:
        return redirect("home:login")
    # path = request.path.split("/")
    user = User.objects.get(email=request.user.email)
    if user.master:
        return redirect("home:master")

def loged(request):
    if request.method == "GET":
        if request.GET.get('logout') == "logout":
            logout(request)
            return redirect("home:index")
    if request.method == "POST":
        if request.POST['log'] == "regist":
            username = request.POST['username']
            age = request.POST['age']
            sex = request.POST['sex']
            email = request.POST['email']
            password = request.POST['password']
            # print(password)
            U.objects.create_user(username=username, email=email, password=password)
            User.objects.create(name=username, age=age, sex=sex, email=email)
            return redirect("home:index")
        elif request.POST['log'] == "login":
            username = request.POST['username']
            password = request.POST['password']
            loguser = authenticate(request, username=username, password=password)
            if loguser is not None:
                login(request, loguser)
                return redirect('home:index')
        else:
            return redirect("home:login")
    context = {
        'PDSI':PDSI,
        'title':'login',
        'active':1,
    }
    return render(request, 'user/login.html', context)

def index(request):
    context = {
        'PDSI':PDSI,
        'title':'home',
        'active':1
    }
    return render(request, 'user/index.html', context)

def csv(request):
    arrcsv = []
    arrlist = []
    nama = []
    data = []
    get = 0
    labels = []
    data = []
    if request.method == "POST":
        Csv.objects.create(name=request.FILES['csv'].name, file=request.FILES['csv'])
        return redirect("home:csv")
    if request.method == "GET":
        if request.GET.get('parse') == 'ya':
            id = request.GET.get('id')
            get = id
            kelompok = []
            sub = []
            nama = []
            survey = []
            nama = []
            header = []

            cld = []
            cloudfreq = {}
            csffile = Csv.objects.get(id=id)
            with open(str(csffile.file), encoding='mac_roman') as f:
                reader = CSV.reader(f)
                
                #ambil header
                for h in reader:
                    header.append(h)
                    break

                #cek jumlah header
                getrange = len(header[0]) - 1

                #insert header ke db + filter
                for lay in header[0]:
                    if len(lay) >= 18:
                        Layanan.objects.get_or_create(layanan=lay, csv=csffile)
                

                for row in reader:
                    
                    #komentar
                    cld.append(row[getrange-3])

                    
                        
                    #masukan semua data dalam array
                    for x in range(getrange):
                        survey.append(row[x])

                    #masukan data kritik
                    nama.append({
                        'nama':row[getrange-2],
                        'jenis kelamin':row[0],
                        'kritik':row[getrange-3],
                        'start':row[getrange-1],
                        'submit':row[getrange],
                        })
            for i in cld:
                cloudfreq[i] = cld.count(i)
            for x,y in cloudfreq.items():
                if x == "":
                    continue
                CsvValue.objects.get_or_create(csv=csffile,value=x, freq=y)
            # memisahkan data array ke sub[]
            for x in list(spilt(survey, getrange)):
                before = []
                for y in x:
                    if y == "":
                        continue
                    else:
                        before.append(y)
                sub.append(before)
            
            
            for s in sub:
                value = []
                getfreq = {}

                #menghitung counter decission
                for jj in s:
                    getfreq[jj] = s.count(jj)
                
                #memecah data array ke value[]
                for ss in s:
                    for h in header[0]:
                        if ss == h:
                            value.append(ss)
                #menjadikannya kelompok
                kelompok.append({
                    # 'nama':s[len(s)-2],
                    'header':value,
                    'Sangat setuju':getfreq.get('Sangat Setuju'),
                    'setuju':getfreq.get('Setuju'),
                    'Tidak setuju':getfreq.get('Tidak Setuju'),
                    'Sangat tidak setuju':getfreq.get('Sangat Tidak Setuju')
                })
            
            for k in kelompok:
                for head in k["header"]:
                    #jika judul kurang dari 18, data tidak di input
                    if len(head) <= 18:
                        continue
                        
                    #proses masuk ke database
                    layan = Layanan.objects.filter(layanan=head)
                    if k['setuju'] != None:
                        layan.update(setuju=layan[0].setuju + k['setuju'] )
                    if k['Sangat setuju'] != None:
                        layan.update(sangat_setuju=layan[0].sangat_setuju + k['Sangat setuju'])
                    if  k['Tidak setuju'] != None:
                        layan.update(tidak_setuju=layan[0].tidak_setuju + k['Tidak setuju'])
                    if k['Sangat tidak setuju'] != None:
                        layan.update(sangat_tidak_setuju=layan[0].sangat_tidak_setuju + k['Sangat tidak setuju'])
            return redirect("home:csv")
        
        if request.GET.get('parse') == 'gak':
            id = request.GET.get('id')
            get = id
            chart = Layanan.objects.filter(csv=Csv(id=id))
            for c in chart:
                labels.append(c.layanan)
                data.append((c.sangat_setuju*2)+(c.setuju)-(c.tidak_setuju)-(c.sangat_tidak_setuju*2))
            
            getcsv = Csv.objects.get(id=id)
            for x in CsvValue.objects.filter(csv=getcsv):
                if x.freq == 1:
                    continue
                if len(x.value) <= 5:
                    continue
                arrlist.append({
                    "name":x.value,
                    "size":x.freq*5
                })
        

        
    for i in Csv.objects.all():
        arrcsv.append({
            'id':i.id,
            'nama':i.name,
            'tanggal':i.time,
            'parse': True if Layanan.objects.filter(csv=i).count() != 0 else False
        })
    context = {
        'PDSI':PDSI,
        'title':'CSV',
        'active':2,
        'csvvalue':arrcsv,
        'value':arrlist,
        'get':get,
        'labels':labels,
        'data':data
    }
    return render(request, 'user/csv.html', context)


def json(request,id):

    kelompok = []
    sub = []
    nama = []
    survey = []
    nama = []
    header = []
    cloud = []
    csffile = Csv.objects.get(id=id)
    with open(str(csffile.file), encoding='mac_roman') as f:
        reader = CSV.reader(f)

        #ambil header
        for h in reader:
            header.append(h)
            break

        #cek jumlah header
        getrange = len(header[0]) - 1

        #insert header ke db + filter
        for lay in header[0]:
            if len(lay) >= 18:
                Layanan.objects.get_or_create(layanan=lay, csv=csffile)
        

        for row in reader:

            #komentar
            cloud.append(row[getrange-3])

            #masukan semua data dalam array
            for x in range(getrange):
                survey.append(row[x])

            #masukan data kritik
            nama.append({
                'nama':row[getrange-2],
                'jenis kelamin':row[0],
                'kritik':row[getrange-3],
                'start':row[getrange-1],
                'submit':row[getrange],
                })
    # memisahkan data array ke sub[]
    for x in list(spilt(survey, getrange)):
        before = []
        for y in x:
            if y == "":
                continue
            else:
                before.append(y)
        sub.append(before)
    
    
    for s in sub:
        value = []
        getfreq = {}

        #menghitung counter decission
        for jj in s:
            getfreq[jj] = s.count(jj)
        
        #memecah data array ke value[]
        for ss in s:
            for h in header[0]:
                if ss == h:
                    value.append(ss)
        #menjadikannya kelompok
        kelompok.append({
            'nama':s[len(s)-2],
            'header':value,
            'Sangat setuju':getfreq.get('Sangat Setuju'),
            'setuju':getfreq.get('Setuju'),
            'Tidak setuju':getfreq.get('Tidak Setuju'),
            'Sangat tidak setuju':getfreq.get('Sangat Tidak Setuju')
        })
    

    for k in kelompok:
        for head in k["header"]:
            #jika judul kurang dari 18, data tidak di input
            if len(head) <= 18:
                continue
                
            #proses masuk ke database
            layan = Layanan.objects.filter(layanan=head)
            if k['setuju'] != None:
                layan.update(setuju=layan[0].setuju + k['setuju'] )
            if k['Sangat setuju'] != None:
                layan.update(sangat_setuju=layan[0].sangat_setuju + k['Sangat setuju'])
            if  k['Tidak setuju'] != None:
                layan.update(tidak_setuju=layan[0].tidak_setuju + k['Tidak setuju'])
            if k['Sangat tidak setuju'] != None:
                layan.update(sangat_tidak_setuju=layan[0].sangat_tidak_setuju + k['Sangat tidak setuju'])

    context = {
        'cloudfreq':kelompok,
        'survey':list(spilt(survey, getrange)),
        'cloud':cloud,
        'nama':nama,
    }
    return JsonResponse({'contenxt':context}, safe=False)

def jsonchart(request, id):
    labels = []
    data = []
    chart = Layanan.objects.filter(csv=Csv.objects.get(id=id))
    for c in chart:
        sumdata = (c.sangat_setuju*2)+(c.setuju)-(c.tidak_setuju)-(c.sangat_tidak_setuju*2)
        if sumdata == 0:
            continue
        labels.append(c.layanan)
        data.append(sumdata)
    data = {
        'labels':labels,
        'data':data

    }
    return JsonResponse(data, safe=False)
def survey(request):
    finish = (False,)
    arrsurvey = []
    for x in Survey.objects.all():
        if request.user.is_authenticated:
            getrespon = Responden.objects.filter(user=User(email=request.user.email),Survey=x)
            finish = True if getrespon.count() != 0 else False,
        arrsurvey.append({
            'id':x.id,
            'name':x.name,
            'pertanyaan':SurveyQuestion.objects.filter(survey=x).count(),
            'responde': Responden.objects.filter(Survey=x).count(),
            'finish':finish[0],
            'berlangsung':x.isOpen
        })
    context = {
        'PDSI':PDSI,
        'title':'SURVEY',
        'active':3,
        'login': True if request.user.is_authenticated else False,
        'survey':arrsurvey
    }
    return render(request, 'user/survey.html', context)

def master(request):
    if not request.user.is_authenticated:
        if not User.objects.get(email=request.user.email).master:
            return redirect("home:index")
    if request.method == 'POST':
        Survey(name=request.POST['nama']).save()
        return redirect("home:master")
    arrsurvey = []
    for x in Survey.objects.all():
        arrsurvey.append({
            'id':x.id,
            'name':x.name,
            'pertanyaan':SurveyQuestion.objects.filter(survey=x).count(),
            'responde':Responden.objects.filter(Survey=x).count(),
            'berlangsung':x.isOpen
        })

    context = {
        'PDSI':PDSI,
        'title':'MASTER',
        'active':4,
        'survey':arrsurvey
    }
    return render(request, 'admin/master.html', context)

def editmaster(request,id):
    arrquest = []
    getsurvey = Survey.objects.get(id=id)
    if request.method == 'POST':
        if request.POST['action'] == "tambah":
            text = True if request.POST.get('isText') == "on" else False
            SurveyQuestion(survey=getsurvey ,name=request.POST['name'], isText=text, value=Question(id=request.POST['value'])).save()
            return redirect("../edit/"+str(id))
        elif request.POST['action'] == "edit":
            text = True if request.POST.get('editisText') == "on" else False
            SurveyQuestion.objects.filter(id=request.POST['id']).update(name=request.POST['editnama'], isText=text, value=Question(id=request.POST['editvalue']))
            return redirect("../edit/"+str(id))
    for i in SurveyQuestion.objects.filter(survey=getsurvey).order_by('-id'):
        respon = ResponSurvey.objects.filter(value=i)
        if respon.count() != 0:
            objrespon = {
                '1':0 if respon.filter(answer__value__contains=1).count() == 0 else int((respon.count()/respon.filter(answer__value__contains=1).count())*100),
                '2':0 if respon.filter(answer__value__contains=2).count() == 0 else int((respon.count()/respon.filter(answer__value__contains=2).count())*100),
                '3':0 if respon.filter(answer__value__contains=3).count() == 0 else int((respon.count()/respon.filter(answer__value__contains=3).count())*100),
                '4':0 if respon.filter(answer__value__contains=4).count() == 0 else int((respon.count()/respon.filter(answer__value__contains=4).count())*100),
                '5':0 if respon.filter(answer__value__contains=5).count() == 0 else int((respon.count()/respon.filter(answer__value__contains=5).count())*100),
            }
        else:
            objrespon = {'1':'20','2':'20','3':'20','4':'20','5':'20',}
        arrquest.append({
            'id':i.id,
            'name':i.name,
            'isText':i.isText,
            'value':i.value,
            'isfilled': True if respon.count() != 0 else False,
            'respon':objrespon,
        })
    context = {
        'survey':getsurvey,
        'question':arrquest,
        'answer':Question.objects.all()
    }
    return render(request, 'admin/editSurvey.html', context)

def masterdetail(request, id):

    label = []
    quest = SurveyQuestion.objects.get(id=id)
    for l in QuestionValue.objects.filter(question=quest.value):
        label.append(l.name)
    respon = ResponSurvey.objects.filter(value=quest)
    data = [
        respon.filter(answer__value__contains=1).count(),
        respon.filter(answer__value__contains=2).count(),
        respon.filter(answer__value__contains=3).count(),
        respon.filter(answer__value__contains=4).count(),
        respon.filter(answer__value__contains=5).count(),
    ]
    context = {
        'labels':label,
        'data':data,
        'respon':respon
    }
    return render(request, 'admin/detail.html', context)

def alljson(request):
    labels = []
    data = []
    for l in Survey.objects.all():
        labels.append(l.name)
        data.append(ResponSurvey.objects.aggregate(Avg('value')))
        
    # data = [1,2]
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
    }, safe=False)

def start(request,id):
    user = User.objects.get(email=request.user.email)
    getsurvey = Survey.objects.get(id=id)
    Responden.objects.get_or_create(user=user, Survey=getsurvey)
    arrsurvey = []
    for i in SurveyQuestion.objects.filter(survey=getsurvey):
        arrsurvey.append({
            'id':i.id,
            'text':i.isText,
            'name':i.name,
            'value':i.value.name,
            'answer':QuestionValue.objects.filter(question=i.value)
        })
    if request.method == 'POST':
        usersurvey = Responden.objects.filter(user=user, Survey=getsurvey)
        for x in arrsurvey:
            if x['text'] == True:
                ResponSurvey(respond=usersurvey[0],value=SurveyQuestion(id=x['id']),text=request.POST['text'+str(x['id'])]).save()
            else:
                ResponSurvey(respond=usersurvey[0], value=SurveyQuestion(id=x['id']), answer=QuestionValue(id=request.POST['answer'+str(x['id'])])).save()
        return redirect("home:survey")
        
    context = {
        'title':"survey",
        'survey':getsurvey,
        'question':arrsurvey,
        'answer':Question.objects.all()
    }
    return render(request, 'user/start.html', context)

def delete(request,act, id):
    if act == "survey":
        Survey(id).delete()
        return redirect("home:master")

@csrf_exempt
def editjson(request, id):
    survey = SurveyQuestion.objects.get(id=id)
    value = []
    for x in Question.objects.all():
        value.append({
            'id':x.id,
            'name':x.name
        })
    context = {
        'id':survey.id,
        'name':survey.name,
        'isText':survey.isText,
        'value':survey.value.name,
        'valueid':survey.value.id
    }
    
    return JsonResponse({'context':context, 'value':value}, safe=False) 