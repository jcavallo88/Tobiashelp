import instabot
import telegram
from telegram.ext import Updater,CommandHandler,MessageHandler,ConversationHandler, Filters
from telegram.ext import CallbackQueryHandler, PicklePersistence
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from instabot.api.api import API 

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)

u = Updater(token='987812301:AAGQhKRmFoWsD_HJ4PqEnKMKkvo4FtCT2T0', use_context=True)
credict = {}
SOLVEVCHALLENGEHELPER = 0
SOLVEVCHALLENGEHELPER2 = 1
dispatcher = u.dispatcher
PASSWORD = 1
PASSWORDHANDLE = 0
HOME = 2
RHELPER = 3
lockdict = {}

j = u.job_queue
botlist = []
lastmediacheck = {}
acceptedusers = ['Idyllic']
logger.info("starting")
globalcount = [0]
botdict = {}
    
def start(update, context):
    logger.info("/start")
    keyboard = [[InlineKeyboardButton("Login", callback_data='button1'),
             InlineKeyboardButton("FAQ", callback_data='button2')],
          [InlineKeyboardButton("My Accounts", callback_data='button3'),
             InlineKeyboardButton("Groupchat", url = "https://t.me/theboostme")],[InlineKeyboardButton("Current Users", callback_data='button5'),
             InlineKeyboardButton("Remove Accounts", callback_data='button6')]]
    name = update.effective_user.first_name
    reply_markup = InlineKeyboardMarkup(keyboard)
    startext = "Hello " + name + " and welcome to *Boostme*!" + "\n" + "" + "\n" + "This bot utilizes automatic likes to help you organically grow your Instagram account; around 30 seconds after you post a photo you will see likes flow in from our other users." + "\n" + "" + "\n" + "At the moment *BoostMe* is completely free to use and enjoy. If you are unfamiliar with autolikes it is highly recommended that you read our FAQ before starting!" + "\n" + "" + "\n" + "If you have any other questions feel free to contact our admins!"
    update.message.reply_text(startext, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN)
    

def return_start(update, context):
    logger.info("/return_start")
    logger.debug("/return_start")
    keyboard = [[InlineKeyboardButton("Login", callback_data='button1'),
             InlineKeyboardButton("FAQ", callback_data='button2')],
          [InlineKeyboardButton("My Accounts", callback_data='button3'),
             InlineKeyboardButton("Groupchat", url = "https://t.me/theboostme")],[InlineKeyboardButton("Current Users", callback_data='button5'),
             InlineKeyboardButton("Remove Accounts", callback_data='button6')]]
    name = update.effective_user.first_name
    reply_markup = InlineKeyboardMarkup(keyboard)
    startext = "Hello " + name + " and welcome to *Boostme*!" + "\n" + "" + "\n" + "This bot utilizes automatic likes to help you organically grow your Instagram account; around 30 seconds after you post a photo you will see likes flow in from our other users." + "\n" + "" + "\n" + "At the moment *BoostMe* is completely free to use and enjoy. If you are unfamiliar with autolikes it is highly recommended that you read our FAQ before starting!" + "\n" + "" + "\n" + "If you have any other questions feel free to contact our admins!"
    logger.debug(update.callback_query.edit_message_text(startext, reply_markup=reply_markup, parse_mode=telegram.ParseMode.MARKDOWN))

