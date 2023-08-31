import os
import stripe
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Configura tu clave secreta de API de Stripe
stripe.api_key = "sk_live_sWrF2uPsg8pBfIiPPPNxPHH4"

def start(update: Update, context: CallbackContext) -> None:
    message = "Haz clic en el botón para realizar el pago."
    keyboard = [
        [InlineKeyboardButton("Pagar", callback_data='stripe')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'stripe':
        print("Botón de pago presionado")  # Para verificar si el evento se ejecuta
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': 'price_1Nl7wQFp9Pnzoti4T2M1C1Ly',
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url='https://tu-sitio.com/success',
                cancel_url='https://tu-sitio.com/cancel',
            )
            
            payment_url = session.url
            query.message.reply_text(f"Haz clic en el enlace para realizar el pago: {payment_url}")
        except Exception as e:
            print("Error al crear la sesión de pago:", e)
            query.message.reply_text("Ocurrió un error al procesar el pago. Por favor, inténtalo más tarde.")

def main():
    token = "6307738962:AAEOr7Xel_u9t_vL1SFDcK-7iTFv26lYHzY"
    updater = Updater(token, use_context=True)
    dispatcher = updater.dispatcher
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_click))
    
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()