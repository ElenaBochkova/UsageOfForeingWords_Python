from tkinter.ttk import Combobox
from tkinter import *

class NewCombo(Combobox):
    def __return_list(self, expression):
        new_list = []
        for row in expression:
            new_list.append(row)
        return new_list

    def on_type(self, v):
        '''    selects appropriate values from all NewCombo['values']
    should be used as NewCombo.bind("<KeyRelease>", NewCombo.on_type)'''
        keys = repr(v).split()
        if (keys[4] not in ('keycode=37',
                            'keycode=39',
                            'keycode=17',
                            'keycode=18',
                            'keycode=38',
                            'keycode=16')):
            self['values'] = ('')
            new_list = []
            val = self.get().lstrip("{").rstrip("}")
            for line in self.expressions:
                if line.startswith(val):
                    new_list.append(line)
            new_list = self.__return_list(new_list)
            self['values']=tuple(new_list)

    def __init__(self, values):
        super().__init__()
        self.expressions = ('')

    def save_value(self):
        '''saves all current NewCombo['values'] to make choice from them in on_type
'''
        self.expressions = self['values']
        
   

if __name__ == '__main__':
    window = Tk()
    combo = NewCombo(window)
    combo.place(x = 5, y = 20)
    combo['values'] = ("Шаринган", "Чакра", "Ци", "Человек")
    combo.save_value()
    combo.bind("<KeyRelease>", combo.on_type)
    mainloop()
