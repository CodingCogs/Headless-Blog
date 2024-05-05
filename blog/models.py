from django.db import models

from django.utils.translation import gettext_lazy as _

from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

# from wagtail.admin.edit_handlers import FieldPanel
from wagtail.admin.panels import FieldPanel

# from wagtail.images.edit_handlers import FieldPanel
from wagtail.fields import StreamField
from wagtail.templatetags.wagtailcore_tags import richtext
from wagtail.contrib.routable_page.models import RoutablePageMixin

# from wagtail.search import index

from wagtail.api import APIField

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

# Create your models here.


class BlogCategory(RoutablePageMixin, Page):
    parent_page_types = ["home.HomePage"]
    subpage_types = ["blog.BlogPost"]
    categoty_title = models.CharField(
        max_length=50, blank=False, null=False, verbose_name=_("categoty_title")
    )
    content_panels = Page.content_panels + [
        FieldPanel("categoty_title"),
    ]


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPost",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )


class BlogPost(Page):
    parent_page_types = ["blog.BlogCategory"]
    subpage_types = []
    post_title = models.CharField(
        max_length=50, blank=False, null=False, verbose_name=_("post_title")
    )

    image_banner = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="++",
        on_delete=models.SET_NULL,
    )
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full_title", icon="title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock(icon="image")),
        ],
    )
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("post_title"),
        FieldPanel("image_banner"),
        FieldPanel("body"),
    ]
