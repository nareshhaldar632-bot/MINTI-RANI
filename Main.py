from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from config import BOT_TOKEN
from database import create_tables, add_user
from products import PRODUCTS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    add_user(
        user.id,
        user.username,
        user.first_name
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🛒 Products",
                callback_data="products"
            )
        ]
    ]

    await update.message.reply_text(
        "🔥 Welcome to Nandu Global Key Store 🔥",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "products":

        buttons = []

        for product in PRODUCTS:
            buttons.append(
                [
                    InlineKeyboardButton(
                        product["name"],
                        callback_data=f"product_{product['id']}"
                    )
                ]
            )

        await query.edit_message_text(
            "🛒 Select Product:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )


def main():

    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button
        )
    )

    print("Bot Started")

    app.run_polling()


if __name__ == "__main__":
    main()
