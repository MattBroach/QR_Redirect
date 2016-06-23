from shutil import rmtree
import os
import qrcode
from qrcode.image.svg import SvgFragmentImage

from django.conf import settings

from redirect.models import Redirect


def publish_qr(image_type, folder_name=None):
    assert image_type is 'svg' or image_type is 'png', (
        "publish_qr must be passed either 'png' or 'svg'"
    )

    if folder_name is None:
        folder_name = image_type

    # Clean old folder, if it exists
    folder = os.path.join(settings.MEDIA_ROOT, folder_name)
    if os.path.exists(folder):
        rmtree(folder)
    os.makedirs(folder)

    # output svgs
    for redirect in Redirect.objects.all():
        qr = qrcode.make(redirect.qr_link) if image_type == 'png' else qrcode.make(redirect.qr_link, 
                                                                                   image_factory=SvgFragmentImage)
        qr.save(os.path.join(folder, str(redirect.id) + '.' + image_type))

    
