import DigitalReciept, functools, os, pprint

#journal will work similar to accounting journal, keep track of expenses and entries to different categories. Contains functions to get analytics from spendings
class Journal:
    def __init__(self, genreList = ['Food','Hygene','Cleaning','Clothes','Alcohol','Recreation','Gaming']):
        self.journal = []
        self.budget = 0
        self.genres = genreList
        self.curFilter = None   
        self.filters = {}    #will hold dictionary of saved filters and their names, filters are FilterReciept objects with special values to be evauluated by the matches filter function
    
    #adds a new genre to the genre list
    def addGenre(self):
        res = input("Enter the name of your new genre:\t")
        if res.lower() in list(map(lambda x: x.lower(), self.genres)):
            print("You must enter a genre does not yet exist")
            return False
        else:
            self.genres.append(res.strip())
            return True

    def writeJournal(self,file):
        pass
        #here we will use pprint.pformat(journal) to print the results to the given file.py and then we can read it in from there whenever we wish
        #TODO: Implement file I/O for reciepts and journal objects, then polish off core functionalities and move on to the main driver class!

    def addReciept(self):
        p = DigitalReciept.DigitalReciept()
        p.fillReciept(self.genres)
        self.journal += p
        self.journal.sort()
        #TODO: inefficient: figure out an insert in order way rather than needlessly sorting list every time

    #allows user to edit a reciept that has been searched for
    def editReciept(self, reciept):
        reciept.editReciept(self.genres)

    #guides the user through adding a new filter to the filters dicitonary and asks if it should be set to the current filter
    def addFilter(self):
        name = input('Please select a name for the new filter:\t')
        while name in self.filters.keys():
            name = input('Please select a name for the new filter that is not already a filter name:\t')
        f = DigitalReciept.FilterReciept()
        f.fillFilter(self.genres)
        self.filters[name] = f
        res = input('Would you like to set this as the current filter?\t')
        if res.lower()[0] == 'y':
            self.curFilter = f 

    #sets the current filter from a name in the filters dicitonary unless the name is not there then it prints an error
    def setFilter(self, filterName):
        if filterName in self.filters.keys():
            self.curFilter = self.filters[filterName]
        else:
            print("It appears there is no filter with that name, please choose a valid name.")

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

    #helper funciton that applies the current filter and returns the resulting sublist 
    def applyFilter(self):
        if not self.curFilter:
            return self.journal
        subJournal = filter(self.curFilter.match, self.journal)
        return subJournal

    
