import sqlite3, datetime, os, sys
from PyQt5 import QtWidgets, QtGui
from mainwindow import Ui_mainWindow


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        create_db()
        self.ui.snapshot_btn.clicked.connect (lambda: capture_image(self))
        self.ui.supports_display_table.itemSelectionChanged.connect(lambda: enable_button(self))
        self.ui.supports_create_new_btn.clicked.connect(lambda: self.ui.supports_sub_page.setCurrentIndex(int(1)))
        self.ui.main_mps_btn.clicked.connect(lambda: choose_mps(self))
        self.ui.main_mes_btn.clicked.connect(lambda: choose_mes(self))
        self.ui.main_admin_btn.clicked.connect(lambda: choose_admin(self))
        self.ui.supports_modify_existing_btn.clicked.connect(lambda: modify_support(self))
        self.ui.supports_mod_save_btn.clicked.connect(lambda: modify_save_support(self))
        self.ui.supports_change_status_btn.clicked.connect (lambda: update_status(self))
        self.ui.supports_stat_update_btn.clicked.connect (lambda: update_save_status(self))
        self.ui.supports_openfile_btn.clicked.connect(lambda: insert_image(self))
        self.ui.supports_create_btn.clicked.connect(lambda: input_validator(self))
        self.ui.supports_cancel_btn.clicked.connect(lambda: cancel_menu(self))
        self.ui.supports_mod_cancel_btn.clicked.connect(lambda: cancel_menu(self))
        self.ui.supports_stat_cancel_btn.clicked.connect(lambda: cancel_menu(self))
        self.ui.supports_refresh_btn.clicked.connect(lambda: load_data(self))
        self.ui.actionSupports_page.triggered.connect(lambda: self.ui.stackedWidget.setCurrentIndex(int(1)))
        self.ui.actionAdmin_page.triggered.connect(
            lambda: self.ui.stackedWidget.setCurrentIndex(int(0)))
        self.ui.supports_display_table.horizontalHeader().setVisible(True)
        self.ui.supports_display_table.setSelectionBehavior(self.ui.supports_display_table.SelectRows)
        self.ui.supports_display_table.selectionMode()
        self.ui.supports_display_table.setEditTriggers(self.ui.supports_display_table.NoEditTriggers)
        load_data(self)


class globvars:
    row_no = 0
    choice = "MPS"
    file_name = " "


def choose_mps(self):
    globvars.choice="MPS"
    print("mps_activated")
    load_data(self)
    print(globvars.choice)


def choose_mes(self):
    globvars.choice="MES"
    print("mes_activated")
    print(globvars.choice)
    load_data(self)


