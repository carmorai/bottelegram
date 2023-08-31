import stripe
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Configurar tu clave secreta de API de Stripe
stripe.api_key = "sk_live_sWrF2uPsg8pBfIiPPPNxPHH4"  # Reemplaza con tu clave secreta de Stripe

def start(update: Update, context: CallbackContext) -> None:
    message = (
        "Suscripción mensual Premium\n\n"
        "Acceso mensual a nuestro grupo privado de Telegram\n\n"
        "TUS BENEFICIOS:\n"
        "✅ NEUROEMPRENDEDOR (Acceso al grupo + 2 grupos adicionales)\n\n"
        "Price: 8,50 €\n"
        "Periodo: 1 month\n"
        "Modo: Recurrente\n\n"
        "Seleccione una opción:"
    )

    keyboard = [
        [InlineKeyboardButton("Tarjeta de Crédito", callback_data='stripe')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)

def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()  # Acknowledge the button click

    if query.data == 'stripe':
        try:
            # Crear un enlace de Checkout de Stripe
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
            
            # Enviar un mensaje al usuario con el enlace de pago
            payment_url = session.url
            message = f"Haz clic en el enlace para realizar el pago: {payment_url}"
            query.message.reply_text(message)
        except stripe.error.StripeError as e:
            print("Error de Stripe:", str(e))
            query.message.reply_text("Ocurrió un error de pago con Stripe. Por favor, inténtalo más tarde.")
        except Exception as e:
            print("Error inesperado:", str(e))
            query.message.reply_text("Ocurrió un error inesperado. Por favor, inténtalo más tarde.")

def main():
    # Token de acceso de tu bot
    token = "6307738962:AAEOr7Xel_u9t_vL1SFDcK-7iTFv26lYHzY"  # Reemplaza con tu token real
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
