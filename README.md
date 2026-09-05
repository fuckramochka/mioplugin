# ✦ Mioplugin — Офіційний каталог та репозиторій плагінів для Miogram ✦

[![Official Repo](https://img.shields.io/badge/Miogram-Official_Plugins-blueviolet?style=for-the-badge&logo=telegram)](https://github.com/fuckramochka/miogram)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

Ласкаво просимо до **Mioplugin** — офіційного автономного репозиторію розробки, публікації та каталогізації плагінів для месенджера **Miogram**.

---

## 🌟 Можливості системи плагінів Miogram

- 🐍 **Повна підтримка Python 3**: пишіть плагіни нативною мовою Python із доступом до внутрішнього API Telegram.
- ⚡ **WebAssembly & Rust**: надшвидкі пісочничні плагіни `.mioplugin` / `.wasm` з обмеженими правами.
- 🎨 **Гнучкий UI**: додавання власних налаштувань (перемикачі, селектори, інпути, власні банери).
- 🪝 **Xposed-style хуки**: перехоплення та підміна будь-яких Java/Android методів на льоту.
- 🛡️ **Система прав доступу**: пісочниця з безпечним запитом дозволів (інтернет, файли, буфер обміну).

---

## 📦 Офіційний каталог плагінів

| Плагін | Категорія | Версія | Опис |
| :--- | :--- | :--- | :--- |
| **[Auto Reaction](plugins/auto_reaction)** | Automation | `1.0.0` | Автоматичні реакції на повідомлення за ключовими словами |
| **[Custom Profile](plugins/custom_profile)** | Customization | `1.8.1` | Кастомізація профілю, кольорові банери та градієнти |
| **[In-App Notifications](plugins/in_app_notifications)** | UI / UX | `1.0.0` | Спливаючі внутрішньоігрові сповіщення із швидкою відповіддю |
| **[Message Styler](plugins/message_styler)** | Formatting | `1.0.0` | Стилізація вихідних повідомлень (шрифти, ефекти) |
| **[Quick Tools](plugins/quick_tools)** | Utility | `1.0.0` | Інструменти швидкої копії ID, Markdown, перекладу в контекстному меню |

Усі метадані каталогу також доступні у машинному форматі [catalog.json](catalog.json).

---

## 🚀 Як встановити плагін у Miogram

1. Відкрийте **Miogram** на своєму пристрої.
2. Перейдіть у **Налаштування** -> **Плагіни**.
3. Натисніть **+** (Додати плагін) або завантажте файл `plugin.py` / `.mioplugin` безпосередньо в Telegram і натисніть на нього.
4. Додаток автоматично імпортує плагін, покаже запитувані права та активує його.

---

## 🛠️ Створення власного плагіна

Мінімальний шаблон плагіна:

```python
from base_plugin import BasePlugin
from android_utils import show_toast

__id__ = "my_custom_plugin"
__name__ = "Мій Кастомний Плагін"
__description__ = "Опис функціоналу вашого плагіна"
__author__ = "@your_username"
__version__ = "1.0.0"

class MyPlugin(BasePlugin):
    def on_plugin_load(self):
        self.log("Плагін завантажено!")
        show_toast("Плагін активовано! ✦")

    def on_plugin_unload(self):
        self.log("Плагін вивантажено")
```

Детальну інформацію про всі доступні хуки, методи та події дивіться у:
- 📖 [HOOKS_REFERENCE.md](HOOKS_REFERENCE.md) — Повний довідник хуків та API.
- 🛠️ [PLUGINS_DEV_GUIDE.md](PLUGINS_DEV_GUIDE.md) — Повне керівництво розробника плагінів.

---

## 📄 Ліцензія

Цей проєкт поширюється під ліцензією MIT. Дивіться [LICENSE](LICENSE) для отримання додаткової інформації.
