


# 🤖 Discord Test Bot (Python)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![Discord.py](https://img.shields.io/badge/discord.py-2.4.0-blueviolet?logo=discord&logoColor=white)

Простой бот для Discord, написанный на **Python** с использованием библиотеки [discord.py](https://discordpy.readthedocs.io/).

---

## ✨ Возможности
- **`!info`** — выводит информацию о сервере.
- **`!rules`** — отправляет правила в личные сообщения.
- **Реакция на слово _"привет"_** — бот отвечает: `Привет, @ник!`.
- **Логирование удалённых сообщений** — отправляет информацию в отдельный канал.



## 🚀 Установка и запуск

### 1️⃣ Клонируем репозиторий
```bash
git clone https://github.com/VladShulik/Test-bot.git
cd Test-bot
```

### 2️⃣ Устанавливаем зависимости

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

pip install -r requirements.txt
```

### 3️⃣ Настраиваем `.env`

Создай файл `.env` по образцу:

```env
DISCORD_TOKEN=ТВОЙ_ТОКЕН_БОТА
LOG_CHANNEL_ID=ID_КАНАЛА_ДЛЯ_ЛОГОВ
```

> ⚠ **Важно:** Никогда не загружай свой токен в GitHub!

### 4️⃣ Запускаем бота

```bash
python bot.py
```

---

## 🛠 Требования

* Python 3.8+
* discord.py 2.x
* python-dotenv

---

## 📷 Скриншоты

<img width="690" height="334" alt="image" src="https://github.com/user-attachments/assets/dbafdfbb-c8a5-419d-8812-056dc67c0bb7" />


---

## 📜 Лицензия

Проект распространяется по лицензии MIT.

````

