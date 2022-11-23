from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from alpha.admin import UserCreationForm as Form
from django.urls import reverse
from django.views import View
from alpha.models import warehouse,People,inwarehouse
from urllib.request import urlopen
import json
from datetime import datetime,timedelta
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request,'alpha/index.html')

@csrf_exempt
def indata(request):
    if request.method=="POST":
        x=json.loads(request.body.decode())
        ware_ins=warehouse.objects.get(pk=x["warehouse"])
        n=inwarehouse(warehouse=ware_ins,temperature=x["temperature"],humidity=x["humidity"],dateandtime=datetime.now())
        n.save()
        return HttpResponse(datetime.now())
    else:
        return HttpResponse("YOU HAVE USED GET METHOD")


class dashboard(LoginRequiredMixin,View):

    def get(self,request):
        today=datetime.now()
        ttime=str(today.time()).split('.')[0]
        tomorrow=today+timedelta(1)
        today=today.date()
        tomorrow=tomorrow.date()
        x = People.objects.get(id=request.user.id).warehouse_set.all()
        l=[]
        alert=[]
        for j in x:
            d={}
            d["name"]=j.name
            d["id"]=j.id
            d["pincode"]=j.pincode
            d["countrycode"]=j.countrycode
            d["id"]=j.id
            try:
                lat_updt=inwarehouse.objects.filter(warehouse_id=j.id).order_by('id')[::-1][0]
                d["iw"]={"temperature":lat_updt.temperature,"humidity":lat_updt.humidity,"updated":lat_updt.dateandtime}
                print(d["iw"])
            except:
                d["iw"]={"temperature":None,"humidity":None,"updated":None}


            response=urlopen("http://api.openweathermap.org/data/2.5/weather?zip={},IN&appid=710833e8507eaccc99e34ceaf6d24884".format(j.pincode))
            data=json.loads(response.read())
            d["cw"]={"weather":data["weather"][0]["description"],"temp":"{:.2f}".format(data["main"]["temp"]-273.15),"humidity":"{:.2f}".format(data["main"]["humidity"]),"wind_speed":"{:.2f}".format(data["wind"]["speed"])}

            if float(d["cw"]["temp"])>40 or float(d["cw"]["temp"])<0:
                alert.append([j.name,j.pincode,today,ttime,"temperature",d["cw"]["temp"]])
            elif float(d["cw"]["humidity"])>0:
                alert.append([j.name,j.pincode,str(today),ttime,"humidity",d["cw"]["humidity"]])

            response=urlopen("http://api.openweathermap.org/data/2.5/forecast?zip={},IN&appid=710833e8507eaccc99e34ceaf6d24884".format(j.pincode))
            data=json.loads(response.read())

            tw_weather=[]
            tw_temp=0
            tw_humidity=0
            tw_wind_speed=0

            for i in data['list']:
                iter=datetime.fromtimestamp(i['dt'])
                if iter.date()==today:
                    continue
                elif iter.date()==tomorrow:

                    tw_weather.append(i['weather'][0]["description"])
                    tw_temp+=i["main"]["temp"]-273.15
                    tw_humidity+=i["main"]["humidity"]
                    tw_wind_speed+=i["wind"]["speed"]
                    if i["main"]["temp"]-273.15>40 or i["main"]["temp"]<0:
                        alert.append([j.name,j.pincode,str(iter.date()),str(iter.time()),"temperature",i["main"]["temp"]])
                    elif i["main"]["humidity"]>0:
                        alert.append([j.name,j.pincode,str(iter.date()),str(iter.time()),"humidity",i["main"]["humidity"]])
                    continue
                break

            tw_weather_str=" & ".join(set(tw_weather))
            d["tw"]={"weather":tw_weather_str,"temp":"{:.2f}".format(tw_temp/8),"humidity":"{:.2f}".format(tw_humidity/8),"wind_speed":"{:.2f}".format(tw_wind_speed/8)}

            l.append(d)


        ctx={'warehouse_list':l,"alert":alert}

        return render(request,'alpha/dashboard.html',ctx)


class createwarehouse(LoginRequiredMixin,CreateView):
    model = warehouse
    fields = ['name','pincode']
    template_name = 'alpha/warehouse.html'


    def form_valid(self, form):
        object = form.save(commit=False)
        object.countrycode='IN'
        x=super(createwarehouse,self).form_valid(form)
        print(x)
        if x:
            object.people.add(self.request.user.id)
        return x

class editwarehouse(LoginRequiredMixin,UpdateView):
    model = warehouse
    fields = ['name','pincode']
    template_name = 'alpha/warehouse.html'

class deletewarehouse(LoginRequiredMixin,DeleteView):
    model = warehouse
    template_name = 'alpha/warehouse_delete.html'

class createuser(View):
    def get(self, request):
        form=Form()
        ctx={'form':form}
        return render(request,'alpha/createuser.html',ctx)

    def post(self, request) :
        form = Form(request.POST)
        if not form.is_valid() :
            ctx = {'form' : form}
            return render(request, 'alpha/createuser.html', ctx)

        alpha = form.save()
        x = reverse('alpha:index')
        return redirect(x)
