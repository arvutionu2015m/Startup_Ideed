from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('regenerate/<int:idea_id>/', views.regenerate_idea, name='regenerate_idea'),
    path('qr/<uuid:public_id>/', views.generate_qr, name='generate_qr'),
    path('idea/<uuid:public_id>/', views.public_idea_view, name='public_idea'),
    path('export/csv/', views.export_ideas_csv, name='export_ideas_csv'),
    path('export/pdf/', views.export_ideas_pdf, name='export_ideas_pdf'),
    path('generate/', views.generate_idea, name='generate_idea'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my-ideas/', views.my_ideas, name='my_ideas'),  # 👈 see rida lisandub
]
