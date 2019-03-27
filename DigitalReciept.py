import re
from datetime import date
#File contains definition for Digital Reciept object that will store data for an individual reciept

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
        return "{0:<9.8} {1:<4}  ${2:>8.2f}  {4:^12.11}  {3:^14.13}  Notes:{5:<50}".format(self.dateOfPurchase.strftime("%x"), self.cardNum, self.cost*self.signCost, self.placeOfPurchase, self.genre, self.information)
        
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
        return (self.dateOfPurchase == other.getDate()) and (self.cardNum == other.getCardNum()) and (self.cost == other.getCost())

    def __le__(self,other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return (self > other) or (self == other)

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
        while success == False:
            try:
                dateStr = input("Enter the date of purchase:\t")
                patt = re.search(r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})',dateStr)
                self.dateOfPurchase = date(int(patt.group(3)), int(patt.group(1)), int(patt.group(2)))
                success = True
            except ValueError:
                print("Please make sure your date is valid and entered in US format.")

    def queryCardNum(self):
        self.cardNum = input("Enter four digit card number:\t")

    def queryCost(self):
        sign = input("Debit or Credit to account:\t").lower()

        while sign != "debit" and sign != "credit":
            sign = input("Debit or Credit to account:\t").lower()
        if sign == "debit":
            self.signCost = 1
        else:
            self.signCost = -1

        self.cost = float(input("Enter the cost accrued:\t\t$"))

    def queryGenre(self, genres):
        i = 1
        for x in genres:
            print(i, x, sep = '\t', end = '\n')
            i+=1
        self.genre = genres[int(input("Select a genre by number:\t"))-1]
    
    def queryPlace(self):
        self.placeOfPurchase = input("Enter location of purchase:\t")

    def queryInfo(self):
        self.information = input("Enter any extra information:\t")

    #edits the member data of a Digital Reciept Object, allows for user choice of which fields to edit
    def editReciept(self, genres):
        option = 0
        while option is not 7:
            option = 0
            while option < 1 or option > 7:
                print(self)
                print("What field do you wish to edit:",
                    "1. Date of Purchase",
                    "2. Card Number",
                    "3. Cost",
                    "4. Genre",
                    "5. Place of Purchase",
                    "6. Notes",
                    "7. Done", sep = '\n',)
                option = int(input(">> "))
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
            else:
                self.queryInfo()

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
    
    def match(self, reciept):
        matches = True
        if self.startDate is not None:
            matches = matches and self.startDate <= reciept.getDate()
        if self.endDate is not None:
             matches = matches and self.endDate > reciept.getDate()
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
        x = input("Filter by Debit/Credit (Enter for none)? (D/C)\t")
        while x is not "D" and x is not "C" and x is not "N":
            x = input("Filter by Debit/Credit (Enter for none)? (D/C)\t")
        if x is "D":
            self.signCost = 1
        elif x is "C":
            self.signCost = -1
            
        x = input("Enter low range value (Press enter for none):\t")
        if x is not '':
            self.loCost = float(x)
        x = input("Enter high range value (Press enter for none):\t")
        if x is not '':
            self.hiCost = float(x)
    
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
                self.startDate = date(int(patt.group(3)), int(patt.group(1)), int(patt.group(2)))
                success = True
            except ValueError:
                print("Please make sure your date is valid and entered in US format.")
            
        success = False
        while success == False:
            try:
                dateStr = input("Enter the date for high range (Press Enter for none):\t")

                if dateStr is "":
                    success = True
                    break

                patt = re.search(r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})',dateStr)
                self.endDate = date(int(patt.group(3)), int(patt.group(1)), int(patt.group(2)))
                success = True
            except ValueError:
                print("Please make sure your date is valid and entered in US format.")

    def queryPlace(self):
        self.placeOfPurchase = input("Enter Place of Purchase: \t")
        
    def queryGenre(self, genres):
        i = 1
        for x in genres:
            print(i, x, sep = '\t', end = '\n')
            i+=1
        self.genre = genres[int(input("Select a genre by number:\t"))-1]

    def queryKeyword(self):
        self.keyWord = input("Enter keyword:\t\t")

    def fillFilter(self, genres):
        option = 0
        while option is not 7:
            option = 0
            while option < 1 or option > 7:
                print("What fields would you like to filter by:",
                    "1. Date of Purchase",
                    "2. Card Number",
                    "3. Cost",
                    "4. Genre",
                    "5. Place of Purchase",
                    "6. Keyword",
                    "7. Done", sep = '\n',)
                option = int(input(">> "))

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

        

r = DigitalReciept()
r.fillReciept(['Food','Hygene','Cleaning','Clothes','Alcohol','Recreation','Gaming'])
print(r)
f = FilterReciept()
f.fillFilter(['Food','Hygene','Cleaning','Clothes','Alcohol','Recreation','Gaming'])
print(f.match(r))

#TODO: make all query functions error proof so code does not break if incorrect input is entered