# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import HttpResponseRedirect

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class SimpleMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path != '/country/login_admin':
            if request.session.get('user', None):
                pass
            else:
                return HttpResponseRedirect('/country/login_admin')

