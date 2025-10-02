from django.db import models
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField

class HomePage(Page):
    template = "home/home.html"

    hero_kicker = models.CharField("顶部字条", max_length=40, blank=True)
    hero_title = models.CharField("主标题", max_length=120, blank=True)
    hero_subtitle = models.CharField("副标题", max_length=200, blank=True)

    cta_primary_text = models.CharField("主按钮文案", max_length=20, blank=True)
    cta_primary_url  = models.URLField("主按钮链接", blank=True)
    cta_secondary_text = models.CharField("次按钮文案", max_length=20, blank=True)
    cta_secondary_url  = models.URLField("次按钮链接", blank=True)
    cta_badge_text = models.CharField("cta标签", blank=True, max_length=20)

    stat_exp = models.CharField("跨境服务经验", max_length=20, blank=True)
    stat_flow = models.CharField("平台资金吞吐", max_length=20, blank=True)

    body = RichTextField("补充内容", blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("hero_kicker"),
            FieldPanel("hero_title"),
            FieldPanel("hero_subtitle"),
        ], heading="Hero"),
        MultiFieldPanel([
            FieldPanel("cta_primary_text"),
            FieldPanel("cta_primary_url"),
            FieldPanel("cta_secondary_text"),
            FieldPanel("cta_secondary_url"),
            FieldPanel("cta_badge_text"),
        ], heading="按钮"),
        MultiFieldPanel([
            FieldPanel("stat_exp"),
            FieldPanel("stat_flow"),
        ], heading="统计"),
        FieldPanel("body"),
    ]