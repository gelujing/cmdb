from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.decorators import login_required
from .form import  AssetForm, AssetUserForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, ListView, View, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.conf import settings
from django.db.models import Q
from asset.models import AssetInfo, AssetLoginUser
from chain import settings
from index.password_crypt import encrypt_p, decrypt_p
from os import system
import json
import logging


logger = logging.getLogger('asset')



class AssetListAll(LoginRequiredMixin, ListView):
    """资产列表"""
    template_name = 'asset/asset.html'
    paginate_by = settings.DISPLAY_PER_PAGE
    model = AssetInfo
    context_object_name = "asset_list"
    queryset = AssetInfo.objects.all()
    ordering = ('id',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_data = self.request.GET.copy()
        try:
            search_data.pop("page")
        except BaseException as e:
            logger.error(e)

        context.update(search_data.dict())
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
            "search_data": search_data.urlencode(),
            "web_ssh": getattr(settings, 'web_ssh'),
            "web_port": getattr(settings, 'web_port'),
        }
        kwargs.update(context)

        return super().get_context_data(**kwargs)

    def get_queryset(self):
        """
         资产查询功能
        :return:
        """
        self.queryset = super().get_queryset()
        if self.request.GET.get('name'):
            query = self.request.GET.get('name', None)
            queryset = self.queryset.filter(Q(network_ip=query) | Q(hostname=query) | Q(
                inner_ip=query) | Q(project=query) | Q(manager=query)).order_by('-id')
        else:
            queryset = super().get_queryset()
        return queryset


class AssetAdd(LoginRequiredMixin, CreateView):
    """资产增加"""
    model = AssetInfo
    form_class = AssetForm
    template_name = 'asset/asset-add-update.html'
    success_url = reverse_lazy('asset:asset_list')

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
        }

        try:
            context['i__next__'] = self.request.META['HTTP_REFERER']
        except Exception as e:
            logger.error(e)
        kwargs.update(context)

        return super().get_context_data(**kwargs)



class AssetUpdate(LoginRequiredMixin, UpdateView):
    """资产更新"""

    model = AssetInfo
    form_class = AssetForm
    template_name = 'asset/asset-add-update.html'
    success_url = reverse_lazy('asset:asset_list')
    def get_context_data(self, **kwargs):

        context = {
            "asset_active": "active",
            "asset_list_active": "active",
        }


        try:
            context['i__next__'] = self.request.META['HTTP_REFERER']
        except Exception as e:
            logger.error(e)

        kwargs.update(context)
        print(context)
        print(super().get_context_data(**kwargs))

        return super().get_context_data(**kwargs)

    def get_success_url(self):
        self.url = self.request.POST['__next__']
        print('111111111111111',self.request.POST)
        return self.url


class AssetDetail(LoginRequiredMixin, DetailView):
    """
     资产详细
    """
    model = AssetInfo
    form_class = AssetForm
    template_name = 'asset/asset-detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = AssetInfo.objects.get(id=pk)
        # varall = Variable.objects.filter(assets=pk).values()
        context = {
            "asset_active": "active",
            "asset_list_active": "active",
            "assets": detail,
            "nid": pk,
            # "vars": varall,

        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AssetAllDel(LoginRequiredMixin, View):
    """
    资产删除
    """
    model = AssetInfo

    @staticmethod
    def post(request):
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('nid'):
                ids = request.POST.get('nid', None)
                AssetInfo.objects.get(id=ids).delete()
            else:
                ids = request.POST.getlist('id', None)
                idstring = ','.join(ids)
                AssetInfo.objects.extra(
                    where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,没有权限{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))


class AssetHardwareUpdate(LoginRequiredMixin, View):
    """
    资产硬件 异步更新
    """
    model = AssetInfo

    @staticmethod
    def post(request):
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('nid'):
                ids = request.POST.get('nid', None)
                asset_obj = AssetInfo.objects.get(id=ids)
                try:
                    asset_obj.user.hostname
                except Exception as e:
                    logger.error(e)
                    ret['status'] = False
                    ret['error'] = '未关联用户，请关联后再更新'.format(e)
                    return HttpResponse(json.dumps(ret))

                assets = [{"hostname": asset_obj.hostname,
                           "ip": asset_obj.network_ip,
                           "port": asset_obj.port,
                           "username": asset_obj.user.username,
                           "password": decrypt_p(asset_obj.user.password),
                           "private_key": asset_obj.user.private_key.name
                           }]
                # ansbile_asset_hardware.delay(ids, assets)

        except Exception as e:
            logger.error(e)
            ret['status'] = False
            ret['error'] = '获取资产信息错误{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))




@login_required
def AssetZtree(request):
    """
    获取 区域 资产树 的相关数据
    :param request:
    :return:
    """

    manager = AssetInfo.objects.values("project").distinct()
    data = [{"id": "1111", "pId": "0", "name": "项目"}, ]
    for i in manager:
        data.append({"id": i['project'], "pId": "1111",
                     "name": i['project'], "page": "xx.action"}, )
    return HttpResponse(json.dumps(data), content_type='application/json')


class AssetUserListAll(LoginRequiredMixin, ListView):
    """
    登录用户列表
    """
    template_name = 'asset/asset-user.html'
    paginate_by = settings.DISPLAY_PER_PAGE
    model = AssetLoginUser
    context_object_name = "asset_user_list"
    queryset = AssetLoginUser.objects.all()
    ordering = ('id',)

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_user_list_active": "active",

        }
        kwargs.update(context)

        return super().get_context_data(**kwargs)


