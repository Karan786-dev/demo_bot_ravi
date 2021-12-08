import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
import requests
import pymongo

url = "mongodb+srv://bot_v2:bot_v2@cluster0.kzreu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
token = '5068117789:AAE7wyc_d_zrZfJy-8zmA_xPPICjgOM3Irg'
admins = [1468386562,1871392276]
client = pymongo.MongoClient(url)
db = client['Demo']
data = db['Demo2']
cha = db['channels']
num = db['numbers']


# Channels Check
def delete_cha2(username):
    cha.delete_one({"Channel": username})


def add_cha2(username):
    cha.insert_one({"Channel": username})


def check1(user):
    channels = cha.find({}, {"Channel": 1, "_id": 0})
    if channels == None:
        return "Not_added"
    for Data in channels:
        for x in Data.values():
            result = bot.get_chat_member(x, user).status
            if 'left' in result:
                return 'Left'


# Pymongo Database Function

def update_user(user, type, newdata):
    user_db = data.find_one({"User": user})
    if user_db == None:
        add_user(user, 'Ban')
    else:
        data.update_one({"User": user}, {"$set": {type: newdata}})


def update_bot(type, newdata):
    data.update_one({"Bot": "Bot"}, {"$set": {type: newdata}})
    return "Done"


def add_user(user, hh):
    if hh == 'Ban':
        user_data = {"User": user, "Balance": 0.0, "Wallet": "None", "Ban": "Ban", "w_amo": 0, "refer": 0,
                     "referby": "None","Verify":"Not"}
    else:
        user_data = {"User": user, "Balance": 0.0, "Wallet": "None", "Ban": "Unban", "w_amo": 0, "refer": 0,
                     "referby": "None","Verify":"Not"}
    data.insert_one(user_data)


def user_data(user, type):
    user_db = data.find_one({"User": user})
    if user_db == None:
        add_user(user, 'add')
    else:
        database = user_db[type]
        return database


def add_bot(type):
    BotData = {"Bot": "Bot", "P_refer": 1.0, "M_with": 2.0, "curr": "INR", "P_channel": "@IDK", "Totalu": 0,
               "Totalw": 0.0}
    data.insert_one(BotData)
    print("Bot New Data Has Been Installed")
    get_bot(type)


def get_bot(type):
    bot_find = data.find_one({"Bot": "Bot"})
    if bot_find == None:
        add_bot(type)
        return
    result = bot_find[type]
    return result


per_refer = get_bot('P_refer')
earn_more = '''*
🎁Earn Easy App 2 Payments Received

Sign Up Bonus ÷ 10 Rs

🔥Per Refer ÷ 10 Rs

😍 Minimum Withdraw 50 Rs

👍Refer Code ÷ *`KGU7p6ml`*

💰App Link ÷ https://play.google.com/store/apps/details?id=com.earneasy.app

⚠️Use Refer Code Else Minimum Withdraw 200 Hujayega And Sign Up Bonus Vi Nhi Milega*'''
bot = telebot.TeleBot(token)


def broad(message):
    all_user = data.find({}, {"User": 1, "_id": 0})
    for Data in all_user:
        for x in Data.values():
            bot.send_message(x, f"*📢Broadcast By Admin*\n\n{message.text}", parse_mode="Markdown")


def add_cha(message):
    msg = message.text
    user = message.chat.id
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.send_message(user, "*Channel Has Been Added Make Sure You Make Bot Admin In Channel*", parse_mode="Markdown")
    add_cha2(msg)


def delete_cha(message):
    msg = message.text
    user = message.chat.id
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.send_message(user, "*channel Has been Deleted*", parse_mode="Markdown")
    delete_cha2(msg)


