"""Antispam Guard Plugin for Miogram.

Passive flood watcher. Warns (toast) when incoming traffic looks automated:
  * same text 4+ times in a rolling window of 12 messages,
  * 5+ messages containing t.me/ invite links in a window of 12,
  * 6+ bare URLs in a window of 12.
Never deletes or blocks anything — purely informative.
"""

import re
import time
from collections import deque

from base_plugin import BasePlugin

__id__ = "antispam_guard"
__name__ = "Antispam Guard"
__description__ = "Passive flood watcher: warns about repeated texts and link blasts"
__author__ = "@miogram"
__version__ = "1.0.0"

_WINDOW = 12
_REPEAT_THRESHOLD = 4
_INVITE_THRESHOLD = 5
_URL_THRESHOLD = 6
_COOLDOWN_S = 90

_INVITE_RE = re.compile(r"t\.me/\+|t\.me/joinchat", re.IGNORECASE)
_URL_RE = re.compile(r"https?://")


class AntispamGuardPlugin(BasePlugin):

    def on_plugin_load(self):
        self.__dict__["recent"] = deque(maxlen=_WINDOW)
        self.__dict__["last_warn"] = 0.0
        self.log("AntispamGuardPlugin loaded (passive mode)")
        self.add_hook("updateNewMessage", match_substring=True, priority=90)

    def on_update_hook(self, *args, **kwargs):
        try:
            update = args[-1] if args else kwargs.get("update")
            msg = getattr(update, "message", None)
            if msg is None:
                return
            if getattr(msg, "out", False):
                return
            text = getattr(msg, "message", "") or ""
            if not isinstance(text, str):
                text = str(text)
            recent = self.__dict__["recent"]
            recent.append(text)
            self._evaluate(list(recent))
        except Exception as e:
            self.log("guard failed: %s" % e)

    def _evaluate(self, recent):
        now = time.time()
        if now - self.__dict__.get("last_warn", 0.0) < _COOLDOWN_S:
            return
        if len(recent) < 6:
            return
        counts = {}
        invites = 0
        urls = 0
        for t in recent:
            counts[t] = counts.get(t, 0) + 1
            if _INVITE_RE.search(t):
                invites += 1
            if len(_URL_RE.findall(t)) >= 1:
                urls += len(_URL_RE.findall(t))
        reason = None
        if max(counts.values()) >= _REPEAT_THRESHOLD:
            top = max(counts, key=counts.get)
            reason = "repeated text x%d: %r" % (counts[top], top[:60])
        elif invites >= _INVITE_THRESHOLD:
            reason = "invite-link blast x%d" % invites
        elif urls >= _URL_THRESHOLD:
            reason = "link blast x%d urls" % urls
        if reason is None:
            return
        self.__dict__["last_warn"] = now
        try:
            from android_utils import show_toast
            show_toast("Antispam guard: possible flood (%s)" % reason)
        except Exception as e:
            self.log("toast failed: %s" % e)
