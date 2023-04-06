
from bs4 import BeautifulSoup
import pandas as pd
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Tag, URLS, NavURLS
import io
from django.http import HttpResponse
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
        return render(request, 'tags.html', {'form': form, 'taglis': taglis, 'navurls': navurllis, 'pk':pk})
    else:
        form = NavURLForm()
        navurllis = NavURLS.objects.filter(user=url)
        taglis = Tag.objects.filter(user=url)
        return render(request, 'tags.html', {'form': form, 'taglis': taglis, 'navurls': navurllis, 'pk':pk})


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
    url = get_object_or_404(URLS, pk=item_id, user=request.user)
    if request.method == 'POST':
        form = NavURLForm()
        dl = Tag.objects.get(pk=item_id)
        dl.delete()
        taglis = Tag.objects.filter(user=url)
        navurllis = NavURLS.objects.filter(user=url)
        return render(request, 'tags.html', {'form': form, 'taglis': taglis, 'navurls': navurllis, 'pk':item_id})


def delete_navurl(request, item_id):
    url = get_object_or_404(URLS, pk=item_id, user=request.user)
    if request.method == 'POST':
        dl = NavURLS.objects.get(pk=item_id)
        dl.delete()
        taglis = Tag.objects.filter(user=url)
        navurllis = NavURLS.objects.filter(user=url)
        return render(request, 'tags.html', {'form': form, 'taglis': taglis, 'navurls': navurllis, 'pk':item_id})


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


def result(request, pk):
    form = DataForm()
    tag_results=[]
    url = get_object_or_404(URLS, pk=pk, user=request.user)
    if request.method == 'POST':
        form = DataForm(request.POST)
        nav_urls = NavURLS.objects.filter(user=url)
        if not url:
            return render(request, 'result.html', {'result_data': []})
        lis = Tag.objects.filter(user=url)
        if form.is_valid():
            page = form.cleaned_data['page']
            if nav_urls.exists():
                if page:
                    df = process(nav_urls, lis, int(page), tag_results, url)
                else:
                    df = process(nav_urls, lis, int(3), tag_results, url)
            else:
                if page:
                    df = process('', lis, int(page), tag_results, url)
                else:
                    df = process('', lis, int(3), tag_results, url)
            html_table = df.to_html(index=False, escape=False, classes=["table table-light table-hover table-bordered p-2"])
            return render(request, 'result.html', {'html_table': html_table, 'form': form, 'pk':pk})
        df = process(nav_urls, lis, int(3), tag_results, url)
        html_table = df.to_html(index=False, escape=False, classes=["table table-light table-hover table-bordered p-2"])
        return render(request, 'result.html', {'html_table': html_table, 'form': form, 'pk':pk})
    else:
        tag_results = Tag.objects.filter(user=request.user)
        df = pd.DataFrame(tag_results)
        html_table = df.to_html(index=False, escape=False, classes=["table table-light table-hover table-bordered p-2"])
        return render(request, 'result.html', {'html_table': html_table, 'form': form, 'pk': pk})


def process(nav_urls, lis, page_val,tag_results, url):
    col_name=[]
    for tag in lis:
        col_name.append(tag.title)
        
    if nav_urls == '':
        page = requests.get(url.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        temp_results = []
        for tag in lis:
                element = tag.element
                attribute = tag.attribute
                value = tag.value
                if element == 'img':
                    img_list = [
                        f"<img src='{img['src']}' />" for img in soup.find_all(element, {attribute: value})]
                    temp_results.append(img_list)
                else:
                    text_list = soup.find_all(element, {attribute: value})
                    text_results = []
                    for text_elem in text_list:
                        text = text_elem.text.strip()
                        text_results.append(text)
                    temp_results.append(text_results)

        tag_results.extend(zip(*temp_results))
    else:

        for nav_url in nav_urls:
            for i in range(0, page_val):
                temp_results = []
                url = nav_url.navvalue
                last_digit_index = len(url) - url[::-1].index('1') - 1
                test_url = url[:last_digit_index] + \
                    "{page_number}".format(page_number=i+1)
                try:
                    
                    page = requests.get(test_url)
                    soup = BeautifulSoup(page.content, 'html.parser')
                except Exception as e:
                    print(f"Error occurred while scraping page {i+1}: {e}")
                for tag in lis:
                    element = tag.element
                    attribute = tag.attribute
                    value = tag.value
                    if element == 'img':
                        img_list = [
                            f"<img src='{img['src']}' />" for img in soup.find_all(element, {attribute: value})]
                        temp_results.append(img_list)
                    else:
                        text_list = soup.find_all(element, {attribute: value})
                        text_results = []
                        for text_elem in text_list:
                            text = text_elem.text.strip()
                            text_results.append(text)
                        temp_results.append(text_results)
                tag_results.extend(zip(*temp_results))
        
    df = pd.DataFrame(tag_results).dropna()
    print(col_name)
    df.columns=col_name
    return df

def download_csv(request, pk):
    url = get_object_or_404(URLS, pk=pk, user=request.user)
    nav_urls = NavURLS.objects.filter(user=url)
    lis = Tag.objects.filter(user=url)
    tag_results=[]
    df = process(nav_urls, lis, int(3), tag_results, url)
    format = request.POST.get('format')
    if format == 'json':
        json_file = io.StringIO()
        df.to_json(json_file, orient='records')
        response = HttpResponse(json_file.getvalue(), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{url.pk}.json"'
    else:
        csv_file = io.StringIO()
        df.to_csv(csv_file, index=False)
        response = HttpResponse(csv_file.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{url.pk}.csv"'

    return response



