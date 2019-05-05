# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from utils.base import PublicView


# Create your views here.
#  class LihuiPage(TemplateView):
class LihuiPage(PublicView):
    template_name = 'index.html'
