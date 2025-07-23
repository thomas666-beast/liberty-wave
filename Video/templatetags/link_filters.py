import bleach
from django import template
from django.utils.html import urlize, strip_tags
import re

from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def urlize_target_blank(text):
    urlized = urlize(text)
    return re.sub(r'<a (.*?)>', r'<a \1 target="_blank" rel="noopener noreferrer">', urlized)


@register.filter
def safe_html(text):
    allowed_tags = ['a', 'p', 'br', 'em', 'strong']
    allowed_attributes = {'a': ['href', 'title', 'target', 'rel']}

    cleaned = bleach.clean(
        text,
        tags=allowed_tags,
        attributes=allowed_attributes,
        protocols=['http', 'https', 'mailto']
    )

    # Ensure links open in new tab securely
    cleaned = cleaned.replace('<a ', '<a target="_blank" rel="noopener noreferrer" ')
    return mark_safe(cleaned)

