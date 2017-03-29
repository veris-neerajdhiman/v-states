#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- state_machine.models.states
~~~~~~~~~~~~~~

- This file contains models of state machine micro service
"""

# future
from __future__ import unicode_literals

# 3rd party
from datetime import datetime

# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# local

# own app
from state_machine import config
from state_machine.models.services import HttpService


class TransactionStateMachine(models.Model):
    """Manage Current State of any Task.

        - Whenever a state is update two new entries in TransactionLifeCycle & HttpService is required so that
        - when we retrieve complete life cycle , we have all information.
    """
    # Attributes
    task_name = models.CharField(
        _('task name'),
        max_length=30,
        help_text=_('Required. 30 characters or fewer.'),
    )
    task_identifier = models.CharField(
        _('any unique identifier of any task'),
        max_length=200,
        unique=True,
        help_text=_('Required. 200 characters or fewer.'),
    )
    state = models.CharField(
        _('current state of any task'),
        max_length=20,
        default=config.INIT,
        choices=config.STATES,
        help_text=_('Task state at any given time.'),
    )
    created_at = models.DateTimeField(
        _('Task state activity create time.'),
        auto_now=False,
        db_index=True,
    )
    modified_at = models.DateTimeField(
        _('Task state activity modify time.'),
        auto_now=False,
        db_index=True,
    )

    # Meta
    class Meta:
        verbose_name = _("Transaction State Machine")
        verbose_name_plural = _("Transaction State Machine")
        ordering = ["-id"]
        get_latest_by = "id"

    # Functions
    def __str__(self):
        return "{transaction_id} -> {task_name} || {state}".format(
            transaction_id=self.id,
            task_name=self.task_name,
            state=self.state
        )

    @property
    def get_current_state(self):
        """

        :return: current state of any transaction
        """
        return self.state

    @property
    def fetch_complete_life_cycle(self):
        """

        :return: fetch complete life cycle of any Transaction.
        """
        return self.transactionlifecycle_set.all()

    def change_state(self, new_state):
        """

        :param new_state: new state of Transaction
        :return: TransactionStateMachine instance

        """
        self.state = new_state
        self.modified_at = datetime.now()
        return self.save()


class TransactionLifeCycle(models.Model):
    """Manage Any Transaction life cycle.

        - We will use Django GenericForeignKey (EAV) to store service which was called by task.
         Why ? - Right now we only support HTTP services but later we will support many others, so it is to be well
         prepare for that.

    """
    task = models.ForeignKey(TransactionStateMachine,
                             verbose_name=_('transaction state machine'),
    )
    content_type = models.ForeignKey(ContentType,
                                     db_index=True,
                                     blank=True,
                                     null=True,
                                     help_text=_('Content Type of Object you want tyo map.'),
    )
    object_id = models.PositiveIntegerField(
        _('id of object you want to map'),
        db_index=True,
        blank=True,
        null=True,
    )
    entity = GenericForeignKey('content_type', 'object_id')
    state = models.CharField(
        _('current state of any task'),
        max_length=20,
        default=config.INIT,
        choices=config.STATES,
        help_text=_('Task state at any given time.'),
    )
    created_at = models.DateTimeField(
        _('Task state activity create time.'),
        auto_now=True,
        db_index=True,
    )

    # Meta
    class Meta:
        verbose_name = _("Transaction Life Cycle")
        verbose_name_plural = _("Transaction Life Cycle")
        ordering = ["-id"]
        get_latest_by = "id"

    # Functions
    def __str__(self):
        return "{cycle_id} -> {state}".format(
            cycle_id=self.id,
            state=self.state
        )

    @property
    def get_http_service_object(self):
        """Method to retrieve related HTTP service instance (if any)

        :return: related HTTP service object
        """
        if self.content_type == ContentType.objects.get_for_model(HttpService):
            return HttpService.objects.get(pk=self.object_id)