def my_accounts(update, context):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("Return Home", callback_data='returnhome2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    accountinfo = ""
    if len(context.user_data) == 0:
        query.edit_message_text(text="You have no accounts currently in the system",reply_markup=reply_markup)
    else:
        for key in context.user_data:
            followers = len(botlist[0].get_user_following(key))
            accountinfo += ("@" + key + " , Followers: " + str(followers) + '\n')
        query.edit_message_text(text="Your *current* *accounts*: " + '\n' + accountinfo,reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)

def removeaccount(update, context):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("Return Home", callback_data='returnhome2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    accountinfo = ""
    if len(context.user_data) == 0:
        query.edit_message_text(text="You have no accounts registered with us yet",reply_markup=reply_markup)
    else:
        for key in context.user_data:
            followers = len(botlist[0].get_user_following(key))
            accountinfo += ("@" + key + " , Followers: " + str(followers) + '\n')
        query.edit_message_text(text="Respond with the username of the account you would like to remove. (no @)" + "\n" + "" + "\n" + accountinfo, reply_markup=reply_markup)
    return RHELPER

def rhelper(update, context):
    logger.info("rhelp")
    toremove = update.message.text
    keyboard = [[InlineKeyboardButton("Return Home", callback_data='returnhome2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if toremove not in user_data:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, the account you specified is not currently registered under you.",reply_markup=reply_markup)
    else:
        idx = botdict[toremove]
        del context.user_data[toremove]
        del botlist[idx]
        context.bot.send_message(chat_id=update.effective_chat.id, text="I removed " + toremove + " , you will no longer recieve or give likes.",reply_markup=reply_markup)      

def users(update, context):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("Return Home", callback_data='returnhome2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    accountinfo = ""
    accountcount = 0
    if len(credict) == 0:
        query.edit_message_text(text="There are currently no accounts registered with us",reply_markup=reply_markup)
    else:
        followersum = 0
        for key in credict:
            accountcount +=1
            followers = len(botlist[0].get_user_following(key))
            followersum += followers
            accountinfo += ("@" + key + " , Followers: " + str(followers) + '\n')
        query.edit_message_text(text="*Our total reach*: " + str(followersum) + "\n" + "" + "\n"+ "*Total accounts in the system*: " + str(accountcount) + "\n" + "" + "\n" + "*Current users*: " + '\n' + accountinfo,reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)       

def addaccount(update, context):
    logger.info("/addaccount")
    query = update.callback_query
    query.edit_message_text(text="Send the username of the account that you want to add, or /cancel")
    return PASSWORD

def password(update, context):
    logger.info("/password")
    username = update.message.text
    keyboard = [[InlineKeyboardButton("Return Home", callback_data='returnhome2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    #if len(botlist) != 0:
        #checkid = botlist[0].get_user_id_from_username(username)
        #if checkid == None:
            #context.bot.send_message(chat_id=update.effective_chat.id, text="That username does not belong to any account on Instagram.",reply_markup=reply_markup)
            #return ConversationHandler.END
            
    newid = update.effective_user.username
    (context.chat_data)[newid] = [username]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Awesome now send your password, or use /cancel to cancel")
    return PASSWORDHANDLE

def passwordhandle(update, context):
    logger.info("/passwordhandle")
    keyboard = [[InlineKeyboardButton("Return Home", callback_data='returnhome2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    newid = update.effective_user.username
    password = update.message.text
    (context.chat_data)[newid].append(password) #adds to local dict, specifc to chat...
    botid = str(update.effective_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Processing give me a second...")
    if context.chat_data[newid][0] in lockdict:
        botid = lockdict[context.chat_data[newid][0]]
    else:
        botid = instabot.Bot(like_delay=4,max_likes_per_day=100000000,max_unlikes_per_day=10000000,max_follows_per_day=3500000,max_unfollows_per_day=350000000,max_comments_per_day=1000000,max_blocks_per_day=100000,max_unblocks_per_day=1000000,max_likes_to_like=1000000000,min_likes_to_like=-1,max_messages_per_day=3000000,filter_users=False,filter_private_users=False,filter_users_without_profile_photo=False,filter_previously_followed=False,filter_business_accounts=False,filter_verified_accounts=False,max_followers_to_follow=5000000,min_followers_to_follow=-1,max_following_to_follow=200000000,min_following_to_follow=-1,max_followers_to_following_ratio=150000000,max_following_to_followers_ratio=1500000000,min_media_count_to_follow=-1,max_following_to_block=20000000000,unlike_delay=10,follow_delay=30,unfollow_delay=30,comment_delay=60,block_delay=30,unblock_delay=30,message_delay=60,stop_words=("shop", "store", "free"),blacklist_hashtags=["#shop", "#store", "#free"],blocked_actions_protection=True,blocked_actions_sleep=False,blocked_actions_sleep_delay=300,verbosity=True,device=None,save_logfile=True,log_filename=None,log_follow_unfollow=False)
    if botid.login(update, context, ask_for_code=True, username = (context.chat_data)[newid][0], password = (context.chat_data)[newid][1],is_threaded = True) == False:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('lock.png', 'rb')) #change this for server
        context.bot.send_message(chat_id=update.effective_chat.id, text="Either your password is incorrect or our servers triggered a location lock. To fix this issue please go to the instagram app/website and click 'this was me'.",reply_markup=reply_markup)
        userlock = context.chat_data[newid][0]
        lockdict[userlock] = botid
        context.chat_data.clear()
        return ConversationHandler.END
    else:
        botlist.append(botid)
        credict[(context.chat_data)[newid][0]] = (context.chat_data)[newid][1] #adds to global user pass dict
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sucessfully logged in! Liking should start automatically next time you post",reply_markup=reply_markup)
        write_file(credict, (str(update.effective_user.id)))
        user = context.chat_data[newid][0]
        botdict[user] = globalcount[0]
        globalcount[0] += 1
        passw = context.chat_data[newid][1]
        context.user_data[user] = passw
        context.chat_data.clear()
        return ConversationHandler.END
    
def like(update, context):
    logger.info("/like")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Processing, one moment please")
    for i in range(len(botlist)):
        newid = botlist[i].get_media_id_from_link("https://www.instagram.com/p/B6gmXValZep/")
        botlist[i].like_medias([newid])
    context.bot.send_message(chat_id=update.effective_chat.id, text="Done!")
        
def write_file(credict,botid):
    logger.info("/writefile")
    file = open("passwords.txt", 'w')
    for key in credict:
        line = key + " " + credict[key] + " " + botid +'\n'
        file.write(line)
    file.close()
    
    
def restore(update, context):
    logger.info("/restore")
    file = open("passwords.txt", 'r')
    context.bot.send_message(chat_id=update.effective_chat.id, text="Processing give me a second.")
    for line in file:
        linelist = line.split()
        newusername = linelist[0]
        newpassword = linelist[1]
        credict[newusername] = newpassword
        botid = linelist[2]
        botid = instabot.Bot(like_delay=4,max_likes_per_day=100000000,max_unlikes_per_day=10000000,max_follows_per_day=3500000,max_unfollows_per_day=350000000,max_comments_per_day=1000000,max_blocks_per_day=100000,max_unblocks_per_day=1000000,max_likes_to_like=1000000000,min_likes_to_like=-1,max_messages_per_day=3000000,filter_users=False,filter_private_users=False,filter_users_without_profile_photo=False,filter_previously_followed=False,filter_business_accounts=False,filter_verified_accounts=False,max_followers_to_follow=5000000,min_followers_to_follow=-1,max_following_to_follow=200000000,min_following_to_follow=-1,max_followers_to_following_ratio=150000000,max_following_to_followers_ratio=1500000000,min_media_count_to_follow=-1,max_following_to_block=20000000000,unlike_delay=10,follow_delay=30,unfollow_delay=30,comment_delay=60,block_delay=30,unblock_delay=30,message_delay=60,stop_words=("shop", "store", "free"),blacklist_hashtags=["#shop", "#store", "#free"],blocked_actions_protection=True,blocked_actions_sleep=False,blocked_actions_sleep_delay=300,verbosity=True,device=None,save_logfile=True,log_filename=None,log_follow_unfollow=False)
        botid.login(update, context, username = newusername, password = newpassword,is_threaded = True)
        botlist.append(botid)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Done!")
    

def check_post(context: telegram.ext.CallbackContext):
    logger.info("checking post")
    for key in credict:
        if len(botlist) != 0:
            newid = botlist[0].get_user_id_from_username(key)
            mediaids = botlist[0].get_user_medias(newid, filtration = False) #gets recent media with username id
            if len(mediaids) > 0:
                lastmedia = mediaids[0]
            if key in lastmediacheck and len(mediaids) > 0:
                if lastmediacheck[key] != lastmedia:
                    for i in botlist:
                        i.like(lastmedia)
                    lastmediacheck[key] = lastmedia
            else:
                if len(mediaids) != 0:
                    lastmediacheck[key] = lastmedia
                else:
                    print("No media detected")
                    
def FAQ_func(update, context):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("Return Home", callback_data='returnhome2')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    faqtext = "» *Why do I need to sign in?*" + "\n" + "BoostMe uses automatic likes which means our servers need to stay logged into your account. No human being ever sees your information, it is encrypted and sent directly through instagrams api" +"\n" + "" + "\n" + "» *Is there a risk of getting banned?*" + "\n" + "Actually BoostMe is hardcoded to login to each individual account under the front of an android phone. This means Instagram just thinks a normal user is liking photos when BoostMe engages."  +"\n" + "" + "\n" + "» *Why is it free?*" + "\n" + "We want a user base before we start charging for premium features, no one would pay for a bot that they don’t know works!" +"\n" + "" + "\n" + "» *How does it work?*" + "\n" + "So basically our bot utilizes Instagrams api to log in and stay logged into your account. Every time you or any other user in the system posts a photo the bot detects this post and makes everyone logged in like it. This therefore boosts your post and helps it go viral." +"\n" + "" + "\n" + "» *Will this bot actually help me grow my account?*" + "\n" + "That all depends, do you post quality content, frequently and have good page appearance? Our bot helps photos go viral, aka hit explore, but it’s no magic growth solution. Automatic likes have been proven to work as a concept." +"\n" + "" + "\n" + "» *Can I even trust you?*" + "\n" + "That’s your choice, if you don’t trust us at first use a smaller account to see that what we made actually works. Telegram is full of scammers, BoostMe is a genuine service made for the benefit of all." +"\n" + "" + "\n" + "» *Additional questions?*" + "\n" + "Contact @idyllic, Im happy to help :)" 
    query.edit_message_text(text=faqtext,reply_markup=reply_markup,parse_mode=telegram.ParseMode.MARKDOWN)
    
    
    
def cancel(update, context):
    logger.info("/cancel")
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("Return Home", callback_data='returnhome')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="I cancelled your request!",reply_markup=reply_markup)
    return ConversationHandler.END
    
def main():
    logger.info("starting bot")
    my_persistence = PicklePersistence(filename='instabot')
    start_handler = CommandHandler(command='start', callback=start)
    like_handler = CommandHandler(command='like', callback=like)
    restore_handler = CommandHandler(command='restore', callback=restore)
    return_home2 = CallbackQueryHandler(return_start, pattern='returnhome2')
    faq = CallbackQueryHandler(FAQ_func, pattern='^' + str('button2') + '$')
    user_handler = CallbackQueryHandler(users, pattern='^' + str('button5') + '$') #registers all handlers
    myaccounts_handler = CallbackQueryHandler(my_accounts, pattern='^' + str('button3') + '$')
    dispatcher.add_handler(myaccounts_handler)
    myapi = API() 
    dispatcher.add_handler(faq)
    dispatcher.add_handler(return_home2)
    dispatcher.add_handler(user_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(like_handler)
    dispatcher.add_handler(restore_handler)
    conv_handler = ConversationHandler(entry_points = [CommandHandler('addaccount',addaccount), CallbackQueryHandler(addaccount, pattern='^' + str('button1') + '$'),CallbackQueryHandler(return_start, pattern='returnhome')], states = {HOME: [CallbackQueryHandler(return_start, pattern='returnhome')], PASSWORD: [MessageHandler(Filters.text, password)],PASSWORDHANDLE: [MessageHandler(Filters.text, passwordhandle)]}, fallbacks=[CallbackQueryHandler(return_start, pattern='returnhome'),CommandHandler(command='cancel', callback=cancel) ],allow_reentry = True)
    conv_handler2 = ConversationHandler(entry_points = [CommandHandler('removeaccount',removeaccount),CallbackQueryHandler(removeaccount, pattern='^' + str('button6') + '$'),CallbackQueryHandler(return_start, pattern='returnhome')], states = {HOME: [CallbackQueryHandler(return_start, pattern='returnhome')], RHELPER: [MessageHandler(Filters.text, rhelper)]}, fallbacks=[CallbackQueryHandler(return_start, pattern='returnhome'),CommandHandler(command='cancel', callback=cancel) ],allow_reentry = True)
    #conv_handler3 = ConversationHandler(entry_points = [CommandHandler('solvechallenge',myapi.solve_challenge)], states = {SOLVEVCHALLENGEHELPER: [MessageHandler(Filters.text, myapi.solve_challenge_helper)], SOLVEVCHALLENGEHELPER2: [MessageHandler(Filters.text, myapi.solve_challenge_helper2)]}, fallbacks=[CallbackQueryHandler(return_start, pattern='returnhome'),CommandHandler(command='cancel', callback=cancel) ],allow_reentry = True)
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(conv_handler2)
    #dispatcher.add_handler(conv_handler3)
    job_time = j.run_repeating(check_post, interval=30, first=0)
    api_handler = MessageHandler(Filters.text, myapi.solve_challenge)
    dispatcher.add_handler(api_handler)
    u.start_polling()
    u.idle()
    
main()

