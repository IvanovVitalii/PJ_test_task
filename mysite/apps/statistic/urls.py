from django.urls import path
from . import views
from .views import UsersView, StatisticUsersView

app_name = 'statistic'
urlpatterns = [
    path('', views.list, name='list'),
    path('<int:user_id>/', views.detail, name='detail'),
    path('api/users/', UsersView.as_view()),
    path('api/users/<int:pk>', UsersView.as_view()),
    path('api/statistic-users/', StatisticUsersView.as_view()),
    path('api/statistic-users/<int:pk>', StatisticUsersView.as_view()),
]
