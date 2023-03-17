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

# Define your button labels
button1_label = "GitHub"
button2_label = "LinkedIn"
button3_label = "YouTube"
button4_label = "Check Stats"
button5_label = "Generate Chart"
menu_button_label = "Menu"

# Define your button payloads
button1_payload = "button1"
button2_payload = "button2"
button3_payload = "button3"
button4_payload = "button4"
button5_payload = "button5"
menu_button_payload = "menu_button"

# Define your reply keyboard markup with buttons
keyboard1 = telebot.types.InlineKeyboardMarkup(row_width=2)
button1 = telebot.types.InlineKeyboardButton(button1_label, callback_data=button1_payload)
button2 = telebot.types.InlineKeyboardButton(button2_label, callback_data=button2_payload)
button3 = telebot.types.InlineKeyboardButton(button3_label, callback_data=button3_payload)
button4 = telebot.types.InlineKeyboardButton(button4_label, callback_data=button4_payload)
button5 = telebot.types.InlineKeyboardButton(button5_label, callback_data=button5_payload)
keyboard1.add(button1, button2, button3, button4, button5)

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
        bot.send_message(call.message.chat.id, "Please enter a valid GitHub link:", reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, get_github_link)
    elif call.data == button2_payload:
        bot.send_message(call.message.chat.id, "Please enter a valid LinkedIn link:", reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, get_linkedin_link)
    elif call.data == button3_payload:
        bot.send_message(call.message.chat.id, "Please enter a valid YouTube link:", reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, get_youtube_link)
    elif call.data == button4_payload:
        bot.send_message(call.message.chat.id, "Checking Stats...", reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, check_stats)
    elif call.data == button5_payload:
        bot.send_message(call.message.chat.id, "Generating Chart...", reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, generate_chart)
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


# Get the LinkedIn link from the user
def get_linkedin_link(message):
    linkedin_link = message.text
    if linkedin_link.startswith("https://www.linkedin.com/") or linkedin_link.startswith("www.linkedin.com/"):
        # Run the pars_git.py script and capture its output
        output = subprocess.check_output(['python', 'pars_linked.py', linkedin_link]).decode()
        # Send the output as a message
        bot.send_message(message.chat.id, output, reply_markup=keyboard2)
        bot.send_message(message.chat.id, "Returning to previous menu...", reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id,
                         "Please enter a valid LinkedIn link starting with 'https://www.linkedin.com/' or "
                         "'www.linkedin.com/'",
                         reply_markup=keyboard2)
        bot.register_next_step_handler(message, get_linkedin_link)


# Get the YouTube link from the user
def get_youtube_link(message):
    youtube_link = message.text
    if youtube_link.startswith("https://www.youtube.com/") or youtube_link.startswith("www.youtube.com/"):
        # Run the pars_git.py script and capture its output
        output = subprocess.check_output(['python', 'pars_you.py', youtube_link]).decode()
        # Send the output as a message
        bot.send_message(message.chat.id, output, reply_markup=keyboard2)
        bot.send_message(message.chat.id, "Returning to previous menu...", reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id,
                         "Please enter a valid YouTube link starting with 'https://www.youtube.com/' or "
                         "'www.youtube.com/'",
                         reply_markup=keyboard2)
        bot.register_next_step_handler(message, get_youtube_link)


# Check the stats of the GitHub repository
def check_stats(message):
    github_link = message.text
    if github_link.startswith("https://github.com/") or github_link.startswith("github.com/"):
        # Run the pars_git.py script and capture its output
        output = subprocess.check_output(['python', 'stats.py', github_link]).decode()
        # Send the output as a message
        bot.send_message(message.chat.id, output, reply_markup=keyboard2)
    else:
        bot.send_message(message.chat.id,
                         "Please enter a valid GitHub link starting with 'https://github.com/' or 'github.com/'",
                         reply_markup=keyboard2)
        bot.register_next_step_handler(message, check_stats)


# Generate a chart of the repository's activity and popularity
def generate_chart(message):
    print("hi")


# Start the bot
bot.polling()
