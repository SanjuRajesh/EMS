from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static
from . views import *
urlpatterns = [
    path('',views.home,name='home'),
    path('events/', views.events, name='events'),
    path('add_event',views.add_event,name='add_event'),
    path('search/', views.search_event, name='search_event'),
    path('report/', views.report_page, name='report_page'),
    path('add_report/', views.add_report, name='add_report'),
    path('search_report/', views.search_report, name='search_report'),
    path('duty_alloc/',views.duty_alloc , name='duty_alloc'),
    path('allocated_duty/',views.allocated_duty , name='allocated_duty'),
    path('add_allocation/',views.add_allocation , name='add_allocation'),
    path('add_dept_club/',views.add_dept_club , name='add_dept_club'),
    path('add_user/', views.add_user, name='add_user'),
    path('add_faculty/', views.add_faculty, name='add_faculty'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.confirm_delete, name='confirm_delete'),
    path('events/update_status/<int:event_id>/<str:status>/', update_event_status, name='update_event_status'),
    path('notification/',views.notification, name='notification'),
    path('delete_report/<int:report_id>/', views.delete_report, name='delete_report'),
    path('edit_report/<int:report_id>/', views.edit_report, name='edit_report'),
]