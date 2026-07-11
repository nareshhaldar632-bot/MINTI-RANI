from config import BOT_TOKEN, QR_IMAGE, UPI_ID
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

from config import BOT_TOKEN
from database import create_tables, add_user
from products import PRODUCTS, DURATIONS


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

    data = query.data


    # Product list
    if data == "products":

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


    # Duration list
    elif data.startswith("product_"):

        product_id = data.replace("product_", "")

        buttons = []

        for duration, price in DURATIONS.items():

            buttons.append(
                [
                    InlineKeyboardButton(
                        f"{duration} - ₹{price}",
                        callback_data=f"buy_{duration}"
                    )
                ]
            )


        await query.edit_message_text(
            f"Select Duration for {product_id}:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data.startswith("buy_"):

    duration = data.replace("buy_", "")

    await query.edit_message_text(
        f"✅ Selected Duration: {duration}\n\n"
        "💳 Payment Details\n"
        "UPI: yourupi@upi\n\n"
        "Payment karne ke baad UTR number bheje."
    )

def main():

    create_tables()

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button)
    )


    print("Bot Started")

    app.run_polling()



if __name__ == "__main__":
    main()
