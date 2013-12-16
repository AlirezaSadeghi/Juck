# -*- coding: utf-8 -*-

import uuid
from PIL import Image
import os

from django.core.files.uploadedfile import SimpleUploadedFile
from cStringIO import StringIO
from django.db import models
from django.conf import settings


class JuckImage(models.Model):
    class Meta:
        verbose_name = u'عکس'
        verbose_name_plural = u'عکس‌ها'


    def __init__(self, *args, **kwargs):
        delete_root = ''
        if 'delete_root' in kwargs:
            delete_root = kwargs.pop('delete_root')
        if 'upload_root' in kwargs:
            self.upload_root = kwargs.pop('upload_root')

        if 'prev_image' in kwargs:
            prev_image = kwargs.pop('prev_image')
            if prev_image:
                self.remove_previous_image(prev_image, delete_root)
        super(JuckImage, self).__init__(*args, **kwargs)


    def remove_previous_image(self, image, root_path):
        if not root_path:
            return

        root_path = settings.UPLOAD_ROOT + '/' + root_path

        thumbnail = root_path + '/small_thumbnails/' + image.file_name
        main = root_path + '/uploads/' + image.file_name
        try:
            os.remove(thumbnail)
            os.remove(main)
        except Exception:
            pass

    def create_upload_path(self, filename):
        s = settings.UPLOAD_ROOT + '/' + '/'.join([(self.upload_root + "/uploads"), self.file_name])
        return s

    def create_small_thumbnail_upath(self, filename):
        return settings.UPLOAD_ROOT + '/' + '/'.join([(self.upload_root + "/small_thumbnails"), self.file_name])


    image = models.ImageField(upload_to=create_upload_path, verbose_name=u'عکس', max_length=250)
    file_name = models.CharField(max_length=60, verbose_name=u'نام عکس')
    size = models.IntegerField(verbose_name=u'حجم عکس')
    thumbnail = models.ImageField(upload_to=create_small_thumbnail_upath, editable=False, max_length=250)


    def create_picture(self, image):
        self.image = image
        self.size = self.image.size / 1000
        self.file_name = str(uuid.uuid4())[0:40] + '.png'
        self.save()


    def save(self, *args, **kwargs):
        self.image.seek(0)
        smallImage = Image.open(self.image)

        (width, height) = smallImage.size

        if width > 160:
            width = int(width / (width / 160))

        if height > 160:
            height = int(height / (height / 160))

        THUMBNAIL_SIZE_SMALL = (width, height )

        if smallImage.mode not in ('L', 'RGB'):
            smallImage = smallImage.convert('RGB')

        smallImage.thumbnail(THUMBNAIL_SIZE_SMALL, Image.ANTIALIAS)

        temp_handle_small = StringIO()

        smallImage.save(temp_handle_small, 'png')

        temp_handle_small.seek(0)

        ssuf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                  temp_handle_small.read(), content_type='image/png')

        self.thumbnail.save(self.file_name + '.png', ssuf, save=False)

        self.image.name = self.file_name

        super(JuckImage, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.file_name

    def get_log_rep(self):
        return self.__unicode__()