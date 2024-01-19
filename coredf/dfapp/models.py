from django.db import models


class PCConfiguration(models.Model):
    pc_config = models.JSONField(null=True)