def with_2(id):
    pay_c = get_bot('P_channel')
    curr = get_bot('curr')
    amo = get_bot('M_with')
    bal = user_data(id, 'Balance')
    wallet = user_data(id, "Wallet")
    if amo > bal:
        bot.send_message(id, "*⛔You Dont Have Enough Amount*", parse_mode="Markdown")
        return
    url = f"https://job2all.xyz/api/index.php?mid=1&mkey=2&guid=3&mob={wallet}&amount={amo}&info=Bot Payment| Made By @KaranYTop"
    r = requests.get(url)
    if r.text == "Please Enter 10 digit Mobile number." or r.text == "Mobile number not valid!.":
        bot.send_message(id, "*🗂️Please Set A Valid Mobile NUmber*", parse_mode="Markdown")
    else:
        bot.send_message(id, f"*⛔Withdrawl Request Procced\n\n🗂️Wallet : {wallet}\n\n💰Amount : {amo} {curr}*",
                         parse_mode="Markdown")
        oldus = get_bot("Totalw")
        newus = oldus + amo
        update_bot("Totalw", newus)
        oldbal = user_data(id, 'Balance')
        newbal = oldbal - amo
        update_user(id, 'Balance', float(newbal))
        bot.send_message(pay_c,
                         f"*⛔New Withdrawl Request Procced\n\n🧍User : *[{id}](tg://user?id={id})*\n\n🗂️Wallet : {wallet}\n\n💰Amount : {amo} {curr}*",
                         parse_mode="Markdown", disable_web_page_preview=True)


def menu(id):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('💰 Balance', '🙌🏻 Invite')
    keyboard.row('🗂 Wallet', '💳 Withdraw', '📊 Statistics')
    keyboard.row('💸Earn More')
    bot.send_message(id, "*🏡 Welcome To Main Menu*", parse_mode="Markdown", reply_markup=keyboard)


