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
