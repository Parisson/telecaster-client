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

class WebView(object):

    hidden_fields = ['started', 'datetime_start', 'datetime_stop', 'public_id']

    def __init__(self, conf_file):
        self.uid = os.getuid()
        self.user = pwd.getpwuid(os.getuid())[0]
        self.user_dir = '/home' + os.sep + self.user + os.sep + '.telecaster'
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)
        self.conf_file = settings.TELECASTER_CONF
        conf_dict = xml2dict(self.conf_file)
        self.conf = conf_dict['telecaster']
        self.title = self.conf['infos']['name']
        self.log_file = self.conf['log']
        self.logger = Logger(self.log_file)
        self.url = self.conf['infos']['url']
        self.status = Status()

    def index(self, request):
        template = 'telecaster/index.html'
        stations = Station.objects.filter(started=True)
        if stations:
            messages.warning(request, 'A station is already started !')
        form = StationForm()
        return render(request, template, {'station': form, 'hidden_fields': self.hidden_fields,
                                            'host': self.get_host(request) })


    def get_host(self, request):
        host = request.META['HTTP_HOST']
        if ':' in host:
            host = host.split(':')[0]
        return host

    @jsonrpc_method('telecaster.get_server_status')
    def get_server_status(request):
        status = Status()
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
        if isinstance(station_dict, dict):
            station = Station(public_id=dict['public_id'])
            station.configure(station_dict)
            conf = xml2dict(settings.TELECASTER_CONF)
            conf = conf['telecaster']
            station.set_conf(conf)
            station.setup()
            station.start()
        else:
            messages.error(request, 'Bad station dictionary')

    @jsonrpc_method('telecaster.stop')
    def stop(request):
        stations = Station.objects.filter(started=True)
        for station in stations:
            station.stop()

