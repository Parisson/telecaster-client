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
    help = "Make all station.started=False"
    admin_email = 'webmaster@parisson.com'

    def handle(self, *args, **options):
        stations = Station.objects.filter(started=True)
        for station in stations:
            station.started = False
            station.save()

