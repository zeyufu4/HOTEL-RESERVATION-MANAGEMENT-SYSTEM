# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib import admin
from django.db import models

class Dayarrive(models.Model):
    username = models.CharField(max_length=20, db_collation='gbk_chinese_ci', blank=True, null=True, verbose_name='用户姓名')
    plantype = models.CharField(max_length=20, db_collation='gbk_chinese_ci', blank=True, null=True, verbose_name='预订类型')
    roomid = models.IntegerField(primary_key=True,blank=True, verbose_name='房间号')
    leavetime = models.DateField(blank=True, null=True, verbose_name='离开时间')

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'dayarrive'
        verbose_name='每日到达报表'
        verbose_name_plural='每日到达报表'


class Daylive(models.Model):
    roomid = models.IntegerField(primary_key=True,blank=True, verbose_name='房间号')
    name = models.CharField(max_length=20, db_collation='gbk_chinese_ci', blank=True, null=True, verbose_name='用户姓名')
    leavetime = models.DateField(blank=True, null=True, verbose_name='离开时间')

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'daylive'
        verbose_name='每日入住报表'
        verbose_name_plural='每日入住报表'


class Livenotes(models.Model):
    bid = models.IntegerField(primary_key=True, verbose_name='id')
    time = models.DateField(blank=True, null=True, verbose_name='时间')
    yufujin = models.IntegerField(blank=True, null=True, verbose_name='预付金预订人数')
    tiqian60 = models.IntegerField(blank=True, null=True, verbose_name='提前60天预订人数')
    changgui = models.IntegerField(blank=True, null=True, verbose_name='常规预订人数')
    zong = models.IntegerField(blank=True, null=True, verbose_name='总预订人数')

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'livenotes'
        verbose_name='预计入住报表'
        verbose_name_plural='预计入住报表'


class Moneynotes(models.Model):
    bid = models.IntegerField(primary_key=True, verbose_name='id')
    time = models.DateField(blank=True, null=True, verbose_name='时间')
    income= models.DecimalField(db_column='income', max_digits=25, decimal_places=4, blank=True, null=True, verbose_name='收入')

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'moneynotes'
        verbose_name='预计房间收入报表'
        verbose_name_plural='预计房间收入报表'


class Notes(models.Model):
    now_field = models.DateTimeField(db_column='now_field', verbose_name='时间')
    usercredit = models.CharField(primary_key=True,max_length=20, db_collation='gbk_chinese_ci', blank=True, verbose_name='信用卡号')
    name = models.CharField(max_length=20, db_collation='gbk_chinese_ci', blank=True, null=True, verbose_name='姓名')
    roomid = models.IntegerField(blank=True, null=True, verbose_name='房号')
    arrivetime = models.DateField(blank=True, null=True, verbose_name='到达时间')
    leavetime = models.DateField(blank=True, null=True, verbose_name='离开时间')
    datediffer = models.BigIntegerField(db_column='datediffer', blank=True, null=True, verbose_name='入住天数')
    paytime = models.DateTimeField(blank=True, null=True, verbose_name='支付时间')
    money = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='金额')

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'notes'
        verbose_name='票据'
        verbose_name_plural='票据'

