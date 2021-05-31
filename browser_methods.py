from logging import warn
from Params import Params
import time
from datetime import date, datetime
import os
from pathlib import Path
import pathlib
from pprint import pprint
from pywinauto.application import Application
from pywinauto import Desktop
from pywinauto.keyboard import send_keys
from datetime import datetime
import ctypes  # An included library with Python install.

import pancake_swap_bot_ui_support

scriptDirectory = pathlib.Path().absolute()

class browser_methods:


    def __init__(self, choix=1, reports="normal"):

        dirpath = os.getcwd()
        # Connect with config page
        self.config = Params()
        self.URL_PANCAKE_SWAP = self.config.robot["URL_PANCAKE_SWAP_SWAP_PAGE"]

    # 
    ''' 
    Start of the (amazing) TAKE PROFIT BOT , if return == TRUE ==> END OF THIS PART
    It is a succession of actions that will take place during the swap scenario
    '''
    def TAKE_PROFIT_BOT(self, token_from, token_to, percentage):

        chrome_dir = self.config.robot["CHROME_DIR"]
        chrome_app_tpb = Application(backend='uia').start(chrome_dir+' --force-renderer-accessibility --start-maximized https://exchange.pancakeswap.finance/#/swap')
        chrome_app_swap_tab = Application(backend='uia').connect(path=chrome_dir, title_re='.*PancakeSwap -.*Chrome$')
        
        # PAUSE IMPORTANTE SINON BUG
        time.sleep(1)


        print("YOU HAVE CHOSEN TO SWAP TO:"+  str(token_to)  )
        swap_percentage_from = percentage
        print("You are willing to swap "+str( percentage )+ "% of your "+ token_from +" token(s)")
        self.wait(1)
        # print("Checking  metamask state")
        pancake_swap_tab = self.findWithPywinAuto('PancakeSwap.*Chrome')

        close_restore_pages_button = self.findButton(pancake_swap_tab, "CloseButton0")
        if(close_restore_pages_button):
            close_restore_pages_button.click();


        print("Opening of Chrome extensions menu:")
        self.openExtensionMenu(pancake_swap_tab)
        self.wait(0.5)
        print("Click on metamask in the list of extensions")
        self.findMetamaskExtension(pancake_swap_tab)
        self.wait(0.5)

        # print("Click on the annoying button that forces us to refresh the page")
        self.respondToRefreshrequest(pancake_swap_tab)
        self.wait(3)
        pancake_swap_tab.maximize().set_focus()

        print("Click on connect button to connect metamask to pancakeswap :")
        self.clickOnConnect(pancake_swap_tab)

        # print("Click and entering swap FROM TOKEN")
        
        try:
            self.wait(3)
            self.enterInputToken(pancake_swap_tab, token_from)
        except:
            print("You tried to enter a non valid contract.. ROBOT QUITS")

        print("Displaying balance of input token")
        my_token_balance = self.getTokenBalance(pancake_swap_tab, token_from)

        print("Typing the desired amount")
        self.typeDefinedPercentage(pancake_swap_tab, my_token_balance, swap_percentage_from, token_from)

        print("Entering the OUTPUT TOKEN")
        lit_token_TO = token_to
        self.enterOutputToken(pancake_swap_tab, lit_token_TO)
        
        pancake_swap_bot_ui_support.UNITY.set(token_to +" per "+token_from)

        self.wait(3)

        return self.getPriceProcess(pancake_swap_tab)

    '''
        This methods defines what happens once user has described either a SL, a TP or both
        minimize().maximize() is a trick to get the focus back on the browser
    '''
    def TAKE_PROFIT_PART_II(self, limit, stoploss,  price, token_from, token_to, root, TYPE_OF_PART_II):
        # Refind pancake swap:
        pancake_swap_tab = self.findWithPywinAuto('PancakeSwap.*Chrome')
        # pancake_swap_tab.restore().set_focus()
        pancake_swap_tab.minimize().maximize()

        print("Before get price process")
        print("You now need to set a TAKE PROFIT LIMIT greater than "+str(price) +" "+token_to+" per "+token_from+"    \n" )


        takeProfitLimit = limit
        stoplossLimit= stoploss
        print("You will swap when price reaches "+str(takeProfitLimit)+" "+token_to+" per "+token_from)
        print("NOW WE WAIT FOR THE PRICE TO CHANGE...")

        if(TYPE_OF_PART_II == 'TAKE_PROFIT'):
            self.waitForPriceToReachSupLimit(pancake_swap_tab, takeProfitLimit, root)
        elif(TYPE_OF_PART_II == 'STOP_LOSS'):
            self.waitForPriceToReachStopLoss(pancake_swap_tab, stoplossLimit, root)
        elif(TYPE_OF_PART_II == 'STOP_LOSS_AND_TP'):
            self.waitWithPriceSLorTP(pancake_swap_tab, stoplossLimit, takeProfitLimit, root)





    # Will user buy a crypto shirt ?
    def BUY_SHIRTS(self):
        # self.findWithPywinAuto('MetaMask Notification')
        # connect:
        dirpath = os.getcwd()

        chrome_dir = self.config.robot["CHROME_DIR"]
        self.Mbox('My Crypto Shirts', 'The purpose of mycryptoshirt.net is to allow you to wear tshirts with your eth20/BEP20, BTC, LTC or dogecoin public address in order to potentially earn crypto tips when scanned!')

        chrome_app_tpb = Application(backend='uia').start(chrome_dir+' --force-renderer-accessibility --start-maximized https://mycryptoshirt.net')


    # Is the user generous ?
    def NANO_TIPS(self):
        self.Mbox('My Crypto Shirts', 'Credit: Developed by MYCRYPTOSHIRT.NET. If you want to support this bot development : nano_1n6g87i3bujqnrpzk56tz8f3gzjud5fpsa1xj85gsxox1sica1jhp54xxgi6')
        chrome_dir = self.config.robot["CHROME_DIR"]
        chrome_app_tpb = Application(backend='uia').start(chrome_dir+' --force-renderer-accessibility --start-maximized https://nano_1n6g87i3bujqnrpzk56tz8f3gzjud5fpsa1xj85gsxox1sica1jhp54xxgi6')

    # Same as previous
    def BNB_ETH_TIPS(self):
        self.Mbox('My Crypto Shirts', 'Credit: Developed by MYCRYPTOSHIRT.NET. If you want to support this bot development, my ERC20: 0xd0e726bE6671fad60A156d075A99a614a9C9fa8e')
        chrome_dir = self.config.robot["CHROME_DIR"]
        chrome_app_tpb = Application(backend='uia').start(chrome_dir+' --force-renderer-accessibility --start-maximized https://MYERC20/BEP20:::0xd0e726bE6671fad60A156d075A99a614a9C9fa8e')


    # Licence
    def WARNING_TEXT(self):
        self.Mbox('ROBOT WARNINGS', '''  
        MIT License

        Copyright (c) [year] [fullname]

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.''')

    # Yes
    def READ_ME(self):
        self.Mbox('Using this bot', '''  
        This bot's purpose is to help you do sth else than starring at your pc for your SHIBA TOKEN or whatever 
        to land on the moon.

        This is an alternate way of making TP (Take Profit) or/and SL (Stop loss) without paying services on the block chain with fees.

        The pros as mentionned is that you don't pay fees for that it is on your PC and isn't going anywhere

        The cons are multiple :
            ==> The bot might be disturbed by your actions on PC (Your using of your pc could be enough for the pancake-bot to get completely f**** up)
                (That is why you should be careful when using your pc with the bot on)
                It is better used when AFK (away from keyboard), or if you are watching a movie or sth)
                You should always make sure that it is running =) !!

            ==> The bot might not be quick enough to fullfill the SWAP ! in case of a Rugg pull, or an internal error from pancakeswap.. 
                They won't be anything the bot can do!

            ==> It is very much like what a retarded human would interact like on pancake swap without any sense of solution-making, trouble shooting..


        Of course I'll better it over time, for now it is more or less stable !
        ''')

        self.Mbox('Manual','''
            Sorry for the long borring text :

            Requirement: Windows ( only tested on Windows 10)
            A computer that is not slow as f***
            a browser with METAMASK INSTALLED

/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\
            /!\ /!\  YOU NEED TO MAKE SURE THAT YOU HAVE OPENED METAMASK WITH YOUR PASSWORD in THE CURRENT SESSION ==> which means, you have :
                    1) Opened metamask on a new tab
                    2) Entered your password and it works OK
                    3) close the tab BUT NOT CLOSED THE BROWSER (you have at least another tab open !!!)

                    /!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\/!\ /!\

            To use the bot just :
            1) Enter a percentage that you want to swap.
            2) Enter the FROM token, either the suggested ones or a custom token.
            3) Enter the TO token, either the suggested ones or a custom token
            4) Click on "START ROBOT"
            5) Wait for bot to get to the swap page where IT WONT LAUNCH THE SWAP don't worry, it is just gathering the price
            6) (Remember that the bot is a big retard)
            7) You get prompted to enter LIMITS OR/AND STOP LOSS
            8) Press go and wait
            9) If you are careful you can move the console so that it is seeable but it MUST not cover the view.

        ''')



    '''
        Belows are all methods used within the differents bots 
    '''

    # Former bot console menu
    def chooseToken(self, direction):
        try:
            print(_("Choose token you want to swap "+direction+" :\n"))
            # If user wants to select a custom token
            custom_contract=''
            token_list= self.config.robot["tokens"]
            for i,token in enumerate(token_list):
                pprint(str(i+1) +") "+token_list[token])

            user_choice = input("Choose which token you want to swap "+direction+": ")
            if(user_choice =='' and direction=='from'):
                print("User entered nothing, so he chooses BNB")
                return '1'

            if(user_choice =='' and direction=='to'):
                print("User entered nothing, so he chooses BNB")
                return '2'

            while( not 1 <= int(user_choice) <=5):
                user_choice = input(_("Please make sure to type a correct digit! Choose which token you want to swap "+direction+": \n"))

            if(user_choice == "5"):
                user_choice = None
                custom_contract = input("Please copy/paste here the contract address of the Token you want to swap "+direction+" : ")
                print("Your custom contract is "+custom_contract)

           

            return user_choice or custom_contract
        except:
            second_chance = input("Please copy/paste here the contract address of the Token you want to swap "+direction+" : ")
            return second_chance


    '''
        Allows user to determine the portion of token he is willing to swap
    '''   
    def swapQuantity(self):
        try:
            quantity = input(_("How much in PERCENTAGE (0 => 100) are you willing to swap (default 100%¨)"))
            if(quantity ==''):
                print("No percentage entered, so default value 100%¨chosen")
                return '100'
            while( not 0<= int(quantity) <=100):
                quantity = input(_("Please enter a percentage, how much in PERCENTAGE are you willing to swap (default 100%¨)"))
            
            return quantity
        except ValueError:
            print("A percentage is a number between 1 and 100")
            return 100


    # The wait method ! RPA bots are really sensitive they need to wait for your pc to handle things
    def wait(self, t):
        time.sleep(t)


    ''' 
        The "find" methods are using PYWIN AUTO library to read user screen and do some action
        Go check out PYWIN AUTO library to learn more
    '''
    def findWithPywinAuto(self, title_regex):
        windows = Desktop(backend="uia").windows()
        print([w.window_text() for w in windows])

        app = Application(backend="uia").connect(title_re='.*'+title_regex+'.*$')
        found_feature = app.window(title_re='.*'+title_regex+'.*$')
        # print(found_feature)
        return found_feature

    def findButton(self, app, child_element):
        resp = app.child_window(best_match=child_element, control_type="Button").exists(timeout=2)
        # print("Element "+child_element+" exists ?"+ str(resp))
        if(resp is not None):
            return app.child_window(best_match=child_element, control_type="Button")
        return None

    def findButtonRegex(self, app, regex):
        resp = app.child_window(title_re=regex, control_type="Button").exists(timeout=2)
        # print("Element "+regex+" exists ?"+ str(resp))
        if(resp is not None):
            return app.child_window(title_re=regex, control_type="Button")
        return None


    def findMenuItem(self, app, child_element):
        resp = app.child_window(best_match=child_element, control_type="MenuItem").exists(timeout=2)
        # print("Menu Item exists ?"+ str(resp))
        if(not resp):
            print("It seems that you don't have METAMASK installed OR you are on incognito mode.")
            return None
        return app.child_window(best_match=child_element, control_type="MenuItem")


    def findTextItem(self, app, child_element):
        # Static35
        texte = app.child_window(best_match=child_element, control_type="Text").exists(timeout=2)
        # print("texte Item exists ?"+ str(texte))
        if(not texte):
            return None
        return app.child_window(best_match=child_element, control_type="Text")

    def findTextItemRegex(self, app, child_element):
            # Static35
        texte = app.child_window(best_match=child_element, control_type="Document").exists(timeout=2)
        # print("texte Item exists ?"+ str(texte))
        if(not texte):
            return None
        return app.child_window(best_match=child_element, control_type="Document")

    def findTextEdit(self, app, child_element):
        input_text = app.child_window(best_match=child_element, control_type="Text").exists(timeout=2)
        print("texte Input exists ?"+ str(input_text))
        if(not input_text):
            return None
        return app.child_window(best_match=child_element, control_type="Edit")

    def findHyperLink(self, app, child_element):
        input_text = app.child_window(title_re=child_element, control_type="Hyperlink").exists(timeout=2)
        # print("texte Input exists ?"+ str(input_text))
        if(not input_text):
            return None
        return app.child_window(title_re=child_element, control_type="Hyperlink")

    def openExtensionMenu(self, app):
        extensionMenu = self.findMenuItem(app,"ExtensionsMenuItem")
        if(extensionMenu is not None):
            extensionMenu.select()
            # app.print_control_identifiers()


    def findMetamaskExtension(self, app):
        metamaskButton = self.findButton(app, "MetaMaskButton")
        if(metamaskButton is not None):
            metamaskButton.click()


    def respondToRefreshrequest(self,app):
        refreshPageToUseMetamaskButton = self.findButton(app, "Button2")
        if(refreshPageToUseMetamaskButton is not None):
            self.wait(0.2)
            refreshPageToUseMetamaskButton.click()
    
    def clickOnConnect(self, app):
        connectButton = self.findButton(app, "ConnectButton")
        if(connectButton is not None):
            connectButton.click()

    def enterInputToken(self,app, TOKEN_FROM):
        print("click on default BNB list button")
        list_button = self.findButton(app, "BNBButton")
        if(list_button is not None):
            list_button.click()
            self.wait(1.8)
            send_keys(TOKEN_FROM)
            send_keys("{ENTER}")

    def enterOutputToken(self,app, TOKEN_TO):
        print("click on 'select a currency' ")
        list_button = self.findButton(app, "Select a currency2")
        if(list_button is not None):
            list_button.click()
            self.wait(1.8)
            send_keys(TOKEN_TO)
            self.wait(0.2)
            send_keys("{ENTER}")
            

    def getTokenBalance(self, app, optional_token_from=None):
        print("Getting token balance..")

        balance = self.findTextItem(app, "Balance:")

        if(balance is None):
            print("Something is off with your balance.. redoing token picking")
            self.enterInputToken(app, optional_token_from)
            return float(0)

        elif(balance is not None):
            balance_text_raw = balance.window_text()
            print("BALANCE :::::"+str(balance_text_raw))
            balance = balance_text_raw.split(":")[1].strip()
            print("Balance is : "+str(balance))
            return float(balance)


    def typeDefinedPercentage(self, app, token_amount, percentage, token_from):
        print("...Typing defined percentage of token to swap ...")
        send_amount = (float(token_amount) * float(percentage)) /100
        text_edit_input = self.findTextEdit(app, "FromEdit")

        if(text_edit_input is not None):
            text_edit_input.set_text(float(send_amount))
            # Register amount to global variable so that it can be shown on UI
            pancake_swap_bot_ui_support.QUANTITY.set(str(send_amount)+ " "+str(token_from))


    def getPriceProcess(self, app):
        print("Clicking the double arrows button to change format.")
        # self.findButton(app, "Button40").click()
        self.wait(2)
        # app.print_control_identifiers()
        swapButton = self.findButtonRegex(app, u"Swap")
        print("DONT WORRY WE ARE NOT SWAPPING YET !!! THE BOT IS JUST TRYING TO GET THE PRICE")
        swapButton.click()
        self.wait(1)
        # .click_input(button='right')
        price_element = self.getPrice(app)

        return price_element
        # arrow_button = self.findButtonRegex(app, "Button40")

    def getPrice(self, app):
        price_element_raw = self.findTextItemRegex(app, "Document").window_text()

        price_element = str(price_element_raw).split(". Price ")[1].split(" ")[0]
        price_element = str(price_element).strip()
        # Set price global variable
        pancake_swap_bot_ui_support.PRICE.set(float(price_element))

        return float(pancake_swap_bot_ui_support.PRICE.get())





    # Former CONSOLE MENU method
    def setTakeprofitLimit(self, app, current_price, lit_token_TO, lit_token_FROM):
        limit=None 
        limitTEMP = input("type a positive number > "+str(current_price)+" "+lit_token_TO+" per "+lit_token_FROM+" : ")
        limitTEMP = float(limitTEMP)
        while(limitTEMP <= current_price):
            limitTEMP = input("type a positive number > "+str(current_price)+" "+lit_token_TO+" per "+lit_token_FROM+" : ")
            limitTEMP = float(limitTEMP)
            if(limitTEMP > current_price):
                return float(limitTEMP)
            else:
                print("You need to enter a limit that is GREATER than current price")
        return float(limitTEMP)
                
    # Loop Methods that waits once user has clicked "go"

    #For LIMIT ONLY
    def waitForPriceToReachSupLimit(self, app, limit, root):
        current_pricing = self.getPrice(app)    
        pricing_on = True
        print("Be patient and wait for the price to go up !")

        def currentPricing():
            current_pricing = self.getPrice(app)  
            if(current_pricing  <= float(limit)):
             
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                unity = pancake_swap_bot_ui_support.UNITY.get()
                print(str(current_time)+ ") Current price: "+str(current_pricing)+ "=> limit: "+str(limit)+" "+unity, end ="\r")
                
                root.after(1000, currentPricing)
            else:
                print("NOT HAPPENNING")

        
            if(current_pricing > float(limit)):
                print("Price reached ! Swap process started")
                print("Accepting a veery likely 'PRICE UPDATED' ACCEPT BUTTON")
                self.acceptPriceChange(app)
                self.swapTokens(app)
                self.congrats()

        currentPricing()

    def congrats(self):
        self.Mbox('Success', 'You have successfully swapped '+str(token_from)+' for '+str(token_to)+', you should go check pancake swap right away! If you enjoyed that software, please visit our website https://mycryptoshirt.net, we sell t-shirts that will get you crypto tips!')
        print("You have succesfully swapped")



    '''
        This methods shows a TKINTER 'loop' to allow the robot to know whether price is under stop loss or not
    '''
    #For STOP LOSS ONLY
    def waitForPriceToReachStopLoss(self, app, stoploss, root):
        current_pricing = self.getPrice(app)    
        pricing_on = True
        print("We'll try to save your token with a stop loss !")

        def currentPricing():
            current_pricing = self.getPrice(app)  
            if(current_pricing  > float(stoploss)):
             
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                unity = pancake_swap_bot_ui_support.UNITY.get()
                print(str(current_time)+ ") Current price: "+str(current_pricing)+ " ==> stoploss : "+str(stoploss)+" "+unity, end ="\r")
                
                root.after(1000, currentPricing)
            else:
                print("NOT HAPPENNING")

        
            if(current_pricing <= float(stoploss)):
                print("Price reached ! STOP LOSS ACTIVATED ! Swap process started")
                print("Accepting a very likely 'PRICE UPDATED' ACCEPT BUTTON")
                self.acceptPriceChange(app)
                self.swapTokens(app)
                self.congrats()
        # Launches above method !
        currentPricing()

    
    '''
        This methods shows a TKINTER 'loop' to allow the robot to know whether price is under stop loss or not
    '''
    #For LIMIT OR STOP LOSS
    def waitWithPriceSLorTP(self, app, stoploss, takeprofit, root):
        current_pricing = self.getPrice(app)    
        pricing_on = True
        print("You both activated Stop loss and Take profit limit! We'll try our best..!")

        def currentPricing():
            current_pricing = self.getPrice(app)  
            if(current_pricing  > float(stoploss) and current_pricing <= float(takeprofit)):
             
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                unity = pancake_swap_bot_ui_support.UNITY.get()
                print(str(current_time)+ ") Current price: "+str(current_pricing)+ " => SL: "+str(stoploss)+ "<=TP:"+str(takeprofit)+" "+unity, end ="\r")
                
                root.after(1000, currentPricing)
            else:
                print("NOT HAPPENNING")

        
            if(current_pricing < float(stoploss) or current_pricing >= float(takeprofit)):
                if(current_pricing < float(stoploss)):
                    print("Stop loss activated !")
                elif(current_pricing > float(takeprofit)):
                    print("Take profit activated !!")
                print("Accepting a very likely 'PRICE UPDATED' ACCEPT BUTTON")
                self.acceptPriceChange(app)
                self.swapTokens(app)
                self.congrats()

        # Launches above method !
        currentPricing()

    # Self explanatory
    def congrats(self):
        self.Mbox('Success', 'You have successfully swapped '+str(token_from)+' for '+str(token_to)+', you should go check pancake swap right away! If you enjoyed that software, please visit our website https://mycryptoshirt.net, we sell t-shirts that will get you crypto tips!')
        print("You have succesfully swapped")
    
    # Confirming a price change
    def acceptPriceChange(self, app):
        acceptPriceButton = self.findButton(app, "AcceptButton")
        if(acceptPriceButton is not None):
            acceptPriceButton.click()

    # To swap tokens
    def swapTokens(self, app):
        swapButton = self.findButton(app, "Confirm Swap")
        if(swapButton is not None):
            print("Click on SWAP button")
            swapButton.click()
            self.wait(1)
            
        else:
            print("Price has slipped again, accepting price change")
            self.acceptPriceChange(self, app)
            print("Click on SWAP button")
            swapButton.click()

        self.wait(2)
        metamask_popup_app = self.findMetamaskPopup()
        metamask_popup_app.maximize().set_focus()

        # ===> Possible pending transactions to be rejected :
        to_be_rejected_transactions = self.findHyperLink(metamask_popup_app, "REJECT .* TRANSACTIONS")
        if(to_be_rejected_transactions is not None):
            to_be_rejected_transactions.invoke()
            self.wait(0.2)
            reject_all_button = self.findButton(metamask_popup_app, "Reject All")
            if(reject_all_button is not None):
                reject_all_button.click()
                self.wait(1)
                # app.print_control_identifiers()
                warning_rejected_transaction = self.findButton(app, "DismissButton")
                if(warning_rejected_transaction is not None):
                    warning_rejected_transaction.click()
                    self.wait(1)
                    

            # re-accept since ALL transactions pending are rejected

            swapButton = self.findButtonRegex(app, u"Swap")
            if(swapButton is not None):
                swapButton.click()
                self.wait(1)
                self.swapTokens(app)
        else:
            print("No transaction waiting to be rejected")

        confirm_in_metamask = self.findButton(metamask_popup_app, "ConfirmButton")
        if(confirm_in_metamask is not None):
            confirm_in_metamask.click()
            pass
        else:
            print("ERROR")


    '''
        This method will help you find the metamask popup
    '''
    def findMetamaskPopup(self):
        metamask_popup = self.findWithPywinAuto('MetaMask Notification')
        if(metamask_popup is not None):
            return metamask_popup
        else:
            print("No metamask popup")
            return None

    def Mbox(self, title, text):
        return ctypes.windll.user32.MessageBoxW(0, text, title, 4096)
    





    # compile to exe : python.exe -m nuitka --standalone --mingw64 --plugin-enable=tk-inter pancake_swap_bot_ui.py