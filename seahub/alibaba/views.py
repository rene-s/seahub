# Copyright (c) 2012-2018 Seafile Ltd.
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import ugettext as _

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from seahub.api2.authentication import TokenAuthentication
from seahub.api2.throttling import UserRateThrottle
from seahub.api2.utils import api_error

from seahub.auth.decorators import login_required
from seahub.utils import is_valid_username, render_error

from seahub.alibaba.models import Profile

@login_required
def alibaba_user_profile(request, email):

    # TODO
    email = 'cathy@alibaba-inc.com'

    if not is_valid_username(email):
        error_msg = _('Email %s invalid.') % email
        return render_error(request, error_msg)

    profile_dict = {}
    profile = Profile.objects.get_profile(email)

    if profile:
        profile_dict['personal_photo_url'] = profile.personal_photo_url
        profile_dict['emp_name'] = profile.emp_name
        profile_dict['nick_name'] = profile.nick_name

        if request.LANGUAGE_CODE == 'zh-cn':
            post_name = profile.post_name
            dept_name = profile.dept_name
            profile_dict['post_name'] = post_name
            profile_dict['dept_name'] = dept_name.replace('-', ' ')
        else:
            post_name_en = profile.post_name_en
            dept_name_en = profile.dept_name_en
            profile_dict['post_name'] = post_name_en
            profile_dict['dept_name'] = dept_name_en.replace('-', ' ')

    return render(request, 'alibaba/profile.html', profile_dict)
