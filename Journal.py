import DigitalReciept, functools

#journal will work similar to accounting journal, keep track of expenses and entries to different categories. Contains functions to get analytics from spendings
class Journal:
    def __init__(self):
        self.journal = []
        self.budget = 0
        self.genres = ['Food','Hygene','Cleaning','Clothes','Alcohol','Recreation','Gaming']
        self.curFilter = None   
        self.filters = {}    #will hold dictionary of saved filters and their names, filters are FilterReciept objects with special values to be evauluated by the matches filter function
    
    def addReciept(self):
        p = DigitalReciept.DigitalReciept()
        p.fillReciept(self.genres)
        self.journal += p
        self.journal.sort()
        #TODO: inefficient: figure out an insert in order way rather than needlessly sorting list every time

    def editReciept(self, reciept):
        reciept.editReciept(self.genres)

    def applyFilter(self):
        subJournal = filter(self.curFilter.match, self.journal)
        return subJournal

