from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime, timedelta
from dateutil import tz, parser
from crawl.graph_helper import get_user
from crawl.auth_helper import get_sign_in_flow, get_token_from_code, store_user, remove_user_and_token, get_token
import yaml
import msal

def initialize_context(request):
    context = {}

    # Check for any errors in the session
    error = request.session.pop('flash_error', None)

    if error != None:
        context['errors'] = []
        context['errors'].append(error)

    # Check for user in the session
    context['user'] = request.session.get('user', {'is_authenticated': False})
    return context

def config(request):
    if request.method == 'POST' and request.FILES['configFile']:
        settings = request.FILES['configFile'].read()
        ySettings = yaml.load(settings.decode('utf-8'), Loader=yaml.FullLoader)
        ## print(ySettings['app_id'])

        return render(request, 'crawl/config.html', {'json': ySettings})
    return render(request, 'crawl/config.html')

def home(request):
    context = initialize_context(request)
    return render(request, 'crawl/home.html', context)

def sign_in(request):
    # Get the sign-in flow
    flow = get_sign_in_flow()
    # Save the expected flow so we can use it in the callback
    try:
        request.session['auth_flow'] = flow
    except Exception as e:
        print(e)
    # Redirect to the Azure sign-in page
    return HttpResponseRedirect(flow['auth_uri'])

def callback(request):
    # Make the token request
    result = get_token_from_code(request)
   
    #Get the user's profile
    user = get_user(result['access_token'])
    
    store_user(request, user)
    return HttpResponseRedirect(reverse('home'))

def sign_out(request):
    # Clear out the user and token
    remove_user_and_token(request)
    return HttpResponseRedirect(reverse('home'))

