from django.contrib import admin
from app02.models import Dayarrive, Daylive, Livenotes, Moneynotes, Notes


# Register your models here.
@admin.register(Dayarrive)
class DayarriveAdmin(admin.ModelAdmin):
    list_display = ('username', 'plantype', 'roomid', 'leavetime')
    ordering = ('roomid',)

@admin.register(Daylive)
class DayliveAdmin(admin.ModelAdmin):
    list_display = ('roomid', 'name', 'leavetime')
    ordering = ('roomid',)


@admin.register(Livenotes)
class LivenotesAdmin(admin.ModelAdmin):
    list_display = ('bid', 'time', 'yufujin', 'tiqian60', 'changgui', 'zong')
    ordering = ('bid',)


@admin.register(Moneynotes)
class MoneynotesAdmin(admin.ModelAdmin):
    list_display = ('bid', 'time', 'income')
    ordering = ('bid',)


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ('now_field', 'usercredit', 'name', 'roomid', 'arrivetime', 'leavetime', 'datediffer', 'paytime', 'money')
    ordering = ('roomid',)
    actions = ['print', ]

    @admin.action(permissions=['view'], description='打印')
    def print(self, request, queryset):
        pass
    print.style = 'color:black;'
    print.layer = {
       'title': '是否打印?',
       'tips': '当前机器-VOX01',
        # 确认按钮显示文本
        'confirm_button': '确定',
        # 取消按钮显示文本
        'cancel_button': '取消',
    }
