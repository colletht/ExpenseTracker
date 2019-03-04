import re
from datetime import date
#File contains definition for Digital Reciept object that will store data for an individual reciept

#digital reciept class, holds data for reciept
class DigitalReciept:
    def __init__(self):
        self.cost = 0.0
        self.signCost = -1
        self.cardNum = ""
        self.dateOfPurchase = date.today()
        self.placeOfPurchase = ""
        self.information = ""
        self.genre = ""
        self.genres = ['Food','Hygene','Cleaning','Clothes','Alcohol','Recreation','Gaming']

    #getters
    def getDate(self):
        return self.dateOfPurchase

    def getCost(self):
        return self.cost

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

    def queryGenre(self):
        i = 1
        for x in self.genres:
            print(i, x, sep = '\t', end = '\n')
            i+=1
        self.genre = self.genres[int(input("Select a genre by number:\t"))-1]
    
    def queryPlace(self):
        self.placeOfPurchase = input("Enter location of purchase:\t")

    def queryInfo(self):
        self.information = input("Enter any extra information:\t")

    #edits the member data of a Digital Reciept Object, allows for user choice of which fields to edit
    def editReciept(self):
        option = 0
        while option is not 7:
            while option < 1 and option > 7:
                print(self.toString())
                print("What field do you wish to edit:",
                    "1. Date of Purchase",
                    "2. Card Number",
                    "3. Cost",
                    "4. Genre",
                    "5. Place of Purchase",
                    "6. Notes"
                    "7. Done", sep = '\n',)
                option = input(">> ")
            if option == 1:
                self.queryDate()
            elif option == 2:
                self.queryCardNum()
            elif option == 3:
                self.queryCost()
            elif option == 4:
                self.queryGenre()
            elif option == 5:
                self.queryPlace()
            else:
                self.queryInfo()

    #fills the reciept in case any missing data was not provided in the constructor
    def fillReciept(self):
        self.queryPlace()

        self.queryDate()

        self.queryCardNum()

        self.queryCost()

        self.queryGenre()
        
        self.queryInfo()

    #parses member data into a formatted string
    def toString(self):
        return "{0:<9.8} {1:<4}  ${2:>8.2f}  {4:^12.11}  {3:^14.13}  Notes:{5:<50}".format(self.dateOfPurchase.strftime("%x"), self.cardNum, self.cost*self.signCost, self.placeOfPurchase, self.genre, self.information)

y = DigitalReciept()
y.fillReciept()
print(y.toString())