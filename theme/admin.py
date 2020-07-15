from copy import deepcopy
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost
from mezzanine.pages.admin import PageAdmin
from mezzanine.pages.models import RichTextPage
from mezzanine.core.admin import (DisplayableAdmin, OwnableAdmin,
                                  BaseTranslationModelAdmin)
from mezzanine.twitter.admin import TweetableAdminMixin
from mezzanine.conf import settings
from theme.models import Projects

blog_fieldsets = deepcopy(BlogPostAdmin.fieldsets)
blog_fieldsets[0][1]["fields"].insert(-2, "retina")


pages_fieldsets = deepcopy(PageAdmin.fieldsets)
pages_fieldsets[0][1]["fields"].insert(-2, "page_image")
pages_fieldsets[0][1]["fields"].insert(-3, "content")

class MyBlogPostAdmin(BlogPostAdmin):
    fieldsets = blog_fieldsets

class MyPageAdmin(PageAdmin):
	fieldsets = pages_fieldsets


class ProjectsAdmin(BlogPostAdmin):
	pass

admin.site.unregister(Projects)
admin.site.unregister(BlogPost)
admin.site.unregister(RichTextPage)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(BlogPost, MyBlogPostAdmin)
admin.site.register(RichTextPage, MyPageAdmin)