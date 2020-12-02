import re
from datetime import date,timedelta
from colorama import Fore, Style
#File contains definition for Digital Reciept object that will store data for an individual reciept

REDTEXT = Fore.RED + Style.BRIGHT
GREENTEXT = Fore.GREEN + Style.BRIGHT

#utility function. Input() does not play nice with colorama so we need to print the string first before calling input
def inputC(argString):
    print(argString, end = '')
    return input()

#digital reciept class, holds data for reciept and all functions responsible for maintaining reciept
class DigitalReciept:
    def __init__(self):
        self.cost = 0.0
        self.signCost = -1
        self.cardNum = ""
        self.dateOfPurchase = date.today()
        self.placeOfPurchase = ""
        self.information = ""
        self.genre = ""

    def __str__(self):
        return "{0:<9.8} {1:<4}  ${2:>8.2f}  {3:^12.11}  {4:^14.13}  Notes: {5:<50}".format(self.dateOfPurchase.strftime("%m/%d/%y"), self.cardNum, self.cost*self.signCost,self.genre, self.placeOfPurchase, self.information)

    def __lt__(self,other):
        if self.dateOfPurchase == other.getDate():
            if self.cardNum == other.getCardNum():
                return self.cost < other.getCost()
            return self.cardNum < other.getCardNum()
        return self.dateOfPurchase < other.getDate()

    def __gt__(self,other):
        if self.dateOfPurchase == other.getDate():
            if self.cardNum == other.getCardNum():
                return self.cost > other.getCost()
            return self.cardNum > other.getCardNum()
        return self.dateOfPurchase > other.getDate()

    def __eq__(self, other):
        return (self.dateOfPurchase == other.getDate()) and (self.cardNum == other.getCardNum()) and (self.getRealCost() == other.getRealCost())

    def __le__(self,other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)

    def toString(self, color = True, verbose = False):
        if color and verbose:
            if self.signCost < 0:
                return "{0:<9.8} {1:<4}  ${2}{3:>8.2f}{4}  {5}  {6}  Notes: {7}".format(self.dateOfPurchase.strftime("%m/%d/%y"), self.cardNum, REDTEXT, self.cost*self.signCost, Style.RESET_ALL,self.genre, self.placeOfPurchase, self.information)
            else:
                return "{0:<9.8} {1:<4}  ${2}{3:>8.2f}{4}  {5}  {6}  Notes: {7}".format(self.dateOfPurchase.strftime("%m/%d/%y"), self.cardNum, GREENTEXT, self.cost*self.signCost, Style.RESET_ALL,self.genre, self.placeOfPurchase, self.information)
        elif color:
            if self.signCost < 0:
                return "{0:<9.8} {1:<4}  ${2}{3:>8.2f}{4}  {5:^12.11}  {6:^14.13}  Notes: {7:<50}".format(self.dateOfPurchase.strftime("%m/%d/%y"), self.cardNum, REDTEXT, self.cost*self.signCost, Style.RESET_ALL,self.genre, self.placeOfPurchase, self.information)
            else:
                return "{0:<9.8} {1:<4}  ${2}{3:>8.2f}{4}  {5:^12.11}  {6:^14.13}  Notes: {7:<50}".format(self.dateOfPurchase.strftime("%m/%d/%y"), self.cardNum, GREENTEXT, self.cost*self.signCost, Style.RESET_ALL,self.genre, self.placeOfPurchase, self.information)
        elif verbose:
            return "{0:<9.8} {1:<4}  ${2:>8.2f}  {3}  {4}  Notes: {5}".format(self.dateOfPurchase.strftime("%m/%d/%y"), self.cardNum, self.cost*self.signCost,self.genre, self.placeOfPurchase, self.information)
        else:
            return self.__str__()

    #getters
    def getDate(self):
        return self.dateOfPurchase

    def getCost(self):
        return self.cost

    def getSign(self):
        return self.signCost

    def getRealCost(self):
        return self.cost*self.signCost

    def getCardNum(self):
        return self.cardNum
    
    def getPlaceOfPurchase(self):
        return self.placeOfPurchase

    def getGenre(self):
        return self.genre
    
    def getInfo(self):
        return self.information

    #query functions defined here: each function queries an attribute from the terminal user, modulated into functions to make future error checking easier
    def queryDate(self):
        success = False
        while not success:
            try:
                dateStr = input("Enter the date of purchase (Enter nothing for todays date):\t")
                if dateStr == "": 
                    self.dateOfPurchase = date.today()
                    return
                patt = re.search(r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})',dateStr)
                #if user only entered two number year make sure it is actually in 2000
                if(int(patt.group(3)) < 100):
                    self.dateOfPurchase = date(2000 + int(patt.group(3)), int(patt.group(1)), int(patt.group(2)))
                else:
                    self.dateOfPurchase = date(int(patt.group(3)), int(patt.group(1)), int(patt.group(2)))
                success = True
            except:
                print("Please make sure your date is valid and entered in US format.")

    def queryCardNum(self):
        self.cardNum = input("Enter four digit card number:\t")

    def queryCost(self):
        sign = inputC(GREENTEXT + "Debit " + Style.RESET_ALL + "or " + REDTEXT + "Credit " + Style.RESET_ALL + "to account:\t").lower()

        while sign != "debit" and sign != "credit":
            sign = inputC(GREENTEXT + "Debit " + Style.RESET_ALL + "or " + REDTEXT + "Credit " + Style.RESET_ALL + "to account:\t").lower()
        if sign == "debit":
            self.signCost = 1
        else:
            self.signCost = -1
        err = True
        while err:
            try:
                self.cost = float(input("Enter the cost accrued:\t\t$"))
                err = False
            except:
                print("Enter a number")

    def queryGenre(self, genres):
        try:
            i = 1
            for x in genres:
                print(i, x, sep = '\t', end = '\n')
                i+=1
            res = int(input("Select a genre by number:\t"))

            while res not in range(1, len(genres)+1):
                for x in genres:
                    print(i, x, sep = '\t', end = '\n')
                    i+=1
                res = int(input("Select a genre by number:\t"))

            self.genre = genres[res - 1]
        except ValueError:
            print("Please enter a number corresponding to a genre on the screen.")
            self.queryGenre(genres)

    def queryPlace(self):
        self.placeOfPurchase = input("Enter location of purchase:\t")

    def queryInfo(self):
        self.information = input("Enter any extra information:\t")

    #edits the member data of a Digital Reciept Object, allows for user choice of which fields to edit
    def editReciept(self, genres):
        try:
            option = 0
            while option is not 7:
                option = 0
                while option not in range(1,8):
                    print(self)
                    print("What field do you wish to edit:",
                        "1. Date of Purchase",
                        "2. Card Number",
                        "3. Cost",
                        "4. Genre",
                        "5. Place of Purchase",
                        "6. Notes",
                        "7. Done", sep = '\n',)
                    option = int(input(">>> "))
                if option == 1:
                    self.queryDate()
                elif option == 2:
                    self.queryCardNum()
                elif option == 3:
                    self.queryCost()
                elif option == 4:
                    self.queryGenre(genres)
                elif option == 5:
                    self.queryPlace()
                elif option == 6:
                    self.queryInfo()
        except ValueError:
            print("Please enter an integer argument.")
            self.editReciept(genres)

    #fills the reciept in case any missing data was not provided in the constructor
    def fillReciept(self, genres):
        self.queryPlace()

        self.queryDate()

        self.queryCardNum()

        self.queryCost()

        self.queryGenre(genres)
        
        self.queryInfo()

