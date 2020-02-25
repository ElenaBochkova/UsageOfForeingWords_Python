from DatabaseControl import *
import play_the_word
from tkinter import *
from tkinter.ttk import Combobox
import webbrowser
import InputWindow
import datetime
from NewCombo import NewCombo as nc

def clicked(the_word):
    play_the_word.play(the_word)

combo_list = []
translations = []
authors = []
titles = []
subtitles = []

link_to_source = ''


def the_window():

    # Ниже workaround для исключения {} у многословных выражений
    def return_list(expression):
        new_list = []
        for row in expression:
            new_list.append(row[0])
        return new_list

    def refresh_data():
        expressions = session.query(Expression.expression)
        combo['values'] = tuple(return_list(expressions))
        combo.event_generate("<<ComboboxSelected>>")


    def select_usage(expr, trans):
        id_word = session.query(Expression).filter_by(
            expression = expr).first()
        id_trans = session.query(Expr_Translation.id).filter_by(
            expression = id_word.id).filter_by(
                translation = trans).first()
        return id_word.id, id_trans.id


    def clear_all():
        lbl_author_name['text'] = ''
        lbl_title_name['text'] = ''
        lbl_subtitle_name['text'] = ''
        global link_to_source
        link_to_source = ''
        text.delete('1.0', END)    

    def open_translate(v):
        """ процедура вставляет варианты перевода выбранного слова
в соответствующий комбобокс после выбора значения в комбобоксе "Слово"

также очищает все прочие значения"""
        clear_all()
        
        expression_id = session.query(Expression.id).filter_by(
            expression = combo.get().lstrip("{").rstrip("}"))
        translation = session.query(Expr_Translation.translation).filter_by(
            expression = expression_id)
        new_list = return_list(translation)
        combo_t['values'] = tuple(new_list)
        combo_t.save_value()


    def on_select_translate(vl):
        clear_all()

    def clicked_u(expr, trans):
        """процедура вставляет в текстовое поле примеры использования
выбранного перевода выбранного слова"""

        combo_numb['values'] = ('')
        
        text.delete(1.0, END)
        id1, id2 = select_usage(expr, trans)

        expr_usage = session.query(Expr_Usage.expr_usage).filter_by(
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
                    if k > 50:
                        text.insert(j, ins+"\n")
                        k = len(a)+1
                        ins = a + " "
                        j = j + 1
                    else:
                        ins = ins + a + " "
                text.insert(j, ins+"\n")
                j = j+1
        combo_numb['values'] = tuple(val_numb_pr)
        if expr_usage!= [('',)]:
            combo_numb.current(0)
            combo_numb.event_generate("<<ComboboxSelected>>")

    def on_select_pr_numb(vl):
        """выводит информацию об источнике примера по его номеру"""

        id1, id2 = select_usage(combo.get().lstrip("{").rstrip("}"),
                                combo_t.get().lstrip("{").rstrip("}"))
        expr_usage = session.query(Expr_Usage).filter_by(
            expression = id1).filter_by(translation = id2)
        
        if expr_usage!=[('',)]:
            number = int(combo_numb.get())
            k = 1
            for line in expr_usage:
                if k == number:
                    source_id = line.usage_source
                    ids = session.query(Source).filter_by(
                        id = source_id).first()
                    author = session.query(Author.author).filter_by(
                        id = ids.author).first()
                    title = session.query(Title.title).filter_by(
                        id = ids.title).first()
                    subtitle = session.query(Subtitle).filter_by(
                        id = ids.subtitle).first()
                    lbl_author_name['text'] = author.author
                    lbl_title_name['text'] = title.title
                    lbl_subtitle_name['text'] = subtitle.subtitle
                    global link_to_source
                    link_to_source = subtitle.link
                    k = k + 1
                else:
                    k = k +1    

    def ask_input():
        def button_click():
            login = combo_user.get()
            login_window.destroy()
            InputWindow.input_window(login)
            
        def button_add_click():
            newUser = User()
            newUser.login_name = combo_user.get()
            newUser.user_score = 0
            date_time = datetime.datetime.now()
            newUser.user_start = date_time
            newUser.user_last_add = date_time
            session.add(newUser)
            session.commit()
            user_names = session.query(User.login_name)
            combo_user['values'] = tuple(user_names)
            
        login_window = Toplevel(window)
        login_window.title("Назовитесь!")
        login_window.geometry('240x125')

        lbl_user = Label(login_window, text = "Пользователь:", fg = "#473773",
                         font = "Arial 11")

        lbl_user.place(x = 10, y = 11)
        
        combo_user = Combobox(login_window)
        combo_user.place (x = 50, y = 39)
        session = connect_to_base()
        user_names = session.query(User.login_name)
        combo_user['values'] = tuple(user_names)
        if tuple(user_names) !=(('',),):
            combo_user.current(0)
        button_ok = Button(login_window, text = "Приступить!", fg = "#473773",
                           font = "Arial 11", command=lambda: button_click())
        button_ok.place(x = 118, y = 76)

        button_add = Button(login_window, text = "Добавить!", fg = "#473773",
                           font = "Arial 11",
                            command=lambda: button_add_click())
        button_add.place(x = 18, y = 76)

    def clicked_link():
        if link_to_source != '':
            webbrowser.open_new(link_to_source)

            

    window = Tk()
    window.title("Помощник в изучении слов")
    window.geometry('430x420')
    create_database()
    session = connect_to_base()
    lbl = Label(window, text="Это слово:")
    lbl.place(x = 10, y = 8)
    combo = nc(window)
    combo.place(x = 5, y = 30)

    expressions = session.query(Expression.expression)
    combo['values'] = tuple(return_list(expressions))
    combo.save_value()
    

    combo.bind("<KeyRelease>", combo.on_type)
    combo.bind("<<ComboboxSelected>>", open_translate)
    
    lbl_t = Label(window, text = "Перевод:")
    lbl_t.place(x = 10, y = 58)
    lbl_u = Label(window, text = "Примеры использования:")
    lbl_u.place(x = 10, y = 108)

    combo_t = nc(window)
    combo_t.place(x = 5, y = 80)
    combo_t.bind("<<ComboboxSelected>>", on_select_translate)
    combo_t.bind("<KeyRelease>", combo_t.on_type)
    

    
    btn = Button(window, text="Произнести", command = lambda:
                 clicked(combo.get().lstrip("{").rstrip("}")))
    btn.place(x = 153, y = 27)

    btn_u = Button(window, text = "Примеры", command = lambda:
                   clicked_u(combo.get().lstrip("{").rstrip("}"),
                             combo_t.get().lstrip("{").rstrip("}")))
    btn_u.place(x = 153, y = 77)

    text = Text()
    text['width'] = 50
    text['height'] = 10
    text.place(x = 5, y = 130)

    lbl_numb = Label(window, text = "Номер примера:")
    lbl_numb.place(x = 10, y = 300)

    combo_numb = Combobox(window, width = 3)
    combo_numb.place(x = 111, y = 300)

    combo_numb.bind("<<ComboboxSelected>>", on_select_pr_numb)

    lbl_author = Label(window, text = "Автор:")
    lbl_author.place(x = 70, y = 335)

    lbl_author_name = Label(window, fg = "#2521C0", font = "Arial 12")
    lbl_author_name.place(x = 111, y = 333)

    lbl_title = Label(window, text = "Книга:")
    lbl_title.place(x = 70, y = 360)

    lbl_title_name = Label(window, fg = "#2521C0", font = "Arial 12")
    lbl_title_name.place(x = 111, y = 358)

    lbl_subtitle = Label(window, text = "Глава:")
    lbl_subtitle.place(x = 70, y = 385)

    lbl_subtitle_name = Label(window, fg = "#2521C0", font = "Arial 12")
    lbl_subtitle_name.place(x = 111, y = 383)

    btn_link = Button(window, text="Ссылка на источник", command = lambda:
                 clicked_link())
    btn_link.place(x = 160, y = 298)

    btn_ask_input = Button(window, text = "Новые данные", command = lambda:
                           ask_input())
    btn_ask_input.place(x = 260, y = 57)

    btn_refresh = Button(window, text = "Обновить данные", command = lambda:
                         refresh_data())
    btn_refresh.place(x = 270, y = 17)

    window.mainloop()

if __name__ == '__main__':
    the_window()
