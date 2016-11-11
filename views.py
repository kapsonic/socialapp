from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from .api import *
import json
# Create your views here.
# 

		
def _getHost():
	host = "https://app.liveensure.com/live-identity"
	if(hasattr(settings, "LIVE_ENSURE") and settings.LIVE_ENSURE["API_HOST"]):
		host = settings.LIVE_ENSURE["API_HOST"]

	return host

def _getMapKey(request):
	map_key = "NO_KEY"
	if(hasattr(settings, "LIVE_ENSURE") and "GOOGLE_MAP_KEY" in settings.LIVE_ENSURE):
		map_key = settings.LIVE_ENSURE["GOOGLE_MAP_KEY"]
	elif "map_key" in request.session:
		map_key = request.session['map_key']
	
	print 'map key', map_key
	return map_key

def createLiveObject(request):
	live = LiveEnsureApi(request.session["api_key"], request.session["api_password"], request.session["agent_id"], _getHost())

	return live

def admin(request):
	if(request.method == 'POST'):
		authType = request.POST['auth_type']
		request.session.clear()
		request.session['auth_type'] = request.POST['auth_type']

		if(authType == 'K'):
			request.session['question'] = request.POST['question']
			request.session['answer'] = request.POST['answer']
		elif(authType == 'L'):
			request.session['lat'] = request.POST['lat']
			request.session['lang'] = request.POST['lang']
		else:
			request.session['orientation'] = request.POST['orientation']
			request.session['touches'] = request.POST['touches']
	else:
		request.session['api_key'] = settings.LIVE_ENSURE["API_KEY"]
		request.session['api_password'] = settings.LIVE_ENSURE["API_PASSWORD"]
		request.session['agent_id'] = settings.LIVE_ENSURE["AGENT_ID"]
		print(request.session.keys())
	ctx = {
		"map_key": _getMapKey(request),
	}
	for i in request.session.keys():
		print(i , request.session[i])
		ctx[i] = request.session[i]
	return render(request, 'demosocial/base.html', ctx)

def home(request):
	return render(request, 'demosocial/social/home.html')

def chat(request):
	return render(request, 'demosocial/social/chat.html', {"username": request.session['username']})

def healthCareHome(request):
	return render(request, 'demosocial/healthcare/home.html')
	
def initSession(request):
	
	live = createLiveObject(request)
	# Call initSession to make call to api server and get the json
	# If None returned then this means unsuccessfull call
	print("Session starting for ", request.POST['email'])

	re = live.initSession(request.POST['email'])

	print(re)
	if(re is not None):
		request.session['username'] = request.POST['email'].split('@')[0]
		return HttpResponse(re, content_type="application/json")

def getCode(request):
	live = createLiveObject(request)
	re = live.getAuthObj("IMG", request.GET["sessionToken"])
	return HttpResponse(re)

def createChallenge(request):
	authType = request.session['auth_type'] if "auth_type" in request.session else ""
	live = createLiveObject(request)
	re = None
	if(authType == 'K'):
		re = live.addPromptChallenge(request.session['question'], request.session['answer'], request.POST['sessionToken'])
	elif(authType == 'L'):
		re = live.addLocationChallenge(request.session["lat"], request.session["lang"], 10, request.POST["sessionToken"])
	elif(authType == 'B'):
		re = live.addTouchChallenge(request.session['orientation'], request.session['touches'], request.POST['sessionToken'])
	else:
		return HttpResponse(json.dumps({"status": True}), content_type="application/json")

	return HttpResponse(re, content_type="application/json")

def pollStatus(request):
	live = createLiveObject(request)

	re = live.pollStatus(request.GET['sessionToken'])
	return HttpResponse(re, content_type="application/json")
