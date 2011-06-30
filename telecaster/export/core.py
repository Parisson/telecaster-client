# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Parisson SARL
# Copyright (c) 2006-2007 Guillaume Pellerin <pellerin@parisson.com>
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# yo"u should have received as part of this distribution. The terms
# are also available at http://svn.parisson.org/telemeta/TelemetaLicense.
#
# Author: Guillaume Pellerin <pellerin@parisson.com>

import os
import re
import string
import subprocess
import mutagen
import export
import xml.dom.minidom
import xml.dom.ext

#from telemeta.core import *
from export import *
from tools import *

class ExporterCore:
    """Defines the main parts of the exporting tools :
    paths, formats, metadata..."""

    def __init__(self):
        self.source = ''
        self.collection = ''
        self.verbose = ''
        self.dest = ''
        self.metadata = []
        self.cache_dir = 'cache'
        self.buffer_size = 0xFFFF

    def set_cache_dir(self,path):
        self.cache_dir = path

    def normalize(self):
        """ Normalize the source and return its path """
        args = ''
        if self.verbose == '0':
            args = '-q'
        try:
            os.system('normalize-audio '+args+' "'+self.source+'"')
            return self.source
        except IOError:
            return 'Exporter error: Cannot normalize, path does not exist.'

    def check_md5_key(self):
        """ Check if the md5 key is OK and return a boolean """
        try:
            md5_log = os.popen4('md5sum -c "'+self.dest+ \
                                '" "'+self.dest+'.md5"')
            return 'OK' in md5_log.split(':')
        except IOError:
            return 'Exporter error: Cannot check the md5 key...'
    
    def get_file_info(self):
        """ Return the list of informations of the dest """
        return self.export.get_file_info()

    def get_wav_length_sec(self) :
        """ Return the length of the audio source file in seconds """
        try:
            file1, file2 = os.popen4('wavinfo "'+self.source+ \
                                     '" | grep wavDataSize')
            for line in file2.readlines():
                line_split = line.split(':')
                value = int(int(line_split[1])/(4*44100))
                return value
        except IOError:
            return 'Exporter error: Cannot get the wav length...'

    def compare_md5_key(self):
        """ Compare 2 files wih md5 method """
        in1, in2 = os.popen4('md5sum -b "'+self.source+'"')
        out1, out2 = os.popen4('md5sum -b "'+self.dest+'"')
        for line in in2.readlines():
            line1 = line.split('*')[0]
        for line in out2.readlines():
            line2 = line.split('*')[0]
        return line1 == line2

    def write_metadata_xml(self,path):
        doc = xml.dom.minidom.Document()
        root = doc.createElement('telemeta')
        doc.appendChild(root)
        for tag in self.metadata.keys() :
            value = self.metadata[tag]
            node = doc.createElement(tag)
            node.setAttribute('value', str(value))
            #node.setAttribute('type', get_type(value))
            root.appendChild(node)
        xml_file = open(path, "w")
        xml.dom.ext.PrettyPrint(doc, xml_file)
        xml_file.close()

    def pre_process(self, item_id, source, metadata, ext,
                    cache_dir, options=None):
        """ Pre processing : prepare the export path and return it"""
        self.item_id = str(item_id)
        self.source = source
        file_name = get_file_name(self.source)
        file_name_wo_ext, file_ext = split_file_name(file_name)
        self.cache_dir = cache_dir
        self.metadata = metadata
        #self.collection = self.metadata['Collection']
        #self.artist = self.metadata['Artist']
        #self.title = self.metadata['Title']

        # Normalize if demanded
        if not options is None:
            self.options = options
            if 'normalize' in self.options and \
                self.options['normalize'] == True:
                self.normalize()

        # Define the export directory
        self.ext = self.get_file_extension()
        export_dir = os.path.join(self.cache_dir,self.ext)

        if not os.path.exists(export_dir):
            export_dir_split = export_dir.split(os.sep)
            path = os.sep + export_dir_split[0]
            for _dir in export_dir_split[1:]:
                path = os.path.join(path,_dir)
                if not os.path.exists(path):
                    os.mkdir(path)
        else:
            path = export_dir

        # Set the target file
        target_file = self.item_id+'.'+self.ext
        dest = os.path.join(path,target_file)
        return dest

    def core_process(self, command, buffer_size, dest):
        """Encode and stream audio data through a generator"""
        
        __chunk = 0
        file_out = open(dest,'w')

        try:
            proc = subprocess.Popen(command,
                    shell = True,
                    bufsize = buffer_size,
                    stdin = subprocess.PIPE,
                    stdout = subprocess.PIPE,
                    close_fds = True)
        except:
            raise ExportProcessError('Command failure:', command, proc)
            

        # Core processing
        while True:
            __chunk = proc.stdout.read(buffer_size)
            status = proc.poll()
            if status != None and status != 0:
                raise ExportProcessError('Command failure:', command, proc)
            if len(__chunk) == 0:
                break
            yield __chunk
            file_out.write(__chunk)

        file_out.close()

    def post_process(self, item_id, source, metadata, ext, 
                     cache_dir, options=None):
        """ Post processing : write tags, print infos, etc..."""
        self.write_tags()
        if not options is None:
            if 'verbose' in self.options and self.options['verbose'] != '0':
                print self.dest
                print self.get_file_info()

