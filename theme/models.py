from django.db import models
from mezzanine.blog.models import BlogPost, BlogCategory
# Create your models here.

class Projects(BlogPost):
	pass
	# MAKE A NEW MODLE NOT USING BLOGPOST
	# THERE MAY ERRORS WHEN TRYING TO IMPORT DISPLAYABLE
	# MAY NOT BE THE CORRECT IMPORT STATEMENT
	# REFRESH YOURSELF ON HOW TO MAKE MODELS
	# KEEP IN MIND PROJECT FIELDS YOU WANT DISPLAYED

class ProjectsCategory(BlogCategory):
	pass


