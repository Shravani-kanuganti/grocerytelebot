import telebot
from telebot import types
import pandas as pd
from telebot.types import Message
from inventory import *
import stripe

# create a bot instance
bot = telebot.TeleBot('6018302450:AAGgysKcaVLiUgDXqQ11-lMZUC7_YWvf-KU')


# define the handler for the /start command
@bot.message_handler(commands=['start'])
def start_handler(message):
    # create a new keyboard with two buttons
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Rice', callback_data='button1')
    button2 = types.InlineKeyboardButton(text='Grains', callback_data='button2')
    button3 = types.InlineKeyboardButton(text='Oils', callback_data='button3')
    button4 = types.InlineKeyboardButton(text='Chips', callback_data='button4')
    button5 = types.InlineKeyboardButton(text='Biscuits', callback_data='button5')
    button6 = types.InlineKeyboardButton(text='Cleaning and household', callback_data='button6')
    button7 = types.InlineKeyboardButton(text='Chocolates', callback_data='button7')
    button8 = types.InlineKeyboardButton(text='Oral care', callback_data='button8')
    button9=types.InlineKeyboardButton(text='🛒Cart',callback_data='button9')
    keyboard.add(button1, button2,button3, button4,button5, button6,button7,button8,button9)
    
    # send a message with the key      board to the user
    bot.send_message(chat_id=message.chat.id, text='Shop by Category', reply_markup=keyboard)

def tableoutput(items):
    output="{:<30} {:<10} {:<10} \n".format("Name","Price","Quantity")
    for item in items:
        output += "{:<30} {:<10} {:<10} \n".format(item['name'],item['price'],item['qty'])
    final_string="```\n"+output.rstrip() + "\n```"
    return final_string
     
def tableoutput_cart(items,user_id):
    output="{:<30} {:<10} {:<10} \n".format("Name","Price","Quantity")
    for item in items:
        if user_id == item['user']:
            output += "{:<30} {:<10} {:<10} \n".format(item['name'],item['price'],item['qty'])
    final_string="```\n"+output.rstrip() + "\n```"
    return final_string

def reduce_qty(rice,qty,count):
    if rice == inventory:
        a = inventory[count]['qty']-qty
        if a<0:
            return False
        inventory[count]['qty'] = a
    elif rice == inventoryf:
        a = inventoryf[count]['qty']-qty
        if a<0:
            return False
        inventoryf[count]['qty']=a
    elif rice == oil_inventory:
        a = oil_inventory[count]['qty']-qty
        if a<0:
            return False
        oil_inventory[count]['qty']=a
    elif rice == inventory_chips:
        a = inventory_chips[count]['qty']-qty
        if a<0:
            return False
        inventory_chips[count]['qty']=a
    elif rice == biscuits_inventory:
        a = biscuits_inventory[count]['qty']-qty
        if a<0:
            return False
        biscuits_inventory[count]['qty']=a
    elif rice == cleaning_inventory:
        a = cleaning_inventory[count]['qty']-qty
        if a<0:
            return False
        cleaning_inventory[count]['qty']=a
    elif rice == chocolate_inventory:
        a = chocolate_inventory[count]['qty']-qty
        if a<0:
            return False
        chocolate_inventory[count]['qty']=a
    elif rice == oral_care_inventory:
        a = oral_care_inventory[count]['qty']-qty
        if a<0:
            return False
        oral_care_inventory[count]['qty']=a

    return True

cart = []   
rice = []
amount = {}

@bot.message_handler(func=lambda message: True)
def handle_message(message: Message):
    print("check")
    text = message.text
    user_id = message.from_user.id
    print(message)
    print(user_id)
    x=text.split(",")
    x[0] = x[0].replace(" ", "").lower()
    print("x  : ",x)
    print("rice = ",rice)
    # price("items = ",items_list)
    count=-1
    for item in rice:
        count=count+1
        name = item['name'].replace(" ", "").lower()
        if name.find(x[0])>=0 and len(x)>1:
            qty=int(x[1].strip(" "))
            can_place = reduce_qty(rice,qty,count)
            if not can_place:
                bot.send_message(chat_id=message.chat.id,text="Item can't be added to cart. Add quantity <"+str(item['qty']))
                break
            cart.append({"name":item['name'],"price":qty*int(item['price']),"qty":qty, 'user':user_id})
            
            # inventory[count]['qty']=int(item['qty'])-qty
            bot.send_message(chat_id=message.chat.id,text="Item added to cart Successfully!!\n Continue your Shopping")
            start_handler(message)
        
        
    if 'y' == x[0] or 'yes' == x[0]:

        keyboard = types.InlineKeyboardMarkup()
        cash_pay = types.InlineKeyboardButton(text='Cash on delivery', callback_data='cash_pay')
        online_pay = types.InlineKeyboardButton(text='UPI payment', callback_data='online_pay')
        keyboard.add(cash_pay, online_pay)
        bot.send_message(chat_id=message.chat.id, text='Payment options', reply_markup=keyboard)
    elif 'n' == x[0] or 'No' == x[0]:
        start_handler(message)
    elif (len(x[0])==1 and (x[0]!='y' or x[0]!='n')):
        bot.send_message(chat_id=message.chat.id,text="Please enter yes or no")
    elif(len(x)==1):
        bot.send_message(chat_id=message.chat.id,text="Wrong format!! (Example: Enter "+x[0]+",6)")


