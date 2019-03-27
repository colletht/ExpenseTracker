import DigitalReciept

#journal will work similar to accounting journal, keep track of expenses and entries to different categories. Contains functions to get analytics from spendings
class Journal:
    def __init__(self):
        self.journal = []
        self.budget = 0
        self.genres = ['Food','Hygene','Cleaning','Clothes','Alcohol','Recreation','Gaming']

    