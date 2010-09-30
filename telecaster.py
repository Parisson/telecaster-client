#!/usr/bin/python
# -*- coding: utf-8 -*-
# *-* coding: utf-8 *-*
"""
   telecaster

   Copyright (c) 2006-2008 Guillaume Pellerin <yomguy@parisson.org>

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

version = '0.4.2'


import os
import pwd
import cgi
import cgitb
import time
from tools import *
from webview import *
from station import *
cgitb.enable()


class TeleCaster:
    """Manage the calls of Station and Webview to get the network and
    disk streams"""

    def __init__(self, conf_file):
        """Main function"""
        self.conf_file = conf_file
        conf_dict = xml2dict(self.conf_file)
        self.conf = conf_dict['telecaster']
        self.title = self.conf['infos']['name']
        self.log_file = self.conf['log']
        self.logger = Logger(self.log_file)
        self.uid = os.getuid()
        self.url = self.conf['infos']['url']
        self.user = pwd.getpwuid(os.getuid())[0]
        self.user_dir = '/home' + os.sep + self.user + os.sep + '.telecaster'
        if not os.path.exists(self.user_dir):
            os.makedirs(self.user_dir)
        self.lock_file = self.user_dir + os.sep + 'telecaster.lock'
        self.form = WebView(self.conf, version)

    def main(self):
        edcast_pid = get_pid('edcast_jack', self.uid)
        deefuzzer_pid = get_pid('/usr/bin/deefuzzer '+self.user_dir+os.sep+'deefuzzer.xml', self.uid)
        writing = edcast_pid != []
        casting = deefuzzer_pid != []

        if deefuzzer_pid == [] and self.form.has_key("action") and \
            self.form.has_key("department") and self.form.has_key("conference") and \
            self.form.has_key("professor") and self.form.has_key("comment") and \
            self.form["action"].value == "start":

            self.conference_dict = {'title': self.title,
                        'department': self.form.getfirst("department"),
                        'conference': self.form.getfirst("conference"),
                        'session': self.form.getfirst("session"),
                        'professor': self.form.getfirst("professor"),
                        'comment': self.form.getfirst("comment")}

            s = Station(self.conf_file, self.conference_dict, self.lock_file)
            s.start()
            self.logger.write_info('starting')
            time.sleep(2)
            self.main()

        elif deefuzzer_pid != [] and os.path.exists(self.lock_file) and not self.form.has_key("action"):
            self.conference_dict = get_conference_from_lock(self.lock_file)
            self.form.stop_form(self.conference_dict, writing, casting)
            self.logger.write_info('page stop')

        elif deefuzzer_pid and self.form.has_key("action") and self.form["action"].value == "stop":
            if os.path.exists(self.lock_file):
                self.conference_dict = get_conference_from_lock(self.lock_file)
            s = Station(self.conf_file, self.conference_dict, self.lock_file)
            s.stop()
            self.logger.write_info('stopping')
            time.sleep(1)
            self.main()

        elif deefuzzer_pid == []:
            self.form.start_form(writing, casting)
            self.logger.write_info('page start')


conf_file = '/etc/telecaster/telecaster.xml'

if __name__ == '__main__':
    t = TeleCaster(conf_file)
    t.main()

