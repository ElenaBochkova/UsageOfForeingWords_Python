from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import pandas as pd
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import datetime
from NewCombo import NewCombo as nc
from DatabaseControl import *
import play_the_word
from FirstWindow import return_list as rl

def the_window():

    def draw_statistics(v):
        user = session.query(User).filter_by(
            login_name = combo_user.get()).first()
        dates = rl(session.query(Expr_Usage.date_time).filter_by(
            add_user = user.id))
        k = 0
        the_scores = {}
        new_scores = []
        for date in dates:
            the_date = date.date()
            the_scores[the_date] = the_scores.get(the_date, 0) + 1
        for date, score in the_scores.items():
            new_scores.append({"date" : date, "score" : score})
        with open('the_scores.csv', "w", newline = "") as file:
            columns = ['date', 'score']
            writer = csv.DictWriter(file, fieldnames = columns)
            writer.writeheader()
            writer.writerows(new_scores)
        df1 = pd.read_csv('the_scores.csv')

        lbl_total_score['text'] = "Очки: " + str(user.user_score)

        f = Figure(figsize = (6,4), dpi = 100)
        a = f.add_subplot(111)
        a.plot(df1['date'], df1['score'], marker='o')
        a.grid()
        
        dataPlot = FigureCanvasTkAgg(f, master = window)
        dataPlot.draw()
        dataPlot.get_tk_widget().place(x = 0, y = 100)

        
        
        
        
    
    window = Tk()
    window.title("Статистика")
    window.geometry("600x500")
    session = connect_to_base()

    combo_user = nc(window, width = 25)
    combo_user.place(x = 7, y = 30)
    users = session.query(User.login_name)
    combo_user['values'] = rl(users)
    combo_user.save_value()

    combo_user.bind("<<ComboboxSelected>>", draw_statistics)

    lbl = Label(window, text="Пользователь:", fg = "#2521C0", font = "Arial 12")
    lbl.place(x = 5, y = 5)

    lbl_gr = Label(window, text = "Количество введенных использований слов, по дням:",
                   font = "Arial 12", fg = "#2521C0")
    lbl_gr.place(x = 100, y = 73)

    lbl_total_score = Label(window, text = "Очки:",
                            fg = "#2521C0", font = "Arial 12")
    lbl_total_score.place(x = 5, y = 52)

    canvas = Canvas(window, width = 600, height = 500, bg = "#E0EBE3")
    canvas.place(x = 0, y = 100)

    window.mainloop()
    
if __name__ == '__main__':
    the_window()
