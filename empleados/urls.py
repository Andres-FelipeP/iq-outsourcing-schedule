from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.registrar, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home_admin/', views.home_admin, name='home_admin'),
    path('home_empleado/', views.home_empleado, name='home_empleado'),
    path('empleados/', views.usuarios_list, name='empleados'),
    path('editar_empleado/<int:usuario_id>/', views.editar_usuario, name='editar_empleado'),
    path('eliminar_empleado/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_empleado'),
    path('calendario_reservas', views.calendario, name='calendario_reservas'),
    path('mis_reservas/', views.mis_reservas, name='mis_reservas'),
    path('eliminar_reserva/<int:id>/', views.eliminar_reserva, name='eliminar_reserva'),

]
