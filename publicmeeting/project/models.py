from django.db import models

from .utils import slugify_uniquely


class TimestampedModelMixin (models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SlugifiedModelMixin (models.Model):
    slug = models.SlugField(blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_uniquely(self.get_pre_slug(), self.__class__)

        return super(SlugifiedModelMixin, self).save(*args, **kwargs)

    def get_pre_slug(self):
        raise NotImplementedError()
