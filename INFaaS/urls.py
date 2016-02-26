"""rainbow_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin

from INFaaS import views, apis

urlpatterns = [
    # Admin Console
    url(r'^admin/', include(admin.site.urls)),

    # INFaaS APIs (CaaS)
    url(r'^api/domains$', apis.handle_domains_mgt),
    url(r'^api/solutions$', apis.handle_solutions_mgt),
    url(r'^api/users$', apis.handle_users_mgt),
    url(r'^api/infer$', apis.infer),
    url(r'^api/hello', apis.hello),

    # INFaaS Console (SaaS)
    url(r'^domain/?$', views.render_page, {"pagename": "domain"}),
    url(r'^solution/?$', views.render_page, {"pagename": "solution"}),
    url(r'^inference/?$', views.render_page, {"pagename": "inference"}),
    url(r'^login/?$', views.login),
    url(r'^logout/?$', views.logout),
    url(r'^domain/mgt?$', views.handle_domains_mgt),
    url(r'^solution/mgt?$', views.handle_solutions_mgt),
    url(r'^$', views.render_page, {"pagename": "index"}),
    url(r'^(?P<page>\w+)$', views.render_page),
]
