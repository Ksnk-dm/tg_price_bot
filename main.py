import telebot
import requests

print("start")
bot = telebot.TeleBot('7268824882:AAHVzSerGR1SpHoHkvs13Gswun-QlI0Uku0')

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    res = requests.get('https://stores-api.zakaz.ua/stores/48246401/products/search?q=04820017003087')
    json = res.json()
    results = json['results']
    prices = [item['price'] for item in results]
    name = [item['title'] for item in results]

    prices_str = ', '.join(map(str, prices))
    names_str = ', '.join(name)
    user_id = message.from_user.id
    bot.reply_to(message, f"{prices_str} {names_str}")



bot.infinity_polling()