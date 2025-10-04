# Voice-to-text_bot
Бот - голос в текст нужен для комфортного и безопасного обшения с родными/друзьями/коллегами

## Возможности
Бот игнорирует обычный текст и отвечает лишь на голосовые и видео сообщения.
Поддержка разных моделей whisper (по умолчанию стоит "small" (440мб))

---

# Установка
###Клонирование репо
```bash
git clone https://github.com/refaxD/Voice-to-text_bot.git cd Voice-to-text_bot
```
### Создание и подготовка виртуального окружения (440мб напомню)
```bash
python -m venv .venv source
.venv/bin/activate # Linux/macOS
.venv\Scripts\activate # Windows
```
### Установка зависимостей (aiogram и whisper)
```bash
pip install -r requirments.txt
```
### Вписать API-Token тг-бота в поле API_TOKEN = "СЮДЫ_ТОКЕН"
