from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler
from telegram.ext import filters
from scraphh import parser_hh

TOKEN = ""
app = ApplicationBuilder().token(TOKEN).build()
async def bot_reply(update: Update, ctx):
    await update.message.reply_text("Подождите пожалуйста...")
    user_input = update.message.text
    jobs_count = parser_hh(user_input)
    reply = f"Найдено вакансий: {jobs_count}" # Запустить Селениум
    await update.message.reply_text(reply)

handler = MessageHandler(filters.TEXT, bot_reply)
app.add_handler(handler)
app.run_polling()
# run_polling - регулярный опрос, апдейты библиотека запрашивает вручную
# run_webhook - запрос делает сервер Телеграм