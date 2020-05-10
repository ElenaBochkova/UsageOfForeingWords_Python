from DatabaseControl import *
import play_the_word
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import webbrowser
import datetime
import json
import InputWindow
from NewCombo import NewCombo as nc
from ImportData import ImportForeignData as IFD
import Statistics

def clicked(the_word):
    play_the_word.play(the_word, "en")

   # Ниже workaround для исключения {} у многословных выражений
def return_list(expression):
    new_list = []
    for row in expression:
        new_list.append(row[0])
    return new_list

class FirstWindow():

    def __init__(self):
        self.link_to_source = ''
        self.window = Tk()
        self.window.title("Помощник в изучении слов")
        self.window.geometry('460x420')
        self.mainmenu = Menu(self.window)
        self.window.config(menu = self.mainmenu)

        self.datamenu = Menu(self.mainmenu, tearoff = 0)
        self.datamenu.add_command(label = "Добавить", command = lambda:
                               self.ask_input())
        self.datamenu.add_command(label = "Обновить", command = lambda:
                             self.refresh_data())
        self.datamenu.add_command(label = "Импорт", command = lambda:
                             self.open_new_datafile())
        self.datamenu.add_command(label = "Статистика", command = lambda:
                             self.ask_statistics())
        self.mainmenu.add_cascade(label = "Данные", menu = self.datamenu)
        create_database()
        self.session = connect_to_base()
        self.lbl = Label(self.window, text="Это слово:")
        self.lbl.place(x = 10, y = 8)
        self.combo = nc(self.window)
        self.combo.place(x = 5, y = 30)

        expressions = self.session.query(Expression.expression)
        self.combo['values'] = tuple(return_list(expressions))
        self.combo.save_value()


        self.combo.bind("<<ComboboxSelected>>", self.open_translate)

        self.lbl_t = Label(self.window, text = "Перевод:")
        self.lbl_t.place(x = 10, y = 58)
        self.lbl_u = Label(self.window, text = "Примеры использования:")
        self.lbl_u.place(x = 10, y = 108)

        self.combo_t = nc(self.window)
        self.combo_t.place(x = 5, y = 80)
        self.combo_t.bind("<<ComboboxSelected>>", self.on_select_translate)



        self.btn = Button(self.window, text="Произнести", command = lambda:
                     clicked(self.combo.get().lstrip("{").rstrip("}")))
        self.btn.place(x = 153, y = 27)

        self.btn_u = Button(self.window, text = "Примеры", command = lambda:
                       self.clicked_u(self.combo.get().lstrip("{").rstrip("}"),
                                 self.combo_t.get().lstrip("{").rstrip("}")))
        self.btn_u.place(x = 153, y = 77)

        self.text = Text()
        self.text['width'] = 55
        self.text['height'] = 10
        self.text.place(x = 5, y = 130)

        self.lbl_numb = Label(self.window, text = "Номер примера:")
        self.lbl_numb.place(x = 10, y = 300)

        self.combo_numb = Combobox(self.window, width = 3)
        self.combo_numb.place(x = 111, y = 300)

        self.combo_numb.bind("<<ComboboxSelected>>", self.on_select_pr_numb)

        self.lbl_author = Label(self.window, text = "Автор:")
        self.lbl_author.place(x = 70, y = 335)

        self.lbl_author_name = Label(self.window, fg = "#2521C0", font = "Arial 12")
        self.lbl_author_name.place(x = 111, y = 333)

        self.lbl_title = Label(self.window, text = "Книга:")
        self.lbl_title.place(x = 70, y = 360)

        self.lbl_title_name = Label(self.window, fg = "#2521C0", font = "Arial 12")
        self.lbl_title_name.place(x = 111, y = 358)

        self.lbl_subtitle = Label(self.window, text = "Глава:")
        self.lbl_subtitle.place(x = 70, y = 385)

        self.lbl_subtitle_name = Label(self.window, fg = "#2521C0", font = "Arial 12")
        self.lbl_subtitle_name.place(x = 111, y = 383)

        self.btn_link = Button(self.window, text="Ссылка на источник", command = lambda:
                     self.clicked_link())
        self.btn_link.place(x = 160, y = 298)

    #    btn_ask_input = Button(window, text = "Новые данные", command = lambda:
    #                           ask_input())
    #    btn_ask_input.place(x = 260, y = 57)

    #    btn_refresh = Button(window, text = "Обновить данные", command = lambda:
    #                         refresh_data())
    #    btn_refresh.place(x = 270, y = 17)

    def activate(self):
        self.window.mainloop()

    def ask_statistics(self):
        Statistics.the_window()

    def open_new_datafile(self):
        file_name = fd.askopenfilename(filetypes = (("Database files", "*.db"),
                                                   ("All files", "*.*")))
        new_session = connect_to_new_base(file_name)
        imp = IFD(self.session, new_session)
        imp.find_expr_diff()
        imp.fill_expr_diff()
        imp.fill_expr()
        self.refresh_data()

        
    def refresh_data(self):
        expressions = self.session.query(Expression.expression)
        self.combo['values'] = tuple(return_list(expressions))
        self.combo.save_value()
        self.combo.event_generate("<<ComboboxSelected>>")
        mb.showinfo("Ok!", f"Новые данные подтянуты в программу!")


    def select_usage(self, expr, trans):
        id_word = self.session.query(Expression).filter_by(
            expression = expr).first()
        id_trans = self.session.query(Expr_Translation.id).filter_by(
            expression = id_word.id).filter_by(
                translation = trans).first()
        return id_word.id, id_trans.id


    def clear_all(self):
        self.lbl_author_name['text'] = ''
        self.lbl_title_name['text'] = ''
        self.lbl_subtitle_name['text'] = ''
        self.link_to_source = ''
        self.text.delete('1.0', END)

    def open_translate(self, v):
        """ процедура вставляет варианты перевода выбранного слова
в соответствующий комбобокс после выбора значения в комбобоксе "Слово"

также очищает все прочие значения"""
        self.clear_all()
        self.combo_t['values'] = ('',)
        self.combo_t.current(0)
        
        expression_id = self.session.query(Expression.id).filter_by(
            expression = self.combo.get().lstrip("{").rstrip("}"))
        translation = self.session.query(Expr_Translation.translation).filter_by(
            expression = expression_id)
        new_list = return_list(translation)
        self.combo_t['values'] = tuple(new_list)
        self.combo_t.save_value()


    def on_select_translate(self, vl):
        self.clear_all()

    def clicked_u(self, expr, trans):
        """процедура вставляет в текстовое поле примеры использования
выбранного перевода выбранного слова"""

        self.combo_numb['values'] = ('')
        
        self.text.delete(1.0, END)
        id1, id2 = self.select_usage(expr, trans)

        expr_usage = self.session.query(Expr_Usage.expr_usage).filter_by(
            expression = id1).filter_by(translation = id2)
        
        j = 1.0
        ins = ""
        numb_pr = 1
        val_numb_pr = []
        for line in expr_usage:
            k = 3
            if line[0] != '':
                lines = line[0].split()
                ins = repr(numb_pr)
                ins = ins + ". "
                val_numb_pr.append(numb_pr)
                numb_pr = numb_pr+1
                for a in lines:
                    k = k + len(a) + 1
                    if k > 55:
                        self.text.insert(j, ins+"\n")
                        k = len(a)+1
                        ins = a + " "
                        j = j + 1
                    else:
                        ins = ins + a + " "
                self.text.insert(j, ins+"\n")
                j = j+1
        self.combo_numb['values'] = tuple(val_numb_pr)
        if expr_usage!= [('',)]:
            self.combo_numb.current(0)
            self.combo_numb.event_generate("<<ComboboxSelected>>")

    def on_select_pr_numb(self, vl):
        """выводит информацию об источнике примера по его номеру"""

        id1, id2 = self.select_usage(self.combo.get().lstrip("{").rstrip("}"),
                                self.combo_t.get().lstrip("{").rstrip("}"))
        expr_usage = self.session.query(Expr_Usage).filter_by(
            expression = id1).filter_by(translation = id2)
        
        if expr_usage!=[('',)]:
            number = int(self.combo_numb.get())
            k = 1
            for line in expr_usage:
                if k == number:
                    source_id = line.usage_source
                    ids = self.session.query(Source).filter_by(
                        id = source_id).first()
                    author = self.session.query(Author).filter_by(
                        id = ids.author).first()
                    title = self.session.query(Title).filter_by(
                        id = ids.title).first()
                    subtitle = self.session.query(Subtitle).filter_by(
                        id = ids.subtitle).first()
                    self.lbl_author_name['text'] = author.author
                    self.lbl_title_name['text'] = title.title
                    self.lbl_subtitle_name['text'] = subtitle.subtitle
                    self.link_to_source = subtitle.link
                    k = k + 1
                else:
                    k = k +1    

    def ask_input(self):
        def button_click():
            login = combo_user.get()
            with open("your_login.json", 'w') as f: 
                json.dump(login, f) #сохраняем выбранного юзера в файл
            login_window.destroy()
            InputWindow.input_window(login) 
            
        def button_add_click():
            answer = mb.askyesno(title = "Уверены?",
                                 message = f"Создать пользователя {combo_user.get()}?")
            if answer == True:
                newUser = User()
                newUser.login_name = combo_user.get()
                newUser.user_score = 0
                date_time = datetime.datetime.now()
                newUser.user_start = date_time
                newUser.user_last_add = date_time
                self.session.add(newUser)
                self.session.commit()
                user_names = self.session.query(User.login_name)
                combo_user['values'] = tuple(user_names)
                mb.showinfo("Ok!",
                            f"Пользователь {combo_user.get()} создан!")
            else:
                mb.showinfo("Ok!",
                            f"Пользователь {combo_user.get()} не создан!")
            
        login_window = Toplevel(self.window)
        login_window.title("Назовитесь!")
        login_window.geometry('240x125')

        lbl_user = Label(login_window, text = "Пользователь:", fg = "#473773",
                         font = "Arial 11")

        lbl_user.place(x = 10, y = 11)
        
        combo_user = Combobox(login_window)
        combo_user.place (x = 50, y = 39)
        login = ''
        try:
            with open("your_login.json", 'r') as f:
                login = json.load(f)
        except:
            pass        
        user_names = self.session.query(User.login_name)
        user_logins = tuple(return_list(user_names))
        combo_user['values'] = user_logins
        k = 0
        for name in user_logins: #ищем пользователя, сохраненного в файле
            if (name == login):
                combo_user.current(k) #выбираем найденного пользователя
                login = '0' #если нашли, отмечаем это так
                break
            else:
                k = k +1
        if login != '0': #если не нашли юзера из файла, берем первого
            combo_user.current(0)
                
        button_ok = Button(login_window, text = "Приступить!", fg = "#473773",
                           font = "Arial 11", command=lambda: button_click())
        button_ok.place(x = 118, y = 76)

        button_add = Button(login_window, text = "Добавить!", fg = "#473773",
                           font = "Arial 11",
                            command=lambda: button_add_click())
        button_add.place(x = 18, y = 76)

    def clicked_link(self):
        if self.link_to_source != '':
            webbrowser.open_new(self.link_to_source)





if __name__ == '__main__':
    f = FirstWindow()
    f.activate()
