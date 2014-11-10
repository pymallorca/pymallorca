# -*- coding: utf-8 -*-

from apconf import Options

opts = Options()


def get(value, default):
    return opts.get(value, default, section='CMS')


class CMSMixin(object):

    CMS_SEO_FIELDS = True
    CMS_REDIRECTS = True
    CMS_SOFTROOT = False
    CMS_TEMPLATE_INHERITANCE = True
    CMS_MENU_TITLE_OVERWRITE = True
    CMS_USE_TINYMCE = False
    CMS_PERMISSION = True

    @property
    def CMS_LANGUAGES(self):
        lang_dict = lambda code, name: {
                'code': code,
                'name': name,
                'hide_untranslated': code == self.LANGUAGE_CODE,
                'redirect_on_fallback': not (code == self.LANGUAGE_CODE),
            }
        langs_list = [lang_dict(code, name) for code, name in self.LANGUAGES]

        return {
            self.SITE_ID: langs_list,
            'default': {
                'fallbacks': [self.LANGUAGE_CODE, ]
                }
            }