def choose_admin(self):
    globvars.choice="ADMIN"
    print("admin_activated")
    print(globvars.choice)

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
            ApprovedDate, RejectedBy, RejectedDate, RejectionReason FROM {}""".format(globvars.choice)
    result = conn.execute(query)
    self.ui.supports_display_table.setRowCount(0)
    for row_number, row_data in enumerate(result):
        self.ui.supports_display_table.insertRow(row_number)
        for column_number, data in enumerate(row_data):
            self.ui.supports_display_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
    conn.close()


def insert_image(self):
    fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')
    globvars.file_name = str(fname[0])

def capture_image(self):
    snapfilename = "HelloSKR.jpg"
    p = QtWidgets.QWidget.grab()
    p.save(snapfilename, 'jpg')
    self.ui.display_image_lab.setPixmap(p)  # just for fun :)


def cancel_menu(self):
    self.ui.supports_unit_line_edit.clear()
    self.ui.supports_area_line_edit.clear()
    self.ui.supports_cwp_line_edit.clear()
    self.ui.supports_desc_line_edit.clear()
    self.ui.supports_mod_unit_line_edit.clear()
    self.ui.supports_mod_area_line_edit.clear()
    self.ui.supports_mod_cwp_line_edit.clear()
    self.ui.supports_mod_desc_line_edit.clear()
    self.ui.supports_display_table.clearSelection()
    self.ui.supports_modify_existing_btn.setEnabled(False)
    self.ui.supports_change_status_btn.setEnabled(False)
    self.ui.supports_sub_page.setCurrentIndex(int(0))
    globvars.file_name = " "


def time_stamp():
    _timestamp = ('{:%d-%b-%Y %H:%M:%S}'.format(datetime.datetime.now()))
    return _timestamp


def input_validator(self):
    _unit = self.ui.supports_unit_line_edit.text()
    _area = self.ui.supports_area_line_edit.text()
    _cwp = self.ui.supports_cwp_line_edit.text()
    _desc = self.ui.supports_desc_line_edit.text()
    file_name = globvars.file_name
    if not bool(_unit.strip()) or not bool(_area.strip()) or not bool(_cwp.strip()) or not bool(
            _desc.strip()) or not bool(file_name.strip()):
        QtWidgets.QMessageBox.information(w, "Message", "Invalid Unit or Area or CWP or Description or Snapshot")
    else:
        create_supp(self)


def create_supp(self):
    _unit = self.ui.supports_unit_line_edit.text()
    _area = self.ui.supports_area_line_edit.text()
    _cwp = self.ui.supports_cwp_line_edit.text()
    _desc = self.ui.supports_desc_line_edit.text()
    _imagename = globvars.file_name
    if _imagename == " ":
        _imagename = None
    else:
        f1 = open(_imagename, 'rb')
        data = f1.read()
        _imagename = sqlite3.Binary(data)
    conn = sqlite3.connect('msm.db')
    c = conn.cursor()
    c.execute("""INSERT INTO {}
              (Unit, Area, CWP, Description, SuppStatus, RequestedBy,
              RequestedDate, SnapShot, ModifiedBy, ModifiedDate,
              ImplementedBy, ImplementedDate, ApprovedBy, ApprovedDate,
              RejectedBy, RejectedDate, RejectionReason)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);""".format(globvars.choice),
              (_unit, _area, _cwp, _desc, "Created", os.getlogin(), time_stamp(),
               _imagename, "", "", "", "", "", "", "", "",""))
    pr = (c.lastrowid)
    c.execute("UPDATE {} SET SuppNo=? WHERE SLNo=?".format(globvars.choice), [globvars.choice + " - " + str(pr), pr])
    conn.commit()
    QtWidgets.QMessageBox.information(w, "Message", "New " + globvars.choice + " - " + str(pr) + " Created")
    c.close()
    conn.close()
    QtWidgets.QMessageBox.question(w, "Message", "Do you want to send notification?")
    load_data(self)
    cancel_menu(self)


def enable_button(self):
    self.ui.supports_modify_existing_btn.setEnabled(True)
    self.ui.supports_change_status_btn.setEnabled(True)



def modify_support(self):
    globvars.row_no = self.ui.supports_display_table.currentRow()+1
    self.ui.supports_sub_page.setCurrentIndex(int(2))
    conn = sqlite3.connect('msm.db')
    c = conn.cursor()
    c.execute("SELECT Unit, Area, CWP, Description FROM {} WHERE ROWID=?".format(globvars.choice),(globvars.row_no,))
    result = c.fetchone()
    self.ui.supports_mod_unit_line_edit.setText(result[0])
    self.ui.supports_mod_area_line_edit.setText(result[1])
    self.ui.supports_mod_cwp_line_edit.setText(result[2])
    self.ui.supports_mod_desc_line_edit.setText(result[3])
    c.close()
    conn.close()

def modify_save_support(self):
    conn = sqlite3.connect('msm.db')
    c = conn.cursor()
    _unit = self.ui.supports_mod_unit_line_edit.text()
    _area = self.ui.supports_mod_area_line_edit.text()
    _cwp = self.ui.supports_mod_cwp_line_edit.text()
    _desc = self.ui.supports_mod_desc_line_edit.text()
    c.execute("""UPDATE {} SET Unit=?, Area=? , CWP=?, Description=?,
                SuppStatus="Modified", ModifiedBy=?, ModifiedDate=?
               WHERE ROWID=?""".format(globvars.choice),
              [_unit, _area, _cwp, _desc, os.getlogin(), time_stamp(), globvars.row_no])
    conn.commit()
    c.close()
    conn.close()
    load_data(self)
    cancel_menu(self)


def update_status(self):
    globvars.row_no = self.ui.supports_display_table.currentRow() + 1
    # cb_letter.model().item(2).setEnabled(False)
    conn = sqlite3.connect('msm.db')
    c = conn.cursor()
    c.execute("SELECT SuppStatus FROM {} WHERE ROWID=?".format(globvars.choice), (globvars.row_no,))
    result = c.fetchone()
    if not result[0] in ("Implemented", "Approved", "Rejected"):
        self.ui.supports_stat_combo_btn.setCurrentIndex(int(0))
    else:
        self.ui.supports_stat_combo_btn.setCurrentText(result[0])
    c.close()
    conn.close()
    self.ui.supports_sub_page.setCurrentIndex(int(3))
    self.ui.supports_stat_combo_btn.insertSeparator(int(1))


def update_save_status(self):
    combo_value = self.ui.supports_stat_combo_btn.currentText()
    conn = sqlite3.connect('msm.db')
    c = conn.cursor()
    c.execute("""UPDATE {} SET SuppStatus=?, {}By=?, {}Date=?
                WHERE ROWID=?""".format(globvars.choice, combo_value, combo_value),
              [combo_value, os.getlogin(), time_stamp(), globvars.row_no])
    conn.commit()
    c.close()
    conn.close()
    load_data(self)
    cancel_menu(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
