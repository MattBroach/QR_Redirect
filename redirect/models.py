import os
import uuid
from tempfile import NamedTemporaryFile
import qrcode

from django.db import models
from django.db.models.signals import post_delete
from django.conf import settings
from django.contrib.sites.models import Site


class Redirect(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference_id = models.PositiveSmallIntegerField()

    qr_code = models.ImageField(blank=True, upload_to='qr/')

    @property 
    def qr_link(self):
        domain = Site.objects.get_current().domain
        protocol = 'https://' if settings.USE_SSL else 'http://'

        return protocol + domain + '/redirect/go/' + str(self.id) + '/'

    def __str__(self):
        return settings.LINK_BASE.format(self.reference_id)

    @classmethod
    def new_from_link_id(cls, link_id):
        """
        Create a new Redirect object from a given 'id'
        Also creates and saves the corresponding QR code
        """
        # get base filepath info
        u = uuid.uuid4()
        base_file = os.path.join('png', str(u) + '.png')
        filepath = os.path.join(settings.MEDIA_ROOT, base_file)

        # Make the requisite folder, if it doesn't exist
        folder = os.path.join(settings.MEDIA_ROOT, 'png')
        if not os.path.exists(folder):
            os.makedirs(folder)

        # create Redirect object
        redirect = cls(id=u,
                       reference_id=link_id,
                       qr_code=base_file)

        # create and save associated QR image
        qr = qrcode.make(redirect.qr_link)
        qr.save(filepath)
        redirect.save()

        return redirect


# remove related QR file after delete
def qr_file_remove(sender, instance, *args, **kwargs):
    os.remove(instance.qr_code.path)

post_delete.connect(qr_file_remove, sender=Redirect)
