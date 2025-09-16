from django.urls import path
from .views import (APIHomeView,StoryGenerateView, ArtisanCreateView, TestEndpointsView, AssessmentsListCreateView, AssessmentsDetailView,
    HeritageNodesListCreateView, HeritageNodesDetailView,
    MentorshipMatchesListCreateView, MentorshipMatchesDetailView,
    ProductsListCreateView, ProductsDetailView,
    StoryDraftsListCreateView, StoryDraftsDetailView,TestCollectionsView
)

urlpatterns=[
    path('', APIHomeView.as_view(), name='api-home'),
    path('test/', TestEndpointsView.as_view(), name='test-endpoints'),
    path('stories/generate/', StoryGenerateView.as_view(), name='story-generate'),
    path('artisans/create/', ArtisanCreateView.as_view(), name='artisan-create'),
    path('assessments/', AssessmentsListCreateView.as_view(), name='assessments-list-create'),
    path('assessments/<str:doc_id>/', AssessmentsDetailView.as_view(), name='assessments-detail'),
    path('heritage_nodes/', HeritageNodesListCreateView.as_view(), name='heritage-nodes-list-create'),
    path('heritage_nodes/<str:doc_id>/', HeritageNodesDetailView.as_view(), name='heritage-nodes-detail'),
    path('mentorship_matches/', MentorshipMatchesListCreateView.as_view(), name='mentorship-matches-list-create'),
    path('mentorship_matches/<str:doc_id>/', MentorshipMatchesDetailView.as_view(), name='mentorship-matches-detail'),
    path('products/', ProductsListCreateView.as_view(), name='products-list-create'),
    path('products/<str:doc_id>/', ProductsDetailView.as_view(), name='products-detail'),
    path('story_drafts/', StoryDraftsListCreateView.as_view(), name='story-drafts-list-create'),
    path('story_drafts/<str:doc_id>/', StoryDraftsDetailView.as_view(), name='story-drafts-detail'),
    path('test_collections/', TestCollectionsView.as_view(), name='test-collections'),
]