# define the handler for button click events
@bot.callback_query_handler(func=lambda call: True)
def button_click_handler(call):
    global rice
    global cart
    if call.data == 'cash_pay':
        bot.send_message(chat_id=call.message.chat.id, text='Cash on delivery accepted \n Order Placed Successfully !!!')
        user_id = call.from_user.id
        cart = [item for item in cart if item['user'] != user_id]
        print("cart Item : ",cart)


    elif call.data == 'online_pay':
        # upi_id = "9234568741@upi"  # Replace with a dummy UPI ID
        # name = "generalstore"  # Replace with a dummy name
        # mobile_number = "9234568741"  # Replace with a dummy mobile number
        user_id = call.from_user.id
        #  # Define a message handler for the '/pay' command
        # @bot.message_handler(commands=['pay'])
        # def handle_pay(message):
        #       # Get the amount to be paid from the user's message
        #     try:
             
        #      # Total  = int(message.text.split()[1])
        #      print("payment")
        #     except (ValueError, IndexError):
        #         bot.send_message(message.chat.id, text = "Please specify a valid amount.")
        #     return

        #     # Generate a dummy UPI link
        # upi_link = f"upi://{upi_id}?amount={amount[user_id]}&name={name}"
        # handle_pay(call.message)
        

        # Set your Stripe API test key
        stripe.api_key = "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"

        # Create a payment intent
        intent = stripe.PaymentIntent.create(
            amount=amount[user_id],
            currency="INR"
        )

        # Get the payment intent's client secret
        client_secret = intent.client_secret

        # Construct the payment URL using the client secret
        payment_url = "https://checkout.stripe.com/pay/" + client_secret + "/test"

        # Redirect the user to the payment URL
        # (Note: this example assumes you are using Flask)
        

        # Send the UPI link to the user
        bot.send_message(call.message.chat.id, f"Please use this link to complete your payment: {payment_url}")
        #bot.send_message(chat_id=call.message.chat.id, text='Currently not accepting online payments .. Continuing with cash on delivery')
    if call.data == 'button1':
        # define the handler for
        bot.send_message(chat_id=call.message.chat.id, text='Rice types available:')
        
        rice=inventory
        final_string=tableoutput(rice)
        print(final_string)
        bot.send_message(chat_id=call.message.chat.id, text=final_string,parse_mode='Markdown')
        bot.send_message(chat_id=call.message.chat.id, text='Enter the name of product,quantity in number')       

    elif call.data == 'button2':
        bot.send_message(chat_id=call.message.chat.id, text='Grain types available:')
        rice=inventoryf
        final_string=tableoutput(rice)
        print(final_string)
        bot.send_message(chat_id=call.message.chat.id, text=final_string,parse_mode='Markdown')
        bot.send_message(chat_id=call.message.chat.id, text='Enter the name of product,quantity in number')       

    elif call.data == 'button3':
        bot.send_message(chat_id=call.message.chat.id, text='Oil types available:')
        rice =oil_inventory
        final_string=tableoutput(rice)
        print(final_string)
        bot.send_message(chat_id=call.message.chat.id, text=final_string,parse_mode='Markdown')
        bot.send_message(chat_id=call.message.chat.id, text='Enter the name of product,quantity in number')       
    
    elif call.data == 'button4':
        bot.send_message(chat_id=call.message.chat.id, text='Chips available:')
        rice=inventory_chips
        final_string=tableoutput(rice)
        print(final_string)
        bot.send_message(chat_id=call.message.chat.id, text=final_string,parse_mode='Markdown')
        bot.send_message(chat_id=call.message.chat.id, text='Enter the name of product,quantity in number')       
    elif call.data == 'button5':
        bot.send_message(chat_id=call.message.chat.id, text='Bisciuts available:')
        rice=biscuits_inventory
        final_string=tableoutput(rice)
        print(final_string)
        bot.send_message(chat_id=call.message.chat.id, text=final_string,parse_mode='Markdown')
        bot.send_message(chat_id=call.message.chat.id, text='Enter the name of product,quantity in number')

    elif call.data == 'button6':
        bot.send_message(chat_id=call.message.chat.id, text='Cleaning & household available:')
        rice=cleaning_inventory
        final_string=tableoutput(rice)
        print(final_string)
        bot.send_message(chat_id=call.message.chat.id, text=final_string,parse_mode='Markdown')
        bot.send_message(chat_id=call.message.chat.id, text='Enter the name of product,quantity in number')       
    elif call.data == 'button7':
        bot.send_message(chat_id=call.message.chat.id, text='Chocolates available:')
        rice=chocolate_inventory
        final_string=tableoutput(rice)
        print(final_string)
        bot.send_message(chat_id=call.message.chat.id, text=final_string,parse_mode='Markdown')
        bot.send_message(chat_id=call.message.chat.id, text='Enter the name of product,quantity in number')       


    elif call.data == 'button8':
        bot.send_message(chat_id=call.message.chat.id, text='Oral Care items available:')
        rice=oral_care_inventory
        final_string=tableoutput(rice)
        print(final_string)
        bot.send_message(chat_id=call.message.chat.id, text=final_string,parse_mode='Markdown')
        bot.send_message(chat_id=call.message.chat.id, text='Enter the name of product,quantity in number')       

    elif call.data == 'button9':
        user_id = call.from_user.id
        print("user_id in button9: ",user_id)
        print("call data : ",call)
        bill=0
        for items in cart:
            if user_id == items['user']:
                bill=bill+items['price']
        if bill==0:
              bot.send_message(chat_id=call.message.chat.id,text="No Items in your cart")
              start_handler(call.message)
        else:
            amount[user_id]= bill
            print("amount : ",amount)
            bot.send_message(chat_id=call.message.chat.id,text="Your items in cart are: ")
            final_string=tableoutput_cart(cart,user_id)
            bot.send_message(chat_id=call.message.chat.id, text=final_string,parse_mode='Markdown')  
            bot.send_message(chat_id=call.message.chat.id,text="Total Amount : "+str(bill))
            bot.send_message(chat_id=call.message.chat.id,text="Are you willing to check out y or n")
bot.polling()