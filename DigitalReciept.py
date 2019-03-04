import re
from datetime import date
#File contains definition for Digital Reciept object that will store data for an individual reciept

#digital reciept class, holds data for reciept
#Member variables: cost, cardNum, dateOfPurchase, placeOfPurchase
class DigitalReciept:
    def __init__(self):
        self.cost = 0.0
        self.cardNum = ""
        self.dateOfPurchase = date.today()
        self.placeOfPurchase = ""
        self.information = ""
        self.genre = ""
        self.genres = ['Food','Hygene','Cleaning','Clothes','Alcohol','Recreation']

    def getDate(self):
        return self.dateOfPurchase

    def readDate(self):
        success = False
        while success == False:
            try:
                dateStr = input("Enter the date of purchase:\t")
                patt = re.search(r'(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})',dateStr)
                self.dateOfPurchase = date(int(patt.group(3)), int(patt.group(1)), int(patt.group(2)))
                success = True
            except ValueError:
                print("Please make sure your date is valid and entered in US format.")
            
        
    '''
    def writeToCSV(self):
        #write all data here to file
        if 
    '''

    def queryGenre(self):
        i = 1
        for x in self.genres:
            print(i, x, sep = '\t', end = '\n')
            i+=1
        self.genre = self.genres[int(input("Select a genre by number:\t"))-1]

    #fills the reciept in case any missing data was not provided in the constructor
    def fillReciept(self):
        self.placeOfPurchase = input("Enter location of purchase:\t")

        self.readDate()

        self.cardNum = input("Enter four digit card number:\t")

        sign = input("Debit or Credit:\t\t").lower()
        while sign != "debit" and sign != "credit":
            sign = input("Debit or Credit:\t\t").lower()

        self.cost = float(input("Enter the cost accrued:\t\t"))
        if sign == "debit":
            self.cost *= -1

        self.queryGenre()
        
        self.information = input("Enter any extra information:\t")

    def toString(self):
        print(self.dateOfPurchase,self.cardNum, '$' + str(abs(self.cost)), self.genre, self.placeOfPurchase, self.information, sep = '\t', end = '\n')

y = DigitalReciept()
y.fillReciept()
y.toString()