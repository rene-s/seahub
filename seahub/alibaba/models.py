# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class ProfileManager(models.Manager):

    def get_profile(self, email):
        try:
            profile = super(ProfileManager, self).get(uid=email)
        except Profile.DoesNotExist:
            return None

        return profile


class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.CharField(max_length=64)
    personal_photo_url = models.CharField(max_length=225, blank=True, null=True)
    person_id = models.BigIntegerField(unique=True)
    emp_name = models.CharField(max_length=64, blank=True, null=True)
    pinyin_name = models.CharField(max_length=64, blank=True, null=True)
    nick_name = models.CharField(max_length=64, blank=True, null=True)
    pinyin_nick = models.CharField(max_length=64, blank=True, null=True)
    work_no = models.CharField(max_length=16)
    post_name = models.CharField(max_length=64)
    post_name_en = models.CharField(max_length=64)
    dept_name = models.CharField(max_length=128)
    dept_name_en = models.CharField(max_length=128)
    work_status = models.CharField(max_length=4)
    gmt_leave = models.DateTimeField(blank=True, null=True)

    objects = ProfileManager()

    class Meta:
        managed = False
        db_table = 'alibaba_profile'


class MessageQueue(models.Model):
    id = models.BigAutoField(primary_key=True)
    topic = models.CharField(max_length=64)
    gmt_create = models.DateTimeField()
    gmt_modified = models.DateTimeField()
    message_body = models.TextField()
    is_consumed = models.IntegerField()
    lock_version = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message_queue'
