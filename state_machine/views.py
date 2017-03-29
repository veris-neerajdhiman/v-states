#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
- state_machine.views
~~~~~~~~~~~~~~

- This file contains state_machine micro-service views, every HTTP request/router points to this file.
"""

# future
from __future__ import unicode_literals

# 3rd party
from rest_framework import exceptions
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

# Django
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

# local

# own app
from state_machine import models, config, serializers


class TransactionStateViewSet(viewsets.GenericViewSet):
    """States viewset , it controls general functions of states like create new, change and get current state

        Note :
            - Whenever a Transaction state is logged it is possible that you have called a Resource or service
              like HTTP or any other, so we need to store that service too, But calling of any service is optional
              so we are going to handle this via `service` key in request data. (type of `service` key will be dict())
            - If service key is available and we are using Generic FK to support multiple service types
              (However rt now we only support HTTP). So how we will identify which service have been requested.
            - To identify type of service we must have another key `type` in `service` dict() which will tell
              what service have been requested. We will validate that service and store in respective service model.
    """
    model = models.TransactionStateMachine
    # TODO : remove AllowAny permission with proper permission class
    permission_classes = (permissions.AllowAny, )

    service = None  # determine wether service key sent in request and a valid service it is
    service_type = None
    service_content_type = None
    service_object_id = None

    def _validate_request(self, request):
        """
        :param request: Django request
        """

        # validate if service key exists in requested data
        if 'service' in request.data.keys():
            if not type(request.data.get('service')) is dict:
                raise exceptions.ParseError({'detail': 'service must be of dict type.'})
            # validate type of requested service
            self.service_type = request.data.get('service').get('type', None)
            if not self.service_type or self.service_type not in config.ENABLED_SERVICES:
                raise exceptions.NotAcceptable({'detail': 'unknown service requested.'})
            self.service = True

    def _choose_service_serializer(self, service_type):
        """

        :param service_type: type of service
        :return: Service Serializer
        """
        if service_type == config.HTTP:
            self.service_content_type = ContentType.objects.get_for_model(models.HttpService)
            return serializers.HttpServiceSerializer
        raise ValueError({'detail': 'unknown service requested.'})

    def _validate_data(self, serializer_cls, data):
        """
        :param serializer_cls: serializer against which data to be validated
        :param data: user input data which is to be validated
        :return: validated serializer instance
        """
        serializer = serializer_cls(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def _validate_and_save_service_data(self, request):
        """
        :param request: Django request
        :return: Service Model object id (For Generic FK)
        """

        serializer = self._choose_service_serializer(self.service_type)
        serializer = self._validate_data(serializer, request.data.get('service'))
        service = serializer.save()
        return service.id

    def get_object(self, task_identifier):
        """

        :param task_identifier: task unique identifier
        :return: Transaction/task instance
        """
        return get_object_or_404(self.model, task_identifier=task_identifier)

    def create_initial_state(self, request):
        """
        :param request: Django request
        :return: 200_ok

        POST EXAMPLE :

        - without service
        {
          "task_name": "My first Task",
          "task_identifier": "1a",
          "state":"init"
        }

        - with service (http)
        {
            "task_name": "My Second Task",
            "task_identifier": "1b",
            "state": "init",
            "service": {
                "type":"http",
                "upstream_url": "http://localhost:8003",
                "method": "post",
                "headers": {
                    "token": "0123654789"
                },
                "dataIn": {
                    "name": "Daniel"
                },
                "dataOut": {
                    "user_id": "1"
                }
            }
        }
        """
        life_cycle_data = dict()

        # ----- validate request and its data ---- #

        # validate for service key
        self._validate_request(request)

        # Validate for main Transaction state Model
        transaction_state = self._validate_data(serializers.TransactionStateMachineSerializer, request.data)

        # if service present oin request then save service data
        if self.service:
            service_object_id = self._validate_and_save_service_data(request)

            # add content type and object_id in life_cycle_dict
            life_cycle_data.update({
                'content_type': self.service_content_type,
                'object_id': service_object_id
            })

        # save main Transaction
        transaction = transaction_state.save()

        life_cycle_data.update({
            'task': transaction,
            'state': request.data.get('state')
        })

        # save Transaction life cycle instance
        models.TransactionLifeCycle.objects.create(**life_cycle_data)

        return Response(status=status.HTTP_200_OK)

    def get_current_state(self, request, task_identifier):
        """
        :param request: Django request
        :param task_identifier: task identifier of whom you want to get current state
        :return: current state of any Transaction/Task
        """
        task_instance = self.get_object(task_identifier)
        return Response({'current_state': task_instance.get_current_state}, status=status.HTTP_200_OK)

    def get_complete_transaction_life_cycle(self, request, task_identifier):
        """
        :param request: Django request
        :param task_identifier: task identifier of whom you want to get complete life cycle
        :return:
        """
        task_instance = self.get_object(task_identifier)
        serializer = serializers.TransactionLifeCycleSerializer(instance=task_instance.fetch_complete_life_cycle,
                                                                many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def change_state(self, request, task_identifier):
        """
        :param request: Django request
        :param task_identifier: task identifier of whom you want to get complete life cycle
        :return: 200_ok

        POST EXAMPLE :
        {
            "state": "fail",
            "service": {
                "type":"http",
                "upstream_url": "http://localhost:8002",
                "method": "post",
                "headers": {
                    "token": "qwer1236544"
                },
                "dataIn": {
                    "name": "Daneil"
                },
                "dataOut": {
                    "user_id": "1"
                }
            }
        }

        """
        life_cycle_data = dict()
        task_instance = self.get_object(task_identifier)

        # ----- validate request and its data ---- #

        # validate new state
        serializer = self._validate_data(serializers.ChangeStateSerializer, request.data)

        # validate for service key
        self._validate_request(request)

        # if service present oin request then save service data
        if self.service:
            service_object_id = self._validate_and_save_service_data(request)

            # add content type and object_id in life_cycle_dict
            life_cycle_data.update({
                'content_type': self.service_content_type,
                'object_id': service_object_id
            })

        life_cycle_data.update({
            'task': task_instance,
            'state': serializer.data.get('state')
        })

        # update state
        task_instance.change_state(serializer.data.get('state'))

        # save Transaction life cycle instance
        models.TransactionLifeCycle.objects.create(**life_cycle_data)

        return Response(status=status.HTTP_200_OK)