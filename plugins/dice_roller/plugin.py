"""Dice Roller Plugin for Miogram.

Tabletop rolls expanded inline before sending:
  .roll 2d6       -> "🎲 2d6: [3, 5] = 8"
  .roll d20       -> "🎲 d20: [17] = 17"
  .roll 4d6dl1    -> drop lowest one (dl1)
  .flip           -> "🪙 Heads" / "🪙 Tails"
Limits: max 20 dice, max 1000 sides (spam control).
"""

import random
import re

from base_plugin import BasePlugin, HookResult, HookStrategy

__id__ = "dice_roller"
__name__ = "Dice Roller"
__description__ = "Tabletop dice in chat: .roll 2d6, .roll d20, .flip"
__author__ = "@miogram"
__version__ = "1.0.0"

_ROLL_RE = re.compile(r"^(\d{1,2})?[dD](\d{1,4})(dl\d{1,2})?\s*$")


class DiceRollerPlugin(BasePlugin):

    def on_plugin_load(self):
        self.log("DiceRollerPlugin loaded: .roll NdM[dlK], .flip")
        self.add_on_send_message_hook(priority=10)

    def on_send_message_hook(self, *args):
        try:
            text = self._extract_text(args)
            if not text:
                return HookResult(HookStrategy.DEFAULT)
            body = text.strip()
            if body == ".flip":
                return HookResult(HookStrategy.MODIFY,
                                  message=":coin: %s" % random.choice(["Heads", "Tails"]))
            if body.startswith(".roll"):
                expr = body[5:].strip() or "1d6"
                rendered = self._render_roll(expr)
                if rendered is not None:
                    return HookResult(HookStrategy.MODIFY, message=rendered)
            return HookResult(HookStrategy.DEFAULT)
        except Exception as e:
            self.log("roll failed: %s" % e)
            return HookResult(HookStrategy.DEFAULT)

    def _render_roll(self, expr):
        m = _ROLL_RE.match(expr)
        if not m:
            return None
        count = int(m.group(1) or 1)
        sides = int(m.group(2))
        drop = 0
        if m.group(3):
            try:
                drop = int(m.group(3)[2:])
            except ValueError:
                drop = 0
        if not (1 <= count <= 20 and 2 <= sides <= 1000 and 0 <= drop < count):
            return None
        rng = random.SystemRandom()
        rolls = [rng.randint(1, sides) for _ in range(count)]
        kept = sorted(rolls)[drop:]
        total = sum(kept)
        shown = "[%s]" % ", ".join(str(r) for r in rolls)
        suffix = " (dropped %d)" % drop if drop else ""
        return ":game_die: %dd%d%s: %s = %d%s" % (count, sides, ("dl%d" % drop) if drop else "", shown, total, suffix)

    @staticmethod
    def _extract_text(args):
        for a in args:
            if isinstance(a, str) and a:
                return a
            message = getattr(a, "message", None)
            if isinstance(message, str) and message:
                return message
        return ""
