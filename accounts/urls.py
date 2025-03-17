from django.urls import path
from .views import register, login , add_crop ,product_list ,product_detail ,user_info ,update_crop,delete_crop

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login, name="login"),
    path("add_crop/", add_crop, name="add-crop"),
    path("products/", product_list, name="product-list"),
    path('product/<slug:slug>/', product_detail, name='product-detail-slug'),
    path("user_info",user_info,name="user_info"),
    path('crop_update/<int:crop_id>/', update_crop, name='update_crop'), 
    path('crop_delete/<int:crop_id>/', delete_crop, name='delete_crop'),  
]


