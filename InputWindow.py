from DatabaseControl import *
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox as mb
import datetime
from NewCombo import NewCombo as nc

combo_list = []
translations = []
authors = []
titles = []
subtitles = []
info = ''

def input_window(user_name):

    def add_language():
        def button_ok_click():
            answer = mb.askyesno(title = "Уверены?",
                                 message = f"Создать язык {combo_language.get()}?")
            if answer == True:
                newlang = Language()
                newlang.language = combo_language.get()
                session.add(newlang)
                session.commit()
                mb.showinfo("Ok!",
                            f"Язык {combo_language.get()} добавлен!")
                languages = session.query(Language.language)
                combo_l_source['values'] = tuple(languages)
                combo_l_source.current(0)
                combo_l_trans['values'] = tuple(languages)
                combo_l_trans.current(1)
                add_l_window.destroy()
            else:
                mb.showinfo("Ok!",
                            f"Язык {combo_language.get()} не добавлен!")
                add_l_window.destroy()
        
        add_l_window = Toplevel(window)
        add_l_window.title("Новый язык!")
        add_l_window.geometry('240x125')

        lbl_language = Label(add_l_window, text = "Язык:", fg = "#473773",
                         font = "Arial 11")
        lbl_language.place(x = 10, y = 11)

        combo_language = nc(add_l_window)
        combo_language.place(x = 50, y = 39)
        session = connect_to_base()
        languages = session.query(Language.language)
        combo_language['values'] = tuple(return_list(languages))
        combo_language.save_value()
        combo_language.bind("<KeyRelease>", combo_language.on_type)
        
        button_ok = Button(add_l_window, text = "Добавить!", fg = "#473773",
                           font = "Arial 11",
                           command=lambda: button_ok_click())
        button_ok.place(x = 118, y = 76)



        
    def return_list(expression):
        new_list = []
        for row in expression:
            new_list.append(row[0])
        return new_list

    def refresh_data():
        expressions = session.query(Expression.expression)
        combo['values'] = tuple(return_list(expressions))

        authors = session.query(Author.author)
        combo_author['values'] = tuple(return_list(authors))
        combo.event_generate("<<ComboboxSelected>>")


    def insert_a_word(a_word):
        """вставляет новое слово без перевода и использования"""
        global info
        info = info + "Вставляем новое слово "+ a_word + "\n"
        new_word = Expression()
        new_word.expression = a_word
        session.add(new_word)
        session.commit()

    def insert_a_translation(a_word, a_trans):
        """вставляет новый перевод заданному слову"""
        global info
        info = info + "Вставляем новый перевод " + a_trans
        info = info + " к слову " + a_word + "\n"
        new_trans = Expr_Translation()
        id_word = session.query(Expression).filter_by(
            expression = a_word).first()
        new_trans.expression = id_word.id
        print(type(id_word))
        lang_from = session.query(Language).filter_by(
            language = combo_l_source.get()).first()
        new_trans.lang_from = lang_from.id
        lang_to = session.query(Language).filter_by(
            language = combo_l_trans.get()).first()
        new_trans.lang_to = lang_to.id
        new_trans.translation = a_trans
        session.add(new_trans)
        session.commit()

    def insert_a_source(an_author, a_title, a_subtitle, a_link):
        """вставляет новый источник использования"""
        a_new_source = False
        global info
        info = info + "Вставляем новый источник:\n" 
        info = info + "\tавтор: " + an_author + "\n"
        info = info + "\tкнига: " + a_title + "\n"
        info = info + "\tглава: " + a_subtitle + "\n"
        info = info + "\tссылка: " + a_link + "\n"
        #если автор новый, добавляем его в базу
        id_author = session.query(Author.id).filter_by(
            author = an_author).first()
        if id_author == None:
            author = Author()
            author.author = an_author
            session.add(author)
            id_author = session.query(Author.id).filter_by(
                author = an_author).first()
        #если книга новая, добавляем ее в базу
        id_title = session.query(Title.id).filter_by(
            title = a_title).first()
        if id_title == None:
            title = Title()
            title.author = id_author.id
            title.title = a_title
            session.add(title)
            id_title = session.query(Title.id).filter_by(
                title = a_title).first()
        #если глава новая, добавляем ее в базу
        id_subtitle = session.query(Subtitle.id).filter_by(
            subtitle = a_subtitle).first()
        if id_subtitle == None:
            subtitle = Subtitle()
            subtitle.title = id_title.id
            subtitle.subtitle = a_subtitle
            subtitle.link = a_link
            session.add(subtitle)
            id_subtitle = session.query(Subtitle.id).filter_by(
                subtitle = a_subtitle).first()
        #добавляем новый источник в базу
        source = Source()
        source.author = id_author.id
        source.title = id_title.id
        source.subtitle = id_subtitle.id
        session.add(source)
        #финальный коммит для сохранения данных
        session.commit()

    def correct_a_source_link(subtitle_id, a_link):
        """изменяет ссылку на источник"""
        global info
        info = info + "Изменяем ссылку " + repr(subtitle_id) + " на "
        info = info + a_link.rstrip('\n') + "\n"
        link = session.query(Subtitle).filter_by(
            id = subtitle_id).first()
        link.link = a_link
        session.add(link)
        session.commit()

    def insert_an_usage(a_word, a_trans, a_usage, a_user,
                        an_author, a_title, a_subtitle):
        """вставляет новый вариант использования"""
        global info
        info = info + "Вставляем новый вариант использования\n"
        info = info + a_usage + "\n"
        info = info + "для слова " + a_word + " с переводом " + a_trans + "\n"
        info = info + "пользователь " + a_user + "\n"
        id_author = session.query(Author.id).filter_by(
            author = an_author).first()
        id_title = session.query(Title.id).filter_by(
            title = a_title).first()
        id_subtitle = session.query(Subtitle.id).filter_by(
            subtitle = a_subtitle).first()
        id_source = session.query(Source.id).filter_by(
            author = id_author.id).filter_by(
                title = id_title.id).filter_by(
                    subtitle = id_subtitle.id).first()
        id_word = session.query(Expression.id).filter_by(
            expression = a_word).first()
        id_trans = session.query(Expr_Translation.id).filter_by(
            expression = id_word.id).filter_by(
                translation = a_trans).first()
        user = session.query(User).filter_by(
            login_name = a_user).first()
        user.user_score = user.user_score + 1
        new_usage = Expr_Usage()
        new_usage.expression = id_word.id
        new_usage.translation = id_trans.id
        new_usage.expr_usage = a_usage
        new_usage.usage_source = id_source.id
        new_usage.add_user = user.id
        new_usage.date_time = datetime.datetime.now()
        user.user_last_add = new_usage.date_time
        session.add(new_usage)
        session.add(user)
        session.commit()




    def error_message(messages):
        """выводит сообщение об ошибках"""
        message_window = Toplevel(window)
        message_window.title("Ошибки!")
        message_window.geometry('240x125')
        entry_message = Text(message_window, fg='#DC3F53')
        entry_message.pack()
        k = 1.0
        for line in messages:
            entry_message.insert(k, line + "\n")
            k = k+1
            print(line)

    def add_word(word):
        messages = []
        global combo_list

        #проверка, что содержится в ячейке "слово"
        a_new_word = True
        is_a_word = True
        if combo.get() == "":
            is_a_word = False
            a_new_word = False
        else:
            for line in expressions:
                print("Сравниваем ", combo.get(), " c ", line[0])
                if combo.get() == line[0]:
                    a_new_word = False


        #проверка, что содержится в ячейке "перевод"
        a_new_translation = True
        is_a_translation = True
        if combo_t.get()=="":
            is_a_translation = False
            a_new_translation = False
        else:
            for line in translations:
                if combo_t.get() == line:
                    a_new_translation = False

        #проверка, что содержится в поле "Пример использования"
        a_new_usage = False
        no_usage = False
        if entr.get(1.0, END) != "\n":
            a_new_usage = True
        else:
            no_usage = True


        #проверка, что содержится в ячейке "автор"
        a_new_author = True
        is_an_author = True
        if combo_author.get() == "":
            is_an_author = False
            a_new_author = False
        else:
            for line in authors:
                if combo_author.get() == line[0]:
                    a_new_author = False

        #проверка, что содержится в ячейке "книга"
        a_new_title = True
        is_a_title = True
        if combo_title.get() == "":
            is_a_title = False
            a_new_title = False
        else:
            for line in titles:
                if combo_title.get() == line[0]:
                    a_new_title = False

        #проверка, что содержится в ячейке "глава"
        a_new_subtitle = True
        is_a_subtitle = True
        if combo_subtitle.get() == "":
            is_a_subtitle = False
            a_new_subtitle = False
        else:
            for line in subtitles:
                if combo_subtitle.get() == line[0]:
                    a_new_subtitle = False

        #проверка, что содержится в ячейке "ссылка"
        changing_the_link = False
        the_source_is_known = False
        the_old_link = False
        if (a_new_author == False) and (a_new_title == False) and (
            a_new_subtitle == False):
            the_source_is_known = True
            subtitle = session.query(Subtitle).filter_by(
                subtitle = combo_subtitle.get()).first()
            if(subtitle !=None):
                if (subtitle.link +'\n' !=entry_link.get("1.0", END)):
                    changing_the_link = True
                else:
                    the_old_link = True
                
        a_new_link = False
        no_link = False
        if entry_link.get(1.0, END) != "\n" and not the_old_link:
            a_new_link = True
        else:
            no_link = True


        #если в ячейке "ссылка" новая ссылка известного источника - вызываем
                #процедуру correct_a_source_link
        the_source_is_known = False
        if not changing_the_link:
            if (is_an_author and is_a_title and is_a_subtitle) and (
                not a_new_author) and (not a_new_title) and (
                    not a_new_subtitle) and the_old_link:
                the_source_is_known = True

        #проверка недостаточности данных про слово
        not_enough_usage_data = False
        if not is_a_word or not is_a_translation or (
           not a_new_word and not a_new_translation and not a_new_usage):
            not_enough_usage_data = True

        #проверка недостаточности данных про источник
        not_enough_source_data = False
        need_source_data = False
        if (not is_an_author) or (not is_a_title) or (
            not is_a_subtitle) or (entry_link.get(1.0, END) == "\n"):
            not_enough_source_data = True
            if entr.get(1.0, END) != "\n":
                need_source_data = True


        #если введено старое слово и недостаточно данных про слово:
        if (not a_new_word or a_new_word) and not_enough_usage_data and(
            is_a_word) and (not a_new_usage):
            messages.append("  Недостаточно данных:")
            if not is_a_translation or (not a_new_translation and not no_usage):
                messages.append("   - нет нового перевода")
            if not a_new_translation and no_usage:
                messages.append("   - нет нового примера")
                
        #если что-то введено про источник, но данных недостаточно
        if ((not a_new_author and is_an_author) and not_enough_source_data) or ((
            is_an_author or is_a_title or is_a_subtitle or not no_link) and (
                not_enough_source_data)) and not a_new_usage:
            messages.append("  Недостаточно данных:")
            if not is_an_author:
                messages.append("   - нет автора!")
            if not is_a_title:
                messages.append("   - нет книги!")
            if not is_a_subtitle:
                messages.append("   - нет главы!")
            if not a_new_link:
                messages.append("   - нет ссылки!")

        #если введен новый пример, но не хватает данных:
        if (a_new_usage) and (not_enough_source_data or not_enough_usage_data):
            messages.append("  Недостаточно данных:")
            if (not is_a_word):
                messages.append("   - нет нового слова")
            if (not is_a_translation):
                messages.append("   - нет нового перевода")
            if (not is_an_author):
                messages.append("   - нет нового автора")
            if (not is_a_title):
                messages.append("   - нет новой книги")
            if (not is_a_subtitle):
                messages.append("   - нет новой главы")
            if no_link:
                messages.append("   - нет новой ссылки")
                
        #Если вообще ничего не введено
        if (not is_a_word) and (not is_a_translation) and (
            not is_an_author) and (not is_a_title) and (
                not is_a_subtitle) and (not a_new_link) and no_usage:
            messages.append("  Недостаточно данных:")
            messages.append("   - не введено ничего!")

        global info
        info = ''
        if messages!=[]:
            error_message(messages)
        else:
            #print("А теперь будем вставлять данные!")
            if a_new_word:
                insert_a_word(combo.get().lstrip("{").rstrip("}"))
            if a_new_translation:
                insert_a_translation(combo.get().lstrip("{").rstrip("}"),
                                     combo_t.get().lstrip("{").rstrip("}"))
            if changing_the_link:
                id_subtitle = session.query(Subtitle.id).filter_by(
                    subtitle = combo_subtitle.get()).first()
                a_link = entry_link.get(1.0, END).rstrip("\n")
                correct_a_source_link(id_subtitle.id, a_link)
            if (a_new_author or a_new_title or a_new_subtitle):
                insert_a_source(combo_author.get(), combo_title.get(),
                                combo_subtitle.get(),
                                entry_link.get(1.0, END).rstrip("\n"))
            if (a_new_usage):
                usage_source = entr.get(1.0, END).rstrip("\n")
                insert_an_usage(combo.get().lstrip("{").rstrip("}"),
                                combo_t.get().lstrip("{").rstrip("}"),
                                usage_source, user_name,
                                combo_author.get(), combo_title.get(),
                                combo_subtitle.get()
                                )
            refresh_data()
            mb.showinfo("Ok!", info)

    def open_link(v):
        """процедура вставляет книги автора в соответствующий комбобокс после выбора автора"""
        entry_link.delete(1.0, END)
        subtitle = session.query(Subtitle).filter_by(
            subtitle = combo_subtitle.get()).first()
        entry_link.insert(1.0, subtitle.link)


    def open_subtitle(v):
        """процедура вставляет книги автора
в соответствующий комбобокс после выбора автора"""
        id_title = session.query(Title.id).filter_by(
            title = combo_title.get()).first()
        global subtitles
        subtitles = session.query(Subtitle.subtitle).filter_by(
            title = id_title.id)
        new_list = []
        for row in subtitles:
            new_list.append(row[0])
        combo_subtitle['value'] = tuple(new_list)
        combo_subtitle.save_value()
        entry_link.delete(1.0, END)
            

    def on_type_t(v):
        """при печати в комбобоксе с переводом выбираются подходящие слова """
        combo_t.on_type(v)
        keys = repr(v).split()
        if (keys[4] not in ["keycode=13", "keycode=39", "keycode=37"]):
            entr.delete(1.0, END)


    def on_type_subtitle(v):
        """при печати в комбобоксе с книгой выбираются подходящие слова """ 
        combo_subtitle.on_type(v)
        keys = repr(v).split()
        if (keys[4] not in ["keycode=13", "keycode=39", "keycode=37"]): 
            entry_link.delete(1.0, END)

    def open_translate(v):
        """ процедура вставляет варианты перевода выбранного слова
в соответствующий комбобокс после выбора значения в комбобоксе "Слово"

также очищает все прочие значения"""
        combo_t['values'] = ('','')
        combo_t.current(0)
        expression_id = session.query(Expression.id).filter_by(
            expression = combo.get().lstrip("{").rstrip("}"))
        translation = session.query(Expr_Translation.translation).filter_by(
            expression = expression_id)
        new_list = return_list(translation)
        combo_t['values'] = tuple(new_list)
        combo_t.save_value()


    def clear_subtitles():
        combo_subtitle['values'] = ('','')
        combo_subtitle.current(0)
        combo_subtitle['values'] = ('')
        combo_subtitle.save_value()
        global subtitles
        subtitles = []
        entry_link.delete(1.0, END)

    def open_books(v):
        """процедура вставляет книги автора
в соответствующий комбобокс после выбора автора"""
        id_author = session.query(Author).filter_by(
            author = combo_author.get()).first()
        combo_title['values'] = ('','')
        combo_title.current(0)
        global titles
        titles = session.query(Title.title).filter_by(
            author = id_author.id)
        combo_title['values'] = tuple(return_list(titles))
        combo_title.save_value()
        clear_subtitles()     

    
    window = Tk()
    window.geometry('430x430')
    window.title("Запись данных")

    mainmenu = Menu(window)
    window.config(menu = mainmenu)
    mainmenu.add_command(label = "Добавить язык", command = lambda:
                         add_language())

    lbl = Label(window, text="Введите слово:")
    lbl.place(x = 30, y = 8)
    
    combo = nc(window, width = 25)
    combo.place(x = 20, y = 30)

    session = connect_to_base()
    expressions = session.query(Expression.expression)
    combo['values'] = tuple(return_list(expressions))
    combo.save_value()

    combo.bind("<KeyRelease>", combo.on_type)
    combo.bind("<<ComboboxSelected>>", open_translate)
 

    lbl_t = Label(window, text = "Введите перевод слова:")
    lbl_t.place(x = 240, y = 8)

    combo_t = nc(window, width = 25)
    combo_t.place(x = 230, y = 30)
    combo_t.bind("<KeyRelease>", on_type_t)    


    lbl_l_source = Label(window, text="Язык источника:")
    lbl_l_source.place(x = 37, y = 55)

    combo_l_source = Combobox(window, state = "readonly")
    combo_l_source.place(x = 36, y = 77)
    languages = session.query(Language.language)
    combo_l_source['values'] = tuple(languages)
    combo_l_source.current(0)


    lbl_l_trans = Label(window, text="Язык перевода:")
    lbl_l_trans.place(x = 247, y = 55)

    combo_l_trans = Combobox(window, state = "readonly")
    combo_l_trans.place(x = 246, y = 77)
    combo_l_trans['values'] = tuple(languages)
    combo_l_trans.current(1)

    lbl_entr = Label(window, text="Пример использования:")
    lbl_entr.place(x = 30, y = 108)
    
    entr = Text(window, width = 50, height = 3)
    entr.place(x = 12, y = 132)

    lbl_author = Label(window, text = "Автор:")
    lbl_author.place(x = 30, y = 188)

    combo_author = nc(window, width = 25)
    combo_author.place(x = 20, y = 210)

    global authors
    authors = session.query(Author.author)
    combo_author['values'] = tuple(return_list(authors))
    combo_author.save_value()
    
    combo_author.bind("<<ComboboxSelected>>", open_books)
    combo_author.bind("<KeyRelease>", combo_author.on_type)
    


    lbl_title = Label(window, text = "Книга:")
    lbl_title.place(x = 30, y = 238)

    combo_title = nc(window, width = 25)
    combo_title.place(x = 20, y = 260)
    combo_title.bind("<<ComboboxSelected>>", open_subtitle)
    combo_title.bind("<KeyRelease>", combo_title.on_type)


    lbl_subtitle = Label(window, text = "Глава:")
    lbl_subtitle.place(x = 220, y = 238)

    combo_subtitle = nc(window, width = 30)
    combo_subtitle.place(x = 210, y = 260)
    combo_subtitle.bind("<<ComboboxSelected>>", open_link)
    combo_subtitle.bind("<KeyRelease>", on_type_subtitle)


    lbl_link = Label(window, text = "Ссылка на источник:")
    lbl_link.place(x=30, y = 290)

    entry_link = Text(window, width = 50, height = 3)
    entry_link.place(x = 12, y = 315)


    btn = Button(window, text="Добавить данные", command = lambda:
                 add_word(combo.get().lstrip("{").rstrip("}")))
    btn.place(x = 155, y = 385)
 

    window.mainloop()

if __name__ == '__main__':
    input_window('admin')

    
