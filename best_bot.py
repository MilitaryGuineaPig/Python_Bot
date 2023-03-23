import telebot
import subprocess
from linkedin_api import Linkedin

with open('/Users/monkey/Public/Python/Hidden files/LinkedIn_Bot.txt', 'r') as file:
    key = file.readline().rstrip('\n')
    mail = file.readline().rstrip('\n')
    passwd = file.readline().rstrip('\n')
bot = telebot.TeleBot(key)
# Check if bot is connected
try:
    bot_info = bot.get_me()
    print('Bot is connected:', bot_info.first_name)
except Exception as e:
    print('Bot is not connected:', e)

# Define your button labels
github_button_label = "GitHub"
linkedin_button_label = "LinkedIn"
png_button_label = "PNG"
pdf_button_label = "PDF"
chart_button_label = "Chart"
menu_button_label = "Menu"
# Define your button payloads
github_btn_pl = "github_press"
linkedin_btn_pl = "linkedin_press"
png_btn_pl = "png_press"
pdf_btn_pl = "pdf_press"
chart_btn_pl = "chart_press"
menu_btn_pl = "menu_press"
# Define buttons
github_press = telebot.types.InlineKeyboardButton(github_button_label, callback_data=github_btn_pl)
linkedin_press = telebot.types.InlineKeyboardButton(linkedin_button_label, callback_data=linkedin_btn_pl)
png_press = telebot.types.InlineKeyboardButton(png_button_label, callback_data=png_btn_pl)
pdf_press = telebot.types.InlineKeyboardButton(pdf_button_label, callback_data=pdf_btn_pl)
chart_press = telebot.types.InlineKeyboardButton(chart_button_label, callback_data=chart_btn_pl)
menu_press = telebot.types.InlineKeyboardButton(menu_button_label, callback_data=menu_btn_pl)
# Define your 1 keyboard
keyboard1 = telebot.types.InlineKeyboardMarkup(row_width=1)
keyboard1.add(github_press, linkedin_press)
# Define your 2 keyboard
keyboard2 = telebot.types.InlineKeyboardMarkup(row_width=1)
keyboard2.add(menu_press)
# Define your 3 keyboard
keyboard3 = telebot.types.InlineKeyboardMarkup(row_width=3)
keyboard3.add(png_press, pdf_press, chart_press, menu_press)


# Send a message with the first keyboard to the user
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to Stat Bot! Choose the site:", reply_markup=keyboard1)


# Handle button taps
@bot.callback_query_handler(func=lambda call: True)
def handle_button_tap(call):
    if call.data == github_btn_pl:
        bot.send_message(call.message.chat.id, "Please enter a valid GitHub link:", reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, get_github_link)
    elif call.data == linkedin_btn_pl:
        bot.send_message(call.message.chat.id, "Please enter a valid LinkedIn link:", reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, get_linkedin_link)
    elif call.data == png_btn_pl:
        bot.send_message(call.message.chat.id, "PNG...", reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, png_gen)
    elif call.data == pdf_btn_pl:
        bot.send_message(call.message.chat.id, "PDF...", reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, pdf_gen)
    elif call.data == chart_btn_pl:
        bot.send_message(call.message.chat.id, "Chart...", reply_markup=keyboard2)
        bot.register_next_step_handler(call.message, chart_gen)
    elif call.data == menu_btn_pl:
        bot.send_message(call.message.chat.id, "\tMenu!\n Choose the site:", reply_markup=keyboard1)
    else:
        bot.send_message(call.message.chat.id, "Unknown button tapped.")
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)


# GitHub part
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


# Linkedin part
def get_linkedin_link(message):
    linkedin_link = message.text
    if linkedin_link.startswith("https://www.linkedin.com/") or linkedin_link.startswith("www.linkedin.com/"):
        # Authenticate using bot account
        api = Linkedin(mail, passwd)
        parts = linkedin_link.split("/")
        username = parts[-1]
        # GET a profile
        profile = api.get_profile(username)
        # Writing data
        with open(f"user_info_{message.chat.id}.txt", "w") as f:
            f.write(f"\t\t{profile['firstName']}'s dossier\n\n")
            f.write(f"Full Name: {profile['firstName']} {profile['lastName']}\n")
            f.write(f"Type of employment: {profile['headline']} \n")
            f.write(f"\t\tSkills:\n")
            counter = 0
            for edu in profile['skills']:
                if 'name' in edu:
                    counter = counter + 1
                    school_name = edu['name']
                    f.write(f" {counter}) {school_name} \n")
                else:
                    print("No school information available")
            counter = 0
            f.write(f"\t\tEducation:\n")
            for edu in profile['education']:
                if 'school' in edu:
                    counter = counter + 1
                    school_name = edu['school']['schoolName']
                    f.write(f"#{counter}: {school_name} \n")
                else:
                    print("No school information available")
            f.write(f"Location: {profile['locationName']} {profile['geoLocationName']}\n")
            f.write(f"\t\tBrief Information\n")
            f.write(f"{profile['summary']} \n")
        # Sending a file
        bot.send_document(chat_id=message.chat.id,
                          document=open(f'/Users/monkey/Public/Python/Python_Bot/user_info_{message.chat.id}.txt',
                                        'rb'))

        bot.send_message(message.chat.id, "Choose another format or return :)", reply_markup=keyboard3)
    else:
        bot.send_message(message.chat.id, "Please enter a valid LinkedIn link starting with 'https://www.linkedin.com/'"
                                          " or 'www.linkedin.com/'", reply_markup=keyboard2)
        bot.register_next_step_handler(message, get_linkedin_link)


def png_gen():

   print("hi")


def pdf_gen():
    print("pdf")


def chart_gen():
    print("chart")


# Start the bot
bot.polling()
