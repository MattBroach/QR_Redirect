from django.core.management.base import BaseCommand

from token_consumer.handlers import api

from redirect.models import Redirect


class Command(BaseCommand):
    help = ('Ensure the proper number of redirect links is'
            'Populated and has the matching QR code')

    def handle(self, *args, **options):
        current_link_count = Redirect.objects.count()
        from django.conf import settings

        # If there are too many link objects, delete the extras
        if current_link_count > settings.LINK_COUNT:
            extra = Redirect.objects.all()[:current_link_count-settings.LINK_COUNT]
            for redirect in extra:
                redirect.delete()

        # Otherwise, add links until the appropriate number is stored
        elif current_link_count < settings.LINK_COUNT:
            untagged = api.get('/references/untagged/')

            while current_link_count < settings.LINK_COUNT:
                # Get the next link.  If out of links, raise RuntimeError
                try:
                    link = untagged.pop()
                except IndexError:
                    raise RuntimeError(
                        'Out of available/relevent links. Consider '
                        'Adding more eligible links in the Axiologue '
                        'servier or changing the `LINK_COUNT` in settings'
                    )

                # skip any reference that already has a redirect link
                if Redirect.objects.filter(reference_id=link['id']):
                    continue

                # Create QR code and associated Redirect object
                Redirect.new_from_link_id(link['id'])
                
                current_link_count += 1
