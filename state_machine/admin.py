#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- state_machine.admin
~~~~~~~~~~~~~~

- This file contains admin models of state_machine micro service
"""

# future
from __future__ import unicode_literals

# 3rd party


# Django
from django.contrib import admin

# local


# own app
from state_machine import models


class TransactionStateMachineAdmin(admin.ModelAdmin):
    """

    """
    list_display = ('id', 'task_name', 'task_identifier', 'state', 'created_at', 'modified_at')
    list_display_links = ('id', 'task_name',)
    list_filter = ('state', )
    search_fields = ('task_name', 'task_identifier')
    list_per_page = 20
    ordering = ('-id',)


class TransactionLifeCycleAdmin(admin.ModelAdmin):
    """

    """
    list_display = ('id', 'task', 'state', 'created_at', )
    list_display_links = ('id', 'task',)
    list_filter = ('state', )
    search_fields = ('task__task_name', 'task__task_identifier')
    list_per_page = 20
    ordering = ('-id',)


class HttpServiceAdmin(admin.ModelAdmin):
    """

    """
    list_display = ('id', 'upstream_url', 'method', 'created_at', )
    list_display_links = ('id', 'upstream_url',)
    list_filter = ('method',)
    search_fields = ('upstream_url', )
    list_per_page = 20
    ordering = ('-id',)


admin.site.register(models.TransactionStateMachine, TransactionStateMachineAdmin)
admin.site.register(models.TransactionLifeCycle, TransactionLifeCycleAdmin)
admin.site.register(models.HttpService, HttpServiceAdmin)
