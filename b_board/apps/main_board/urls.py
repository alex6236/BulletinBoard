from django import views
from django.urls import path
from .views import (AdListView, AdDetailView, 
    CategoryAdListView, AdCreateView, 
    AdUpdateView, AdDeleteView, 
    AuthorAdsListView, SearchHeaderView, 
    AllAdAuthorView, ReplyDeleteView, 
    ReplyPublishView, DraftListView, 
    DraftDetailView, DraftDeleteView, 
    DraftUpdateView, subscription_view, 
    unsubscribe_user, subscribe_category, 
    ad_like_user)


urlpatterns = [
    path('', AdListView.as_view(), name='ad_list'),
    path('ad_list/ad_create/', AdCreateView.as_view(), name='ad_create'),
    path('ad_list/<str:slug>/ad_update/', AdUpdateView.as_view(), name='ad_update'),
    path('ad_list/<str:slug>/ad_delete/', AdDeleteView.as_view(), name='ad_delete'),
    path('ad_list/<str:slug>/', AdDetailView.as_view(), name='ad_detail'),
    path('draft_list/', DraftListView.as_view(), name='draft_list'),
    path('draft_list/<str:slug>/', DraftDetailView.as_view(), name='draft_detail'),
    path('draft_list/<str:slug>/ad_update/', DraftUpdateView.as_view(), name='draft_update'),
    path('draft_list/<str:slug>/ad_delete/', DraftDeleteView.as_view(), name='draft_delete'),
    path('subscribe_list/', subscription_view, name='subscribe_list'),
    # =======================================
    path('reply_publish/<int:pk>/', ReplyPublishView.as_view(), name='reply_publish'),
    path('reply_delete/<int:pk>/', ReplyDeleteView.as_view(), name='reply_delete'),
    # ===========================
    path('category/<str:category_slug>/', CategoryAdListView.as_view(), name='category'),
    path('ad_author/', AuthorAdsListView.as_view(), name='ad_author'),
    path('subscribe/', subscribe_category, name='subscribe'),
    path('unsubscribe/', unsubscribe_user, name='unsubscribe'),
    path('search_header/', SearchHeaderView.as_view(), name='search_header'),
    path('all_ad_author/<int:author_id>/', AllAdAuthorView.as_view(), name='all_ad_author'),
    path('ad-like/<str:slug>', ad_like_user, name="ad_like"),
]

