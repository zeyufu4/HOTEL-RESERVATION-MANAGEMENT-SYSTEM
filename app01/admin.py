import datetime

from django.contrib import admin, auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User as authUser
from django.contrib.auth.models import Group

from app01.models import Base, Room, User, Worker, Plan, Ticket, Mailbox

# Register your models here.
from hotelManage import settings

admin.site.site_header = 'Oasis管理系统'
admin.site.site_title = 'Oasis管理系统'
admin.site.index_title = 'Oasis管理系统'


@admin.register(Base)
class BaseAdmin(admin.ModelAdmin):
    list_display = ('time', 'money')
    ordering = ('time',)


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('usercredit', 'roomid', 'plantype', 'plantime', 'arrivetime', 'leavetime', 'paytime', 'money')
    fields = ('roomid', 'plantype', 'plantime', 'arrivetime', 'leavetime')
    actions = ['payment', ]

    @admin.action(permissions=['view'], description='支付')
    def payment(self, request, queryset):
        for obj in queryset:
            if (self.money(obj) != 0):
                queryset.update(paytime=datetime.datetime.now())
                User.objects.filter(creditcard=obj.usercredit).update(money=0)

            # queryset.update(money=0)

    actions_on_bottom = True
    actions_on_top = False

    def money(self, obj):
        return User.objects.get(creditcard=obj.usercredit).money

    money.short_description = '待支付金额'

    def get_fields(self, request, obj=None):
        if request.user.is_superuser:
            return 'roomid', 'usercredit', 'plantype', 'plantime', 'arrivetime', 'leavetime'
        else:
            return 'roomid', 'plantype', 'arrivetime', 'leavetime'

    # Override form field for foreign key,
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "roomid":
            kwargs["queryset"] = Room.objects.filter(state='no')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(PlanAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            try:
                iddt = Worker.objects.get(name=request.user.username).identify
                if (iddt == '雇员') or (iddt == '管理'):
                    return qs
            except Worker.DoesNotExist:
                return qs.filter(usercredit=request.user.username)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            super().save_model(request, obj, form, change)
        else:
            obj.usercredit = User.objects.get(creditcard=request.user.username)
            super().save_model(request, obj, form, change)
        if not Mailbox.objects.filter(mcard=User.objects.get(creditcard=obj.usercredit)).exists():
            Mailbox.objects.create(mcard=User.objects.get(creditcard=obj.usercredit),
                                   mail=(str(obj.usercredit) + "@hotelmail.com"))
        return
    # 预约时间默认值不触发


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    # 'usercredit', 'plantype', 'plantime', 'arrivetime', 'leavetime'
    list_display = ('rid', 'state',)
    fields = ('state',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'creditcard', 'money')
    actions = ['payment', ]

    @admin.action(permissions=['delete'], description='清除支付')
    def payment(self, request, queryset):
        queryset.update(money=0)

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(creditcard=request.user.username)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            try:
                authUser.objects.get(username=request.POST.get('creditcard'))
            except authUser.DoesNotExist:
                tempuser = authUser.objects.create(
                    username=request.POST.get('creditcard'),
                    password=make_password(request.POST.get('password')),
                    is_staff=1
                )
                tempuser.groups.add(Group.objects.get(name='客户'))
            finally:
                super().save_model(request, obj, form, change)
                return
        else:
            super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        iddt = obj.creditcard
        try:
            if request.user.is_superuser:
                authUser.objects.get(username=iddt).delete()
        except authUser.DoesNotExist:
            super().delete_model(request, obj)
            return
        finally:
            super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('wid', 'name', 'identify')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if request.user.is_superuser:
            iddt = request.POST.get('name')
            try:
                authUser.objects.get(username=request.POST.get(iddt))
            except authUser.DoesNotExist:
                tempuser = authUser.objects.create(
                    username=iddt,
                    password=make_password(request.POST.get('password')),
                    is_staff=1
                )
                tempuser.groups.add(Group.objects.get(name=request.POST.get('identify')))
            finally:
                super().save_model(request, obj, form, change)
                return

    def delete_model(self, request, obj):
        iddt = obj.name + str(obj.wid)
        try:
            if request.user.is_superuser:
                authUser.objects.get(username=iddt).delete()
        except authUser.DoesNotExist:
            super().delete_model(request, obj)
            return
        finally:
            super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            self.delete_model(request, obj)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('tcard', 'tmoney', 'tjudge')
    actions = ['payment', ]

    @admin.action(permissions=['view'], description='支付')
    def payment(self, request, queryset):
        queryset.update(tjudge='yes')



@admin.register(Mailbox)
class MailboxAdmin(admin.ModelAdmin):
    list_display = ('mcard', 'mail', 'mtime', 'content')
    actions = ['inform', ]

    @admin.action(permissions=['change'], description='生成通知')
    def inform(self, request, queryset):
        queryset.update(content='请在15天内支付退款或取消预订', mtime=datetime.datetime.now())

    def get_queryset(self, request):
        qs = super(MailboxAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            try:
                iddt = Worker.objects.get(name=request.user.username).identify
                if (iddt == '雇员') or (iddt == '管理'):
                    return qs
            except Worker.DoesNotExist:
                return qs.filter(mcard=request.user.username)

# admin.site.register(Base, BaseAdmin)
# admin.site.register(Plan, PlanAdmin)
# admin.site.register(Room, RoomAdmin)
# admin.site.register(User, UserAdmin)
# admin.site.register(Worker, WorkerAdmin)
# admin.site.register(Dayarrive, DayarriveAdmin)
# admin.site.register(Daylive, DayliveAdmin)
