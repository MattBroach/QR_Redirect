from django.core.management.base import BaseCommand

from redirect.management.publish import publish_qr


class Command(BaseCommand):
    help = ('Publish the current set of Redirect links to svg. '
            'WARNING: this will delete all old svg files. Ensure '
            'They are backed up if you want to save them.')

    def handle(self, *args, **kwargs):
        publish_qr('svg')
