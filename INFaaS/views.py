'''
Author: Moon Kwon Kim <mkdmkk@gmail.com>
'''
from django.shortcuts import render_to_response
from django.template.context import Context

import sourceman.views as sourceman


def render(request, page):
    context = Context()
    context['page'] = page
    template = "index.html"
    if page == 'user':
        template = "user/index.html"
    elif page == 'context':
        template = "context/index.html"
    elif page == 'solution':
        template = "solution/index.html"
    elif page == 'source':
        context['sources'] = sourceman.crud('r')
        template = "source/index.html"
    elif page == 'dashboard':
        pass

    return render_to_response(template, context)
