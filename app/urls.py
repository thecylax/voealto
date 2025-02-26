from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit/', views.budget_submit, name='submit_form'),
    path('submit/<str:budget_id>/', views.budget_submit, name='budget_submit'),
    path('history/', views.history, name='list'),
    path('detail/<str:budget_id>/', views.budget_detail, name='budget_detail'),
    path('render_pdf/<str:budget_id>/', views.render_pdf, name='render_pdf'),
    path('client/', views.client_view, name='client_view'),
    path('client/create', views.client_create, name='client_create'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('foo/', views.budget_formset, name='formset'),
    path('foo/', views.create_budget_item, name='create_budget_item'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)