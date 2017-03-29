#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- - state_machine.serializers
~~~~~~~~~~~~~~

- **file description**
"""

# future
from __future__ import unicode_literals

# 3rd party
from datetime import datetime
from rest_framework import serializers


# Django


# local


# own app
from state_machine import config
from state_machine.models import TransactionLifeCycle, TransactionStateMachine, HttpService


class TransactionStateMachineSerializer(serializers.ModelSerializer):
    """

    """
    state = serializers.ChoiceField(required=True,
                                    choices=config.STATES)

    class Meta:
        model = TransactionStateMachine
        exclude = ('created_at', 'modified_at', )

    def create(self, validated_data):
        """

        :param validated_data: validated data
        :return:
        """
        created_at = modified_at = datetime.now()

        validated_data.update({
            'created_at': created_at,
            'modified_at': modified_at
        })

        return super(TransactionStateMachineSerializer, self).create(validated_data)


class HttpServiceSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = HttpService
        exclude = ('id', )


class TransactionLifeCycleSerializer(serializers.ModelSerializer):
    """

    """
    task_identifier = serializers.ReadOnlyField(source='task.task_identifier')
    service = serializers.SerializerMethodField()

    class Meta:
        model = TransactionLifeCycle
        fields = ('id', 'task_identifier', 'service', 'state', 'created_at', )

    def get_service(self, obj):
        """

        :param obj: TransactionLifeCycle object
        :return: object related service data
        """
        return HttpServiceSerializer(instance=obj.get_http_service_object).data


class ChangeStateSerializer(serializers.Serializer):
    """Change State serializer

    """
    state = serializers.ChoiceField(required=True,
                                    choices=config.STATES)
