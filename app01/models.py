# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class Base(models.Model):
    bid = models.AutoField(primary_key=True)
    time = models.DateField(blank=True, null=True, verbose_name='时间')
    money = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='价格')

    class Meta:
        managed = False
        db_table = 'base'
        verbose_name = '房间价格信息'
        verbose_name_plural = '房间价格信息'


class Plan(models.Model):
    pid = models.AutoField(primary_key=True)
    roomid = models.ForeignKey('Room', models.DO_NOTHING, db_column='roomid', blank=True, null=True,
                               verbose_name="预订房间", unique=True)
    usercredit = models.ForeignKey('User', models.DO_NOTHING, db_column='usercredit', blank=True, null=True,
                                   verbose_name="信用卡号")
    plantype = models.CharField(max_length=20, blank=True, null=True,
                                choices=(('提前60天预订', '提前60天预订'), ('常规预订', '常规预订'), ('预付金预订', '预付金预订'), ('常规预订', '奖励预订')),
                                verbose_name="预约类型")
    plantime = models.DateTimeField(blank=True, null=True, verbose_name="预约时间", default=datetime.datetime.now())
    arrivetime = models.DateField(blank=True, null=True, verbose_name="到达时间")
    leavetime = models.DateField(blank=True, null=True, verbose_name="离开时间")
    paytime = models.DateTimeField(blank=True, null=True, verbose_name="支付时间")

    def __str__(self):
        return "卡号" + str(self.usercredit) + "的用户"

    class Meta:
        managed = False
        db_table = 'plan'
        verbose_name = '预订信息'
        verbose_name_plural = '预订信息'


class Room(models.Model):
    rid = models.IntegerField(primary_key=True, verbose_name='房间ID', auto_created=True)
    state = models.CharField(max_length=3,
                             choices=(('yes', '已住'), ('no', '空房'),),
                             verbose_name='房间状态')

    def __str__(self):
        return str(self.rid) + "号房"
        # return str(self.rid)+"号房("+self.get_state_display()+")"

    class Meta:
        managed = False
        db_table = 'room'
        verbose_name = '房间信息'
        verbose_name_plural = '房间信息'


class User(models.Model):
    creditcard = models.CharField(primary_key=True, max_length=20, verbose_name="信用卡号")
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name="姓名")
    password = models.CharField(max_length=20, blank=True, null=True, verbose_name="密码")
    money = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="待付金额")

    def __str__(self):
        return self.creditcard

    def __unicode__(self):
        return self.creditcard

    class Meta:
        managed = False
        db_table = 'user'
        verbose_name = '客户信息'
        verbose_name_plural = '客户信息'


class Worker(models.Model):
    wid = models.AutoField(primary_key=True, verbose_name="id")
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name="姓名")
    password = models.CharField(max_length=20, blank=True, null=True, verbose_name="密码")
    identify = models.CharField(max_length=2, blank=True, null=True,
                                choices=(('雇员', '雇员'), ('管理', '管理'),),
                                verbose_name="职位")

    class Meta:
        managed = False
        db_table = 'worker'
        verbose_name = '工作人员信息'
        verbose_name_plural = '工作人员信息'


class Ticket(models.Model):
    tid = models.AutoField(primary_key=True, verbose_name="id")
    tcard = models.ForeignKey('User', models.DO_NOTHING, db_column='tcard', blank=True, null=True, verbose_name='卡号')
    tmoney = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="金额")
    tjudge = models.CharField(max_length=3, verbose_name="是否完成支付",
                              choices=(('yes', '已支付'), ('no', '未支付'),),
                              default='no')

    class Meta:
        managed = False
        db_table = 'ticket'
        verbose_name = '罚单'
        verbose_name_plural = '罚单'


class Mailbox(models.Model):
    mid = models.AutoField(primary_key=True, verbose_name="id")
    mcard = models.ForeignKey('User', models.DO_NOTHING, db_column='mcard', blank=True, null=True, verbose_name="卡号")
    mail = models.CharField(max_length=30, blank=True, null=True, verbose_name="邮箱")
    mtime = models.DateField(blank=True, null=True, verbose_name="时间")
    content = models.CharField(max_length=100, blank=True, null=True, verbose_name="内容",)

    class Meta:
        managed = False
        db_table = 'mailbox'
        verbose_name = '邮箱'
        verbose_name_plural = '邮箱'
