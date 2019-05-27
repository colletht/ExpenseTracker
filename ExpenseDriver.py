#!PYTHON

import os, pickle
from pathvalidate import is_valid_filename
from Journal import Journal

PATH_TO_APPFILES = "C:\\Users\\colle\\Documents\\Python Experiments\\ExpenseTracker\\AppFiles"

class ExpenseDriver:
    def __init__(self):
        #list of values for menu. this structure acts as a map that redirects the program to the appropriate functions
        #if a none value is present it means redirect and display the page at the index of the number at the current option
        self.curJournal = Journal()
        self.__menu = [[("0.\tExit", self.__exit) , ("1.\tReciepts", None), ("2.\tGenres", None), ("3.\tFilters", None), ("4.\tAnalytics", None), ("5.\tGenerate a Report", self._ExpenseDriver__generateReport), ("6.\tSettings", None)], 
                        [("0.\tBack", None), ("1.\tAdd a new Reciept", self.__addReciept), ("2.\tEdit an existing Reciept", self.__editReciept), ("3.\tDelete a Reciept", self.__deleteReciept)],
                        [("0.\tBack", None), ("1.\tAdd a new Genre", self.__addGenre), ("2.\tEdit your Genre Settings", self.__editGenre)],
                        [("0.\tBack", None), ("1.\tAdd a new Filter", self.__addFilter), ("2.\tEdit your Filters", self.__editFilter), ("3.\tSet a Current Filter", self.__setFilter)],
                        [("0.\tBack", None), ("1.\tPrint your Journal", self.__printJournal), ("2.\tView Journal Sum", self.__sumJournal), ("3.\tView Journal Averages", self.__averageJournal)],
                        None,
                        None]



        #case no files in appfiles == user never created journal. Walks through journal creation
        if not os.listdir(PATH_TO_APPFILES):
            filename = input("It appears you have no journals yet. Please enter the name of your first journal:\t") + ".pkl"
            while(not is_valid_filename(filename)):
                filename = input("Please enter a valid filename:\t") + ".pkl"
            #create file
            open(os.path.join(PATH_TO_APPFILES, filename),"w+").close()
            self.curFile = filename


        #case files in appfiles == user has created journals, must select a journal to load or create a  new one
        else:
            self.curFile = self._ExpenseDriver__selectFile()
            if os.stat(os.path.join(PATH_TO_APPFILES, self.curFile)).st_size is not 0:
                with open(os.path.join(PATH_TO_APPFILES, self.curFile),"rb") as infile:
                    self.curJournal = pickle.load(infile)
                    print("Succesfully loaded journal from file " + self.curFile, end = ".\n")

    #walks user through selecting from existing files in directory or creating a new file, return the name of the file created
    def __selectFile(self):
        try:
            res = -1
            while res not in range(0, len(os.listdir(PATH_TO_APPFILES)) + 1):
                print("0.\tNew File.")
                i = 1
                for fName in os.listdir(PATH_TO_APPFILES):
                    print(str(i) + ".\t" + fName[0:-4] + ".")
                    i = i + 1

                res = int(input("Please select which file you would like to load your journal from:\t"))
            
            if res is not 0:
                return os.listdir(PATH_TO_APPFILES)[res-1]
            else:
                return self.__createFile()
        except ValueError:
            print("Please enter an integer argument.")
            return self._ExpenseDriver__selectFile()

    def __createFile(self):
        filename = input("Please enter the name of your new journal:\t") + ".pkl"
        while(not is_valid_filename(filename)):
            filename = input("Please enter a valid filename:\t") + ".pkl"
        #create file
        open(os.path.join(PATH_TO_APPFILES, filename),"w+").close()
        print("Succesfully created save file for " + str(filename[0:-4]))
        return filename

    #prints to the console the menu. SubMenu represents the level of the menu, -1 represents head menu, see plan.txt for menu structure
    def __printMenu(self, subMenu = 0):
        for x,_ in self._ExpenseDriver__menu[subMenu]:
            print(x)
        print()
    
    #helper that constructs prompt depending on state of program
    def __getPrompt(self):
        promptString = self.curFile[0:-4]
        if self.curJournal.curFilter:
            promptString += " - Filtering by: \"" + str(self.curJournal.curFilter[0]) + "\""
            
        promptString += " >>>\t"
        return promptString

    #recursive function, returns the code selected by the user
    def __getMenuOption(self, subMenu = 0):
        try:
            #get the option from the user
            self._ExpenseDriver__printMenu(subMenu = subMenu)
            res = int(input(self._ExpenseDriver__getPrompt()))
            print()

            #make sure res is a in the range of the possible options
            while res not in range(0,len(self._ExpenseDriver__menu[subMenu])):
                self._ExpenseDriver__printMenu(subMenu = subMenu)
                res = int(input(self._ExpenseDriver__getPrompt()))
                print()

            if self._ExpenseDriver__menu[subMenu][res][-1]:
                #if there is a function return it so that it may be executed
                return self._ExpenseDriver__menu[subMenu][res][-1]
            else:
                #if there is no argument that means we still need to traverse the menu so recursively call the function
                return self._ExpenseDriver__getMenuOption(subMenu = res)

        except ValueError:
            #current option failed so recursively call the same function and try again
            print("Please enter an integer argument.")
            return self._ExpenseDriver__getMenuOption(subMenu = subMenu)

    #performs all necessary procedures to exit the program, namely saving the journal into the default, or entered by user, file
    def __exit(self):
        try:
            print("Save your journal to \"" + self.curFile[0:-4] + "\"",
                    "0.\tDon't Save",
                    "1.\tOK",
                    "2.\tChoose another File", sep = "\n", end = "\n")
            res = int(input(self._ExpenseDriver__getPrompt()))

            while res not in range(0,3):
                print("Save your journal to \"" + self.curFile[0:-4] + "\"",
                        "0.\tDon't Save",
                        "1.\tOK",
                        "2.\tChoose another File", sep = "\n", end = "\n")
                res = int(input(self._ExpenseDriver__getPrompt()))

            if res is 1:
                self.curJournal.writeJournal(os.path.join(PATH_TO_APPFILES, self.curFile))
            elif res is not 0:
                self.curJournal.writeJournal(os.path.join(PATH_TO_APPFILES, self._ExpenseDriver__selectFile()))

            #indicate that exit has been ran by returning false, thus terminating the loop in REPL
            return False
        except ValueError:
            print("Please enter an integer argument.")
            return self._ExpenseDriver__exit()

    def __addGenre(self):
        self.curJournal.addGenre()
        return True

    def __editGenre(self):
        self.curJournal.editGenres()
        return True

    def __addReciept(self):
        self.curJournal.addReciept()
        return True

    def __editReciept(self):
        print("Create a temporary filter to narrow our search.")
        self.curJournal.editReciept(self.curJournal.searchReciept(self.curJournal.temporaryFilter()))
        return True

    def __deleteReciept(self):
        print("Create a temporary filter to narrow our search.")
        self.curJournal.deleteReciept(self.curJournal.searchReciept(self.curJournal.temporaryFilter()))
        return True

    def __addFilter(self):
        self.curJournal.addFilter()
        return True

    def __editFilter(self):
        self.curJournal.editFilters()
        return True

    def __setFilter(self):
        self.curJournal.setFilter()
        return True

    def __printJournal(self):
        if self.curJournal.size() is 0:
            print("You don't have any reciepts to display yet. Add some!")
            return True

        self.curJournal.printJournal(filt = self.curJournal.curFilter)
        print()
        return True

    def __sumJournal(self):
        if self.curJournal.size() is 0:
            print("You don't have any reciepts to sum yet. Add some!")
            return True

        self.curJournal.sumJournal(filt = self.curJournal.curFilter)
        print()
        return True

    def __averageJournal(self):
        if self.curJournal.size() is 0:
            print("You don't have any reciepts to average yet. Add some!")
            return True

        self.curJournal.averageJournal(filt = self.curJournal.curFilter)
        print()
        return True

    #TODO: add future functionality for different time spans
    def __generateReport(self):
        self.curJournal.generateReport()
        return True

    def REPL(self):
        run = True
        while run:
            fun = self._ExpenseDriver__getMenuOption(subMenu = 0)
            run = fun()
            


if __name__ == '__main__':
    expenseTracker = ExpenseDriver()
    expenseTracker.REPL()
            
            



