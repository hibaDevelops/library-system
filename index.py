from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb

from PyQt5.uic import loadUiType

# from Library import Ui_MainWindow


ui, _ = loadUiType('Library.ui')


# ui = Ui_MainWindow


class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handle_ui_changes()
        self.handle_buttons()

        self.show_categories()
        self.show_authors()
        self.show_publishers()

        self.show_category_dropdown()
        self.show_author_dropdown()
        self.show_publisher_dropdown()

    def handle_ui_changes(self):
        self.hide_themes()
        self.tabWidget.tabBar().setVisible(False)

    def handle_buttons(self):
        self.pushButton_5.clicked.connect(self.show_themes)
        self.pushButton_21.clicked.connect(self.hide_themes)
        self.pushButton.clicked.connect(self.open_day_to_day_tab)
        self.pushButton_2.clicked.connect(self.open_books_tab)
        self.pushButton_3.clicked.connect(self.open_users_tab)
        self.pushButton_4.clicked.connect(self.open_settings_tab)
        self.pushButton_7.clicked.connect(self.add_new_book)
        self.pushButton_14.clicked.connect(self.add_category)
        self.pushButton_15.clicked.connect(self.add_author)
        self.pushButton_16.clicked.connect(self.add_publisher)
        self.pushButton_9.clicked.connect(self.search_book)
        self.pushButton_8.clicked.connect(self.edit_book)
        self.pushButton_10.clicked.connect(self.delete_book)

    def show_themes(self):
        self.groupBox_3.show()

    def hide_themes(self):
        self.groupBox_3.hide()

    ##################
    ###### Tabs ######
    def open_day_to_day_tab(self):
        self.tabWidget.setCurrentIndex(0)

    def open_books_tab(self):
        self.tabWidget.setCurrentIndex(1)

    def open_users_tab(self):
        self.tabWidget.setCurrentIndex(2)

    def open_settings_tab(self):
        self.tabWidget.setCurrentIndex(3)

    ##################
    ###### Books ######
    def add_new_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_description = self.textEdit.toPlainText()
        book_code = self.lineEdit_3.text()
        category = self.comboBox_3.currentIndex()
        author = self.comboBox_4.currentIndex()
        publisher = self.comboBox_5.currentIndex()
        quantity = self.lineEdit_20.text()

        self.cur.execute('''
            INSERT INTO book (name, description, code, category, author, publisher, quantity)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (book_title, book_description, book_code, category, author, publisher, quantity))

        self.db.commit()
        self.statusBar().showMessage('Book Added!')

        self.lineEdit_2.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit_3.setText('')
        self.lineEdit_20.setText('')
        self.comboBox_3.setCurrentIndex(0)
        self.comboBox_4.setCurrentIndex(0)
        self.comboBox_5.setCurrentIndex(0)

    def search_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        name = self.lineEdit_5.text()

        sql = '''SELECT * FROM book where name = %s'''
        self.cur.execute(sql, [name])
        data = self.cur.fetchone()

        self.lineEdit_6.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_4.setText(data[3])
        self.comboBox_7.setCurrentIndex(data[4])
        self.comboBox_8.setCurrentIndex(data[5])
        self.comboBox_6.setCurrentIndex(data[6])
        self.lineEdit_21.setText(str(data[7]))

    def edit_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_6.text()
        book_description = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_4.text()
        category = self.comboBox_7.currentIndex()
        author = self.comboBox_8.currentIndex()
        publisher = self.comboBox_6.currentIndex()
        quantity = self.lineEdit_21.text()

        searched_title = self.lineEdit_5.text()

        self.cur.execute('''UPDATE book SET name = %s, description = %s, code = %s, category = %s, author = %s, publisher = %s, quantity = %s WHERE name = %s
            ''', (book_title, book_description, book_code, category, author, publisher, quantity, searched_title))

        self.db.commit()
        self.statusBar().showMessage('Book Updated!')

    def delete_book(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        searched_title = self.lineEdit_5.text()

        warning = QMessageBox.warning(self, 'Delete Book', 'Are you sure you want to delete this book?', QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes:
            self.cur.execute('''DELETE FROM book WHERE name=%s''', (searched_title,))
            self.db.commit()
            self.lineEdit_6.setText('')
            self.textEdit_2.setPlainText('')
            self.lineEdit_4.setText('')
            self.comboBox_7.setCurrentIndex(0)
            self.comboBox_8.setCurrentIndex(0)
            self.comboBox_6.setCurrentIndex(0)
            self.lineEdit_21.setText('')
            self.lineEdit_5.setText('')
            self.statusBar().showMessage('Book Deleted!')


    ##################
    ###### Users ######
    def add_new_user(self):
        pass

    def login(self):
        pass

    def edit_user(self):
        pass

    ##################
    ###### Settings ######
    def add_category(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        name = self.lineEdit_17.text()

        self.cur.execute('''
                         INSERT INTO category (name) VALUES (%s)
                         ''', (name,))

        self.db.commit()
        self.statusBar().showMessage('New Category Added')

        self.lineEdit_17.setText('')
        self.show_categories()
        self.show_category_dropdown()

    def show_categories(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT name FROM category''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

    def add_author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        name = self.lineEdit_18.text()

        self.cur.execute('''
                                 INSERT INTO authors (name) VALUES (%s)
                                 ''', (name,))

        self.db.commit()
        self.statusBar().showMessage('New Author Added')

        self.lineEdit_18.setText('')
        self.show_authors()
        self.show_author_dropdown()

    def show_authors(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT name FROM authors''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

    def add_publisher(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        name = self.lineEdit_19.text()

        self.cur.execute('''
                                         INSERT INTO publisher (name) VALUES (%s)
                                         ''', (name,))

        self.db.commit()
        self.statusBar().showMessage('New Publisher Added')

        self.lineEdit_19.setText('')
        self.show_publishers()
        self.show_publisher_dropdown()

    def show_publishers(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT name FROM publisher''')
        data = self.cur.fetchall()

        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

    ##################
    ###### Show Settings in UI ######
    def show_category_dropdown(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT name FROM category''')
        data = self.cur.fetchall()

        self.comboBox_3.clear()
        for category in data:
            self.comboBox_3.addItem(category[0])
            self.comboBox_7.addItem(category[0])

    def show_author_dropdown(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT name FROM authors''')
        data = self.cur.fetchall()

        self.comboBox_4.clear()
        for author in data:
            self.comboBox_4.addItem(author[0])
            self.comboBox_8.addItem(author[0])

    def show_publisher_dropdown(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='mySqlLearning96', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT name FROM publisher''')
        data = self.cur.fetchall()

        self.comboBox_5.clear()
        for author in data:
            self.comboBox_5.addItem(author[0])
            self.comboBox_6.addItem(author[0])


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    # ui = Ui_MainWindow()
    # ui.setupUi(MainWindow)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
