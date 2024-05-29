import telebot
import requests
import cv2 
from pyzbar.pyzbar import decode
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

print("start")
bot = telebot.TeleBot('7268824882:AAHVzSerGR1SpHoHkvs13Gswun-QlI0Uku0')

def format_price(price):
    price_str = str(price)
    if len(price_str) > 2:
        return price_str[:-2] + ',' + price_str[-2:]
    return price_str

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Сохранение изображения
        src = 'photo.jpg'
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Распознавание штрих-кода
        barcode_data = BarcodeReader(src)
        print(f"sss {barcode_data}")
        if barcode_data:
          
            res = requests.get(f'https://stores-api.zakaz.ua/stores/48246401/products/search?q={barcode_data}')
            json = res.json()
            results = json['results']
            prices = [item['price'] for item in results]
            names = [item['title'] for item in results]
            images = [item['img']['s350x350'] for item in results if 'img' in item and 's350x350' in item['img']]
            url = [item['web_url'] for item in results]
            print(f"s11 {images}")
            formatted_prices = [format_price(price) for price in prices]
            prices_str = ', '.join(formatted_prices)
            names_str = ', '.join(names)
            img_str = ', '.join(images)
            url_str = ', '.join(url)

            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(InlineKeyboardButton(f"Ашан: {prices_str}", callback_data='button1', url= f"{url_str}" ),
                 InlineKeyboardButton("Сільпо", callback_data='button2'),
                 InlineKeyboardButton("Ашан", callback_data='button3'),
                 InlineKeyboardButton("Фора", callback_data='button4'))
            # Отправка ответа пользователю
            bot.reply_to(message, f"Prices: {prices_str}\nProducts: {names_str}\nProducts: {img_str}", reply_markup=keyboard)
        else:
            bot.reply_to(message, "Barcode not detected or the image is corrupted.")
        
        # Удаление изображения после обработки
        os.remove(src)
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")


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

def BarcodeReader(image): 
    img = cv2.imread(image)
    detectedBarcodes = decode(img)
    
    if not detectedBarcodes: 
        print("Barcode Not Detected or your barcode is blank/corrupted!")
        return None
    else:
        for barcode in detectedBarcodes:
            if barcode.data != "":
                return barcode.data.decode("utf-8")
    return None
                  
    #Display the image 
    # cv2.imshow("Image", img) 
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows() 

bot.polling(none_stop=True)