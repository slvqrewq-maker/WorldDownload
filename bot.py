import asyncio, os, json, logging
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8947350461:AAHuw9oKnKOr7I_AYjSkLwC80B4-V1D8riA"
CHANNEL_ID = "@WorlldStudios"
CHANNEL_URL = "https://t.me/WorlldStudios"
USERS_DB = "users.json"
WORLDS_DB = "worlds.json"

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

TEXTS = {
"ru": {
"choose_lang": "🌍 <b>Выбери язык</b>\n\nChoose your language / अपनी भाषा चुनें",
"subscribe": "📢 <b>Подпишись на наш канал</b>, чтобы получить файл.\n\nПосле подписки нажми «Проверить подписку».",
"btn_sub": "📢 Подписаться на канал",
"btn_check": "✅ Проверить подписку",
"btn_settings": "⚙️ Настройки",
"not_subbed": "❌ <b>Подписка не найдена.</b>\n\nПожалуйста, подпишись на канал и нажми «Проверить подписку» ещё раз.",
"confirmed": "✅ <b>Подписка подтверждена.</b>\n\nОтправляю твой файл...",
"file_caption": "🎮 <b>Твой мир Minecraft</b>\n\nСпасибо за подписку! Приятной игры.",
"settings_hdr": "⚙️ <b>Настройки</b>\n\nТекущий язык: Русский 🇷🇺",
"btn_chlang": "🌐 Сменить язык",
"btn_back": "⬅️ Назад",
"pick_lang_hdr": "🌐 <b>Выбери новый язык:</b>",
"no_world": "⚠️ <b>Мир не найден.</b>",
},
"en": {
"choose_lang": "🌍 <b>Choose your language</b>\n\nВыбери язык / अपनी भाषा चुनें",
"subscribe": "📢 <b>Subscribe to our channel</b> to get the file.\n\nAfter subscribing, press «Check subscription».",
"btn_sub": "📢 Subscribe to channel",
"btn_check": "✅ Check subscription",
"btn_settings": "⚙️ Settings",
"not_subbed": "❌ <b>Subscription not found.</b>\n\nPlease subscribe to the channel and press «Check subscription» again.",
"confirmed": "✅ <b>Subscription confirmed.</b>\n\nSending your file...",
"file_caption": "🎮 <b>Your Minecraft world</b>\n\nThanks for subscribing! Enjoy the game.",
"settings_hdr": "⚙️ <b>Settings</b>\n\nCurrent language: English 🇬🇧",
"btn_chlang": "🌐 Change language",
"btn_back": "⬅️ Back",
"pick_lang_hdr": "🌐 <b>Choose a new language:</b>",
"no_world": "⚠️ <b>World not found.</b>",
},
"hi": {
"choose_lang": "🌍 <b>अपनी भाषा चुनें</b>\n\nВыбери язык / Choose your language",
"subscribe": "📢 फ़ाइल प्राप्त करने के लिए <b>हमारे चैनल को सब्सक्राइब करें</b>।\n\nसब्सक्राइब करने के बाद «सब्सक्रिप्शन जांचें» दबाएं।",
"btn_sub": "📢 चैनल सब्सक्राइब करें",
"btn_check": "✅ सब्सक्रिप्शन जांचें",
"btn_settings": "⚙️ सेटिंग्स",
"not_subbed": "❌ <b>सब्सक्रिप्शन नहीं मिला।</b>\n\nकृपया चैनल सब्सक्राइब करें और फिर से «सब्सक्रिप्शन जांचें» दबाएं।",
"confirmed": "✅ <b>सब्सक्रिप्शन की पुष्टि हो गई।</b>\n\nआपकी फ़ाइल भेजी जा रही है...",
"file_caption": "🎮 <b>आपकी Minecraft दुनिया</b>\n\nसब्सक्राइब करने के लिए धन्यवाद! खेल का आनंद लें।",
"settings_hdr": "⚙️ <b>सेटिंग्स</b>\n\nवर्तमान भाषा: हिन्दी 🇮🇳",
"btn_chlang": "🌐 भाषा बदलें",
"btn_back": "⬅️ वापस",
"pick_lang_hdr": "🌐 <b>नई भाषा चुनें:</b>",
"no_world": "⚠️ <b>दुनिया नहीं मिली।</b>",
},
}

def load_users():
    if os.path.exists(USERS_DB):
        try:
            with open(USERS_DB, "r", encoding="utf-8") as f:
                return {str(k): v for k, v in json.load(f).items()}
        except:
            return {}
    return {}

