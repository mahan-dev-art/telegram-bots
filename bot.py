import re
from telebot import TeleBot , types
import requests

bot = TeleBot("8289262749:AAE7SbEQj_fTjVcdfbs1c1Q9H6qlmkF_Ee0")


url = "https://api.majidapi.ir/instagram/download"

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button1 = types.KeyboardButton(text="دریافت ویدیو از اینستاگرام")
    keyboard.add(button1)
    bot.send_message(message.chat.id, "یک گزینه را انتخاب کنید.", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "دریافت ویدیو از اینستاگرام")
def download_instagram_video(message):
    msg = bot.send_message(message.chat.id, "لطفا لینک ویدیو اینستاگرام را ارسال کنید:")
    bot.register_next_step_handler(msg, process_instagram_link)
    
def process_instagram_link(message):
    instagram_link = message.text.strip()
    if not re.match(r'^https?://(www\.)?instagram\.com/', instagram_link):
        bot.send_message(message.chat.id, "لطفا یک لینک معتبر از اینستاگرام ارسال کنید.")
        return

    params = {
        'url': instagram_link,
        'token': 'ugcnzj3ahbbx9kg:Vzog7ojvKLZwFuKVwi92'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        data = data["result"]

        video_url = data["videos"][0]["url"]
        cover_url = data["cover"]
        caption = data["caption"]
        username = data["user"]["username"]
        likes = data["likes"]
        comments = data["comments"]

        bot.send_message(
            message.chat.id,
            f"✅ ویدیو با موفقیت دریافت شد!\n\n"
            f"👤 سازنده: @{username}\n"
            f"❤️ لایک‌ها: {likes}\n"
            f"💬 کامنت‌ها: {comments}\n\n"
            f"📝 توضیحات:\n{caption}\n\n"
            f"🔗 لینک دانلود:\n{video_url}"
        )

        bot.send_photo(
            message.chat.id,
            cover_url,
            caption=f"🎬 کاور ویدیو از @{username}"
        )

    else:
        bot.send_message(
            message.chat.id,
            f"❌ خطا در دریافت ویدیو!\nکد خطا: {response.status_code}"
        )

bot.polling()