import os
import stripe
import secrets
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters

# Configurar tu clave secreta de API de Stripe
stripe.api_key = "sk_live_sWrF2uPsg8pBfIiPPPNxPHH4"  # Reemplaza con tu clave secreta de Stripe

# Generar una clave secreta para la generación de enlaces temporales
TEMP_LINK_SECRET = "X00CLAVESECRETAUNI68XXxx:"  # Cambia esto a tu propia clave secreta

# Diccionario para almacenar la información del usuario
user_info = {}

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
        [InlineKeyboardButton("Tarjeta de Crédito", callback_data='collect_info')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(message, reply_markup=reply_markup)

def collect_info(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()  # Acknowledge the button click
    
    user_info[query.message.chat.id] = {"chat_id": query.message.chat.id}
    
    message = "Por favor, ingresa los siguientes datos:\n\n"
    message += "Número de tarjeta (sin espacios ni guiones):\n"
    query.message.reply_text(message)
    
    context.user_data["collect_step"] = "card_number"

def process_info(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    step = context.user_data.get("collect_step")
    
    if step == "card_number":
        user_info[chat_id]["card_number"] = update.message.text
        context.user_data["collect_step"] = "name"
        update.message.reply_text("Ingresa tu nombre y apellidos:")
    elif step == "name":
        user_info[chat_id]["name"] = update.message.text
        context.user_data["collect_step"] = "phone"
        update.message.reply_text("Ingresa tu número de teléfono:")
    elif step == "phone":
        user_info[chat_id]["phone"] = update.message.text
        context.user_data["collect_step"] = "message"
        update.message.reply_text("Ingresa un mensaje adicional (opcional):")
    elif step == "message":
        user_info[chat_id]["message"] = update.message.text
        context.user_data.pop("collect_step")
        create_subscription(chat_id)

def create_subscription(chat_id):
    # Crear una suscripción en Stripe
    customer = stripe.Customer.create(email=user_info[chat_id]["chat_id"])
    subscription = stripe.Subscription.create(
        customer=customer.id,
        items=[
            {"price": "price_1Nl7wQFp9Pnzoti4T2M1C1Ly"}  # Reemplaza con el ID del precio que creaste en Stripe
        ]
    )

    # Generar un enlace temporal de invitación único
    temp_link = generate_temp_link(chat_id)
    invite_link = f'https://t.me/+QO3qSol1tMwwN2E8?start={temp_link}'
    
    # Enviar un mensaje al usuario con el enlace de pago y el enlace temporal
    payment_url = subscription.latest_invoice.hosted_invoice_url
    message = f"Haz clic en el enlace para realizar el pago: {payment_url}\n\n"
    message += f"O utiliza este enlace temporal para unirte al grupo: {invite_link}"
    message += "\n\nGracias por proporcionar la información. Tu suscripción está en proceso."
    
    # Limpiar la información del usuario
    user_info.pop(chat_id)
    
    # Enviar el mensaje
    context.bot
