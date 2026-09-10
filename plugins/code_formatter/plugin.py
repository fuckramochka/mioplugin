"""Code Formatter Plugin for Miogram.

  .code [lang] <text>   fenced block, optional language tag
  .inline <text>        `monospace`
  .spoiler <text>       ||hidden until tapped||
  .quote <text>         > quoted line(s)
"""

from base_plugin import BasePlugin, HookResult, HookStrategy

__id__ = "code_formatter"
__name__ = "Code Formatter"
__description__ = ".code .inline .spoiler .quote shortcuts for outgoing text"
__author__ = "@miogram"
__version__ = "1.0.0"


class CodeFormatterPlugin(BasePlugin):

    def on_plugin_load(self):
        self.log("CodeFormatterPlugin loaded: .code .inline .spoiler .quote")
        self.add_on_send_message_hook(priority=10)

    def on_send_message_hook(self, *args):
        try:
            text = self._extract_text(args)
            if not text:
                return HookResult(HookStrategy.DEFAULT)
            rendered = self._render(text)
            if rendered is not None:
                return HookResult(HookStrategy.MODIFY, message=rendered)
            return HookResult(HookStrategy.DEFAULT)
        except Exception as e:
            self.log("format failed: %s" % e)
            return HookResult(HookStrategy.DEFAULT)

    @staticmethod
    def _render(text):
        if text.startswith(".code"):
            rest = text[5:].strip()
            if not rest:
                return None
            head, _, body = rest.partition("\n")
            if body and " " not in head and len(head) <= 20:
                return "```%s\n%s\n```" % (head, body)
            return "```\n%s\n```" % rest
        if text.startswith(".inline "):
            body = text[8:].strip()
            return "`%s`" % body if body else None
        if text.startswith(".spoiler "):
            body = text[9:].strip()
            return "||%s||" % body if body else None
        if text.startswith(".quote "):
            body = text[7:].strip()
            if not body:
                return None
            return "\n".join("> " + line for line in body.split("\n"))
        return None

    @staticmethod
    def _extract_text(args):
        for a in args:
            if isinstance(a, str) and a:
                return a
            message = getattr(a, "message", None)
            if isinstance(message, str) and message:
                return message
        return ""
