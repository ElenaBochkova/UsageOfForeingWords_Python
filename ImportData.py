from DatabaseControl import *
import datetime

class ImportForeignData():
    def __init__(self, session, new_session):
        self.session = session
        self.new_session = new_session

    def test_it(self):
        try:
            expr1 = self.session.query(Expression.expression)
            expr2 = self.new_session.query(Expression.expression)
            for row in expr1:
                print(row[0])
            for row in expr2:
                print(row[0])
            return 'OK!'
        except:
            return 'Something gone wrong!'

    def find_expr_diff(self):
        self.expr_diff = []
        expr1 = self.session.query(Expression.expression)
        expr2 = self.new_session.query(Expression.expression)
        for row in expr2:
            if row not in expr1:
                self.expr_diff.append(row[0])
        for row in self.expr_diff:
            print(row)

    def return_language(self, lang1_id, lang2_id):
        lang = []
        lang.append(self.new_session.query(Language.language).filter_by(
            id = lang1_id).first())
        lang.append(self.new_session.query(Language.language).filter_by(
            id = lang2_id).first())
        langIds = []
        for langN in lang:
            language = self.session.query(Language.id).filter_by(
                language = langN[0]).first()
            if language == None:
                lang_new = Language()
                lang_new.language = langN[0]
                self.session.add(lang_new)
                self.session.commit()
                language = self.session.query(Language.id).filter_by(
                    language = langN[0]).first()
            langIds.append(language[0])
        return langIds[0], langIds[1]

    def return_user(self, old_user_id):
        old_user = self.new_session.query(User).filter_by(
            id = old_user_id).first()
        new_user = self.session.query(User).filter_by(
            login_name = old_user.login_name).first()
        if new_user == None:
            add_user = User()
            add_user.login_name = old_user.login_name
            add_user.user_score = 0
            add_user.user_start = old_user.user_start
            add_user.user_last_add = datetime.datetime.now()
            self.session.add(add_user)
            self.session.commit()
            new_user = self.session.query(User).filter_by(
                login_name = old_user.login_name).first()
        return new_user.id

    def return_usage_source(self, old_source_id):
        old_source = self.new_session.query(Source).filter_by(
            id = old_source_id).first()
        old_author = self.new_session.query(Author).filter_by(
            id = old_source.author).first()
        old_title = self.new_session.query(Title).filter_by(
            id = old_source.title).first()
        old_subtitle = self.new_session.query(Subtitle).filter_by(
            id = old_source.subtitle).first()
        new_author = self.session.query(Author).filter_by(
            author = old_author.author).first()
        if new_author == None:
            add_author = Author()
            add_author.author = old_author.author
            self.session.add(add_author)
            self.session.commit()
            new_author = self.session.query(Author).filter_by(
                author = old_author.author).first()
        new_title = self.session.query(Title).filter_by(
            author = new_author.id).filter_by(
                title = old_title.title).first()
        if new_title == None:
            add_title = Title()
            add_title.author = new_author.id
            add_title.title = old_title.title
            self.session.add(add_title)
            self.session.commit()
            new_title = self.session.query(Title).filter_by(
                author = new_author.id).filter_by(
                    title = old_title.title).first()
        new_subtitle = self.session.query(Subtitle).filter_by(
            title = new_title.id).filter_by(
                subtitle = old_subtitle.subtitle).first()
        if new_subtitle == None:
            add_subtitle = Subtitle()
            add_subtitle.title = new_title.id
            add_subtitle.subtitle = old_subtitle.subtitle
            add_subtitle.link = old_subtitle.link
            self.session.add(add_subtitle)
            self.session.commit()
            new_subtitle = self.session.query(Subtitle).filter_by(
                title = new_title.id).filter_by(
                    subtitle = old_subtitle.subtitle).first()
        new_source = self.session.query(Source).filter_by(
            author = new_author.id).filter_by(
                title = new_title.id).filter_by(
                    subtitle = new_subtitle.id).first()
        if new_source == None:
            add_source = Source()
            add_source.author = new_author.id
            add_source.title = new_title.id
            add_source.subtitle = new_subtitle.id
            self.session.add(add_source)
            self.session.commit()
            new_source = self.session.query(Source).filter_by(
                author = new_author.id).filter_by(
                    title = new_title.id).filter_by(
                        subtitle = new_subtitle.id).first()
        return new_source.id

    def test_lang(self):
        trans = self.new_session.query(Expr_Translation).filter_by(
            expression = 1).first()
        lang1 = trans.lang_from
        lang2 = trans.lang_to
        self.return_language(lang1, lang2)

    def fill_expr_diff(self):
        for row in self.expr_diff:
            #вставляем новое слово
            old_e_id = self.new_session.query(Expression.id).filter_by(
                expression = row).first()
            new_word = Expression()
            new_word.expression = row
            self.session.add(new_word)
            self.session.commit()
            #вставляем переводы этого слова
            new_e_id = self.session.query(Expression.id).filter_by(
                expression = row).first()
            new_trans = self.new_session.query(Expr_Translation).filter_by(
                expression = old_e_id[0])
            for r in new_trans:
                langId1, langId2 = self.return_language(r.lang_from,
                                                   r.lang_to)
                add_trans = Expr_Translation()
                add_trans.expression = new_e_id[0]
                add_trans.translation = r.translation
                add_trans.lang_from = langId1
                add_trans.lang_to = langId2
                self.session.add(add_trans)
                self.session.commit()
            #вставляем использование слова
                add_trans_id = self.session.query(
                    Expr_Translation.id).filter_by(
                        expression = new_e_id[0]).filter_by(
                            translation = add_trans.translation).first()
                old_expr_usage = self.new_session.query(
                    Expr_Usage).filter_by(
                        expression = old_e_id[0]).filter_by(
                            translation = r.id)
                for usage in old_expr_usage:
                    print(usage.expr_usage)
                    add_usage = Expr_Usage()
                    add_usage.usage_source = self.return_usage_source(
                        usage.usage_source)
                    add_usage.add_user = self.return_user(usage.add_user)
                    add_usage.expression = new_e_id[0]
                    add_usage.translation = add_trans_id[0]
                    add_usage.expr_usage = usage.expr_usage
                    user = self.session.query(User).filter_by(
                        id = add_usage.add_user).first()
                    user.user_score = user.user_score + 1
                    add_usage.date_time = datetime.datetime.now()
                    user.user_last_add = add_usage.date_time
                    self.session.add(add_usage)
                    self.session.add(user)
                    self.session.commit()
                    
                
                
                
            
