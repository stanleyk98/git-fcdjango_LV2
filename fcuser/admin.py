from django.contrib import admin
from .models import Fcuser
# 만든앱의 클래스 내 속성을 받아야 하기때문에 ...

# Register your models here.


class FcuserAdmin(admin.ModelAdmin):
    list_display = ('email', )


admin.site.register(Fcuser, FcuserAdmin)
