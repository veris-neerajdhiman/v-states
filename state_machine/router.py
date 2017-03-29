#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- state_machine.router
~~~~~~~~~~~~~~

- Routers of state_machine micro-service
"""

# future
from __future__ import unicode_literals

# 3rd party


# Django
from django.conf.urls import url


# local


# own app
from state_machine import views

create_initial_state = views.TransactionStateViewSet.as_view({
    'post': 'create_initial_state',
})

get_current_state = views.TransactionStateViewSet.as_view({
    'get': 'get_current_state',
})

get_complete_transaction_life_cycle = views.TransactionStateViewSet.as_view({
    'get': 'get_complete_transaction_life_cycle',
})

change_state = views.TransactionStateViewSet.as_view({
    'put': 'change_state',
})

urlpatterns = [
    url(r'^new/$',
        create_initial_state,
        name='create-initial-state'),
    url(r'^(?P<task_identifier>[0-9a-z-]+)/current/$',
        get_current_state,
        name='get-current-state'),
    url(r'^(?P<task_identifier>[0-9a-z-]+)/life-cycle/$',
        get_complete_transaction_life_cycle,
        name='get-complete-transaction-life-cycle'),
    url(r'^(?P<task_identifier>[0-9a-z-]+)/change/$',
        change_state,
        name='change-state'),
]
