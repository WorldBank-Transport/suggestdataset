from django import template
from newsletter.models import Submission, Article


register = template.Library()


@register.assignment_tag
def get_newsletter_submissions(limit=5, order_by='-publish_date'):
    return Submission.objects\
        .filter(sent=True)\
        .prefetch_related('message', 'newsletter')\
        .order_by(order_by)[:limit]