def save_users():
    try:
        with open(USERS_DB, "w", encoding="utf-8") as f:
            json.dump(user_lang, f, ensure_ascii=False)
    except:
        pass

user_lang = load_users()

def get_lang(uid):
    return user_lang.get(str(uid))

def set_lang(uid, lang):
    user_lang[str(uid)] = lang
    save_users()

def t(uid, key):
    return TEXTS[get_lang(uid) or "ru"][key]

def load_worlds():
    if os.path.exists(WORLDS_DB):
        try:
            with open(WORLDS_DB, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_worlds():
    try:
        with open(WORLDS_DB, "w", encoding="utf-8") as f:
            json.dump(worlds, f, ensure_ascii=False, indent=2)
    except:
        pass

worlds = load_worlds()
user_world = {}

def kb_lang():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang:en")],
        [InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="lang:hi")],
    ])

def kb_sub(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_sub"), url=CHANNEL_URL)],
        [InlineKeyboardButton(text=t(uid, "btn_check"), callback_data="check_sub")],
        [InlineKeyboardButton(text=t(uid, "btn_settings"), callback_data="settings")],
    ])

def kb_settings(uid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t(uid, "btn_chlang"), callback_data="chlang")],
        [InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="back_sub")],
    ])

def kb_chlang(uid):
    cur = get_lang(uid) or "ru"
    names = {"ru": "🇷🇺 Русский", "en": "🇬🇧 English", "hi": "🇮🇳 हिन्दी"}
    rows = []
    for code in ["ru", "en", "hi"]:
        mark = "✅ " if code == cur else ""
        rows.append([InlineKeyboardButton(text=mark + names[code], callback_data="lang:" + code)])
    rows.append([InlineKeyboardButton(text=t(uid, "btn_back"), callback_data="settings")])
    return InlineKeyboardMarkup(inline_keyboard=rows)

async def is_subbed(uid):
    try:
        m = await bot.get_chat_member(CHANNEL_ID, uid)
        return m.status in ("creator", "administrator", "member")
    except:
        return False

@dp.message(F.document)
async def catch_file(msg: Message):
    fid = msg.document.file_id
    name = msg.document.file_name or "file"
    key = name.replace(".mcworld", "").strip().lower()
    worlds[key] = fid
    save_worlds()
    await msg.answer(f"✅ Сохранил мир: <b>{key}</b>\n\n<code>{fid}</code>")

@dp.message(CommandStart())
async def start(msg: Message):
    uid = msg.from_user.id
    args = msg.text.split(maxsplit=1)
    if len(args) > 1:
        user_world[uid] = args[1].strip().lower()
    if not get_lang(uid):
        await msg.answer(TEXTS["ru"]["choose_lang"], reply_markup=kb_lang())
    else:
        await msg.answer(t(uid, "subscribe"), reply_markup=kb_sub(uid))

@dp.callback_query(F.data.startswith("lang:"))
async def set_lang_cb(call: CallbackQuery):
    set_lang(call.from_user.id, call.data.split(":")[1])
    await call.message.edit_text(t(call.from_user.id, "subscribe"), reply_markup=kb_sub(call.from_user.id))
    await call.answer()

@dp.callback_query(F.data == "check_sub")
async def check(call: CallbackQuery):
    uid = call.from_user.id
    if not await is_subbed(uid):
        await call.message.edit_text(t(uid, "not_subbed"), reply_markup=kb_sub(uid))
        await call.answer()
        return
    await call.message.edit_text(t(uid, "confirmed"))
    world_key = user_world.get(uid)
    if world_key and world_key in worlds:
        await bot.send_document(uid, worlds[world_key], caption=t(uid, "file_caption"))
    elif worlds:
        first = list(worlds.values())[0]
        await bot.send_document(uid, first, caption=t(uid, "file_caption"))
    else:
        await call.message.answer(t(uid, "no_world"))
    await call.answer()

@dp.callback_query(F.data == "settings")
async def settings(call: CallbackQuery):
    await call.message.edit_text(t(call.from_user.id, "settings_hdr"), reply_markup=kb_settings(call.from_user.id))
    await call.answer()

@dp.callback_query(F.data == "chlang")
async def chlang(call: CallbackQuery):
    await call.message.edit_text(t(call.from_user.id, "pick_lang_hdr"), reply_markup=kb_chlang(call.from_user.id))
    await call.answer()

@dp.callback_query(F.data == "back_sub")
async def back_sub(call: CallbackQuery):
    await call.message.edit_text(t(call.from_user.id, "subscribe"), reply_markup=kb_sub(call.from_user.id))
    await call.answer()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
