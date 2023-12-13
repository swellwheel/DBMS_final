from django.urls import path
from . import views
from .api_views import PersonalEvaluationAPIView
from .api_views import EvlueateAPIView
from .api_views import PostEvaluationAPIView

app_name = 'evaluate'
urlpatterns = [
    path('evaluate_detail/<int:user_id>', views.evaluate_detail, name='evaluate_detail'),
    path('api/personal_evaluation/<int:user_id>', PersonalEvaluationAPIView.as_view(), name='personal-evaluation-api'),
    path('api/evaluate/<int:user_id>', EvlueateAPIView.as_view(), name='evaluate-api'),
    path('api/post/<int:user_id>/<int:target_id>', PostEvaluationAPIView.as_view(), name='post-evaluation-api'),

]