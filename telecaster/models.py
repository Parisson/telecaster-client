#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
   telecaster

   Copyright (c) 2006-2011 Guillaume Pellerin <yomguy@parisson.com>

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
import pwd
import datetime
import time
import urllib2
import liblo

from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3, TIT2, TP1, TAL, TDA, TDAT, TDRC, TCO, COM

import django.db.models as models
from django.db.models import *
from django.forms import ModelForm, TextInput, Textarea
from django.utils.translation import ugettext_lazy as _

from south.modelsinspector import add_introspection_rules

from teleforma.models import Conference


from tools import *

app_label = 'telecaster'
spacer = '_-_'


class ShortTextField(models.TextField):

    def formfield(self, **kwargs):
         kwargs.update(
            {"widget": Textarea(attrs={'rows':4, 'cols':40})}
         )
         return super(ShortTextField, self).formfield(**kwargs)

add_introspection_rules([], ["^telecaster\.models\.ShortTextField"])


class OSC(Model):
    "OSC server"

    host               = CharField(_('host'), max_length=255)
    port               = IntegerField(_('port'))

    def __unicode__(self):
        return self.host + ':' + str(self.port)

    class Meta:
        db_table = app_label + '_' + 'osc'


class Station(Model):
    "Media streaming station"

    public_id         = CharField(_('public_id'), max_length=255)
    started           = BooleanField(_('started'))
    conference        = ForeignKey(Conference, related_name='station',
                                    verbose_name=_('conference'))
    pid               = IntegerField(_('pid'), blank=True, null=True)
    osc               = ManyToManyField(OSC, related_name="station",
                                    verbose_name=_('OSC'), blank=True, null=True)
    record_dir        = CharField(_('record directory'), max_length=255, blank=True)
    deefuzzer_file    = FileField(_('deefuzzer file'), upload_to='cache/',
                                   blank=True)
    format            = CharField(_('format'), max_length=100, blank=True)

    class Meta:
        db_table = app_label + '_' + 'station'
        ordering = ['-conference__date_begin']

    def __unicode__(self):
        return self.description

    def to_dict(self):
        return self.conference.to_dict()

    @property
    def description(self):
        return self.conference.description

    @property
    def slug(self):
        return self.conference.slug

    @property
    def date_added(self):
        return self.conference.date_added

    def setup(self, conf_file):
        self.course = self.conference.course
        self.department = self.course.department.name
        self.organization = self.course.department.organization.name
        self.mount_point = self.slug

        self.conf = xml2dict(conf_file)
        self.date = datetime.datetime.now().strftime("%Y")
        self.time = datetime.datetime.now().strftime("%x-%X")
        self.time_txt = self.time.replace('/','_').replace(':','_').replace(' ','_')

        self.uid = os.getuid()
        self.user = pwd.getpwuid(self.uid)[0]
        self.encoder = 'TeleCaster system by Parisson'
        self.save()

        self._stations = self.conf['deefuzzer']['station']
        if not isinstance(self._stations,list):
            self._stations = [self._stations]
        for station in self._stations:
            if station['control']['mode'] != '0':
                port = int(station['control']['port'])
                osc = OSC.objects.filter(port=port)
                if osc:
                    self.osc.add(osc[0])
                else:
                    self.osc.create(host='localhost', port=port)

    def deefuzzer_setup(self):
        self.output_dirs = []
        self.urls = []
        for station in self._stations:
            if station['record']['mode'] != '0':
                output_dir = station['record']['dir']
                if output_dir[-1] != os.sep:
                    output_dir += os.sep
                output_dir += os.sep.join([self.organization, self.department, self.date,
                                        self.course.code + spacer + self.conference.course_type.name,
                                        self.public_id
                                        ])
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                station['record']['dir'] = output_dir
                self.output_dir = output_dir
                self.record_dir = output_dir

            station['infos']['short_name'] = self.mount_point
            station['infos']['name'] = self.slug
            station['infos']['description'] = self.slug
            if self.conference.professor:
                station['relay']['author'] = unicode(self.conference.professor.user.username)
            else:
                station['relay']['author'] = 'None'

        #FIXME: only one format in deefuzzer conf file
        self.format = station['media']['format']
        self.deefuzzer_file = 'cache' + os.sep + 'station_' + \
                                        station['media']['format'] + '.xml'
        self.save()
        self.deefuzzer_xml = dicttoxml(self.conf)

    def deefuzzer_write_conf(self):
        conf_file = open(self.deefuzzer_file.path,'w')
        conf_file.write(self.deefuzzer_xml)
        conf_file.close()

    def deefuzzer_start(self):
        command = 'nohup /usr/local/bin/deefuzzer ' + self.deefuzzer_file.path + ' &'
        os.system(command)
        time.sleep(0.5)
        pid = get_pid('deefuzzer', args=self.deefuzzer_file.path)
        if pid:
            self.pid = pid

    def deefuzzer_stop(self):
        pid = get_pid('deefuzzer', args=self.deefuzzer_file.path)
        if pid == self.pid:
            os.system('kill -9 '+str(self.pid))
        else:
            if self.format == 'mp3':
                os.system('touch "' + self.record_dir + os.sep + 'mp3.tofix"')
            elif self.format == 'webm':
                os.system('touch "' + self.record_dir + os.sep + 'webm.tofix"')
            try:
                os.system('kill -9 '+str(self.pid))
            except:
                pass

    def rec_stop(self):
        for osc in self.osc.all():
            target = liblo.Address(int(osc.port))
            liblo.send(target, '/record', 0)

    def write_tags_ogg(self):
       file = self.file_dir + os.sep + self.filename
       if os.path.exists(file):
            audio = OggVorbis(file)
            audio['TITLE'] = self.new_title.decode('utf8')
            audio['ARTIST'] = self.professor.decode('utf8')
            audio['ALBUM'] = self.organization.decode('utf8')
            audio['DATE'] = self.date.decode('utf8')
            audio['GENRE'] = self.genre.decode('utf8')
            audio['SOURCE'] = self.organization.decode('utf8')
            audio['ENCODER'] = self.encoder.decode('utf8')
            audio['COMMENT'] = self.comment.decode('utf8')
            audio.save()

    def write_tags_mp3(self):
        file = self.file_dir + os.sep + self.filename
        if os.path.exists(file):
            os.system('mp3info -t "a" -a "a" '+file)
            audio = ID3(file)
            #tag = tags.__dict__['TITLE']
            audio.add(TIT2(encoding=3, text=self.new_title.decode('utf8')))
            #tag = tags.__dict__['ARTIST']
            audio.add(TP1(encoding=3, text=self.professor.decode('utf8')))
            #tag = tags.__dict__['ALBUM']
            audio.add(TAL(encoding=3, text=self.organization.decode('utf8')))
            #tag = tags.__dict__['DATE']
            audio.add(TDRC(encoding=3, text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            #tag = tags.__dict__['GENRE']
            audio.add(TCO(encoding=3, text=self.genre.decode('utf8')))
            #tag = tags.__dict__['COMMENT']
            #audio.add(COM(encoding=3, text=self.comment))
            audio.save()

    def get_snapshot(self):
        pass

    def start(self):
        self.started = True
        self.deefuzzer_setup()
        self.deefuzzer_write_conf()
        self.deefuzzer_start()
        self.save()

    def stop(self):
        self.started = False
        self.datetime_stop = datetime.datetime.now()
        self.rec_stop()
        self.deefuzzer_stop()
        self.save()


