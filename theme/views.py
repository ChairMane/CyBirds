from django.shortcuts import render, redirect
from calendar import month_name

from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _

#from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.blog.models import BlogPost, BlogCategory
from mezzanine.blog.feeds import PostsRSS, PostsAtom
from mezzanine.conf import settings
from mezzanine.generic.models import Keyword
from mezzanine.utils.views import paginate
User = get_user_model()
# Create your views here.

def blog_redirect(request):
	return redirect('/', permanent=True)


def project_list(request, tag=None, year=None, month=None, username=None,
                   category='project', template="projects/projects.html",
                   extra_context=None):
    """
    Display a list of blog posts that are filtered by tag, year, month,
    author or category. Custom templates are checked for using the name
    ``blog/project_list_XXX.html`` where ``XXX`` is either the
    category slug or author's username if given.
    """
# TODO HERE IS WHAT IS NEXT
# I HAVE TO FIGURE OUT HOW TO GET OBJECTS BY THEIR TAGS
    templates = []
    projects = BlogPost.objects.published(for_user=request.user)
    if tag is not None:
        tag = get_object_or_404(Keyword, slug=tag)
        projects = projects.filter(keywords__keyword=tag)
    if year is not None:
        projects = projects.filter(publish_date__year=year)
        if month is not None:
            projects = projects.filter(publish_date__month=month)
            try:
                month = _(month_name[int(month)])
            except IndexError:
                raise Http404()
    if category is not None:
        category = get_object_or_404(BlogCategory, slug=category)
        projects = projects.filter(categories=category)
        templates.append(u"projects/projects_%s.html" %
                          str(category.slug))
    author = None
    if username is not None:
        author = get_object_or_404(User, username=username)
        projects = projects.filter(user=author)
        templates.append(u"projects/projects_%s.html" % username)

    prefetch = ("categories", "keywords__keyword")
    projects = projects.select_related("user").prefetch_related(*prefetch)
    projects = paginate(projects, request.GET.get("page", 1),
                          settings.PROJECTS_PER_PAGE,
                          settings.MAX_PAGING_LINKS)
    context = {"projects": projects, "year": year, "month": month,
               "tag": tag, "category": category, "author": author}
    context.update(extra_context or {})
    templates.append(template)
    return TemplateResponse(request, templates, context)


def project_detail(request, slug, year=None, month=None, day=None,
                     template="projects/projects_detail.html",
                     extra_context=None):
    """. Custom templates are checked for using the name
    ``blog/project_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    projects = BlogPost.objects.published(
                                     for_user=request.user).select_related()
    project = get_object_or_404(projects, slug=slug)
    related_posts = project.related_posts.published(for_user=request.user)
    context = {"project": project, "editable_obj": project,
               "related_posts": related_posts}
    context.update(extra_context or {})
    templates = [u"projects/projects_detail_%s.html" % str(slug), template]
    return TemplateResponse(request, templates, context)
