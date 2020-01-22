from django.http import Http404
from django.shortcuts import render
from django.core.paginator import Paginator
from qsstats import QuerySetStats
from django.db.models import Sum

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from datetime import datetime, timedelta
from .models import User, Statistic
from .serializers import UsersSerializer, StatisticUsersSerializer

USERS_PAGE = 50


class UsersView(APIView):
    def get(self, request, pk=None):
        if pk:
            user = User.objects.filter(id=pk)
            serializer = UsersSerializer(user, many=True)
        else:
            users = User.objects.all()[:10]
            serializer = UsersSerializer(users, many=True)
        return Response({'user': serializer.data})

    def post(self, request):
        user = request.data.get('user')
        serializer = UsersSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        return Response({'success': f'User {user_saved.id} created successfully'})

    def put(self, request, pk):
        saved_user = get_object_or_404(User.objects.all(), pk=pk)
        data = request.data.get('user')
        serializer = UsersSerializer(instance=saved_user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user_saved = serializer.save()
        return Response({'success': f'User {user_saved.id} updated successfully'})

    def delete(self, request, pk):
        user = get_object_or_404(User.objects.all(), pk=pk)
        user.delete()
        return Response({'message': f'User with id {pk} has been deleted.'}, status=204)


class StatisticUsersView(APIView):
    def get(self, request, pk=None):
        if pk:
            user = Statistic.objects.filter(user=pk)
            serializer = StatisticUsersSerializer(user, many=True)
        else:
            users = Statistic.objects.all()[:10]
            serializer = StatisticUsersSerializer(users, many=True)
        return Response({'statistic': serializer.data})

    def post(self, request):
        statistic_user = request.data.get('statistic')
        serializer = StatisticUsersSerializer(data=statistic_user)
        if serializer.is_valid(raise_exception=True):
            statistic_user_saved = serializer.save()
        return Response({'success': f'Statistic {statistic_user_saved.id} created successfully'})

    def put(self, request, pk):
        saved_statistic_users = get_object_or_404(Statistic.objects.all(), pk=pk)
        data = request.data.get('statistic')
        serializer = StatisticUsersSerializer(instance=saved_statistic_users, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            statistic_users_saved = serializer.save()
        return Response({'success': f'Statistic {statistic_users_saved.id} updated successfully'})

    def delete(self, request, pk):
        statistic_users = get_object_or_404(Statistic.objects.all(), pk=pk)
        statistic_users.delete()
        return Response({'message': f'Statistic with id {pk} has been deleted.'}, status=204)


def list(request):
    users_list = User.objects.order_by('id')
    paginator = Paginator(users_list, USERS_PAGE)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = f'?page={page.previous_page_number()}'
    else:
        prev_url = ''

    if page.has_next():
        next_url = f'?page={page.next_page_number()}'
    else:
        next_url = ''

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'prev_url': prev_url,
        'next_url': next_url
    }

    return render(request, 'users/list.html', context=context)


def detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        statistic = Statistic.objects.filter(user=user_id)

        if 'start' in request.GET and request.GET['start'] and 'end' in request.GET and request.GET['end']:
            start_date = datetime.strptime(request.GET['start'], '%Y-%m-%d').date()
            end_date = datetime.strptime(request.GET['end'], '%Y-%m-%d').date()
        else:
            end_date = Statistic.get_end_date(user_id=user_id)
            start_date = end_date - timedelta(days=6)

        qsstats_page_views = QuerySetStats(statistic, date_field='date', aggregate=Sum('page_views'))
        charts_page_views = qsstats_page_views.time_series(start_date, end_date, interval='days')

        qsstats_clicks = QuerySetStats(statistic, date_field='date', aggregate=Sum('clicks'))
        charts_clicks = qsstats_clicks.time_series(start_date, end_date, interval='days')


        context = {
            'user': user,
            'statistic': statistic,
            'start_date': start_date,
            'end_date': end_date,
            'charts_page_views': charts_page_views,
            'charts_clicks': charts_clicks
        }
    except:
        raise Http404('User is not found.')
    return render(request, 'users/detail.html', context=context)
