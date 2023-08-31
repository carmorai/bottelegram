import os
import stripe
import secrets
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Configurar tu clave secreta de API de Stripe
stripe.api_key = "sk_live_sWrF2uPsg8pBfIiPPPNxPHH4"  # Reemplaza con tu clave secreta de Stripe

# Generar una clave secreta para la generación de enlaces temporales
TEMP_LINK_SECRET = "X00CLAVESECRETAUNI68XXxx:"  # Cambia esto a tu propia clave secreta

def generate_temp_link(user_id):
    return secrets.token_urlsafe(32)  # Genera un token seguro para el enlace temporal

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
        # Crear una suscripción en Stripe
        customer = stripe.Customer.create(email=query.message.chat.username)
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {"price": "price_1Nl7wQFp9Pnzoti4T2M1C1Ly"}  # Reemplaza con el ID del precio que creaste en Stripe
            ]
        )
        
        # Generar un enlace temporal de invitación único
        temp_link = generate_temp_link(query.message.chat.id)
        invite_link = f'https://t.me/+QO3qSol1tMwwN2E8?start={temp_link}'
        
        # Enviar un mensaje al usuario con el enlace de pago y el enlace temporal
        payment_url = subscription.latest_invoice.hosted_invoice_url
        message = f"Haz clic en el enlace para realizar el pago: {payment_url}\n\n"
        message += f"O utiliza este enlace temporal para unirte al grupo: {invite_link}"
        query.message.reply_text(message)

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
