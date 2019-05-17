import DigitalReciept, functools, os, pickle

#journal will work similar to accounting journal, keep track of expenses and entries to different categories. Contains functions to get analytics from spendings
class Journal:
    def __init__(self, genreList = {'Food':None,'Hygene':None,'Cleaning':None,'Clothes':None,'Alcohol':None,'Recreation':None,'Gaming':None,'Gas':None}):
        self.journal = []
        self.budget = 0
        self.genres = genreList
        self.curFilter = None   
        self.filters = {}    #will hold dictionary of saved filters and their names, filters are FilterReciept objects with special values to be evauluated by the matches filter function
    
    #prompts for value for a budget
    def queryBudget(self):
        while True:
            try:
                res = input("Enter a monthly budget:\t")
                res = float(res)
                return res
            except:
                print("Please enter a valid value for a budget")
        
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

    def writeJournal(self,file):
        with open(file,"wb") as output:
            pickle.dump(self,output,-1)

        #use pickle module to print to a file. will use pickle to read from file as well
        #TODO: Implement file I/O for reciepts and journal objects, then polish off core functionalities and move on to the main driver class!

    def addReciept(self):
        p = DigitalReciept.DigitalReciept()
        p.fillReciept(self.genres.keys())
        self.journal += p
        self.journal.sort()
        #TODO: inefficient: figure out an insert in order way rather than needlessly sorting list every time

    #searches for a reciept based on the given filter. Returns the reciept if found, returns None if cancel is entered
    def searchReciept(self, filter):
        tmpJournal = applyFilter(tmpFilter = filter)
        res = -1
        while res < 0 and res > len(tmpJournal):
            print("0.\tCancel\n")
            i = 1
            for reciept in tmpJournal:
                print(str(i) + ".", str(reciept), sep = "\t", end = "\n")
                i = i+1
        
            res = int(input("Enter the desired reciept:\t"))

        if(res is not 0):
            return tmpJournal[res-1]
        return None

    #allows user to edit a reciept that has been searched for
    def editReciept(self, reciept):
        reciept.editReciept(self.genres.keys())

    #guides the user through adding a new filter to the filters dicitonary and asks if it should be set to the current filter
    def addFilter(self):
        name = input('Please select a name for the new filter:\t')
        while name in self.filters.keys():
            name = input('Please select a name for the new filter that is not already a filter name:\t')
        f = DigitalReciept.FilterReciept()
        f.fillFilter(self.genres.keys())
        self.filters[name] = f
        res = input('Would you like to set this as the current filter?\t')
        if res.lower()[0] == 'y':
            self.curFilter = f 

    #sets the current filter from a name in the filters dicitonary unless the name is not there then it prints an error
    def setFilter(self, filterName):
        if filterName in self.filters.keys():
            self.curFilter = self.filters[filterName]
            return True
        else:
            print("It appears there is no filter with that name, please choose a valid name.")
            return False

    #prints the journal, if a filter is passed it it is set to the current filter for the duration of the function, if a cur filter is set then it filters
    #off of that otherwise it prints the entire contents
    def printJournal(self, filter = None):
        if filter and isinstance(filter, str) and filter in self.filters.keys():
            self.curFilter = self.filters[filter]
        tmpJournal = self.applyFilter()

        for reciept in tmpJournal:
            print(reciept)
        #if a temporary filter was passed in erase it afte rthe funciton
        if filter:
            self.curFilter = None
        
    #sums the journal, using the same methods for filtering as printJournal. Gives the user the option
    #to sum regardless of sign and purely on magnitude or regarding sign and based off net costs
    def sumJournal(self, filter = None):
        if filter and isinstance(filter, str) and filter in self.filters.keys():
            self.curFilter = self.filters[filter]
        tmpJournal = self.applyFilter()

        sum = 0.0
        res = input("Sum unbiased (ignore sign) or biased (include sign)?")
        if 'un' in res: 
            for reciept in tmpJournal:
                sum = sum + reciept.getCost()
            print("The unbiased sum (inconsiderate of sign) is:\t" + sum)
        else:
            for reciept in tmpJournal:
                sum = sum + reciept.getRealCost()
            print("The biased sum (considerate of sign) is:\t" + sum)

        #if a temporary filter was passed in erase it afte rthe funciton
        if filter:
            self.curFilter = None
    
    #averages the journal, using the same methods for filtering as printJournal. Gives the user the option
    #to saverage regardless of sign and purely on magnitude or regarding sign and based off net costs
    def averageJournal(self, filter = None):
        if filter and isinstance(filter, str) and filter in self.filters.keys():
            self.curFilter = self.filters[filter]
        tmpJournal = self.applyFilter()

        sum = 0.0
        res = input("Average unbiased (ignore sign) or biased (include sign)?")
        if 'un' in res: 
            for reciept in tmpJournal:
                sum = sum + reciept.getCost()
            sum = sum/len(tmpJournal)
            print("The unbiased average (inconsiderate of sign) is:\t" + sum)
        else:
            for reciept in tmpJournal:
                sum = sum + reciept.getRealCost()
            sum = sum/len(tmpJournal)
            print("The biased average (considerate of sign) is:\t" + sum)

        #if a temporary filter was passed in erase it afte rthe funciton
        if filter:
            self.curFilter = None

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
        if "m" == timeUnit:
            print("--------------------\n" + 
                  " LAST MONTHS REPORT \n" + 
                  "--------------------\n")
            tmpJournal = applyFilter(tmpFilter = DigitalReciept.getLastMonthFilter())
        
        balance = 0.0
        sum = 0.0
        minReciept = maxReciept = tmpJournal[0]
        for reciept in tmpJournal:
            balance = balance + reciept.getRealCost()
            sum = sum + reciept.getCost()
            if minReciept.getRealCost() > reciept.getRealCost(): minReciept = reciept
            if maxReciept.getRealCost() < reciept.getRealCost(): maxReciept = reciept


        print("MONTHLY BUDGET:\t" + str(self.budget), end = "\n")
        print("MONTHLY BALANCE:\t${0:>8.2f}".format(balance), end = "\n")
        print("MONTHLY SUM:\t${0:>8.2f}".format(sum), end = "\n")
        print("AVERAGE DAILY EXPENDITURE:\t${0:>8.2f}".format(balance/len(tmpJournal)), end = "\n")
        print("MINIMUM RECIEPT:\t" + str(minReciept), end = "\n")
        print("MAXIMUM RECIEPT:\t" + str(maxReciept), end = "\n")
        print("--------------------\n" +
              "  REPORT BY GENRE   \n" + 
              "--------------------\n")
        for genre in self.genres.keys():
            self.generateGenreReport(genre, timeUnit, tmpJournal)

    #NOTE: inefficient if time implement method to generate all information for reports in a single run through the list. Use a dictionary for that
    def generateGenreReport(self, genre, timeUnit, tmpJournal):
        print("    --------------------\n" +
              "    {0:^20.20}\n".format(genre) + 
              "    --------------------\n")

        balance = 0.0
        sum = 0.0
        minReciept = maxReciept = tmpJournal[0]
        for reciept in tmpJournal:
            if reciept.genre == genre:
                balance = balance + reciept.getRealCost()
                sum = sum + reciept.getCost()
                if minReciept.getRealCost() > reciept.getRealCost(): minReciept = reciept
                if maxReciept.getRealCost() < reciept.getRealCost(): maxReciept = reciept


        print("    MONTHLY BUDGET:\t" + str(self.budget), end = "\n")
        print("    MONTHLY BALANCE:\t${0:>8.2f}".format(balance), end = "\n")
        print("    MONTHLY SUM:\t${0:>8.2f}".format(sum), end = "\n")
        print("    AVERAGE DAILY EXPENDITURE:\t${0:>8.2f}".format(balance/len(tmpJournal)), end = "\n")
        print("    MINIMUM RECIEPT:\t" + str(minReciept), end = "\n")
        print("    MAXIMUM RECIEPT:\t" + str(maxReciept), end = "\n")

    #provides menu interface to edit individual genres. You have two options when editing a genre:
    #   1. Change Budget
    #   2. Delete Genre
    def editGenres(self):
        print("0.\tBack\n")
        i = 1
        for genre, bud in genres.items():
            print(str(i) + ".", genre, "Budget: " + str(bud), sep = "\t", end = "\n")
            i = i+1
        
        res = int(input("Enter a genre to edit. You may delete a Genre or modify its Budget:\t"))

        if(res is not 0):
            self.editGenre(res-1)

    #provides actual submenu for editing a genre
    def editGenre(self, genreIndex):
        print(str(genreIndex+1) + ".\t" + self.genres.keys().at(genreIndex) + "\tBudget: " + str(self.genres.values.at(genreIndex)) + "\n" +
              "\t0.\tBack\n" +
              "\t1.\tChange Budget\n" +
              "\t2.\tDelete Genre\n")

        res = int(input("Enter an option:\t"))
        
        if(res == 1):
            self.genres[self.genres.keys.at(genreIndex)] = float(input("Please enter the new genre budget:\t"))
        elif(res == 2):
            if( "y" == str(input("Deleting a genre will delete all its associated digital reciepts. Are you sure you still want to delete it? (Y/N)\t")).lower()):
                self.deleteGenre(genreIndex)
    
    #deletes the genre in genres at the given index and all associated DigitalReciept objects in journal
    def deleteGenre(self, genreIndex):
        delGenre = self.genres.keys.at(genreIndex)
        i = 0
        while i < len(self.journal):
            if self.journal[i].genre == delGenre:
                del self.journal[i]
            else:
                i = i+1
        del self.genres[delGenre]


    #helper funciton that applies the current filter and returns the resulting sublist 
    def applyFilter(self, tmpFilter = None):
        if not tmpFilter:
            if not self.curFilter:
                return self.journal
            subJournal = filter(self.curFilter.match, self.journal)
        else:
            subJournal = filter(tmpFilter.match, self.journal)
        return subJournal

    
