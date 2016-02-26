import json

import math
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from INFaaS import apis, constants
from model.domain import DomainManager
from model.user import UserManager
from bson import json_util


@csrf_protect
def render_page(request, pagename, context=None):
    user = request.session.get('user')
    if not user:
        return render(request, 'index.html')
    context = {} if not context else context
    context['pagename'] = pagename
    template = "dashboard.html"
    if pagename == 'index':
        template = "dashboard.html"
    elif pagename == 'domain':
        template = "domain.html"
        context['domains'] = DomainManager().get_domains()
        context['currpage'] = int(request.GET.get('currpage', 1))
        context['numpages'] = math.ceil(context['domains'].count()/10)
        if context['currpage'] > context['numpages']:
            context['currpage'] = context['numpages']
        baseidx = (context['currpage']-1)*10
        if context['numpages'] == 0:
            context['currpage_domains'] = []
            context['numpages'] += 1
        else:
            context['currpage_domains'] = context['domains'][baseidx:baseidx+10]
    elif pagename == 'solution':
        template = "solution.html"
    elif pagename == 'inference':
        template = "inference.html"
    return render(request, template, context)


@csrf_protect
def handle_domains_mgt(request):
    res = apis.handle_domains_mgt(request)
    return render_page(request, 'domain', {'res': res})


@csrf_protect
def handle_solutions_mgt(request):
    res = apis.handle_solutions_mgt(request)
    return render_page(request, 'solution', {'res': res})


@csrf_protect
def login(request):
    # Check if logged in
    if not request.session.get('user'):
        # Check email and password
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password:
            user = UserManager().get_user(email=email, password=password)
            if user:
                request.session['user'] = json.loads(json_util.dumps(user))
    return redirect('/')


@csrf_protect
def logout(request):
    if 'user' in request.session:
        del request.session['user']
    return render_page(request, 'index')