class AssetUserAdd(LoginRequiredMixin, CreateView):
    """
    登录用户增加
    """
    model = AssetLoginUser
    form_class = AssetUserForm
    template_name = 'asset/asset-user-add-update.html'
    success_url = reverse_lazy('asset:asset_user_list')

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_user_list_active": "active",
        }
        kwargs.update(context)
        print(super().get_context_data(**kwargs))
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        forms = form.save()
        password_form = form.cleaned_data['password']
        if password_form is not None:
            password = encrypt_p(password_form)
            forms.password = password
            forms.save()

        name = form.cleaned_data['hostname']
        obj = AssetLoginUser.objects.get(hostname=name).private_key.name
        system("chmod  600  {0}".format(obj))
        return super().form_valid(form)


class AssetUserUpdate(LoginRequiredMixin, UpdateView):
    """登录用户更新"""

    model = AssetLoginUser
    form_class = AssetUserForm
    template_name = 'asset/asset-user-add-update.html'
    success_url = reverse_lazy('asset:asset_user_list')

    def get_context_data(self, **kwargs):
        context = {
            "asset_active": "active",
            "asset_user_list_active": "active",
        }
        kwargs.update(context)
        print(super().get_context_data(**kwargs))
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        obj = AssetLoginUser.objects.get(id=pk)

        old_password = obj.password
        new_password = form.cleaned_data['password']
        forms = form.save()

        if new_password is None:
            forms.password = old_password
        else:
            password = encrypt_p(new_password)
            forms.password = password

        forms.save()
        name = form.cleaned_data['hostname']
        obj = AssetLoginUser.objects.get(hostname=name).private_key.name
        system("chmod  600  {0}".format(obj))


        return super().form_valid(form)


class AssetUserDetail(LoginRequiredMixin, DetailView):
    """
    登录用户详细
    """
    model = AssetLoginUser
    template_name = 'asset/asset-user-detail.html'

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        detail = AssetLoginUser.objects.get(id=pk)

        context = {
            "asset_active": "active",
            "asset_user_list_active": "active",
            "assets": detail,
            "nid": pk,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


def AssetUserAsset(request, pk):
    obj = AssetInfo.objects.filter(user=pk)
    return render(request, "asset/asset-user-asset.html",
                  {"nid": pk, "assets_list": obj,
                   "asset_active": "active",
                   "asset_user_list_active": "active"})


class AssetUserAllDel(LoginRequiredMixin, View):
    """
    登录用户删除
    """
    model = AssetLoginUser

    @staticmethod
    def post(request):
        ret = {'status': True, 'error': None, }
        try:
            if request.POST.get('nid'):
                ids = request.POST.get('nid', None)
                AssetLoginUser.objects.get(id=ids).delete()
            else:
                ids = request.POST.getlist('id', None)
                idstring = ','.join(ids)
                AssetLoginUser.objects.extra(
                    where=['id IN (' + idstring + ')']).delete()
        except Exception as e:
            ret['status'] = False
            ret['error'] = '删除请求错误,没有权限{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))


class AssetWeb(LoginRequiredMixin, View):
    """
    终端登录
    """

    @staticmethod
    def post(request, ):
        ret = {'status': True, }
        try:
            ids = request.POST.get('id', None)
            obj = AssetInfo.objects.get(id=ids)

            ip = obj.network_ip
            port = obj.port
            username = obj.user.username
            password = obj.user.password
            try:
                privatekey = obj.user.private_key.path
            except Exception as e:
                logger.error(e)
                privatekey = None

            ret.update({"ip": ip, 'port': port, "username": username,
                        'password': password,"privatekey": privatekey})
            print(ret)
        except Exception as e:
            logger.error(e)
            ret['status'] = False
            ret['error'] = '请求错误,{}'.format(e)
        finally:
            return HttpResponse(json.dumps(ret))
