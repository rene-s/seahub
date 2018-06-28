# Copyright (c) 2012-2018 Seafile Ltd.

from django.conf.urls import url

from seahub.alibaba.views import alibaba_user_profile, SearchUser

urlpatterns = [
    url(r'^profile/(?P<email>[^/]*)/$', alibaba_user_profile, name="alibaba-user-profile"),
]
