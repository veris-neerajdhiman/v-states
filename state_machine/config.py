#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- state_machine.config
~~~~~~~~~~~~~~

- General settings of state machine micro-service
"""

# future
from __future__ import unicode_literals

# 3rd party


# Django


# local


# own app


INIT = 'init'
PROCESSING = 'processing'
COMPLETE = 'complete'
FAIL = 'fail'
RESUME = 'resume'
RESTART = 'restart'

GET = 'get'
POST = 'post'
PUT = 'put'
DELETE = 'delete'

STATES = (
    (INIT, 'Initialize'),
    (PROCESSING, 'processing'),
    (COMPLETE, 'complete'),
    (FAIL, 'fail'),
    (RESUME, 'resume'),
    (RESTART, 'restart'),
)

METHODS = (
    (GET, 'get'),
    (POST, 'post'),
    (PUT, 'put'),
    (DELETE, 'delete'),
)

HTTP = 'http'

ENABLED_SERVICES = (HTTP, )
