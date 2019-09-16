from django.contrib import admin
from login.models import User

# Register your models here.
# 在admin中进行注册，请求将polls的模型加入站点内接受站点管理

admin.site.register(User)