def set_prefer(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    curr = get_bot('curr')
    id = message.chat.id
    if message.text.isdigit == False:
        bot.send_message(id, "*Please Send A Valid ID*", parse_mode="Markdown")
    else:
        id = message.chat.id
        amo = message.text
        if amo < '1':
            haha = f'{amo}'
        else:
            haha = f'{amo}.0'
        set = update_bot('P_refer', float(haha))
        if set == "Done":
            bot.send_message(id, f"*Per Refer Has Been Set To {amo} {curr}*", parse_mode="Markdown")


def m_withdraw(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    curr = get_bot('curr')
    id = message.chat.id
    amo = int(message.text)
    update_bot("M_with", amo)
    bot.send_message(id, f"*Minimum Withdrwa Has Been Set To {amo} {curr}*", parse_mode="Markdown")


def set_curr(message):
    id = message.chat.id
    cur = message.text
    update_bot('curr', cur)
    bot.send_message(id, f"*Currency Has Been Set To {cur}*", parse_mode="Markdown")


def Pay_channel(message):
    id = message.chat.id
    cha = message.text
    update_bot('P_channel', cha)
    bot.send_message(id, f"*Your Payment Channel Has Been Set To {cha}*", parse_mode="Markdown")


def banu(message):
    id = message.chat.id
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    banid = message.text
    if banid.isdigit == True:
        bot.send_message(id, "*Please Send A Valid ID*", parse_mode="Markdown")
    else:
        update_user(int(banid), "Ban", "Ban")
        bot.send_message(id, "*User Has Been Banned*", parse_mode="Markdown")


def unbanu(message):
    id = message.chat.id
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    banid = message.text
    if banid.isdigit == True:
        bot.send_message(id, "*Please Send A Valid ID*", parse_mode="Markdown")
    else:
        update_user(int(banid), "Ban", "Unban")
        bot.send_message(id, "*User Has Been Unbanned*", parse_mode="Markdown")


def setnum(message):
    land = num.find_one({"Number": message.text})
    if message.text.isdigit == False:
        bot.send_message(message.chat.id, "*⛔Please Send A Valid Mobile Number*", parse_mode="Markdown")
    elif len(message.text) != 10:
        bot.send_message(message.chat.id, "*⛔Please Send A Valid Mobile Number*", parse_mode="Markdown")
    elif land != None:
        bot.send_message(message.chat.id, "*⛔This Number is Already Added In Bot*", parse_mode="Markdown")
    else:
        update_user(message.chat.id, "Wallet", message.text)
        num.insert_one({"Number": message.text, "User": message.chat.id})
        bot.send_message(message.chat.id, f"*🗂️Your Number Has Been Updated To {message.text}*", parse_mode="Markdown")


@bot.message_handler(commands=['add'])
def add(message):
    id = message.chat.id
    if id in admins:
        oldbal = user_data(id, 'Balance')
        newbal = oldbal + 1000
        update_user(id, 'Balance', float(newbal))


@bot.message_handler(commands=['panel'])
def panel(message):
    if message.chat.id in admins:
        pay_c = get_bot('P_channel')
        curr = get_bot('curr')
        m_with = get_bot('M_with')
        per_refer = get_bot('P_refer')
        channels = cha.find({}, {"Channel": 1, "_id": 0})
        if channels == None:
            return
        text = "*Channels : \n"
        for Data in channels:
            for x in Data.values():
                text += f"{x}\n"
        text += f"Per Refer : {per_refer} {curr}\nMinimun Withdraw : {m_with} {curr}\nPayment Channel : {pay_c}"
        text += "*"
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton('Per Refer',callback_data="Per_r"),InlineKeyboardButton('Minimum Withdraw',callback_data="Minimum_w"),
    InlineKeyboardButton("Add Channel",callback_data="Add_cha"),InlineKeyboardButton("Delete Channel",callback_data="Delete_cha"),InlineKeyboardButton("Pay Channel",callback_data="Pay_cha"),
    InlineKeyboardButton("Ban",callback_data="Ban"),InlineKeyboardButton("Unban",callback_data="Unban"),InlineKeyboardButton("Broadcast",callback_data="Broad"),
    InlineKeyboardButton("Set Currency",callback_data="Set_curr"))
        bot.send_message(message.chat.id,text, parse_mode="Markdown", reply_markup=markup)
@bot.callback_query_handler(func=lambda call : True)
def callbck_query(call):
    user = call.message.chat.id
    if call.data == 'Per_r':
        msg = bot.send_message(user, "*Send Amount You Want To Set*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, set_prefer)
    elif call.data == 'Minimum_w':
        msg = bot.send_message(user, "*Send Amount You Want To Set*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, m_withdraw)
    elif call.data == 'Add_cha':
        msg = bot.send_message(user, "*Send Channel Username You Want To Add*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, add_cha)
    elif call.data == 'Delete_cha':
        msg = bot.send_message(user, "*Send Channel Username You Want To Delete*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, delete_cha)
    elif call.data == 'Pay_cha':
        msg = bot.send_message(user, "*Send Channel Username You Want To Set*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, Pay_channel)
    elif call.data == 'Ban':
        msg = bot.send_message(user,"*Send His telegram Id*",parse_mode="Markdown")
        bot.register_next_step_handler(msg,banu)
    elif call.data == 'Unban':
        msg = bot.send_message(user, "*Send His Telegram Id*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, unbanu)
    elif call.data == 'Set_curr':
        msg = bot.send_message(user, "*Send Currency Name You Want To Set*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, set_curr)
    elif call.data == 'Broad':
        msg = bot.send_message(user, "*Send Message You Want To Broadcast*", parse_mode="Markdown")
        bot.register_next_step_handler(msg, broad)
    elif call.data == 'set_wallet':
        msg = bot.send_message(user, "*🗂️Send Your Paytm Number\n\n⚠️Notice: You Cant Change Your Wallet Again*",parse_mode="Markdown")
        bot.register_next_step_handler(msg, setnum)

def refer(user):
    curr = get_bot('curr')
    refer = user_data(user, 'refer')
    if refer == 0:
        update_user(user, 'refer', 1)
        oldus = get_bot('Totalu')
        newus = oldus + 1
        update_bot('Totalu', newus)
        hh = user_data(user, "referby")
        if int(hh) == user:
            return
        elif int(hh) == 1:
            return
        else:
            p_refer = get_bot('P_refer')
            oldB = user_data(int(hh), "Balance")
            newB = float(oldB) + float(p_refer)
            update_user(int(hh), "Balance", float(newB))
            bot.send_message(int(hh),
                             f"💰[{user}](tg://user?id={user})* {float(p_refer)} {curr} Added To Your Balance*",
                             parse_mode="Markdown")
    


def send_start(user):
    channels = cha.find({}, {"Channel": 1, "_id": 0})
    if channels == None:
        return
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    keyboard.row('🟢Joined')
    msg_start = "*⛔Must Join All Our Channel\n"
    for Data in channels:
        for x in Data.values():
            msg_start += f"\n {x}\n"
    msg_start += "\n✅After Joining, Click On '🟢Joined'"
    msg_start += "*"
    bot.send_message(user, msg_start, parse_mode="Markdown", reply_markup=keyboard)


def subs(user):
    check = check1(user)
    if check == 'Left':
        send_start(user)
    else:
        menu(user)
        refer(user)


@bot.message_handler(content_types=['contact'])
def contact(message):
    phone = message.contact.phone_number
    if phone.startswith("+91") or phone.startswith("91"):
        update_user(message.chat.id,"Verify","Done")
        subs(message.chat.id)
    else:
        update_user(int(message.chat.id), "Ban", "Ban")
        bot.send_message(message.chat.id, "*⛔Only Indian Accounts Are Allowed*", parse_mode="Markdown")


@bot.message_handler(commands=['start'])
def start(message):
    user = message.chat.id
    msg = message.text
    username = message.from_user.username
    if username == None:
        update_user(int(user), "Ban", "Ban")
        return
    ban = user_data(user, 'Ban')
    if ban == "Ban":
        bot.send_message(message.chat.id, "*You Are Banned From Using This Bot*", parse_mode="Markdown")
        return
    user_data(user, "User")
    try:
        refid = message.text.split()[1]
    except:
        refid = 1
    refer = user_data(user, 'refer')
    if refer == 0:
        update_user(user, "referby", refid)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="🔰Share Contact", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id,
                     "*© Share Your Contact In Order\nTo Use This Bot ,It's Just A Number Verification\n\n⚠️Note :* `We Will Never Share Your Details With Anyone`",
                     parse_mode="Markdown", reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def send_text(message):
    curr = get_bot('curr')
    m_with = get_bot('M_with')
    per_refer = get_bot('P_refer')
    user = message.chat.id
    if user in admins:
        admin = user
    else:
        admin = 1
    msg = message.text
    wallet = user_data(user, "Wallet")
    ban = user_data(user, 'Ban')
    verify = user_data(user,'Verify')
    if verify == "Not":
        bot.send_message(user,"*Please Verify Your Account First /start*",parse_mode="Markdown")
        return
    elif ban == "Ban":
        bot.send_message(message.chat.id, "*You Are Banned From Using This Bot*", parse_mode="Markdown")
        return
    elif msg == "🟢Joined":
        subs(user)
        bot.delete_message(message.chat.id,message.message_id)
        bot.delete_message(message.chat.id,message.message_id-1)
    elif message.text == "💰 Balance":
        balance = user_data(user, 'Balance')
        wallet = user_data(user, 'Wallet')
        msg = f'*🙌🏻 User = {message.from_user.first_name}\n\n💰 Balance = {balance} {curr}\n\n🗂️Wallet : *`{wallet}`'
        bot.send_message(message.chat.id, msg, parse_mode="Markdown")
    elif message.text == "🙌🏻 Invite":
        user = message.chat.id
        bot_name = bot.get_me().username
        msg = f"*🙌🏻 User = {message.from_user.first_name}\n\n🙌🏻 Your Invite Link = https://t.me/{bot_name}?start={user}\n\n🧬Invite To {per_refer} {curr}*"
        bot.send_message(user, msg, parse_mode="Markdown")
    elif message.text == "🗂 Wallet":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(f'🚧 Set {curr} Wallet 🚧',callback_data="set_wallet"))
        text = f"*💡 Your Currently Set {curr} Wallet Is: *`'{wallet}'`*\n\n🗂 It Will Be Used For Future Withdrawals*"
        bot.send_message(user,text,parse_mode="Markdown",reply_markup=markup)
    elif message.text == "📊 Statistics":
        id = message.chat.id
        witth = get_bot('Totalw')
        total = get_bot('Totalu')
        msg = f"*📊 Bot Live Stats 📊\n\n📤 Total Payouts : {witth} {curr}\n\n💡 Total Users : {total} Users\n\n🔎 Coded By: *[ⲘᏒ᭄кᴀʀᴀɴ✓](https://t.me/KaranYTop)"
        bot.send_message(id, msg, parse_mode="Markdown", disable_web_page_preview=True)
    elif message.text == "💳 Withdraw":
        id = message.chat.id
        bal = user_data(id, 'Balance')
        wallet = user_data(id, "Wallet")
        if bal < m_with:
            bot.send_message(id, f"*⛔You Need {m_with} {curr} To Withdraw*", parse_mode="Markdown")
        elif wallet == "None":
            bot.send_message(id, "*⛔Please Set Your Wallet First*", parse_mode="Markdown")
        else:
            with_2(id)
    elif message.text == "💸Earn More":
        bot.send_message(message.chat.id, earn_more, parse_mode="Markdown", disable_web_page_preview=True)



print("Done")
if __name__ == "__main__":
    bot.polling(none_stop=True)
