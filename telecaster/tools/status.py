#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
   TeleCaster

   Copyright (c) 2006-2012 Guillaume Pellerin <yomguy@altern.org>

# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".

# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.

# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.

# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

# Author: Guillaume Pellerin <yomguy@parisson.com>
"""

import os
from telecaster.tools import *
from django.conf import settings


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
