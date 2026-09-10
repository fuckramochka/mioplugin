"""Link Cleaner Plugin for Miogram.

Strips tracking parameters from every URL in outgoing messages:
  utm_source/medium/campaign/term/content, fbclid, gclid, gbraid, wbraid,
  msclkid, ttclid, twclid, igshid, si, s, ref, ref_src, spm, scm, yclid.
The visible text and the rest of the query string are preserved.
"""

import re
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

from base_plugin import BasePlugin, HookResult, HookStrategy

__id__ = "link_cleaner"
__name__ = "Link Cleaner"
__description__ = "Strips tracking params (utm_*, fbclid, si, ...) from outgoing links"
__author__ = "@miogram"
__version__ = "1.0.0"

_TRACKING = {
    "fbclid", "gclid", "gbraid", "wbraid", "msclkid", "ttclid", "twclid",
    "igshid", "si", "s", "ref", "ref_src", "spm", "scm", "yclid",
    "mc_cid", "mc_eid", "_openstat", "vero_conv", "vero_id",
}

_UTM_PREFIX = ("utm_",)


def _is_tracking(name):
    low = name.lower()
    if low in _TRACKING:
        return True
    return low.startswith(_UTM_PREFIX)


_URL_RE = re.compile(r"https?://[^\s<>\"]+")


def _clean_url(url):
    try:
        parts = urlsplit(url)
        if not parts.query:
            return url
        kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                if not _is_tracking(k)]
        if len(kept) == len(parse_qsl(parts.query, keep_blank_values=True)):
            return url
        return urlunsplit((parts.scheme, parts.netloc, parts.path,
                           urlencode(kept, doseq=True), parts.fragment))
    except Exception:
        return url


class LinkCleanerPlugin(BasePlugin):

    def on_plugin_load(self):
        self.log("LinkCleanerPlugin loaded")
        self.add_on_send_message_hook(priority=30)

    def on_send_message_hook(self, *args):
        try:
            text = self._extract_text(args)
            if not text or "http" not in text:
                return HookResult(HookStrategy.DEFAULT)
            cleaned = _URL_RE.sub(lambda m: _clean_url(m.group(0)), text)
            if cleaned != text:
                return HookResult(HookStrategy.MODIFY, message=cleaned)
            return HookResult(HookStrategy.DEFAULT)
        except Exception as e:
            self.log("clean failed: %s" % e)
            return HookResult(HookStrategy.DEFAULT)

    @staticmethod
    def _extract_text(args):
        for a in args:
            if isinstance(a, str) and a:
                return a
            message = getattr(a, "message", None)
            if isinstance(message, str) and message:
                return message
        return ""
