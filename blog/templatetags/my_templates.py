from django import template
from django.contrib import auth
register = template.Library()
from blog.models import Question, Profile,  Answer,Tag
from django.db.models import Count, Avg
@register.inclusion_tag('blog/base_help.html')
def render_all():
    profiles = Profile.objects.best()
    tags  = Tag.objects.annotate(q=Count('question')).order_by('-q')
    return {'profiles' : profiles, 'tags' : tags}

