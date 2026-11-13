from django.urls import path

from . import views

urlpatterns = [
    path("catalog/", views.CatalogView.as_view(), name="guides-catalog"),
    path(
        "recommendations/",
        views.RecommendationsView.as_view(),
        name="guides-recommendations",
    ),
    # Studies
    path("studies/", views.StudyListView.as_view(), name="guides-studies"),
    path(
        "studies/<uuid:study_id>/", views.StudyDetailView.as_view(), name="guides-study"
    ),
    path(
        "studies/<uuid:study_id>/lessons/<int:number>/",
        views.LessonView.as_view(),
        name="guides-lesson",
    ),
    path(
        "studies/<uuid:study_id>/lessons/<int:number>/respond/",
        views.LessonRespondView.as_view(),
        name="guides-lesson-respond",
    ),
    path(
        "studies/<uuid:study_id>/lessons/<int:number>/simplify/",
        views.LessonSimplifyView.as_view(),
        name="guides-lesson-simplify",
    ),
    path(
        "studies/<uuid:study_id>/lessons/<int:number>/personalize/",
        views.LessonPersonalizeView.as_view(),
        name="guides-lesson-personalize",
    ),
    # Growth profile
    path("profile/", views.ProfileView.as_view(), name="guides-profile"),
    path(
        "profile/assessment/",
        views.ProfileAssessmentView.as_view(),
        name="guides-assessment",
    ),
    path(
        "profile/insights/", views.ProfileInsightsView.as_view(), name="guides-insights"
    ),
    path(
        "profile/insights/<str:insight_id>/feedback/",
        views.ProfileInsightFeedbackView.as_view(),
        name="guides-insight-feedback",
    ),
    # Growth plans
    path("plans/", views.PlanListView.as_view(), name="guides-plans"),
    path("plans/<uuid:plan_id>/", views.PlanDetailView.as_view(), name="guides-plan"),
    path(
        "plans/<uuid:plan_id>/goals/",
        views.PlanGoalsView.as_view(),
        name="guides-plan-goals",
    ),
    path(
        "plans/<uuid:plan_id>/goals/<uuid:goal_id>/",
        views.PlanGoalDetailView.as_view(),
        name="guides-plan-goal",
    ),
    path(
        "plans/<uuid:plan_id>/checkins/",
        views.PlanCheckInsView.as_view(),
        name="guides-plan-checkins",
    ),
]
