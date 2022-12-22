
from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.contrib import messages
import requests # pip install requests
from bs4 import BeautifulSoup as bs # pip install beautifulsoup4
import pandas as pd

# Create your views here.
def about(request):
    return render(request, 'base.html', {})   

def home(request):
    return render(request, 'home.html', {})

def signup(request):
    if request.method == 'POST':
        username = request.POST['name']
        password1 = request.POST['pwd']
        password2 = request.POST['pwd2']
        email = request.POST['email']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username is Already Taken!!")
                return redirect('signup.html')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email)
                user.save()
                user = auth.authenticate(username=username, password=password1)
                auth.login(request, user)
                return redirect('home.html')

        else:
            messages.info(request, "Password didn't match!!")
            return redirect('signup.html')

    else:
        return render(request, 'signup.html', {})

def login(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pwd']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home.html')
        else:
            messages.info(request, "Password or Username Is Wrong!!")
            return redirect('login.html')
    else:
        return render(request, 'login.html', {})

data=[]
raw_data=[]
raw=[]
def result(request):
    if request.method == 'POST':
        URL = request.POST.get('url_pattern')
        element = request.POST.get('element_dropdown')
        attribute = request.POST.get('attr_dropdown')
        value = request.POST.get('value')

        if len(tags) == 0:
            tags.append([element, attribute, value])
            r = requests.get(URL)
            soup = bs(r.content)
            new_list = [d for d in tags if None not in d]
            print("new_list", new_list)
            for i in range(len(new_list)):
                #print(new_list[i])
                if new_list[i][0] == "img":
                    img_temp=soup.find_all(new_list[i][0], attrs={new_list[i][1]: new_list[i][2]})
                    img_list=[link["src"] for link in img_temp]
                    #print(img_temp)
                else:
                    raw_data.append(soup.find_all(new_list[i][0], attrs={new_list[i][1]: new_list[i][2]}))
                #print("raw_data", raw_data)
            for el in range(len(raw_data)):
                raw_data[el]
                temp=[]
                for product in raw_data[el]:
                        temp.insert(el, product.get_text())
                raw.append(temp)
            for i in range(len(new_list)):
                if new_list[i][0] == "img":
                    raw.append(img_list)
            #print("raw", raw)
            df = pd.DataFrame(raw).T
            df.drop(df.columns[[0, 1]], axis=1, inplace=True)
            html_table=df.to_html(index=False, classes=["table"])
            #print(html_table)
            return render(request, 'result.html', {"data":html_table})
        elif len(tags) != 0:
            if element != tags[-1][0] and attribute != tags[-1][1] and value != tags[-1][2]:
                tags.append([element, attribute, value])
                r = requests.get(URL)
                soup = bs(r.content)
                new_list = [d for d in tags if None not in d]
                print("new_list", new_list)
                for i in range(len(new_list)):
                    if new_list[i][0] == "img":
                        img_temp=soup.find_all(new_list[i][0], attrs={new_list[i][1]: new_list[i][2]})
                        img_list=[link["src"] for link in img_temp]
                        #print(img_temp)
                    else:
                        raw_data.append(soup.find_all(new_list[i][0], attrs={new_list[i][1]: new_list[i][2]}))
                        #print("raw_data", raw_data)
                for el in range(len(raw_data)):
                    raw_data[el]
                    temp=[]
                    for product in raw_data[el]:
                            temp.insert(el, product.get_text())
                    raw.append(temp)
                for i in range(len(new_list)):
                    if new_list[i][0] == "img":
                        raw.append(img_list)
                #print("raw", raw)
                df = pd.DataFrame(raw).T
                df.drop(df.columns[[0, 1]], axis=1, inplace=True)
                html_table=df.to_html(index=False, classes=["table"])
                #print(html_table)
                return render(request, 'result.html', {"data":html_table})
            else:
                return render(request, 'result.html', {"data":html_table})
        return render(request, 'result.html', {"data":html_table})
    else:
        return render(request, 'result.html', {})

tags=[]
def create_tag(request):
    if request.method == 'POST':
        element = request.POST.get('element_dropdown')
        attribute = request.POST.get('attr_dropdown')
        value = request.POST.get('value')
        #print(len(tags))
        if len(tags) == 0:
            tags.append([element, attribute, value])
            #print(tags)
            return render(request, 'home.html', {'tags':tags})
        elif len(tags) != 0:
            if element != tags[-1][0] and attribute != tags[-1][1] and value != tags[-1][2]:
                tags.append([element, attribute, value])
#print(tags)
                return render(request, 'home.html', {'tags':tags})
            else:
                return render(request, 'home.html', {'tags':tags})

        return render(request, 'home.html', {})
    else:
        return render(request, 'home.html', {})
