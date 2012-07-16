from optparse import make_option
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from telemeta.models import *
from telemeta.util.unaccent import unaccent
from teleforma.models import *
from telecaster.models import *
from telecaster.tools import *
import os

class Command(BaseCommand):
    help = "Synchronize local archives with backup server"
    admin_email = 'webmaster@parisson.com'
    archives = settings.MEDIA_ROOT
    server = settings.TELECASTER_RSYNC_SERVER
    log = settings.TELECASTER_RSYNC_LOG
    logger = Logger(log)
    command = 'rsync -aq '

    def handle(self, *args, **options):
        pid = get_pid('rsync')
        if not pid:
            stations = Station.objects.filter(started=True)
            ids = [station.public_id for station in stations]
            if ids:
                for id in ids:
                    self.command += '--exclude=%s ' % id
            self.command += self.archives + ' ' + self.server
            try:
                os.system(self.command)
                self.logger.write_info(self.command)
            except:
                self.logger.write_error('NOT rsynced')
