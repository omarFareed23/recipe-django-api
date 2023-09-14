from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
router.register('recipes', views.RecipeView)
router.register('tags', views.TagView)

app_name = 'recipe'
# import pdb; pdb.set_trace()
urlpatterns = [
    path('', include(router.urls))
]
