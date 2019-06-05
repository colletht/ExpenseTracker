import DigitalReciept, functools, pickle, traceback, csv
from datetime import date
from dateutil import relativedelta

#journal will work similar to accounting journal, keep track of expenses and entries to different categories. Contains functions to get analytics from spendings
class Journal:
    def __init__(self, genreList = {'Food':None,'Hygene':None,'Cleaning':None,'Clothes':None,'Alcohol':None,'Recreation':None,'Gaming':None,'Gas':None}):
        self.journal = []
        self.budget = 0
        self.genres = genreList
        self.curFilter = None   #holds tuple (<filter name>, <filter value>)
        self.filters = {}    #will hold dictionary of saved filters and their names, filters are FilterReciept objects with special values to be evauluated by the matches filter function
    
    def size(self):
        return len(self.journal)

    #prompts for value for a budget
    def queryBudget(self):
        try:
            res = input("Enter a monthly budget:\t")
            res = float(res)
            return res
        except ValueError:
            print("Please enter a valid value for a budget")
            return queryBudget(self)
    
    #writes the journal to the pickle file specified in file
    def writeJournal(self,file):
        with open(file,"wb") as output:
            pickle.dump(self,output,-1)

        #use pickle module to print to a file. will use pickle to read from file as well
        #TODO: Implement file I/O for reciepts and journal objects, then polish off core functionalities and move on to the main driver class!

    #adds a new reciept to the journal, user enters the data for the new reciept in this function
    def addReciept(self):
        p = DigitalReciept.DigitalReciept()
        p.fillReciept(list(self.genres.keys()))
        self.journal.append(p)
        self.journal.sort()
        return True

    #TODO: inefficient: figure out an insert in order way rather than needlessly sorting list every time

    #searches for a reciept based on the given filter. Returns the reciept if found, returns None if cancel is entered
    def searchReciept(self, filt = None):
        try:
            tmpJournal = self._Journal__applyFilter(filt = filt)
            if tmpJournal == []:
                print("Nothing matches that filter. Try a different one!\n")
                return

            res = -1
            while res not in range(0, len(tmpJournal) + 1):
                print("0.\tCancel")
                i = 1
                for reciept in tmpJournal:
                    print(str(i) + ".", str(reciept), sep = "\t", end = "\n")
                    i = i+1
        
                res = int(input("Enter the desired reciept:\t"))

            if(res is not 0):
                return tmpJournal[res-1]
            return None
        except ValueError:
            print("Please enter an integer argument.")
            traceback.print_exc()
            return self.searchReciept(filt = filt)

    #allows user to edit a reciept that has been searched for
    def editReciept(self, reciept):
        reciept.editReciept(list(self.genres.keys()))

    def deleteReciept(self,reciept):
        for x in range(0,len(self.journal)):
            if self.journal[x] == reciept:
                del self.journal[x]

    #guides the user through adding a new filter to the filters dicitonary and asks if it should be set to the current filter
    def addFilter(self):
        name = input('Please select a name for the new filter:\t')
        while name in self.filters.keys():
            name = input('Please select a name for the new filter that is not already a filter name:\t')
        f = DigitalReciept.FilterReciept()
        f.fillFilter(list(self.genres.keys()))
        self.filters[name] = f
        res = input('Would you like to set this as the current filter? (Y/N)\t')
        if res.lower()[0] == 'y':
            self.curFilter = (name, f) 
        return True

    #gets a temporary filter
    def temporaryFilter(self):
        f = DigitalReciept.FilterReciept()
        f.fillFilter(list(self.genres.keys()))
        return ("TEMP",f)

    def editFilters(self):
        try:
            print("0.\tBack")
            i = 1
            for name, filt in self.filters.items():
                print(str(i) + ".", name + ":", str(filt), sep = "\t", end = "\n")
                i = i+1
        
            res = int(input("Enter a filter to edit. You may delete a filter or modify it:\t"))

            while res not in range(0, len(self.filters) + 1):
                print("0.\tBack\n")
                i = 1
                for name, filt in self.filters.items():
                    print(str(i) + ".", name + ":", str(filt), sep = "\t", end = "\n")
                    i = i+1
        
                res = int(input("Enter a filter to edit. You may delete a filter or modify it:\t"))

            if(res is not 0):
                self._Journal__editFilter(res-1)
        except ValueError:
            print("Please enter an integer argument.")
            self.editFilters()

    #menu for editing a filter can only delete a filter as filters are easily dispensable and creatable
    def __editFilter(self, filterIndex):
        try:
            print(str(filterIndex+1) + ".\t" + list(self.filters.keys())[filterIndex] + ":\t " + str(list(self.filters.values())[filterIndex]) + "\n" +
                    "\t0.\tBack\n" +
                    "\t1.\tDelete Filter\n")

            res = int(input("Enter an option:\t"))
        
            while res not in range(0,3):
                print(str(filterIndex+1) + ".\t" + list(self.filters.keys())[filterIndex] + ":\t " + str(list(self.filters.values())[filterIndex]) + "\n" +
                        "\t0.\tBack\n" +
                        "\t.\tDelete Filter\n")

                res = int(input("Enter an option:\t"))
            
            if(res == 1):
                if( "y" == str(input("Are you sure you want to delete this filter? (Y/N)\t")).lower()):
                    self.__deleteFilter(filterIndex)
        
        except ValueError:
            print("Please enter an integer argument.")
            self._Journal__editFilter(filterIndex)

    #deletes the filter at the given index in the dictionary
    def __deleteFilter(self, filterIndex):
        #if the filter to be deleted is the current filter then set the current filter to None
        if self.curFilter and self.filters[list(self.filters.keys())[filterIndex]] is self.curFilter[-1]:
            self.curFilter = None
        del self.filters[list(self.filters.keys())[filterIndex]]

    #helper funciton that applies the current filter and returns the resulting sublist 
    def __applyFilter(self, filt = None):
        if not filt:
            return self.journal
        subJournal = list(filter(filt[-1].match, self.journal))
        return subJournal

    def setFilter(self):
        try:
            print("0.\tBack\n" + "1.\tNo Filter")
            i = 2
            for name, filt in self.filters.items():
                print(str(i) + ".", name + ":", str(filt), sep = "\t", end = "\n")
                i = i+1
            print(i, "Temporary Filter", sep = "\t", end = "\n")
            
            res = int(input("Enter a filter to edit, or " + str(i) + " to create a temporary filter: \t"))

            while res not in range(0, len(self.filters) + 3):
                print("0.\tBack\n" + "1.\tNo Filter")
                i = 2
                for name, filt in self.filters.items():
                    print(str(i) + ".", name + ":", str(filt), sep = "\t", end = "\n")
                    i = i+1
                print(i, "Temporary Filter", sep = "\t", end = "\n")

                res = int(input("Enter a filter to edit, or " + str(i) + " to create a temporary filter: \t"))

            if res == i:
                self._Journal__setCurFilter("Temp", filt = self.temporaryFilter())
            elif res is 1:
                self.curFilter = None
            elif res is not 0:
                self._Journal__setCurFilter(list(self.filters.keys())[res-2])

        except ValueError:
            print("Please enter an integer argument")
            self.setFilter()

    #sets the current filter from a name in the filters dicitonary unless the name is not there then it prints an error
    def __setCurFilter(self, filterName, filt = None):
        if filt:
            self.curFilter = filt
            return True
        elif filterName in self.filters.keys():
            self.curFilter = (filterName, self.filters[filterName])
            return True
        else:
            print("It appears there is no filter with that name, please choose a valid name.")
            return False

    #outputs the journal generated by filt to the given exportFile. Excel csv file expected
    def exportJournal(self, exportFile, filt = None, sep = None):
        tmpJournal = self._Journal__applyFilter(filt = filt)
        if tmpJournal == []:
            print("You don't have any data to report yet. Add some reciepts now!\n")
            return

        curMonth = None
        with open(exportFile, "w", newline='') as csvFile:
            writer = csv.writer(csvFile, dialect='excel')
            if sep == "m": 
                writer.writerow(['Reciepts for month of ' + tmpJournal[0].getDate().strftime("%B")])
                curMonth = tmpJournal[0].getDate().month
            writer.writerow(['Date of Purchase', 'Card Number', 'Cost', 'Place of Purchase', 'Genre', 'Details'])

            for reciept in tmpJournal:
                if curMonth != reciept.getDate().month:
                    curMonth = reciept.getDate().month
                    writer.writerow([])
                    writer.writerow(['Reciepts for month of ' + reciept.getDate().strftime("%B")])
                    writer.writerow(['Date of Purchase', 'Card Number', 'Cost', 'Place of Purchase', 'Genre', 'Details'])

                writer.writerow([reciept.getDate().strftime("%m/%d/%y"), reciept.getCardNum(), str(reciept.getRealCost()), reciept.getPlaceOfPurchase(), reciept.getGenre(), reciept.getInfo()])

    #prints the journal, if a filter is passed it it is set to the current filter for the duration of the function, if a cur filter is set then it filters
    #off of that otherwise it prints the entire contents
    def printJournal(self, filt = None):
        tmpJournal = self._Journal__applyFilter(filt = filt)
        if tmpJournal == []:
            print("You don't have any data to report yet. Add some reciepts now!\n")
            return

        for reciept in tmpJournal:
            print(reciept)
        
    #sums the journal, using the same methods for filtering as printJournal. Gives the user the option
    #to sum regardless of sign and purely on magnitude or regarding sign and based off net costs
    def sumJournal(self, filt = None):
        tmpJournal = self._Journal__applyFilter(filt = filt)
        if tmpJournal == []:
            print("You don't have any data to report yet. Add some reciepts now!\n")
            return

        sumBal =  0.0
        for reciept in tmpJournal:
            sumBal += reciept.getRealCost()
        print("Your current Journal Balance is:\t${0:>8.2f}".format(sumBal))
    
    #averages the journal, using the same methods for filtering as printJournal. Gives the user the option
    #to saverage regardless of sign and purely on magnitude or regarding sign and based off net costs
    def averageJournal(self, filt = None):
        tmpJournal = self._Journal__applyFilter(filt = filt)
        if tmpJournal == []:
            print("You don't have any data to report yet. Add some reciepts now!\n")
            return

        sum = 0.0
        startDate = tmpJournal[0].getDate()
        endDate = tmpJournal[-1].getDate()
        for reciept in tmpJournal:
            sum = sum + reciept.getRealCost()

        perPurchase = sum/len(tmpJournal)

        if relativedelta.relativedelta(endDate, startDate).months is not 0:
            perMonth = sum/relativedelta.relativedelta(endDate, startDate).months 
        else:
            perMonth = sum

        if (endDate != startDate):
            perDay = sum/(endDate - startDate).days
        else: 
            perDay = sum

        print("Your averages are:\t$ {0:>8.2f}  per purchase\n\t\t\t$ {1:>8.2f}  per Month\n\t\t\t$ {2:>8.2f}  per Day\n".format(perPurchase, perMonth, perDay))

    def exportReport(self, exportFile, timeUnit = "m"):
        outString = self.generateReport()
        if outString != "":
            with open(exportFile, "w") as exportTxt:
                exportTxt.write(outString)
            return True
        return False

    #generates a report of the journal based off of given filter. A report includes:
    #   Journal Budget
    #   Journal Balance Sum
    #   Journal Sum
    #   Journal Average Daily, Monthly, Yearly (If Any are not applicable will not display)
    #   Journal Min Reciept
    #   Journal Max Reciept
    # for each genre:
    #   Genre Name:
    #       Budget
    #       Balance Sum
    #       Sum
    #       Average Daily, Monthly, Yearly
    #       Min Reciept
    #       Max Reciept
    #   
    def generateReport(self, timeUnit = "m"):
        outString = ""
        f = None
        if "m" == timeUnit:
            f = ("Last Month", DigitalReciept.getLastMonthFilter())
            outString += ("------------------------------------------------------------------------------------------------------------------------\n" + 
                  "{:^120}\n".format("LAST MONTHS REPORT: " + f[-1].startDate.strftime("%b, %Y")) + 
                  "------------------------------------------------------------------------------------------------------------------------\n\n")
        tmpJournal = self._Journal__applyFilter(filt = f)
        if tmpJournal == []:
            print("You don't have any data to report yet. Add some reciepts now!\n")
            return ""

        balance = 0.0
        sum = 0.0
        minReciept = tmpJournal[0]
        maxReciept = tmpJournal[0]
        for reciept in tmpJournal:
            balance = balance + reciept.getRealCost()
            sum = sum + reciept.getCost()
            if minReciept.getRealCost() > reciept.getRealCost(): minReciept = reciept
            if maxReciept.getRealCost() < reciept.getRealCost(): maxReciept = reciept


        outString += ("MONTHLY BUDGET:\t" + str(self.budget) + "\n")
        outString += ("MONTHLY BALANCE:\t${:>8.2f}".format(balance) + "\n")
        outString += ("MONTHLY SUM:\t${:>8.2f}".format(sum) + "\n")
        outString += ("AVERAGE DAILY EXPENDITURE:\t${:>8.2f}".format(balance/len(tmpJournal)) + "\n")
        outString += ("MINIMUM RECIEPT:\t" + str(minReciept) + "\n")
        outString += ("MAXIMUM RECIEPT:\t" + str(maxReciept) + "\n\n")
        outString += ("--------------------\n" +
              "  REPORT BY GENRE   \n" + 
              "--------------------\n")
        for genre in self.genres.keys():
            outString += self.generateGenreReport(genre, timeUnit, tmpJournal)
        outString += ("------------------------------------------------------------------------------------------------------------------------\n" +
              "{:^120}\n".format("END REPORT") + 
              "------------------------------------------------------------------------------------------------------------------------\n\n")
        return outString

    #NOTE: inefficient if time implement method to generate all information for reports in a single run through the list. Use a dictionary for that
    def generateGenreReport(self, genre, timeUnit, tmpJournal):
        outString = ""
        outString += ("    --------------------\n" +
              "    {:^20.20}\n".format(genre) + 
              "    --------------------\n\n")

        balance = 0.0
        sum = 0.0
        minReciept = maxReciept = None
        for reciept in tmpJournal:
            if reciept.genre == genre:
                balance = balance + reciept.getRealCost()
                sum = sum + reciept.getCost()
                if not minReciept or minReciept.getRealCost() > reciept.getRealCost(): minReciept = reciept 
                if not maxReciept or maxReciept.getRealCost() < reciept.getRealCost(): maxReciept = reciept


        outString += ("    MONTHLY BUDGET:\t" + str(self.budget) + "\n")
        outString += ("    MONTHLY BALANCE:\t${0:>8.2f}".format(balance) + "\n")
        outString += ("    MONTHLY SUM:\t${0:>8.2f}".format(sum) + "\n")
        outString += ("    AVERAGE DAILY EXPENDITURE:\t${0:>8.2f}".format(balance/len(tmpJournal)) + "\n")
        outString += ("    MINIMUM RECIEPT:\t" + str(minReciept) + "\n")
        outString += ("    MAXIMUM RECIEPT:\t" + str(maxReciept) + "\n\n")
        return outString
   
    #adds a new genre to the genre list
    def addGenre(self):
        res = input("Enter the name of your new genre:\t")
        if res.lower() in list(map(lambda x: x.lower(), self.genres.keys())):
            print("You must enter a genre does not yet exist")
            return False
        else:
            newBudget = self.queryBudget()
            self.genres[res.strip()] = newBudget
            return True

    #provides menu interface to edit individual genres. You have two options when editing a genre:
    #   1. Change Budget
    #   2. Delete Genre
    def editGenres(self):
        try:
            print("0.\tBack")
            i = 1
            for genre, bud in self.genres.items():
                print(str(i) + ".", str(genre), "Budget: " + str(bud), sep = "\t", end = "\n")
                i = i+1
        
            res = int(input("Enter a genre to edit. You may delete a Genre or modify its Budget:\t"))

            while res not in range(0, len(self.genres) + 1):
                print("0.\tBack\n")
                i = 1
                for genre, bud in self.genres.items():
                    print(str(i) + ".", str(genre), "Budget: " + str(bud), sep = "\t", end = "\n")
                    i = i+1
        
                res = int(input("Enter a genre to edit. You may delete a Genre or modify its Budget:\t"))

            if(res is not 0):
                self.__editGenre(list(self.genres.keys())[res-1])

        except ValueError:
            print("Please enter an integer argument.")
            self.editGenres()

    #provides actual submenu for editing a genre
    def __editGenre(self, genre):
        try:

            print(genre + "\tBudget: " + str(self.genres[genre]) + "\n" +
                    "\t0.\tBack\n" +
                    "\t1.\tChange Budget\n" +
                    "\t2.\tDelete Genre\n")

            res = int(input("Enter an option:\t"))
        
            while res not in range(0,3):
                print(genre + "\tBudget: " + str(self.genres[genre]) + "\n" +
                        "\t0.\tBack\n" +
                        "\t1.\tChange Budget\n" +
                        "\t2.\tDelete Genre\n")

                res = int(input("Enter an option:\t"))

            if(res == 1):
                self.genres[genre] = float(input("Please enter the new genre budget:\t"))
            elif(res == 2):
                if( "y" == str(input("Deleting a genre will delete all its associated digital reciepts. Are you sure you still want to delete it? (Y/N)\t")).lower()):
                    self.__deleteGenre(genre)
        
        except ValueError:
            print("Please enter an integer argument.")
            self._Journal__editGenre(genre)
    
    #deletes the genre in genres at the given index and all associated DigitalReciept objects in journal
    def __deleteGenre(self, genre):
        i = 0
        while i < len(self.journal):
            if self.journal[i].genre == genre:
                del self.journal[i]
            else:
                i = i+1
        del self.genres[genre]

    
