from django.urls import path
from asset import views
from asset import api

urlpatterns = [
    path('asset.html', views.AssetListAll.as_view(), name='asset_list'),
    path('asset-add.html', views.AssetAdd.as_view(), name='asset_add'),
    path('asset-all-del.html', views.AssetAllDel.as_view(), name='asset_all_del'),
    path('asset-detail-<int:pk>.html', views.AssetDetail.as_view(), name='asset_detail'),
    path('asset-update-<int:pk>.html', views.AssetUpdate.as_view(), name='asset_update'),

    path('asset-ztree.html', views.AssetZtree, name='asset_ztree'),

    path('api/asset.html', api.AssetList.as_view(), name='asset_api_list'),
    path('api/asset-detail-<int:pk>.html', api.AssetDetail.as_view(), name='asset_api_detail'),

    path('asset-user.html', views.AssetUserListAll.as_view(), name='asset_user_list'),
    path('asset-user-add.html', views.AssetUserAdd.as_view(), name='asset_user_add'),
    path('asset-user-all-del.html', views.AssetUserAllDel.as_view(), name='asset_user_all_del'),
    path('asset-user-detail-<int:pk>.html', views.AssetUserDetail.as_view(), name='asset_user_detail'),
    path('asset-user-update-<int:pk>.html', views.AssetUserUpdate.as_view(), name='asset_user_update'),

    path('asset-user-asset-<int:pk>.html', views.AssetUserAsset, name='asset_user_asset'),

    path('asset-webssh.html', views.AssetWeb.as_view(), name='asset_web'),
    path('asset-hardware-update.html', views.AssetHardwareUpdate.as_view(), name='asset_hardware_update'),
]

app_name = "asset"
