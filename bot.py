import os
import stripe
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Configurar tu clave secreta de API de Stripe
stripe.api_key = "sk_live_sWrF2uPsg8pBfIiPPPNxPHH4"

def start(update: Update, context: CallbackContext) -> None:
    message = (
        "Haz clic en el botón para pagar:"
    )

    keyboard = [
        [InlineKeyboardButton("Pagar con Tarjeta", callback_data='stripe')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'stripe':
        # Crea un Checkout Session en Stripe
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': 'price_1Nl7wQFp9Pnzoti4T2M1C1Ly',  # Reemplaza con el ID del precio que creaste en Stripe
                    'quantity': 1,
                }
            ],
            mode='payment',
            success_url='https://tusitio.com/success',
            cancel_url='https://tusitio.com/cancel',
        )

        # Enviar el enlace de pago a través de Telegram
        payment_url = session.url
        message = f"Haz clic en el enlace para realizar el pago: {payment_url}"
        query.message.reply_text(message)

def main():
    # Token de acceso de tu bot
    token = "6307738962:AAEOr7Xel_u9t_vL1SFDcK-7iTFv26lYHzY"
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    
    # Manejador para el comando /start
    dispatcher.add_handler(CommandHandler("start", start))
    
    # Manejador para los botones
    dispatcher.add_handler(CallbackQueryHandler(button_click))
    
    # Iniciar el bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()