from django.db import models

from wagtail.models import Page


class HomePage(Page):
    max_count = 1
    parent_page_type = ["wagtailcore.Page"]
