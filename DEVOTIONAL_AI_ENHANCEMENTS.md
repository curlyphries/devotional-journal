# Devotional Journal AI Enhancements

## Overview
This document summarizes the AI-powered devotional generation and auditing enhancements made to the Devotional Journal application.

## Features Implemented

### 1. On-Demand Devotional Generation
- **Endpoint**: `POST /api/reflections/passages/generate_on_demand/`
- **Purpose**: Generate devotional content instantly for any topic
- **Features**:
  - Topic-based generation
  - Theme extraction
  - Scripture passage curation
  - Reflection prompts and application suggestions

### 2. Daily Scheduled Devotional Generation
- **Task**: `reflections.generate_daily_devotionals`
- **Schedule**: Daily at 5:00 AM
- **Features**:
  - Automatic generation for active focus intentions
  - Prevents duplicate generation
  - Tracks sequence numbers

### 3. Devotional Accuracy Auditing
- **Task**: `reflections.audit_devotional_accuracy`
- **Schedule**: Daily at 11:00 PM
- **Features**:
  - Scripture reference verification
  - Accuracy scoring (0.0-1.0)
  - Relevance scoring based on theme matching
  - Automatic flagging of issues

### 4. DevotionalAudit Model
- **Purpose**: Track AI accuracy and user feedback
- **Fields**:
  - Scripture accuracy score
  - Relevance score
  - User rating (1-5)
  - User feedback
  - Manual review status
  - Theological accuracy flag

### 5. User Feedback System
- **Endpoint**: `POST /api/reflections/passages/{id}/provide_feedback/`
- **Features**:
  - User ratings (1-5 stars)
  - Written feedback
  - Issue reporting
  - Automatic flagging for review

## API Usage Examples

### Generate On-Demand Devotional
```bash
POST /api/reflections/passages/generate_on_demand/
{
  "topic": "Finding peace in difficult times",
  "themes": ["peace", "trials", "faith"]
}
```

### Provide Feedback
```bash
POST /api/reflections/passages/{passage_id}/provide_feedback/
{
  "rating": 5,
  "feedback": "This devotional really spoke to my situation",
  "reported_issue": ""
}
```

## Celery Task Schedule
```python
# Daily devotional generation - Every day at 5:00 AM
'generate-daily-devotionals': {
    'task': 'reflections.generate_daily_devotionals',
    'schedule': crontab(hour=5, minute=0),
},

# Devotional accuracy audit - Daily at 11:00 PM
'audit-devotional-accuracy': {
    'task': 'reflections.audit_devotional_accuracy',
    'schedule': crontab(hour=23, minute=0),
},
```

## Accuracy Verification
The system uses multiple methods to ensure devotional accuracy:

1. **Scripture Verification**: Cross-references with trusted Bible APIs
2. **Theme Relevance**: Calculates how well content matches user intentions
3. **User Feedback**: Collects ratings and reports
4. **Manual Review**: Flags problematic content for human review

## Admin Review Interface

### Audit Dashboard
```bash
GET /api/reflections/admin/audits/dashboard/
# Returns statistics on audit status, accuracy scores, and issues
```

### Review Flagged Passages
```bash
GET /api/reflections/admin/audits/flagged_passages/
# Returns all flagged passages grouped by issue type
```

### Submit Manual Review
```bash
POST /api/reflections/admin/audits/{audit_id}/review/
{
  "theological_accuracy": true,
  "review_notes": "Verified accurate interpretation",
  "status": "verified",
  "corrected_content": null,
  "apply_corrections": false
}
```

### Bulk Review
```bash
POST /api/reflections/admin/audits/bulk_review/
{
  "audit_ids": ["uuid1", "uuid2"],
  "action": "verify",
  "notes": "Batch verified after manual check"
}
```

### Quality Report
```bash
GET /api/reflections/admin/quality-report/?days=30
# Returns comprehensive quality metrics and recommendations
```

## Database Migration
Run the migration to create the DevotionalAudit table:
```bash
cd backend
python manage.py migrate reflections
```

## Future Enhancements
- Machine learning to improve relevance scoring
- Integration with more Bible translation APIs
- Export devotionals to PDF/email
- Community sharing of highly-rated devotionals
- Real-time accuracy checking during generation
- A/B testing for different AI prompts

## Technical Notes
- Uses CrewAI's DevotionalCurator agent for content generation
- Integrates with existing Bible text verification system
- Audit data stored in PostgreSQL with JSON fields
- Asynchronous processing via Celery for scalability
- Admin endpoints require IsAdminUser permission
