from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

TOKEN = "PASTE_YOUR_TOKEN_HERE"
OWNER_ID = PASTE_YOUR_NUMERIC_TELEGRAM_ID_HERE

NAME, PHONE, MODEL, PROBLEM, ADDRESS = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "👋 Привет! Это Tech Vibe Service.\n"
        "Чтобы оставить заявку на ремонт телевизора, напишите, пожалуйста, ваше имя:"
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📞 Укажите, пожалуйста, номер телефона для связи:")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("📺 Какая у вас модель телевизора? (можно пропустить, если не знаете)")
    return MODEL

async def get_model(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["model"] = update.message.text
    await update.message.reply_text("🛠️ В чём проблема? Опишите коротко:")
    return PROBLEM

async def get_problem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["problem"] = update.message.text
    await update.message.reply_text("📍 Укажите ваш район или адрес (если уже знаете):")
    return ADDRESS

async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["address"] = update.message.text

    text = (
        "📥 *Новая заявка на ремонт:*\n\n"
        f"👤 Имя: {context.user_data['name']}\n"
        f"📞 Телефон: {context.user_data['phone']}\n"
        f"📺 Модель: {context.user_data['model']}\n"
        f"🔧 Проблема: {context.user_data['problem']}\n"
        f"📍 Адрес: {context.user_data['address']}"
    )

    await context.bot.send_message(chat_id=OWNER_ID, text=text, parse_mode='Markdown')
    await update.message.reply_text("✅ Спасибо! Мы получили вашу заявку и свяжемся с вами в ближайшее время.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Заявка отменена.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            MODEL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_model)],
            PROBLEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_problem)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
