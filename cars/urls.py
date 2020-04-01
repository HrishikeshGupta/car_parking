from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    path('create', views.parking_create_view),
    path('exit_car', views.exit_car),
    path('search_by_colour', views.search_by_colour),
    path('view_result_reg_source', views.view_result_reg_source),
    path('search_by_reg_number', views.search_by_reg_number),
    path('auto_generate', views.auto_generate),
    path('view_result', views.view_result),
    path('get_total_count_of_cars',views.get_total_count_of_cars),
    path('get_total_income',views.get_total_income),
    path('test',views.test),
    path('test_001',views.test),
    path('about',views.about),
    path('contactus',views.contactus),
    path('get_slot_details',views.get_slot_details),
    ]
