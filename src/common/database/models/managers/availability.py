from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    def soft_delete(self):
        return self.update(is_deleted=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)
