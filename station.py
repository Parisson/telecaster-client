#!/usr/bin/python
# -*- coding: utf-8 -*-
# *-* coding: utf-8 *-*
"""
   telecaster

   Copyright (c) 2006-2010 Guillaume Pellerin <yomguy@parisson.org>

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
import shutil
import datetime
import time
import urllib
from tools import *
from mutagen.oggvorbis import OggVorbis
from mutagen.id3 import ID3, TIT2, TP1, TAL, TDA, TDAT, TDRC, TCO, COM
#import jack


class Conference:
    """A conference object including metadata"""

    def __init__(self, dict):
        self.dict = dict
        self.title = dict['title']
        self.department = dict['department']
        if '....' in self.department or self.department == '':
            self.department = 'Undefined'
        self.conference = dict['conference']
        if '....' in self.conference or self.conference == '':
            self.conference = 'Undefined'
        self.session = dict['session']
        self.professor = dict['professor']
        if '....' in self.professor or self.professor == '':
            self.professor = 'Undefined'
        self.comment = dict['comment']

    def get_info(self):
        return self.title, self.department, self.conference, self.session, self.professor, self.comment


class Station(Conference):
    """Control the Oddcastv3-jack thread which send audio data to the icecast server
    and the Streamripper thread which write audio on the hard disk"""

    def __init__(self, conf_file, conference_dict, lock_file):
        Conference.__init__(self, conference_dict)
        self.date = datetime.datetime.now().strftime("%Y")
        self.time = datetime.datetime.now().strftime("%x-%X")
        self.time_txt = self.time.replace('/','_').replace(':','_').replace(' ','_')
        self.conf = xml2dict(conf_file)
        self.lock_file = lock_file
        self.conf = self.conf['telecaster']
        self.user = os.get_login()
        self.user_dir = '/home/' + self.user + '.telecaster'
        self.url_ext = self.conf['infos']['url']
        self.media_dir = self.conf['media']['dir']
        self.host = self.conf['server']['host']
        self.port = self.conf['server']['port']
        self.rss_dir = self.conf['server']['rss']['dir']
        self.rss_file = 'telecaster.xml'
        self.password = self.conf['server']['sourcepassword']
        self.url_int = 'http://'+self.host+':'+self.port
        self.deefuzzer_default_conf_file = self.conf['server']['deefuzzer_dict']
        self.deefuzzer_user_file = self.user + os.sep + 'deefuzzer.xml'
        self.bitrate = self.conf['media']['bitrate']
        self.dict['Bitrate'] = str(self.bitrate) + ' kbps'
        self.ogg_quality = self.conf['media']['ogg_quality']
        self.format = self.conf['media']['format']
        self.channels = int(self.conf['media']['channels'])
        self.description = [self.title, self.department, self.conference, self.session, self.professor, self.comment]
        self.server_name = [self.title, self.department, self.conference]
        self.ServerDescription = clean_string('_-_'.join(self.description))
        self.ServerName = clean_string('_-_'.join(self.server_name))
        self.mount_point = '/' + clean_string(self.title) + '_-_' + \
                                 clean_string(self.department) + '_-_' + \
                                 clean_string(self.conference)
        self.filename = clean_string('_-_'.join(self.description[1:])) + '_-_' + self.time_txt + '.' + self.format
        self.output_dir = self.media_dir + os.sep + self.department + os.sep + self.date
        self.file_dir = self.output_dir + os.sep + self.ServerName
        self.uid = os.getuid()
        self.odd_pid = get_pid('^edcast_jack\ -n', self.uid)
        self.deefuzzer_pid = get_pid('deefuzzer', self.uid)
        self.new_title = clean_string('_-_'.join(self.server_name)+'_-_'+self.session+'_-_'+self.professor+'_-_'+self.comment)
        self.short_title = clean_string('_-_'.join(self.conference)+'_-_'+self.session+'_-_'+self.professor+'_-_'+self.comment)
        self.genre = 'Vocal'
        self.encoder = 'TeleCaster by Parisson'
        self.rsync_host = self.conf['server']['rsync_host']
        self.record = str_to_bool(self.conf['media']['record'])
        self.rec_dir = self.conf['media']['rec_dir']
        self.user = os.get_login()
        self.user_dir = '/home/' + self.user + '.telecaster'

        if not os.path.exists(self.media_dir):
            os.makedirs(self.media_dir)
        if not os.path.exists(self.rec_dir):
            os.makedirs(self.rec_dir)

        self.jack_inputs = []
        if 'jack' in self.conf:
            jack_inputs = self.conf['jack']['input']
            if len(jack_inputs) > 1:
                for jack_input in jack_inputs:
                    self.jack_inputs.append(jack_input['name'])
            else:
                self.jack_inputs.append(jack_inputs['name'])

    def set_deefuzzer_dict(self):
        conf_file = open(self.deefuzzer_default_conf_file,'r')
        xml_data = conf_file.read()
        deefuzzer_dict.close()
        deefuzzer_dict = xml2dict(xml_data)

        deefuzzer_dict['deefuzzer']['station']['infos']['short_name'] = self.mount_point
        deefuzzer_dict['deefuzzer']['station']['infos']['name'] = self.ServerName
        deefuzzer_dict['deefuzzer']['station']['infos']['description'] = self.ServerDescription.replace(' ','_')
        deefuzzer_dict['deefuzzer']['server']['host'] = self.host
        deefuzzer_dict['deefuzzer']['server']['port'] = self.port
        deefuzzer_dict['deefuzzer']['server']['password'] = self.password
        deefuzzer_dict['deefuzzer']['media']['bitrate'] = self.bitrate
        deefuzzer_dict['deefuzzer']['media']['voices'] = str(len(self.jack_inputs))
        deefuzzer_dict['deefuzzer']['record']['mode'] = '1'
        deefuzzer_dict['deefuzzer']['record']['dir'] = self.rec_dir
        deefuzzer_dict['deefuzzer']['relay']['mode'] = '1'

        deefuzzer_xml = dicttoxml(deefuzzer_dict)
        conf_file = open(self.deefuzzer_user_file,'w')
        conf_file.write(deefuzzer_xml)
        conf_file.close()

    def start_deefuzzer(self):
        #if not self.jack_inputs:
            #jack.attach('telecaster')
            #for jack_input in jack.get_ports():
                #if 'system' in jack_input and 'capture' in jack_input.split(':')[1] :
                    #self.jack_inputs.append(jack_input)
        #jack_ports = ' '.join(self.jack_inputs)

        command = 'deefuzzer ' + self.deefuzzer_user_file + ' &'
        os.system(command)
        self.set_lock()

    def set_lock(self):
        lock = open(self.lock_file,'w')
        lock_text = clean_string('_*_'.join(self.description))
        lock_text = lock_text.replace('\n','')
        lock.write(lock_text)
        lock.close()

    def del_lock(self):
        os.remove(self.lock_file)

    def stop_deefuzzer(self):
        if len(self.deefuzzer_pid) != 0:
            os.system('kill -9 '+self.deefuzzer_pid[0])

    def stop_rec(self):
        pass
        #if len(self.rip_pid) != 0:
            #os.system('kill -9 ' + self.rip_pid[0])
        #time.sleep(1)
        #date = datetime.datetime.now().strftime("%Y")
        #if os.path.exists(self.file_dir) and os.path.exists(self.file_dir + os.sep + 'incomplete'):
            #try:
                #shutil.move(self.file_dir+os.sep+'incomplete'+os.sep+' - .'+self.format, self.file_dir+os.sep)
                #os.rename(self.file_dir+os.sep+' - .'+self.format, self.file_dir+os.sep+self.filename)
                #shutil.rmtree(self.file_dir+os.sep+'incomplete'+os.sep)
            #except:
                #pass

    def mp3_convert(self):
        os.system('oggdec -o - '+ self.file_dir+os.sep+self.filename+' | lame -S -m m -h -b '+ self.bitrate + \
            ' --add-id3v2 --tt "'+ self.new_title + '" --ta "'+self.professor+'" --tl "'+self.title+'" --ty "'+self.date+ \
        '" --tg "'+self.genre+'" - ' + self.file_dir+os.sep+self.ServerDescription + '.mp3 &')

    def write_tags_ogg(self):
       file = self.file_dir + os.sep + self.filename
       if os.path.exists(file):
            audio = OggVorbis(file)
            audio['TITLE'] = self.new_title.decode('utf8')
            audio['ARTIST'] = self.professor.decode('utf8')
            audio['ALBUM'] = self.title.decode('utf8')
            audio['DATE'] = self.date.decode('utf8')
            audio['GENRE'] = self.genre.decode('utf8')
            audio['SOURCE'] = self.title.decode('utf8')
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
            audio.add(TAL(encoding=3, text=self.title.decode('utf8')))
            #tag = tags.__dict__['DATE']
            audio.add(TDRC(encoding=3, text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            #tag = tags.__dict__['GENRE']
            audio.add(TCO(encoding=3, text=self.genre.decode('utf8')))
            #tag = tags.__dict__['COMMENT']
            #audio.add(COM(encoding=3, text=self.comment))
            audio.save()
        time.sleep(1)

    def start(self):
        self.set_lock()
        self.set_deefuzzer_conf()
        self.start_deefuzzer()
        #self.update_rss()

    def stop(self):
        self.stop_rec()
        self.stop_deefuzzer()
        if self.format == 'ogg':
            self.write_tags_ogg()
        elif self.format == 'mp3':
            self.write_tags_mp3()
        self.del_lock()
        #self.mp3_convert()
        #self.rsync_out()

    def update_rss(self):
        rss_item_list = []
        if not os.path.exists(self.rss_dir):
            os.makedirs(self.rss_dir)

        time_now = datetime.datetime.now().strftime("%x-%X")

        media_description = '<table>'
        media_description_item = '<tr><td>%s:   </td><td><b>%s</b></td></tr>'
        for key in self.dict.keys():
            if self.dict[key] != '':
                media_description += media_description_item % (key.capitalize(), self.dict[key])
        media_description += '</table>'

        media_link = self.url_ext + '/rss/' + self.rss_file
        media_link = media_link.decode('utf-8')

        rss_item_list.append(RSSItem(
            title = self.ServerName,
            link = media_link,
            description = media_description,
            guid = Guid(media_link),
            pubDate = self.time_txt,)
            )

        rss = RSS2(title = self.title + ' - ' + self.department,
                            link = self.url_ext,
                            description = self.ServerDescription.decode('utf-8'),
                            lastBuildDate = str(time_now),
                            items = rss_item_list,)

        #f = open(self.rss_dir + os.sep + self.rss_file, 'w')
        #rss.write_xml(f, 'utf-8')
        #f.close()
