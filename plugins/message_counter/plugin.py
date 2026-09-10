"""Message Counter Plugin for Miogram.

Session tallies of incoming vs outgoing messages.
  .stats            prints the counters into the current chat (as your message)
  Main menu -> "Session stats" shows the same via toast.

Counters reset on app restart. Nothing leaves the device.
"""

from base_plugin import BasePlugin, HookResult, HookStrategy, MenuItemData, MenuItemType

__id__ = "message_counter"
__name__ = "Message Counter"
__description__ = "Session stats for incoming/outgoing messages (.stats)"
__author__ = "@miogram"
__version__ = "1.0.0"


class MessageCounterPlugin(BasePlugin):

    def on_plugin_load(self):
        self.__dict__["incoming"] = 0
        self.__dict__["outgoing"] = 0
        self.log("MessageCounterPlugin loaded")
        try:
            from android_utils import show_toast  # noqa: F401
            self.add_menu_item(MenuItemData(
                menu_type=MenuItemType.MAIN_MENU,
                text="Session stats",
                on_click=lambda ctx: self._show_stats(),
            ))
        except Exception as e:
            self.log("menu unavailable: %s" % e)
        self.add_on_send_message_hook(priority=90)
        self.add_hook("updateNewMessage", match_substring=True, priority=90)

    # ---- outgoing ----

    def on_send_message_hook(self, *args):
        try:
            text = self._extract_text(args)
            if text and text.strip() == ".stats":
                return HookResult(HookStrategy.MODIFY, message=self._report())
            self.__dict__["outgoing"] = self.__dict__.get("outgoing", 0) + 1
        except Exception as e:
            self.log("count out failed: %s" % e)
        return HookResult(HookStrategy.DEFAULT)

    # ---- incoming (defensive: loader signature varies) ----

    def on_update_hook(self, *args, **kwargs):
        try:
            update = args[-1] if args else kwargs.get("update")
            msg = getattr(update, "message", None)
            if msg is None and hasattr(update, "get"):
                try:
                    msg = update.get("message")
                except Exception:
                    msg = None
            if msg is None:
                return
            if getattr(msg, "out", False):
                return
            self.__dict__["incoming"] = self.__dict__.get("incoming", 0) + 1
        except Exception as e:
            self.log("count in failed: %s" % e)

    def _report(self):
        inc = self.__dict__.get("incoming", 0)
        out = self.__dict__.get("outgoing", 0)
        total = inc + out
        ratio = ("%.1f%% out" % (100.0 * out / total)) if total else "no traffic yet"
        return "Session stats\nIncoming: %d\nOutgoing: %d\n%s" % (inc, out, ratio)

    def _show_stats(self):
        try:
            from android_utils import show_toast
            show_toast(self._report())
        except Exception as e:
            self.log("toast failed: %s" % e)

    @staticmethod
    def _extract_text(args):
        for a in args:
            if isinstance(a, str) and a:
                return a
            message = getattr(a, "message", None)
            if isinstance(message, str) and message:
                return message
        return ""
