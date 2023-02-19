
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Tag, URLS
from .form import TagForm, URLForm




def home(request):
	if request.method == 'POST':
		form = URLForm(request.POST)
		if form.is_valid():
			url = form.cleaned_data['url']
			existing_url = URLS.objects.filter(user=request.user, url=url).first()
			if not existing_url:
				new_url = URLS(user=request.user, url=url)
				new_url.save() 
			lis = URLS.objects.filter(user=request.user)
			return render(request, 'home.html', {'lis' : lis})
		lis = URLS.objects.filter(user=request.user)
		return render(request, 'home.html', {'lis' : lis})
	else:
		lis = URLS.objects.filter(user=request.user)
		return render(request, 'home.html', {'lis' : lis})

def tag(request, pk):
    url = get_object_or_404(URLS, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            element = form.cleaned_data['element']
            attribute = form.cleaned_data['attribute']
            value = form.cleaned_data['value']
            existing_tag = Tag.objects.filter(user=url, title=title, element=element, attribute=attribute, value=value).first()
            if not existing_tag:
                new_tag = Tag(user=url, title=title, element=element, attribute=attribute, value=value)
                new_tag.save() 
            lis = Tag.objects.filter(user=url)
            return render(request, 'tags.html', {'lis' : lis})
        lis = Tag.objects.filter(user=url)
        return render(request, 'tags.html', {'lis' : lis})
    else:
        lis = Tag.objects.filter(user=url)
        return render(request, 'tags.html', {'lis' : lis})



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


from django.shortcuts import render, get_object_or_404
import requests
import pandas as pd
from bs4 import BeautifulSoup


def result(request):
	if request.method == 'POST':
		user_url = URLS.objects.filter(user=request.user).first()
		if not user_url:
			# Handle the case where the user has not added any URL
			return render(request, 'result.html', {'result_data': []})
		lis = Tag.objects.filter(user=user_url)
		text_list = []
		img_list=[]
		tag_results=[]
		for tag in lis:
			element = tag.element
			attribute = tag.attribute
			value = tag.value
			page = requests.get(user_url.url)
			soup = BeautifulSoup(page.content, 'html.parser')
			
			if element == 'img':
				# Handle image tags separately
				img_list = [f"<img src='{img['src']}' />" for img in soup.find_all(element, {attribute: value})]
				tag_results.append(img_list)
			else:
				text_list = soup.find_all(element, {attribute: value})
				tag_results.append(text_list)

		# Here you can process the tag_result_data as per your requirement
		df = pd.DataFrame(tag_results).T
		html_table = df.to_html(index=False, escape=False, classes=["table"])
		return render(request, 'result.html', {'html_table': html_table})
	else:
		tag_results = Tag.objects.filter(user=request.user)
		df = pd.DataFrame(tag_results).T
		html_table = df.to_html(index=False, escape=False, classes=["table"])
		return render(request, 'result.html', {'html_table': html_table})

