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


class SearchUser(APIView):
    """ Search user from alibaba profile table.
    """

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRateThrottle,)

    def get(self, request, format=None):

        q = request.GET.get('q', None)
        if not q:
            error_msg = 'q invalid.'
            return api_error(status.HTTP_400_BAD_REQUEST, error_msg)

        # TODO
        request.LANGUAGE_CODE = 'zh-cn'

        # users.query
        # SELECT `alibaba_profile`.`id`, `alibaba_profile`.`uid`, `alibaba_profile`.`personal_photo_url`, `alibaba_profile`.`person_id`, `alibaba_profile`.`emp_name`, `alibaba_profile`.`pinyin_name`, `alibaba_profile`.`nick_name`, `alibaba_profile`.`pinyin_nick`, `alibaba_profile`.`work_no`, `alibaba_profile`.`post_name`, `alibaba_profile`.`post_name_en`, `alibaba_profile`.`dept_name`, `alibaba_profile`.`dept_name_en`, `alibaba_profile`.`work_status`, `alibaba_profile`.`gmt_leave` FROM `alibaba_profile` WHERE (`alibaba_profile`.`emp_name` LIKE %0% OR `alibaba_profile`.`pinyin_name` LIKE %0% OR `alibaba_profile`.`nick_name` = 0 OR `alibaba_profile`.`pinyin_nick` = 0) ORDER BY `alibaba_profile`.`dept_name` DESC LIMIT 10
        if request.LANGUAGE_CODE == 'zh-cn':
            users = Profile.objects.filter(
                    Q(emp_name__icontains=q) | Q(pinyin_name__icontains=q) | \
                    Q(nick_name=q) | Q(pinyin_nick=q)).order_by('-dept_name')[:10]
        else:
            users = Profile.objects.filter(
                    Q(emp_name__icontains=q) | Q(pinyin_name__icontains=q) | \
                    Q(nick_name=q) | Q(pinyin_nick=q)).order_by('-dept_name_en')[:10]

        result = []
        for user in users:

            user_info = {}
            user_info['uid'] = user.uid
            user_info['personal_photo_url'] = user.personal_photo_url

            # TODO
            user_info['personal_photo_url'] = "https://demo.seafile.top/image-view/avatars/7/a/ce4483526f8aefec13fb8c14458893/resized/32/6da2b650e2dfbf842490f9ff0b4d63a6.png"
            user_info['emp_name'] = user.emp_name
            user_info['nick_name'] = user.nick_name

            if request.LANGUAGE_CODE == 'zh-cn':
                user_info['post_name'] = user.post_name
                user_info['dept_name'] = user.dept_name
            else:
                user_info['post_name'] = user.post_name_en
                user_info['dept_name'] = user.dept_name_en

            result.append(user_info)

        return Response({"users": result})
