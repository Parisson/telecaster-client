# Create your views here.

import os
import datetime
import time
import string

from tools import *
from models import *
from forms import*

from jsonrpc import jsonrpc_method
from jsonrpc.proxy import ServiceProxy

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


class Status(object):

    interfaces = ['eth0', 'eth1', 'eth2', 'eth0-eth2', 'eth3', 'eth4', 'eth5',
                  'eth6', 'eth7', 'eth8', 'eth9', 'eno0', 'eno1',
                  'wlan0', 'wlan1', 'wlan2', 'wlan3', 'wlan4']
    
    acpi_states = {0: 'battery', 1: 'battery', 2: 'AC'}

    def __init__(self):
        self.acpi = acpi.Acpi()
        self.uid = os.getuid()
        self.user = pwd.getpwuid(os.getuid())[0]
        self.cache = settings.MEDIA_ROOT + 'cache/'
        self.monitoring_conf_dir = '/etc/telecaster/deefuzzer/'
        self.mp3_monitoring_conf = self.monitoring_conf_dir + 'telecaster_mp3_monitor.yaml'
        self.webm_monitoring_conf = self.monitoring_conf_dir + 'telecaster_webm_monitor.yaml'
        self.mp3_streaming_conf = self.cache + 'station_mp3.xml'
        self.webm_streaming_conf = self.cache + 'station_webm.xml'

    def update(self):
        self.acpi.update()
        try:
            self.temperature = self.acpi.temperature(0)
        except:
            self.temperature = 'N/A'
        self.get_pids()
        self.get_hosts()

    def to_dict(self):
        status = [
          {'id': 'name', 'class': 'default', 'value': self.name, 'label': 'Name'},
          {'id': 'ip', 'class': 'default', 'value': self.ip, 'label': 'IP address'},
          {'id': 'acpi_state','class': 'default', 'value': 'AC', 'label': 'Power'},
          {'id': 'acpi_percent', 'class': 'default', 'value': str(self.acpi.percent()), 'label': 'Charge (%)'},
          {'id': 'temperature', 'class': 'default', 'value': self.temperature, 'label': 'Temperature'},
          {'id': 'jackd', 'class': 'default', 'value': self.jacking, 'label': 'Jack server'},
          {'id': 'audio_encoding','class': 'default',
                'value': self.audio_encoding, 'label': 'Audio encoding'},
          {'id': 'video_encoding','class': 'default',
                'value': self.video_encoding, 'label': 'Video encoding'},
          {'id': 'audio_monitoring', 'class': 'default',
                'value': self.audio_monitoring, 'label': 'Audio monitoring'},
          {'id': 'video_monitoring', 'class': 'default',
                'value': self.video_monitoring, 'label': 'Video monitoring'},
          {'id': 'audio_streaming', 'class': 'default',
                'value': self.audio_streaming, 'label': 'Audio streaming'},
          {'id': 'video_streaming', 'class': 'default',
                'value': self.video_streaming, 'label': 'Video streaming'},
          ]

        for stat in status:
            if stat['value'] == False or stat['value'] == 'localhost' or stat['value'] == 'battery':
                stat['class'] = 'warning'

        return status

    def get_hosts(self):
        ip = ''
        for interface in self.interfaces:
            try:
                ip = get_ip_address(interface)
                if ip:
                    self.ip = ip
                    break
            except:
                self.ip = '127.0.0.1'
        self.url = 'http://' + self.ip
        self.name = get_hostname()

    def get_pids(self):
        self.jacking = get_pid('jackd', args=False) != None

        self.audio_encoding = get_pid('gst-launch-1.0', args='lamemp3enc') != None
        self.video_encoding = get_pid('gst-launch-1.0', args='vp8enc') != None

        self.audio_monitoring = get_pid('deefuzzer', args=self.mp3_monitoring_conf) != None
        self.video_monitoring = get_pid('deefuzzer', args=self.webm_monitoring_conf) != None

        self.audio_streaming = get_pid('deefuzzer', args=self.mp3_streaming_conf) != None
        self.video_streaming = get_pid('deefuzzer', args=self.webm_streaming_conf) != None


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

status = Status()