class FilterReciept:
    def __init__(self):
        self.loCost = None
        self.hiCost = None
        self.signCost = None
        self.cardNum = None
        self.startDate = None
        self.endDate = None
        self.placeOfPurchase = None
        self.genre = None
        self.keyWord = None

    def __str__(self):
        finalString = ""
        if self.startDate is not None:
            finalString += "{0:>9.8}".format(self.startDate.strftime("%x"))
        if self.startDate is not None and self.endDate is not None:
            finalString += " - "
        if self.endDate is not None:
            finalString += "{0:<9.8}".format(self.endDate.strftime("%x"))
        if self.cardNum is not None:
            finalString += " {0:<4}".format(self.cardNum)
        if self.signCost is not None:
            if self.loCost is not None and self.hiCost is None:
                finalString += " ${0:>8.2f} <".format(self.signCost*self.loCost)
            elif self.loCost is None and self.hiCost is not None:
                finalString += " < ${0:>8.2f}".format(self.signCost*self.hiCost)
            else:
                finalString += " ${0:>8.2f} < ${1:>8.2f}".format(self.signCost*self.loCost, self.signCost*self.hiCost)
        else:
            if self.loCost is not None and self.hiCost is None:
                finalString += " ${0:>8.2f} <".format(self.loCost)
            elif self.loCost is None and self.hiCost is not None:
                finalString += " < ${0:>8.2f}".format(self.hiCost)
            elif self.loCost and self.hiCost:
                finalString += " ${0:>8.2f} < ${1:>8.2f}".format(self.loCost, self.hiCost)
        if self.genre is not None:
            finalString += " {0:^12.11}".format(self.genre)
        if self.placeOfPurchase is not None:
            finalString += " {0:^14.13}".format(self.placeOfPurchase)
        if self.keyWord is not None:
            finalString += " Keyword: {0:<50}".format(self.keyWord)
        return finalString

    def __eq__(self, other):
        return self.loCost == other.loCost and self.hiCost == other.hiCost and self.signCost == other.signCost and self.cardNum == other.cardNum and self.startDate == other.startDate and self.endDate.date() == other.endDate.date() and self.placeOfPurchase == other.placeOfPurchase and self.genre == other.genre and self.keyWord == other.keyWord

    def match(self, reciept):
        matches = True
        if self.startDate is not None:
            matches = matches and (self.startDate <= reciept.getDate())
        if self.endDate is not None:
             matches = matches and (self.endDate > reciept.getDate())
        if self.cardNum is not None:
            matches = matches and (self.cardNum == reciept.getCardNum())
        if self.signCost is not None:
            matches = matches and (self.signCost == reciept.getSign())
        if self.loCost is not None:
            matches = matches and (self.loCost <= reciept.getCost())
        if self.hiCost is not None:
            matches = matches and (self.hiCost > reciept.getCost())
        if self.placeOfPurchase is not None:
            matches = matches and (self.placeOfPurchase == reciept.getPlaceOfPurchase())
        if self.genre is not None:
            matches = matches and (self.genre == reciept.getGenre())
        if self.keyWord is not None:
            matches = matches and (self.keyWord in reciept.getInfo())
        return matches

    def queryCost(self):
        err = True
        x = inputC("Filter by " + GREENTEXT + " Debit " + Style.RESET_ALL + "or " + REDTEXT + "Credit " + Style.RESET_ALL +  "(Enter for none)? (D/C)\t")
        while x is not "D" and x is not "C" and x is not "N":
            x = inputC("Filter by " + GREENTEXT + " Debit " + Style.RESET_ALL + "or " + REDTEXT + "Credit " + Style.RESET_ALL +  "(Enter for none)? (D/C)\t")
        if x is "D":
            self.signCost = 1
        elif x is "C":
            self.signCost = -1
        while err:
            try:
                x = input("Enter low range value (Press enter for none):\t")
                if x is not '':
                    self.loCost = float(x)
                err = False
            except ValueError:
                print("Enter a number")
        err = True
        while err:
            try:
                x = input("Enter high range value (Press enter for none):\t")
                if x is not '':
                    self.hiCost = float(x)
                err = False
            except ValueError:
                print("Enter a number")

    def queryCardNum(self):
        self.cardNum = input("Enter 4 digit Card Number:\t")
    
    def queryDate(self):
        success = False
        while success == False:
            try:
                dateStr = input("Enter the date for low range (Press Enter for none):\t")
                     
                if dateStr is "":
                    success = True
                    break

                patt = re.search(r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})',dateStr)
                #if user only entered two number year make sure it is actually in 2000
                if(int(patt.group(3)) < 100):
                    self.startDate = date(2000 + int(patt.group(3)), int(patt.group(1)), int(patt.group(2)))
                else:
                    self.startDate = date(int(patt.group(3)), int(patt.group(1)), int(patt.group(2)))
                success = True
            except:
                print("Please make sure your date is valid and entered in US format.")
            
        success = False
        while success == False:
            try:
                dateStr = input("Enter the date for high range (Press Enter for none):\t")

                if dateStr is "":
                    success = True
                    break

                patt = re.search(r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})',dateStr)
                if(int(patt.group(3)) < 100):
                    self.endDate = date(2000 + int(patt.group(3)), int(patt.group(1)), int(patt.group(2)))
                else:
                    self.startDate = date(int(patt.group(3)), int(patt.group(1)), int(patt.group(2)))
                success = True
            except:
                print("Please make sure your date is valid and entered in US format.")

    def queryPlace(self):
        self.placeOfPurchase = input("Enter Place of Purchase: \t")
        
    def queryGenre(self, genres):
        try:
            i = 1
            for x in genres:
                print(i, x, sep = '\t', end = '\n')
                i+=1
            res = int(input("Select a genre by number:\t"))

            while res not in range(1, len(genres) + 1):
                for x in genres:
                    print(i, x, sep = '\t', end = '\n')
                    i+=1
                res = int(input("Select a genre by number:\t"))

            self.genre = genres[res - 1]
        except ValueError:
            print("Please enter a number corresponding to a genre on the screen.")
            self.queryGenre(genres)
        
    def queryKeyword(self):
        self.keyWord = input("Enter keyword:\t\t")

    def fillFilter(self, genres):
        try:
            option = 0
            while option is not 7:
                option = 0
                while option not in range(1,8):
                    print("What fields would you like to filter by:",
                        "1. Date of Purchase",
                        "2. Card Number",
                        "3. Cost",
                        "4. Genre",
                        "5. Place of Purchase",
                        "6. Keyword",
                        "7. Done", sep = '\n',)
                    option = int(input(">>> "))

                if option == 1:
                    self.queryDate()
                elif option == 2:
                    self.queryCardNum()
                elif option == 3:
                    self.queryCost()
                elif option == 4:
                    self.queryGenre(genres)
                elif option == 5:
                    self.queryPlace()
                elif option == 6:
                    self.queryKeyword()     
            return 
        except ValueError:
            print("Please enter an integer argument.")
            self.fillFilter(genres)

def getGenreFilter(genre = ""):
    f = FilterReciept()
    f.genre = genre
    return f

def getLastMonthFilter():
    f = FilterReciept()
    f.startDate = (date.today().replace(day=1) - timedelta(days=1)).replace(day = 1)
    f.endDate = date.today().replace(day = 1)
    return f

def getLastYearFilter():
    f = FilterReciept()
    f.startDate = date.today().replace(month=1, day=2) - timedelta(days = 1)
    return f

#TODO: make all query functions error proof so code does not break if incorrect input is entered