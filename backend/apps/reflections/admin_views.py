"""
Admin views for devotional content review and management.
"""

import logging
from datetime import timedelta

from django.db.models import Avg, Q
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import DevotionalAudit, DevotionalPassage

logger = logging.getLogger(__name__)


class DevotionalAuditViewSet(viewsets.ModelViewSet):
    """
    Admin viewset for reviewing and managing devotional audits.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        queryset = DevotionalAudit.objects.select_related(
            "devotional_passage",
            "devotional_passage__user",
            "devotional_passage__focus_intention",
            "reviewed_by",
        )

        # Filter by status
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(audit_status=status_filter)

        # Filter by date range
        days = self.request.query_params.get("days", 7)
        try:
            days = int(days)
            start_date = timezone.now().date() - timedelta(days=days)
            queryset = queryset.filter(created_at__date__gte=start_date)
        except ValueError:
            pass

        # Filter by accuracy threshold
        accuracy = self.request.query_params.get("min_accuracy")
        if accuracy:
            try:
                min_accuracy = float(accuracy)
                queryset = queryset.filter(
                    Q(scripture_accuracy_score__lt=min_accuracy)
                    | Q(relevance_score__lt=min_accuracy)
                )
            except ValueError:
                pass

        return queryset.order_by("-created_at")

    def get_serializer_class(self):
        from .serializers import DevotionalAuditSerializer

        return DevotionalAuditSerializer

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        """Get audit dashboard statistics."""
        days = int(request.query_params.get("days", 30))
        start_date = timezone.now().date() - timedelta(days=days)

        audits = DevotionalAudit.objects.filter(created_at__date__gte=start_date)

        stats = {
            "total_audits": audits.count(),
            "pending_reviews": audits.filter(audit_status="pending").count(),
            "flagged_issues": audits.filter(audit_status="flagged").count(),
            "verified_accurate": audits.filter(audit_status="verified").count(),
            "manually_corrected": audits.filter(audit_status="corrected").count(),
            "average_scripture_accuracy": audits.aggregate(
                avg=Avg("scripture_accuracy_score")
            )["avg"]
            or 0,
            "average_relevance_score": audits.aggregate(avg=Avg("relevance_score"))[
                "avg"
            ]
            or 0,
            "average_user_rating": audits.filter(user_rating__isnull=False).aggregate(
                avg=Avg("user_rating")
            )["avg"]
            or 0,
            "issues_by_type": self._categorize_issues(audits),
        }

        return Response(stats)

    def _categorize_issues(self, audits):
        """Categorize issues found in audits."""
        issues = {
            "scripture_accuracy": 0,
            "relevance": 0,
            "user_reported": 0,
            "parsing_errors": 0,
        }

        for audit in audits.filter(audit_status="flagged"):
            if audit.scripture_accuracy_score and audit.scripture_accuracy_score < 0.8:
                issues["scripture_accuracy"] += 1
            if audit.relevance_score and audit.relevance_score < 0.5:
                issues["relevance"] += 1
            if audit.reported_issue:
                issues["user_reported"] += 1
            if "Could not parse" in " ".join(audit.scripture_warnings):
                issues["parsing_errors"] += 1

        return issues

    @action(detail=True, methods=["post"])
    def review(self, request, pk=None):
        """Submit a manual review for a devotional."""
        audit = self.get_object()

        theological_accuracy = request.data.get("theological_accuracy")
        review_notes = request.data.get("review_notes", "")
        corrected_content = request.data.get("corrected_content")
        new_status = request.data.get("status")

        # Update audit record
        audit.reviewed_by = request.user
        audit.reviewed_at = timezone.now()

        if theological_accuracy is not None:
            audit.theological_accuracy = theological_accuracy

        if review_notes:
            audit.review_notes = review_notes

        if corrected_content:
            audit.corrected_content = corrected_content
            audit.audit_status = "corrected"
        elif new_status in ["verified", "flagged"]:
            audit.audit_status = new_status

        audit.save()

        # If content was corrected, optionally update the original passage
        if corrected_content and request.data.get("apply_corrections", False):
            passage = audit.devotional_passage
            for field, value in corrected_content.items():
                if hasattr(passage, field):
                    setattr(passage, field, value)
            passage.save()

        serializer = self.get_serializer(audit)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def flagged_passages(self, request):
        """Get all flagged passages requiring review."""
        flagged = (
            self.get_queryset()
            .filter(audit_status="flagged")
            .select_related("devotional_passage")
        )

        # Group by issue type
        grouped = {
            "low_accuracy": [],
            "user_reported": [],
            "parsing_errors": [],
            "low_relevance": [],
        }

        for audit in flagged:
            if audit.scripture_accuracy_score and audit.scripture_accuracy_score < 0.8:
                grouped["low_accuracy"].append(audit)
            if audit.reported_issue:
                grouped["user_reported"].append(audit)
            if "Could not parse" in " ".join(audit.scripture_warnings):
                grouped["parsing_errors"].append(audit)
            if audit.relevance_score and audit.relevance_score < 0.5:
                grouped["low_relevance"].append(audit)

        serializer = self.get_serializer
        return Response(
            {
                "total_flagged": flagged.count(),
                "by_issue_type": {
                    issue_type: serializer(passages, many=True).data
                    for issue_type, passages in grouped.items()
                },
            }
        )

    @action(detail=False, methods=["post"])
    def bulk_review(self, request):
        """Bulk review multiple devotionals."""
        audit_ids = request.data.get("audit_ids", [])
        action_type = request.data.get("action")
        notes = request.data.get("notes", "")

        if not audit_ids or not action_type:
            return Response(
                {"error": "audit_ids and action are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        audits = DevotionalAudit.objects.filter(id__in=audit_ids)

        if action_type == "verify":
            audits.update(
                audit_status="verified",
                reviewed_by=request.user,
                reviewed_at=timezone.now(),
                review_notes=notes,
            )
        elif action_type == "flag":
            audits.update(
                audit_status="flagged",
                reviewed_by=request.user,
                reviewed_at=timezone.now(),
                review_notes=f"Bulk flagged: {notes}",
            )
        else:
            return Response(
                {"error": "Invalid action type"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({"updated": audits.count(), "action": action_type})


class DevotionalQualityReportView(APIView):
    """
    Generate quality reports for devotional content.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        """Generate a comprehensive quality report."""
        days = int(request.query_params.get("days", 30))
        start_date = timezone.now().date() - timedelta(days=days)

        # Get all devotionals with audits in date range
        audits = DevotionalAudit.objects.filter(
            created_at__date__gte=start_date
        ).select_related("devotional_passage")

        # Calculate metrics
        total_generated = DevotionalPassage.objects.filter(
            created_at__date__gte=start_date
        ).count()

        report = {
            "period": {
                "start": start_date.isoformat(),
                "end": timezone.now().date().isoformat(),
                "days": days,
            },
            "generation_stats": {
                "total_generated": total_generated,
                "total_audited": audits.count(),
                "audit_coverage": (
                    (audits.count() / total_generated * 100)
                    if total_generated > 0
                    else 0
                ),
            },
            "accuracy_metrics": {
                "average_scripture_accuracy": audits.aggregate(
                    avg=Avg("scripture_accuracy_score")
                )["avg"]
                or 0,
                "average_relevance_score": audits.aggregate(avg=Avg("relevance_score"))[
                    "avg"
                ]
                or 0,
                "passages_below_threshold": audits.filter(
                    Q(scripture_accuracy_score__lt=0.8) | Q(relevance_score__lt=0.5)
                ).count(),
            },
            "user_satisfaction": {
                "average_rating": audits.filter(user_rating__isnull=False).aggregate(
                    avg=Avg("user_rating")
                )["avg"]
                or 0,
                "total_ratings": audits.filter(user_rating__isnull=False).count(),
                "reported_issues": audits.filter(reported_issue__gt="").count(),
            },
            "review_status": {
                "pending": audits.filter(audit_status="pending").count(),
                "verified": audits.filter(audit_status="verified").count(),
                "flagged": audits.filter(audit_status="flagged").count(),
                "corrected": audits.filter(audit_status="corrected").count(),
            },
            "top_issues": self._get_top_issues(audits),
            "recommendations": self._generate_recommendations(audits),
        }

        return Response(report)

    def _get_top_issues(self, audits):
        """Identify the most common issues."""
        issues = []

        # Analyze scripture warnings
        warning_counts = {}
        for audit in audits:
            for warning in audit.scripture_warnings:
                warning_counts[warning] = warning_counts.get(warning, 0) + 1

        # Sort by frequency
        for warning, count in sorted(
            warning_counts.items(), key=lambda x: x[1], reverse=True
        )[:5]:
            issues.append(
                {
                    "type": "scripture_warning",
                    "description": warning,
                    "occurrences": count,
                }
            )

        return issues

    def _generate_recommendations(self, audits):
        """Generate recommendations based on audit data."""
        recommendations = []

        avg_accuracy = audits.aggregate(avg=Avg("scripture_accuracy_score"))["avg"] or 0
        if avg_accuracy < 0.85:
            recommendations.append(
                {
                    "priority": "high",
                    "area": "scripture_accuracy",
                    "recommendation": "Consider reviewing the scripture verification process. Average accuracy is below 85%.",
                }
            )

        avg_relevance = audits.aggregate(avg=Avg("relevance_score"))["avg"] or 0
        if avg_relevance < 0.7:
            recommendations.append(
                {
                    "priority": "medium",
                    "area": "relevance",
                    "recommendation": "Theme matching could be improved. Consider refining the AI prompts for better relevance.",
                }
            )

        flagged_ratio = (
            audits.filter(audit_status="flagged").count() / audits.count()
            if audits.count() > 0
            else 0
        )
        if flagged_ratio > 0.1:
            recommendations.append(
                {
                    "priority": "high",
                    "area": "quality_control",
                    "recommendation": f"{flagged_ratio*100:.1f}% of devotionals are flagged. Manual review process may need scaling.",
                }
            )

        return recommendations
