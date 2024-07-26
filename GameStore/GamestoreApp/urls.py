from django.urls import path
from GamestoreApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.Anas),
    path("D",views.B),
    path('H',views.S),
    path('update/<rid>',views.Update),
    path('delete/<rid>',views.Delete),
    path('W',views.R),
    path('L',views.User_Login),
    path('LG',views.Logout),
    path('Cart/<rid>',views.Carty),
    path('P',views.RC),
    path('delete_cart/<rid>',views.T),
    path('update_cart/<rid>/<q>',views.Update_cart),
    path('create_order/<rid>',views.CO),
    path('RO',views.Read_O),
    path('RRO/<rid>',views.RRO2),
    path('RPD/<rid>',views.ReadPD1),
    path('FP2',views.FP1),
    path('Verification_OTP',views.OTP),
    path('NP',views.New_Password)
]


urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)