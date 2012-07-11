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
import urllib
import liblo

from tools import *

from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3, TIT2, TP1, TAL, TDA, TDAT, TDRC, TCO, COM

import django.db.models as models
from django.db.models import *
from django.forms import ModelForm, TextInput, Textarea
from django.utils.translation import ugettext_lazy as _

from south.modelsinspector import add_introspection_rules

from teleforma.models import *

app_label = 'telecaster'


class ShortTextField(models.TextField):

    def formfield(self, **kwargs):
         kwargs.update(
            {"widget": Textarea(attrs={'rows':4, 'cols':40})}
         )
         return super(ShortTextField, self).formfield(**kwargs)


add_introspection_rules([], ["^telecaster\.models\.ShortTextField"])


class Station(Model):

    public_id         = CharField(_('public_id'), max_length=255)
    started           = BooleanField(_('started'))
    conference        = ForeignKey(Conference, related_name='station', verbose_name=_('conference'))

    class Meta:
        db_table = app_label + '_' + 'station'

    def __unicode__(self):
        return self.description

    def to_dict(self):
        return self.conference.to_dict()

    @property
    def description(self):
        return self.conference.description

    def set_conf(self, conf):
        self.conf = conf

    def setup(self):
        self.date = datetime.datetime.now().strftime("%Y")
        self.time = datetime.datetime.now().strftime("%x-%X")
        self.time_txt = self.time.replace('/','_').replace(':','_').replace(' ','_')
        self.user = pwd.getpwuid(os.getuid())[0]
        self.user_dir = '/home' + os.sep + self.user + os.sep + '.telecaster'
        self.rec_dir = self.conf['media']['rec_dir']
        self.deefuzzer_default_conf_file = self.conf['deefuzzer']['conf']
        self.deefuzzer_user_file = self.user_dir + os.sep + 'deefuzzer.xml'
        self.bitrate = self.conf['media']['bitrate']
        self.record = str_to_bool(self.conf['media']['record'])
        self.rec_dir = self.conf['media']['rec_dir']
        self.play_dir = self.conf['media']['play_dir']
        self.ogg_quality = self.conf['media']['ogg_quality']
        self.format = self.conf['media']['format']
        self.channels = int(self.conf['media']['channels'])
        self.server_name = [self.organization, self.department, self.conference]
        self.ServerDescription = clean_string('-'.join(self.description))
        self.ServerName = clean_string('_-_'.join(self.server_name))
        self.mount_point = self.ServerName + '.' + self.format
        self.filename = clean_string('_-_'.join(self.description[1:])) + '-' + self.time_txt + '.' + self.format
        self.output_dir = self.rec_dir + os.sep + self.date + os.sep + self.department
        self.file_dir = self.output_dir + os.sep + self.ServerName
        self.uid = os.getuid()
        self.deefuzzer_pid = get_pid('/usr/bin/deefuzzer '+self.deefuzzer_user_file, self.uid)
        self.new_title = clean_string('-'.join(self.description))
        self.short_title = self.new_title
        self.genre = self.conf['infos']['genre']
        self.encoder = 'TeleCaster by Parisson'

        if not os.path.exists(self.file_dir):
            os.makedirs(self.file_dir)

        self.jack_inputs = []
        if 'jack' in self.conf:
            jack_inputs = self.conf['jack']['input']
            if len(jack_inputs) > 1:
                for jack_input in jack_inputs:
                    self.jack_inputs.append(jack_input['name'])
            else:
                self.jack_inputs.append(jack_inputs['name'])

        self.deefuzzer_dict = xml2dict(self.deefuzzer_default_conf_file)
        self.deefuzzer_osc_ports =  []
        self.server_ports = []

        for station in self.deefuzzer_dict['deefuzzer']['station']:
            if station['control']['mode'] == '1':
                self.deefuzzer_osc_ports.append(station['control']['port'])
                self.server_ports.append(station['server']['port'])
            if station['server']['host'] == 'localhost' or  station['server']['host'] == '127.0.0.1':
                self.conf['play_port'] = station['server']['port']
            else:
                self.conf['play_port'] = '8000'

    def deefuzzer_setup(self):
        i = 0
        for station in self.deefuzzer_dict['deefuzzer']['station']:
            station['infos']['short_name'] = self.mount_point
            station['infos']['name'] = self.ServerName
            station['infos']['description'] = self.ServerDescription.replace(' ','_')
            station['infos']['genre'] = self.genre
            station['media']['bitrate'] = self.bitrate
            station['media']['dir'] = self.play_dir
            station['media']['voices'] = str(len(self.jack_inputs))
            station['record']['dir'] = self.file_dir
            station['relay']['mode'] = '1'
            station['relay']['author'] = self.professor
            self.deefuzzer_dict['deefuzzer']['station'][i] = station
            i += 1
        self.deefuzzer_xml = dicttoxml(self.deefuzzer_dict)

    def deefuzzer_write_conf(self):
        conf_file = open(self.deefuzzer_user_file,'w')
        conf_file.write(self.deefuzzer_xml)
        conf_file.close()

    def deefuzzer_start(self):
        command = 'deefuzzer ' + self.deefuzzer_user_file + ' > /dev/null &'
        os.system(command)
        self.set_lock()

    def deefuzzer_stop(self):
        if len(self.deefuzzer_pid) != 0:
            os.system('kill -9 '+self.deefuzzer_pid[0])

    def rec_stop(self):
        if len(self.deefuzzer_pid) != 0:
            for port in self.deefuzzer_osc_ports:
                target = liblo.Address(int(port))
                liblo.send(target, '/record', 0)

    def mp3_convert(self):
        os.system('oggdec -o - '+ self.file_dir+os.sep+self.filename+' | lame -S -m m -h -b '+ self.bitrate + \
            ' --add-id3v2 --tt "'+ self.new_title + '" --ta "'+self.professor+'" --tl "'+self.organization+'" --ty "'+self.date+ \
            '" --tg "'+self.genre+'" - ' + self.file_dir+os.sep+self.ServerDescription + '.mp3 &')

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

    def start(self):
        self.started = True
        self.datetime_start = datetime.datetime.now()
#        self.deefuzzer_setup()
#        self.deefuzzer_write_conf()
#        self.deefuzzer_start()
        self.save()

    def stop(self):
        self.started = False
        self.datetime_stop = datetime.datetime.now()
#        self.rec_stop()
#        time.sleep(2)
#        self.deefuzzer_stop()
        self.save()

    def configure(self, dict):
        self.organization = dict['organization']
        self.department = dict['department']
        self.session = dict['session']
        self.professor = dict['professor']
        self.comment = dict['comment']
        self.save()


class Record(Model):

    station = ForeignKey(Station, related_name='records', verbose_name='station',
                         blank=True, null=True, on_delete=models.SET_NULL)
    datetime = DateTimeField(_('record_date'), auto_now=True)
    file = FileField(_('file'), upload_to='items/%Y/%m/%d')



