from django.shortcuts import render
from django.shortcuts import redirect
from login.models import User
from login.forms import UserForm, RegisterForm
import hashlib


def hash_code(s, salt='mysite'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

# Create your views here.


def index(request):
    pass
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect("/index/")
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(user_name=username)
                if user.user_pwd == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True  # 实际的用户数据和状态以Session会话的方式保存在服务器端
                    request.session['user_id'] = user.id  # 有了用户状态，就可以根据用户登录与否，展示不同的页面
                    request.session['user_name'] = user.user_name
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except User.DoesNotExist:
                message = "用户不存在！"
    login_form = UserForm()
    return render(request, 'login/login.html', locals())

# def login(request):
#     if request.method == "POST":
#         login_form = UserForm(request.POST)  # 表单直接“封装”好POST的信息
#         message = "请检查填写的内容！"
#         if login_form.is_valid():  # 一步完成数据验证工作
#             username = login_form.cleaned_data['username']
#             password = login_form.cleaned_data['password']
#             try:
#                 user = User.objects.get(user_name=username)
#                 if user.user_pwd == password:
#                     return redirect('/index/')
#                 else:
#                     message = "密码不正确！"
#             except User.DoesNotExist:
#                 message = "用户不存在！"
#         return render(request, 'login/login.html', locals())  # 如果验证不通过，则返回一个包含先前数据的表单给前端页面
#     login_form = UserForm()
#     return render(request, 'login/login.html', locals())  # locals()函数，返回当前所有的本地变量字典
#
# # def login(request):
# #     if request.method == "POST":
# #         username = request.POST.get('username', None)
# #         password = request.POST.get('password', None)
# #         message = "所有字段都必须填写！"
# #         if username and password:  # 确保用户名和密码都不为空
# #             username = username.strip()
# #             # 用户名字符合法性验证
# #             # 密码长度验证
# #             # 更多的其它验证.....
# #             try:
# #                 user = User.objects.get(user_name=username)
# #                 if user.user_pwd == password:
# #                     return redirect('/index/')
# #                 else:
# #                     message = "密码不正确！"
# #             except User.DoesNotExist:
# #                 message = "用户名不存在！"
# #         # message变量可将错误信息打包成一个字典，作为参数提供给render()方法，传递到模板里供调用显示。
# #         return render(request, 'login/login.html', {"message": message})
# #     return render(request, 'login/login.html')  #也可以用locals()函数，返回当前所有的本地变量字典


def register(request):
    if request.session.get('is_login', None):  # 登录状态不允许注册
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(user_name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(user_email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切正常的情况下，创建新用户
                new_user = User()
                new_user.user_name = username
                new_user.user_pwd = hash_code(password1)  # 使用加密密码！！！
                new_user.user_email = email
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()  # 一次性将session中的所有内容全部清空
    return redirect("/index/")