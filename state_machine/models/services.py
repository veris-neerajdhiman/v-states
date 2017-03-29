#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- state_machine.models.services
~~~~~~~~~~~~~~

- This file contains models of services state_machine micro-service support
"""

# future
from __future__ import unicode_literals

# 3rd party

# Django
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

# local

# own app
from state_machine import config


class HttpService(models.Model):
    """Http service Model

    """
    upstream_url = models.URLField(
        _('upstream url of HTTP service.'),
        null=False,
        blank=False,
        max_length=200,
        help_text=_('Required. 200 characters or fewer.'),
    )
    method = models.CharField(
        _('Service Supported Method '),
        max_length=6,
        default=config.POST,
        choices=config.METHODS,
        help_text=_('Service Supported Methods.'),
    )
    headers = JSONField(
        _('Request Headers'),
        blank=True,
        null=True,
        help_text=_('Request Headers.'),
    )
    dataIn = JSONField(
        _('Request payload'),
        blank=True,
        null=True,
        help_text=_('Request payload, includes query_params, data etc.'),
    )
    dataOut = JSONField(
        _('Request response'),
        blank=True,
        null=True,
        help_text=_('Response that is returned via service.'),
    )
    created_at = models.DateTimeField(
        _('service request time.'),
        auto_now=True,
        db_index=True,
    )

    # Meta
    class Meta:
        verbose_name = _("HTTP Service")
        verbose_name_plural = _("HTTP Service")
        ordering = ["-id"]
        get_latest_by = "id"

        # Functions
    def __str__(self):
        return "{service_id}".format(
            service_id=self.id,
        )

