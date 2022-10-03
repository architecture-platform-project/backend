from django.db import models


class TimeStampModel(models.Model):
    """타임 추상화 모델"""

    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        abstract = True
