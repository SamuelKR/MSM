import sqlite3, datetime, os, sys
from PyQt5 import QtWidgets, QtGui
from mainwindow import Ui_mainWindow


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        create_db()
        self.ui.create_new.clicked.connect(lambda: self.ui.mps_sub_page.setCurrentIndex(int(0)))
        self.ui.mps_openfile_button.clicked.connect(lambda: insert_image(self))
        self.ui.mps_create_button.clicked.connect(lambda: input_validator(self))
        self.ui.mps_cancel_button.clicked.connect(lambda: cancel_menu(self))
        self.ui.mps_btn_refresh.clicked.connect(lambda: load_data(self))
        self.ui.actionMPS_Misc_Pipe_Supports.triggered.connect(lambda: self.ui.stackedWidget.setCurrentIndex(int(1)))
        self.ui.actionMES_Misc_Electrical_Supports.triggered.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(int(2)))
        self.ui.main_menu_mps.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(int(1)))
        self.ui.main_menu_mes.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(int(2)))
        self.ui.mes_display_support.horizontalHeader().setVisible(True)
        self.ui.mps_display_support.horizontalHeader().setVisible(True)
        self.ui.mps_display_support.setSelectionBehavior(self.ui.mps_display_support.SelectRows)
        self.ui.mps_display_support.setEditTriggers(self.ui.mps_display_support.NoEditTriggers)
        load_data(self)


def create_db():
    conn = sqlite3.connect('msm.db')
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS MPS (
        SLNo integer PRIMARY KEY AUTOINCREMENT,
        SuppNo TEXT,
        Unit TEXT,
        Area TEXT,
        CWP TEXT,
        Description TEXT,
        SuppStatus TEXT,
        RequestedBy TEXT,
        RequestedDate TEXT,
        ModifiedBy TEXT,
        ModifiedDate TEXT,
        ImplementedBy TEXT,
        ImplementedDate TEXT,
        ApprovedBy TEXT,
        ApprovedDate TEXT,
        RejectedBy TEXT,
        RejectedDate TEXT,
        RejectionReason TEXT,
        SnapShot BLOB
    );''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS MES (
        SLNo integer PRIMARY KEY AUTOINCREMENT,
        SuppNo TEXT,
        Unit TEXT,
        Area TEXT,
        CWP TEXT,
        Description TEXT,
        SuppStatus TEXT,
        RequestedBy TEXT,
        RequestedDate TEXT,
        ModifiedBy TEXT,
        ModifiedDate TEXT,
        ImplementedBy TEXT,
        ImplementedDate TEXT,
        ApprovedBy TEXT,
        ApprovedDate TEXT,
        RejectedBy TEXT,
        RejectedDate TEXT,
        RejectionReason TEXT,
        SnapShot BLOB
    );''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS STRUC_USERS (
        SLNo integer PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Role TEXT
    );''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS PIPING_USERS (
        SLNo integer PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Role TEXT
    );''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS ELEC_USERS (
        SLNo integer PRIMARY KEY AUTOINCREMENT,
        Name TEXT,
        Role TEXT
    );''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS PROJ_INFO (
        SLNo integer PRIMARY KEY AUTOINCREMENT,
        ProjectName TEXT,
        ProjectCode TEXT
    );''')
    conn.commit()
    c.close()
    conn.close()


def load_data(self):
    conn = sqlite3.connect('msm.db')
    query = """SELECT SuppNo, Unit, Area, CWP, Description,
            SuppStatus, RequestedBy, RequestedDate, ModifiedBy,
            ModifiedDate, ImplementedBy, ImplementedDate, ApprovedBy,
            ApprovedDate, RejectedBy, RejectedDate, RejectionReason FROM MPS"""
    result = conn.execute(query)
    self.ui.mps_display_support.setRowCount(0)
    for row_number, row_data in enumerate(result):
        self.ui.mps_display_support.insertRow(row_number)
        for column_number, data in enumerate(row_data):
            self.ui.mps_display_support.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    conn.close()


def insert_image(self):
    fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
    file_name = open("filename", 'w')
    file_name.write(str(fname[0]))
    file_name.close()


def cancel_menu(self):
    self.ui.mps_unit_line_edit.clear()
    self.ui.mps_area_line_edit.clear()
    self.ui.mps_cwp_line_edit.clear()
    self.ui.mps_desc_line_edit.clear()
    file_name = open("filename", 'w')
    file_name.write(" ")
    file_name.close()
    self.ui.mps_cancel_button.clicked.connect(lambda: self.ui.mps_sub_page.setCurrentIndex(int(1)))


def time_stamp():
    _timestamp = ('{:%d-%b-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    return _timestamp


def input_validator(self):
    _unit = self.ui.mps_unit_line_edit.text()
    _area = self.ui.mps_area_line_edit.text()
    _cwp = self.ui.mps_cwp_line_edit.text()
    _desc = self.ui.mps_desc_line_edit.text()
    file_name = open("filename", 'r')
    file_read = file_name.read()
    file_name.close()
    if not bool(_unit.strip()) or not bool(_area.strip()) or not bool(_cwp.strip()) or not bool(
            _desc.strip()) or not bool(file_read.strip()):
        QtWidgets.QMessageBox.information(w, "Message", "Invalid Unit or Area or CWP or Description or Snapshot")
    else:
        create_supp(self)


def create_supp(self):
    _unit = self.ui.mps_unit_line_edit.text()
    _area = self.ui.mps_area_line_edit.text()
    _cwp = self.ui.mps_cwp_line_edit.text()
    _desc = self.ui.mps_desc_line_edit.text()
    _imagename_file = open("filename", 'r')
    _imagename = _imagename_file.read()
    _imagename_file.close()
    if _imagename == " ":
        _imagename = None
    else:
        f1 = open(_imagename, 'rb')
        data = f1.read()
        _imagename = sqlite3.Binary(data)

    conn = sqlite3.connect('msm.db')
    c = conn.cursor()
    c.execute("""INSERT INTO MPS
              (Unit, Area, CWP, Description, SuppStatus, RequestedBy, RequestedDate, SnapShot, ModifiedBy,
              ModifiedDate, ImplementedBy, ImplementedDate, ApprovedBy, ApprovedDate, RejectedBy, RejectedDate, RejectionReason)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""", (
        _unit, _area, _cwp, _desc, "Created", os.getlogin(), time_stamp(), _imagename, "", "", "", "", "", "", "", "",""))
    pr = (c.lastrowid)
    c.execute("UPDATE MPS SET SuppNo=? WHERE SLNo=?", ["MPS - " + str(pr), pr])
    conn.commit()
    QtWidgets.QMessageBox.information(w, "Message", "New MPS" + str(pr) + "Created")
    c.close()
    conn.close()
    QtWidgets.QMessageBox.question(w, "Message", "Do you want to send notification?")
    load_data(self)
    cancel_menu(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
