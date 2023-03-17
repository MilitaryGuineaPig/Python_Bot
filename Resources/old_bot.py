import telebot
import os
import subprocess

# Set up your bot using your bot token
bot = telebot.TeleBot('6259149794:AAGmRnVUJ-OvvHSLsKmvPmUIk6T642jreWY')
# Check if bot is connected
try:
    bot_info = bot.get_me()
    print('Bot is connected:', bot_info.first_name, bot_info.last_name)
except Exception as e:
    print('Bot is not connected:', e)


def read_commands():
    with open('/Resources/Commands.txt', 'r') as f:
        commands = f.read().splitlines()
    return commands


# Define your button labels
button1_label = "List of commands"
button2_label = "Get GitHub Stat"
menu_button_label = "Menu"

# Define your button payloads
button1_payload = "button1"
button2_payload = "button2"
menu_button_payload = "menu_button"

# Define your reply keyboard markup with buttons
keyboard1 = telebot.types.InlineKeyboardMarkup(row_width=2)
button1 = telebot.types.InlineKeyboardButton(button1_label, callback_data=button1_payload)
button2 = telebot.types.InlineKeyboardButton(button2_label, callback_data=button2_payload)
keyboard1.add(button1, button2)

keyboard2 = telebot.types.InlineKeyboardMarkup(row_width=1)
menu_button = telebot.types.InlineKeyboardButton(menu_button_label, callback_data=menu_button_payload)
keyboard2.add(menu_button)


# Send a message with the first keyboard to the user
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to Stat Bot! Choose an action:", reply_markup=keyboard1)


# Handle button taps
@bot.callback_query_handler(func=lambda call: True)
def handle_button_tap(call):
    if call.data == button1_payload:
        commands = read_commands()
        bot.send_message(call.message.chat.id, '\n'.join(commands), reply_markup=keyboard2)
    elif call.data == button2_payload:
        bot.send_message(call.message.chat.id, "Please enter a valid GitHub link:", reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, get_github_link)
    elif call.data == menu_button_payload:
        bot.send_message(call.message.chat.id, "\tMenu!\n Choose an action:", reply_markup=keyboard1)
    else:
        bot.send_message(call.message.chat.id, "Unknown button tapped.")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  reply_markup=None)


# Get the GitHub link from the user
def get_github_link(message):
    github_link = message.text
    if github_link.startswith("https://github.com/") or github_link.startswith("github.com/"):
        # Run the pars_git.py script and capture its output
        output = subprocess.check_output(['python', 'pars_git.py', github_link]).decode()
        # Send the output as a message
        bot.send_message(message.chat.id, output, reply_markup=keyboard2)
    else:
        bot.send_message(message.chat.id,
                         "Please enter a valid GitHub link starting with 'https://github.com/' or 'github.com/'",
                         reply_markup=keyboard2)
        bot.register_next_step_handler(message, get_github_link)


# Start the bot
bot.polling()
