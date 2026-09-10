"""Text Transformer Plugin for Miogram.

Dot-commands applied to outgoing messages before sending:
  .upper <text>    UPPERCASE EVERYTHING
  .lower <text>    lowercase everything
  .reverse <text>  txet esrever
  .mock <text>     sPoNgEbOb mOcK
  .uwu <text>      soft uwu-ified text
"""

from base_plugin import BasePlugin, HookResult, HookStrategy

__id__ = "text_transformer"
__name__ = "Text Transformer"
__description__ = "Dot-commands for outgoing text: .upper .lower .reverse .mock .uwu"
__author__ = "@miogram"
__version__ = "1.0.0"


def _mock(text):
    out = []
    upper = False
    for ch in text:
        if ch.isalpha():
            out.append(ch.upper() if upper else ch.lower())
            upper = not upper
        else:
            out.append(ch)
    return "".join(out)


def _uwu(text):
    t = text.replace("r", "w").replace("l", "w")
    t = t.replace("R", "W").replace("L", "W")
    t = t.replace("ove", "uv")
    return t + " uwu"


_COMMANDS = {
    ".upper": lambda s: s.upper(),
    ".lower": lambda s: s.lower(),
    ".reverse": lambda s: s[::-1],
    ".mock": _mock,
    ".uwu": _uwu,
}


class TextTransformerPlugin(BasePlugin):

    def on_plugin_load(self):
        self.log("TextTransformerPlugin loaded: .upper .lower .reverse .mock .uwu")
        self.add_on_send_message_hook(priority=10)

    def on_send_message_hook(self, *args):
        try:
            text = self._extract_text(args)
            if not text:
                return HookResult(HookStrategy.DEFAULT)
            for cmd, fn in _COMMANDS.items():
                prefix = cmd + " "
                if text.startswith(prefix):
                    return HookResult(HookStrategy.MODIFY, message=fn(text[len(prefix):]))
            return HookResult(HookStrategy.DEFAULT)
        except Exception as e:
            self.log("transform failed: %s" % e)
            return HookResult(HookStrategy.DEFAULT)

    @staticmethod
    def _extract_text(args):
        # Loader may call as (peer, message, params) or (account, params).
        for a in args:
            if isinstance(a, str) and a:
                return a
            message = getattr(a, "message", None)
            if isinstance(message, str) and message:
                return message
        return ""
