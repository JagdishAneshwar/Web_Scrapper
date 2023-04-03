
from bs4 import BeautifulSoup
import pandas as pd
import requests
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Tag, URLS, NavURLS
from .form import TagForm, URLForm, NavURLForm, DataForm


def home(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            existing_url = URLS.objects.filter(
                user=request.user, url=url).first()
            if not existing_url:
                new_url = URLS(user=request.user, url=url)
                new_url.save()
            lis = URLS.objects.filter(user=request.user)
            return render(request, 'home.html', {'lis': lis})
        lis = URLS.objects.filter(user=request.user)
        return render(request, 'home.html', {'lis': lis})
    else:
        lis = URLS.objects.filter(user=request.user)
        return render(request, 'home.html', {'lis': lis})


def tag(request, pk):
    url = get_object_or_404(URLS, pk=pk, user=request.user)
    if request.method == 'POST':
        tagform = TagForm(request.POST)
        form = NavURLForm(request.POST)
        if tagform.is_valid():
            title = tagform.cleaned_data['title']
            element = tagform.cleaned_data['element']
            attribute = tagform.cleaned_data['attribute']
            value = tagform.cleaned_data['value']
            existing_tag = Tag.objects.filter(
                user=url, title=title, element=element, attribute=attribute, value=value).first()
            if not existing_tag:
                new_tag = Tag(user=url, title=title, element=element,
                              attribute=attribute, value=value)
                new_tag.save()
        taglis = Tag.objects.filter(user=url)
        if form.is_valid():
            navurl = NavURLS()
            navurl.user = url
            navurl.navelement = form.cleaned_data['navelement']
            navurl.navattribute = form.cleaned_data['navattribute']
            navurl.navtitle = form.cleaned_data['navtitle']
            navurl.navvalue = form.cleaned_data['navvalue']
            navurl.save()

        navurllis = NavURLS.objects.filter(user=url)
        return render(request, 'tags.html', {'form': form, 'taglis': taglis, 'navurls': navurllis})
    else:
        navurllis = NavURLS.objects.all()
        taglis = Tag.objects.filter(user=url)
        return render(request, 'tags.html', {'taglis': taglis, 'navurls': navurllis})


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
                user = User.objects.create_user(
                    username=username, password=password1, email=email)
                user.save()
                user = auth.authenticate(username=username, password=password1)
                auth.login(request, user)
                return redirect('home.html')

        else:
            messages.info(request, "Password didn't match!!")
            return redirect('signup.html')

    else:
        return render(request, 'signup.html', {})


def delete_tag(request, item_id):
    if request.method == 'POST':
        dl = Tag.objects.get(pk=item_id)
        dl.delete()
        return redirect('/tags.html')


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


def result(request):
    form = DataForm()
    tag_results=[]
    if request.method == 'POST':
        form = DataForm(request.POST)
        user_url = URLS.objects.filter(user=request.user).first()
        nav_urls = NavURLS.objects.filter(user=user_url)
        if not user_url:
            return render(request, 'result.html', {'result_data': []})
        lis = Tag.objects.filter(user=user_url)
        if form.is_valid():
            raw = form.cleaned_data['raw']
            page = form.cleaned_data['page']
            format = form.cleaned_data['format']
            df = process(nav_urls, lis, raw, int(page), tag_results)
        else:
            df = process(nav_urls, lis, True, int(3), tag_results)
        html_table = df.to_html(index=False, escape=False, classes=["table"])
        return render(request, 'result.html', {'html_table': html_table, 'form': form})
    else:
        tag_results = Tag.objects.filter(user=request.user)
        df = pd.DataFrame(tag_results)
        html_table = df.to_html(index=False, escape=False, classes=["table"])
        return render(request, 'result.html', {'html_table': html_table, 'form': form})


def process(nav_urls, lis, raw_val, page_val,tag_results):
    col_name=[]
    for nav_url in nav_urls:
        for i in range(0, page_val):
            temp_results = []
            url = nav_url.navvalue
            last_digit_index = len(url) - url[::-1].index('1') - 1
            test_url = url[:last_digit_index] + \
				"{page_number}".format(page_number=i+1)
            try:
                 print(test_url)
                 page = requests.get(test_url)
                 soup = BeautifulSoup(page.content, 'html.parser')
            except Exception as e:
                 print(f"Error occurred while scraping page {i+1}: {e}")
            
            for tag in lis:
                 element = tag.element
                 attribute = tag.attribute
                 value = tag.value
                 col_name.append(tag.title)
                 if element == 'img':
                    img_list = [
						f"<img src='{img['src']}' />" for img in soup.find_all(element, {attribute: value})]
                    temp_results.append(img_list)
                 else:
                    text_list = soup.find_all(element, {attribute: value})
                    temp_results.append(text_list)
            tag_results.extend(zip(*temp_results))
    if raw_val == "True":
        df = pd.DataFrame(tag_results)
        df.columns = col_name[:3]
    else:
        df = pd.DataFrame(tag_results).dropna()
        df.columns = col_name[:3]
    return df


