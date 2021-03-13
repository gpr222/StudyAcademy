from django.contrib import admin
from django.urls import path, include
from courses.views import home, coursePage, signupView, loginView, signout, checkout, verifyPayment, my_courses
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home, name='home'),
    path('logout', signout, name='logout'),
    path('my_courses', my_courses, name='my_courses'),
    path('checkout/<str:slug>', checkout, name='checkout'),
    path('signup', signupView.as_view(), name='signup'),
    path('login', loginView.as_view(), name='login'),
    path('course/<str:slug>', coursePage, name='coursepage'),
    path('verify_payment', verifyPayment, name='verify_payment'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
