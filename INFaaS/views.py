import json

from django.shortcuts import render, render_to_response, redirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect

from model.user import UserManager
from bson import json_util


@csrf_protect
def render_page(request, page):
    user = request.session.get('user')
    if not user:
        return render(request, 'index.html')
    context = {}
    context['page'] = page
    template = "dashboard.html"
    return render(request, template, context)


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