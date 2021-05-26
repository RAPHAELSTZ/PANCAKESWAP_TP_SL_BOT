
import browser_methods, locale
from Params import Params
from babel import Locale 
import gettext, sys, os

if sys.platform.startswith('win'):
    import locale
    if os.getenv('LANG') is None:
        lang, enc = locale.getdefaultlocale()
        os.environ['LANG'] = lang


def changeLanguage(langue=1, helper=False):
    if(helper):
        print(_("Welcome to PancakeSwapBot, choose language"))
        print(_("Enter (1) for English (default)"))
        print(_("ENTREZ (2) for French"))

    if langue not in (1,2):
        langue=1

    possible_languages = {
        1: "en",
        2: "fr"
    }
    chosen_language = possible_languages[langue]
    try:
        traduction = gettext.translation(chosen_language, localedir='locale', languages=[chosen_language])
        traduction.install()
    except:
        gettext.install('en')

changeLanguage(langue=1)

print(_("Welcome to PancakeSwapBot, choose language"))
print(_("Enter (1) for English (default)"))
print(_("ENTREZ (2) for French"))

# language_choice = input("What language/ Quelle langue ?")
language_choice=1
changeLanguage(language_choice, False)



print(_("This bot allows you to place either, a BOT_TAKE_PROFIT_LIMIT, a BOT_STOP_LOSS or both a STOP LOSS & TAKE PROFIT"))
print(_("Be aware that this is an early version of the bot, it might not work 100%¨ of the time"))
print(_("There might be times when some events on your computer 'block' the interactions of the bot"))
print(_("You need to understand that these are not PROPER limit order/ STOP LOSS orders"))
print(_("This is just a creative way for you to try to focus else where or go to sleep.."))
print(_(".. as long as you let it on, and that you don't turn your computer off"))
print(_("It mimics what a human would do, for now just try it ONE token at a time"))

print("================================================")
print("======================MENU======================")
print("================================================")
print(_("1) TAKE PROFIT BOT (WORKS)"))
print(_("2) STOP LOSS BOT (NOT YET IMPLEMENTED)"))
print(_("3) TAKE PROFIT AND STOP LOSS (NOT YET IMPLEMENTED)"))
print(_("4) I want to buy one of your magic CRYPTO Tshirts and hoodies!"))
print(_("5) I want to give you some nanos"))
print(_("6) Change language ? (NOT YET IMPLEMENTED)"))
print(_("7) Licence"))
print(_("8) IM OUTTA HERE "))

choix = 0
while ( choix!='8' ):
    choix = input(_("You get the idea, pick a number "))
    

    print("================================================")
    print("=================Let's go for option "+str(choix)+"==========")
    print("================================================")

    bm = browser_methods.browser_methods(choix)

#         2019-10-17






# <div>Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
# pyinstaller.exe --onefile --windowed --icon=pancakes_icon.ico pancake.py