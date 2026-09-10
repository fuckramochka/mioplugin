# Text Transformer

Dot-commands for outgoing messages. Type the command, the plugin rewrites
the text before sending:

| Command   | Example              | Result               |
|-----------|----------------------|----------------------|
| `.upper`  | `.upper hello`       | `HELLO`              |
| `.lower`  | `.lower SHOUT`       | `shout`              |
| `.reverse`| `.reverse abc`       | `cba`                |
| `.mock`   | `.mock hello world`  | `hElLo wOrLd`        |
| `.uwu`    | `.uwu hello friend`  | `hewwo fwiend uwu`   |

No settings. No network. Pure string ops on the send hook.
