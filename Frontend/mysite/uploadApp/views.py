from django.shortcuts import render,redirect
from .models import Video
from .forms import VideoForm
from django.template import RequestContext

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import os



def success(request):
	return render(request,'success.html')

def base(request):
	return render(request,'base.html')

def removeFile(request):
	name = request.GET.get('name', None)
	documents = Video.objects.all()
	for document in documents:
		name1=document.__str__().split('/')
		if name1[1] == name:
			document.delete()
	return render(request,'base.html')
	
def index(request):
    form= VideoForm(request.POST, request.FILES)
    if form.is_valid():
    	form.save()
    	print("Success")
    else:
    	print("Error")
    	form = VideoForm()
    return render(request, 'index.html',{'form':form},RequestContext(request))


@csrf_exempt
def test(request):

    print(request.POST.get('name'))

    return HttpResponse("WHATWHAT")
