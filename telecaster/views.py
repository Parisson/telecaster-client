# Create your views here.

import os
import datetime
import time
import string

from tools import *
from models import *
from forms import*

from jsonrpc import jsonrpc_method

from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.template import RequestContext, loader
from django import template
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.views.generic import list_detail
from django.conf import settings
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.context_processors import csrf
from django.forms.models import modelformset_factory, inlineformset_factory
from django.contrib.auth.models import User
from django.utils.translation import ugettext
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ObjectDoesNotExist


def render(request, template, data = None, mimetype = None):
    return render_to_response(template, data, context_instance=RequestContext(request),
                              mimetype=mimetype)

def get_host(request):
    host = request.META['HTTP_HOST']
    if ':' in host:
        host = host.split(':')[0]
    return host

status = Status()

class StatusView(object):

    @jsonrpc_method('telecaster.get_server_status')
    def get_server_status(request):
        status.update()
        return status.to_dict()

    @jsonrpc_method('telecaster.get_station_status')
    def get_station_status(request):
        stations = Station.objects.filter(started=True)
        if stations:
            station = stations[0].to_dict()
        else:
            station = {}
        return station

    @jsonrpc_method('telecaster.start')
    def start(request, station_dict):
        pass

    @jsonrpc_method('telecaster.stop')
    def stop(request):
        pass
