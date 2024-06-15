from django.urls import path, include

from . import views

app_name = "quotes"

urlpatterns = [
    path('', views.main, name="root"),
    path('quotes/', views.main, name="quotes"),
    path('<int:page>', views.main, name="root_paginate"),
    path('users/', include('users.urls')),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('delete/<int:quote_id>/', views.delete_quote, name='delete_quote'),
    path("show_author/<int:author_id>", views.show_author, name="show_author"),
]

