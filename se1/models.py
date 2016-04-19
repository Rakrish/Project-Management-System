# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

import os
from django.utils import timezone
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'




class Studentinfo(models.Model):
    usn = models.CharField(primary_key=True, max_length=10)
    name = models.TextField(blank=True, null=True)
    passwd = models.TextField(blank=True, null=True)
    sem = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.usn + "," + self.passwd
    class Meta:
        managed = False
        db_table = 'studentinfo'

class Studcontact(models.Model):
    usn = models.ForeignKey(Studentinfo, models.DO_NOTHING, db_column='usn')
    phno = models.IntegerField(primary_key=True)
    usn = models.CharField(max_length=10)
    class Meta:
        managed = False
        db_table = 'studcontact'
        unique_together = (('usn', 'phno'),)

class Profinfo(models.Model):
    profid = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    passwd = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'profinfo'

class Project(models.Model):
    projid = models.IntegerField(primary_key=True)
    title = models.TextField(blank=True, null=True)
    dateofreg = models.DateField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    complete = models.NullBooleanField()
    def __str__(self):
        return self.title
    class Meta:
        managed = False
        db_table = 'project'

class Domains(models.Model):
    domid = models.IntegerField(primary_key=True)
    domainname = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'domains'

class Profcontact(models.Model):
    profid = models.ForeignKey(Profinfo, models.DO_NOTHING, db_column='profid')
    profid = models.IntegerField()
    phno = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'profcontact'
        unique_together = (('profid', 'phno'),)


class Profemail(models.Model):
    profid = models.ForeignKey(Profinfo, models.DO_NOTHING, db_column='profid')
    profid = models.IntegerField(primary_key=True)
    email = models.TextField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'profemail'
        unique_together = (('profid', 'email'),)


class Profidea(models.Model):
    profid = models.ForeignKey(Profinfo, models.DO_NOTHING, db_column='profid')
    idea = models.TextField(blank=True, null=True)
    synopsis = models.TextField(blank=True, null=True)
    newprojid = models.IntegerField(primary_key=True)
    profid = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'profidea'
        unique_together = (('profid', 'newprojid'),)



class Projdom(models.Model):
    projid = models.ForeignKey(Project, models.DO_NOTHING, db_column='projid')
    domid = models.ForeignKey(Domains, models.DO_NOTHING, db_column='domid')
    projid = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'projdom'
        unique_together = (('projid', 'domid'),)


class Projfiles(models.Model):
    projid = models.ForeignKey(Project, models.DO_NOTHING, db_column='projid')
    fileid = models.IntegerField()
    fpath = models.TextField(blank=True, null=True)
    adate = models.DateField(blank=True, null=True)
    projid = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'projfiles'
        unique_together = (('projid', 'fileid'),)


class Projprof(models.Model):
    projid = models.ForeignKey(Project, models.DO_NOTHING, db_column='projid')
    profid = models.ForeignKey(Profinfo, models.DO_NOTHING, db_column='profid')
    projid = models.IntegerField(primary_key=True)
    profid = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'projprof'
        unique_together = (('projid', 'profid'),)


class Projprofcom(models.Model):
    projid = models.ForeignKey(Project, models.DO_NOTHING, db_column='projid')
    profid = models.ForeignKey(Profinfo, models.DO_NOTHING, db_column='profid')
    commentid = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    projid = models.IntegerField()
    profid = models.IntegerField()
    commentid = models.IntegerField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'projprofcom'
        unique_together = (('projid', 'profid', 'commentid'),)




class Studemail(models.Model):
    usn = models.ForeignKey(Studentinfo, models.DO_NOTHING, db_column='usn')
    usn = models.CharField(max_length=10)
    email = models.TextField(primary_key=True)
    class Meta:
        managed = False
        db_table = 'studemail'
        unique_together = (('usn', 'email'),)



class Studprojgrade(models.Model):
    usn = models.ForeignKey(Studentinfo, models.DO_NOTHING, db_column='usn')
    projid = models.ForeignKey(Project, models.DO_NOTHING, db_column='projid')
    grade = models.CharField(max_length=1, blank=True, null=True)
    usn = models.CharField(max_length=10)
    projid = models.IntegerField(primary_key = True)
    class Meta:
        managed = False
        db_table = 'studprojgrade'
        unique_together = (('usn', 'projid'),)

def content_file_name(instance, filename):
    upload_dir = str(instance.projid)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)

class FilesUpload(models.Model):
    projid = models.ForeignKey(Project, models.DO_NOTHING, db_column='projid')
    fileid = models.IntegerField(primary_key = True)
    filename = models.CharField(max_length = 100)
    file=models.FileField(upload_to=content_file_name)
    projid = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'filesupload'
        unique_together = (('projid', 'fileid'),)

class Chat(models.Model):
    chatid = models.IntegerField(primary_key = True)
    #usn = models.ForeignKey('Studentinfo', models.DO_NOTHING, db_column='usn')
    usn = models.TextField(blank = True, null = True)
    name = models.TextField(blank = True, null = True)
    projid = models.ForeignKey('Project', models.DO_NOTHING, db_column='projid')
    chatcontent = models.TextField(blank=True, null=True)
    time_stamp = models.DateTimeField(auto_now_add = True,auto_now = False, blank=True, null=True)
    projid = models.IntegerField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'chat'
        unique_together = (('chatid', 'usn', 'projid'),)
