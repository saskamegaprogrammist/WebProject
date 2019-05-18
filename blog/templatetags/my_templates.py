from django import template
register = template.Library()
from blog.models import Question, Profile,  Answer,Tag
@register.inclusion_tag('blog/base_help.html')
def render_all():
    profiles = Profile.objects.best()
    tags  = Tag.objects.popular()
    return {'profiles' : profiles, 'tags' : tags}