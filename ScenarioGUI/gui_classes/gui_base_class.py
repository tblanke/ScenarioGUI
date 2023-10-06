"""
This document contains some base functionality for the GUI.
It contains a function to reformat the graphs to a layout for the gui,
and it contains the main class that creates the framework for the GUI (top bar etc.)
"""
from platform import system

import PySide6.QtCore as QtC  # type: ignore
import PySide6.QtGui as QtG  # type: ignore
import PySide6.QtWidgets as QtW  # type: ignore

import ScenarioGUI.global_settings as globs
from ScenarioGUI.utils import set_default_font
from ScenarioGUI.gui_classes.status_bar_logger import StatusBar


class BaseUI:
    """
    This class contains the framework of the GUI, with the top bar,
    the scenario/run/ ... buttons and the shortcuts.
    """

    menu_language: QtW.QMenu
    status_bar: StatusBar
    tool_bar: QtW.QToolBar
    menu_scenario: QtW.QMenu
    menu_settings: QtW.QMenu
    menu_calculation: QtW.QMenu
    push_button_cancel: QtW.QPushButton
    menu_file: QtW.QMenu
    push_button_start_multiple: QtW.QPushButton
    push_button_start_single: QtW.QPushButton
    progress_bar: QtW.QProgressBar
    horizontal_layout_start_buttons: QtW.QHBoxLayout
    label_status: QtW.QLabel
    horizontal_layout_progress_bar: QtW.QHBoxLayout
    stacked_widget: QtW.QStackedWidget
    vertical_layout_main: QtW.QVBoxLayout
    vertical_layout_menu: QtW.QVBoxLayout
    list_widget_scenario: QtW.QListWidget
    button_rename_scenario: QtW.QPushButton
    push_button_save_scenario: QtW.QPushButton
    vertical_layout_scenario: QtW.QVBoxLayout
    horizontal_layout_main: QtW.QHBoxLayout
    central_widget: QtW.QWidget
    push_button_delete_scenario: QtW.QPushButton
    action_start_single: QtG.QAction
    action_rename_scenario: QtG.QAction
    action_save_as: QtG.QAction
    action_delete_scenario: QtG.QAction
    action_add_scenario: QtG.QAction
    action_update_scenario: QtG.QAction
    menubar: QtW.QMenuBar
    push_button_add_scenario: QtW.QPushButton
    action_start_multiple: QtG.QAction
    action_open: QtG.QAction
    action_open_add: QtG.QAction
    action_save: QtG.QAction
    action_new: QtG.QAction
    frame_progress_bar: QtW.QFrame
    status_bar_progress_bar: QtW.QStatusBar

    def setup_ui(self, window: QtW.QMainWindow, screen_size: QtC.QSize, gui_name: str = "ScenarioGUI"):
        if not window.objectName():
            window.setObjectName(gui_name)
        window.resize(screen_size)
        size_policy = QtW.QSizePolicy(QtW.QSizePolicy.Preferred, QtW.QSizePolicy.Preferred)  # type: ignore
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(window.sizePolicy().hasHeightForWidth())
        window.setSizePolicy(size_policy)
        window.setMaximumSize(QtC.QSize(16777215, 16777215))
        font = QtG.QFont()
        font.setFamily(globs.FONT)
        font.setPointSize(globs.FONT_SIZE)
        font.setBold(False)
        font.setItalic(False)
        window.setFont(font)
        icon = QtG.QIcon()
        icon.addFile(f"{globs.FOLDER}/icons/{globs.ICON_NAME}", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        window.setWindowIcon(icon)
        window.setStyleSheet(
            f"*{'{'}color: {globs.WHITE};background-color: {globs.DARK};selection-background-color: {globs.LIGHT};"
            f"alternate-background-color: {globs.LIGHT};{'}'}\n"
            f"QPushButton{'{'}border: 3px solid {globs.LIGHT};border-radius: 5px;color:{globs.WHITE};gridline-color:{globs.LIGHT};"
            f"background-color:{globs.LIGHT};font-weight:700;{'}'}"
            f"QPushButton:hover{'{'}background-color: {globs.DARK};{'}'}\n"
            f"QPushButton:disabled{'{'}border: 3px solid {globs.GREY};border-radius: 5px;color: {globs.WHITE};gridline-color: {globs.GREY};"
            f"background-color: {globs.GREY};{'}'}\n"
            f"QPushButton:disabled:hover{'{'}background-color: {globs.DARK};{'}'}\n"
            f"QComboBox{'{'}border: 1px solid {globs.WHITE};border-bottom-left-radius: 0px;border-bottom-right-radius: 0px;{'}'}\n"
            f"QSpinBox{'{'}selection-color: {globs.WHITE};selection-background-color: {globs.LIGHT};border: 1px solid {globs.WHITE};{'}'}\n"
            f"QLineEdit{'{'}border: 3px solid {globs.LIGHT};border-radius: 5px;color: {globs.WHITE};gridline-color: {globs.LIGHT};background-color: "
            f"{globs.LIGHT};selection-background-color: {globs.LIGHT_SELECT};{'}'}\n"
            f"QLineEdit:hover{'{'}background-color: {globs.DARK};{'}'}"
            f"QTabBar::tab{'{'}background-color: {globs.DARK};padding-top:5px;padding-bottom:5px;padding-left:5px;padding-right:5px;color: {globs.WHITE};{'}'}"
            f"QTabBar::tab:selected, QTabBar::tab:hover{'{'}background-color: {globs.LIGHT};{'}'}"
            f"QTabBar::tab:selected{'{'}background-color: {globs.LIGHT};{'}'}"
            f"QTabBar::tab:!selected{'{'}background-color:  {globs.DARK};{'}'}"
            f"QTabWidget::pane{'{'}border: 1px solid {globs.WHITE};{'}'}"
            f"QTabWidget::tab-bar{'{'}left: 5px;{'}'}"
            f"QToolTip{'{'}color:{globs.WHITE};background-color:{globs.BLACK}; border: 2px solid {globs.LIGHT};font: {globs.FONT_SIZE}pt {globs.FONT};{'}'}"
        )
        self.action_new = QtG.QAction(window)
        self.action_new.setObjectName("actionNew")
        self.action_new.setCheckable(False)
        self.action_new.setChecked(False)
        self.action_new.setEnabled(True)
        icon1 = QtG.QIcon()
        icon1.addFile(f"{globs.FOLDER}/icons/New.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        icon1.addFile(f"{globs.FOLDER}/icons/New_Inv.svg", QtC.QSize(), QtG.QIcon.Active, QtG.QIcon.Off)  # type: ignore
        self.action_new.setIcon(icon1)
        self.action_save = QtG.QAction(window)
        self.action_save.setObjectName("actionSave")
        self.action_save.setEnabled(True)
        icon2 = QtG.QIcon()
        icon2.addFile(f"{globs.FOLDER}/icons/Save.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        icon2.addFile(f"{globs.FOLDER}/icons/Save_Inv.svg", QtC.QSize(), QtG.QIcon.Active, QtG.QIcon.Off)  # type: ignore
        self.action_save.setIcon(icon2)
        self.action_open = QtG.QAction(window)
        self.action_open.setObjectName("actionOpen")
        self.action_open.setEnabled(True)
        icon3 = QtG.QIcon()
        icon3.addFile(f"{globs.FOLDER}/icons/Open.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        icon3.addFile(f"{globs.FOLDER}/icons/Open_Inv.svg", QtC.QSize(), QtG.QIcon.Active, QtG.QIcon.Off)  # type: ignore
        self.action_open.setIcon(icon3)
        self.action_open_add = QtG.QAction(window)
        self.action_open_add.setObjectName("action_open_add")
        self.action_open_add.setEnabled(True)
        icon_open_add = QtG.QIcon()
        icon_open_add.addFile(f"{globs.FOLDER}/icons/Open_Add.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        icon_open_add.addFile(f"{globs.FOLDER}/icons/Open_Add_Inv.svg", QtC.QSize(), QtG.QIcon.Active, QtG.QIcon.Off)  # type: ignore
        self.action_open_add.setIcon(icon_open_add)
        self.action_start_multiple = QtG.QAction(window)
        self.action_start_multiple.setObjectName("action_start_multiple")
        self.action_start_multiple.setEnabled(True)
        icon4 = QtG.QIcon()
        icon4.addFile(
            f"{globs.FOLDER}/icons/Start_multiple_inv.svg",
            QtC.QSize(),
            QtG.QIcon.Normal,  # type: ignore
            QtG.QIcon.Off,  # type: ignore
        )
        icon4.addFile(
            f"{globs.FOLDER}/icons/Start_multiple.svg",
            QtC.QSize(),
            QtG.QIcon.Active,  # type: ignore
            QtG.QIcon.Off,  # type: ignore
        )
        self.action_start_multiple.setIcon(icon4)
        self.action_update_scenario = QtG.QAction(window)
        self.action_update_scenario.setObjectName("actionUpdate_Scenario")
        icon7 = QtG.QIcon()
        icon7.addFile(
            f"{globs.FOLDER}/icons/Update_Inv.svg",
            QtC.QSize(),
            QtG.QIcon.Normal,  # type: ignore
            QtG.QIcon.Off,  # type: ignore
        )
        icon7.addFile(f"{globs.FOLDER}/icons/Update.svg", QtC.QSize(), QtG.QIcon.Active, QtG.QIcon.Off)  # type: ignore
        self.action_update_scenario.setIcon(icon7)
        self.action_add_scenario = QtG.QAction(window)
        self.action_add_scenario.setObjectName("actionAdd_Scenario")
        icon8 = QtG.QIcon()
        icon8.addFile(f"{globs.FOLDER}/icons/Add_Inv.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        icon8.addFile(f"{globs.FOLDER}/icons/Add.svg", QtC.QSize(), QtG.QIcon.Active, QtG.QIcon.Off)  # type: ignore
        self.action_add_scenario.setIcon(icon8)
        self.action_delete_scenario = QtG.QAction(window)
        self.action_delete_scenario.setObjectName("actionDelete_scenario")
        icon9 = QtG.QIcon()
        icon9.addFile(
            f"{globs.FOLDER}/icons/Delete_Inv.svg",
            QtC.QSize(),
            QtG.QIcon.Normal,  # type: ignore
            QtG.QIcon.Off,  # type: ignore
        )
        icon9.addFile(f"{globs.FOLDER}/icons/Delete.svg", QtC.QSize(), QtG.QIcon.Active, QtG.QIcon.Off)  # type: ignore
        self.action_delete_scenario.setIcon(icon9)
        self.action_save_as = QtG.QAction(window)
        self.action_save_as.setObjectName("actionSave_As")
        icon10 = QtG.QIcon()
        icon10.addFile(f"{globs.FOLDER}/icons/SaveAs.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        icon10.addFile(
            f"{globs.FOLDER}/icons/Save_As_Inv.svg",
            QtC.QSize(),
            QtG.QIcon.Active,  # type: ignore
            QtG.QIcon.Off,  # type: ignore
        )
        self.action_save_as.setIcon(icon10)
        self.action_rename_scenario = QtG.QAction(window)
        self.action_rename_scenario.setObjectName("actionRename_scenario")
        icon14 = QtG.QIcon()
        icon14.addFile(
            f"{globs.FOLDER}/icons/Rename_Inv.svg",
            QtC.QSize(),
            QtG.QIcon.Normal,  # type: ignore
            QtG.QIcon.Off,  # type: ignore
        )
        icon14.addFile(f"{globs.FOLDER}/icons/Rename.svg", QtC.QSize(), QtG.QIcon.Active, QtG.QIcon.Off)  # type: ignore
        self.action_rename_scenario.setIcon(icon14)
        self.action_start_single = QtG.QAction(window)
        self.action_start_single.setObjectName("action_start_single")
        icon15 = QtG.QIcon()
        icon15.addFile(
            f"{globs.FOLDER}/icons/Start_inv.svg",
            QtC.QSize(),
            QtG.QIcon.Normal,  # type: ignore
            QtG.QIcon.Off,  # type: ignore
        )
        icon15.addFile(f"{globs.FOLDER}/icons/Start.svg", QtC.QSize(), QtG.QIcon.Active, QtG.QIcon.Off)  # type: ignore
        self.action_start_single.setIcon(icon15)
        self.central_widget = QtW.QWidget(window)
        self.central_widget.setObjectName("central_widget")
        self.horizontal_layout_main = QtW.QHBoxLayout(self.central_widget)
        self.horizontal_layout_main.setObjectName("horizontalLayout_23")
        self.vertical_layout_scenario = QtW.QVBoxLayout()
        self.vertical_layout_scenario.setObjectName("verticalLayout_scenario")
        self.push_button_save_scenario = QtW.QPushButton(self.central_widget)
        self.push_button_save_scenario.setObjectName("pushButton_SaveScenario")
        size_policy1 = QtW.QSizePolicy(QtW.QSizePolicy.Minimum, QtW.QSizePolicy.Minimum)  # type: ignore
        size_policy1.setHorizontalStretch(0)
        size_policy1.setVerticalStretch(0)
        size_policy1.setHeightForWidth(self.push_button_save_scenario.sizePolicy().hasHeightForWidth())
        self.push_button_save_scenario.setSizePolicy(size_policy1)
        self.push_button_save_scenario.setMinimumSize(QtC.QSize(180, 30))
        self.push_button_save_scenario.setMaximumHeight(30)
        self.push_button_save_scenario.setStyleSheet("text-align:left;")
        icon18 = QtG.QIcon()
        icon18.addFile(f"{globs.FOLDER}/icons/Update.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        self.push_button_save_scenario.setIcon(icon18)
        self.push_button_save_scenario.setIconSize(QtC.QSize(20, 20))

        self.vertical_layout_scenario.addWidget(self.push_button_save_scenario)

        self.push_button_add_scenario = QtW.QPushButton(self.central_widget)
        self.push_button_add_scenario.setObjectName("pushButton_AddScenario")
        self.push_button_add_scenario.setMinimumSize(QtC.QSize(180, 30))
        self.push_button_add_scenario.setMaximumHeight(30)
        self.push_button_add_scenario.setStyleSheet("text-align:left;")
        icon19 = QtG.QIcon()
        icon19.addFile(f"{globs.FOLDER}/icons/Add.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        self.push_button_add_scenario.setIcon(icon19)
        self.push_button_add_scenario.setIconSize(QtC.QSize(20, 20))

        self.vertical_layout_scenario.addWidget(self.push_button_add_scenario)

        self.push_button_delete_scenario = QtW.QPushButton(self.central_widget)
        self.push_button_delete_scenario.setObjectName("pushButton_DeleteScenario")
        self.push_button_delete_scenario.setMinimumSize(QtC.QSize(180, 30))
        self.push_button_delete_scenario.setMaximumHeight(30)
        self.push_button_delete_scenario.setStyleSheet("text-align:left;")
        icon20 = QtG.QIcon()
        icon20.addFile(f"{globs.FOLDER}/icons/Delete.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        self.push_button_delete_scenario.setIcon(icon20)
        self.push_button_delete_scenario.setIconSize(QtC.QSize(20, 20))

        self.vertical_layout_scenario.addWidget(self.push_button_delete_scenario)

        self.button_rename_scenario = QtW.QPushButton(self.central_widget)
        self.button_rename_scenario.setObjectName("button_rename_scenario")
        self.button_rename_scenario.setMinimumSize(QtC.QSize(180, 30))
        self.button_rename_scenario.setMaximumHeight(30)
        self.button_rename_scenario.setStyleSheet("text-align:left;")
        icon21 = QtG.QIcon()
        icon21.addFile(f"{globs.FOLDER}/icons/Rename.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        self.button_rename_scenario.setIcon(icon21)
        self.button_rename_scenario.setIconSize(QtC.QSize(20, 20))

        self.vertical_layout_scenario.addWidget(self.button_rename_scenario)

        self.list_widget_scenario = QtW.QListWidget(self.central_widget)
        QtW.QListWidgetItem(self.list_widget_scenario)
        self.list_widget_scenario.setObjectName("list_widget_scenario")
        size_policy.setHeightForWidth(self.list_widget_scenario.sizePolicy().hasHeightForWidth())
        self.list_widget_scenario.setSizePolicy(size_policy)
        self.list_widget_scenario.setMaximumSize(QtC.QSize(16666711, 16666711))
        self.list_widget_scenario.setStyleSheet(
            f"*{'{'}border: 1px solid {globs.WHITE};{'}'}\n"
            "QListWidget{outline: 0;}\n"
            f"QListWidget::item:selected{'{'}background:{globs.LIGHT};color: {globs.WHITE};border: 0px solid {globs.WHITE};{'}'}\n"
            f"QListWidget::item:hover{'{'}border: 1px solid {globs.WHITE};color: {globs.WHITE};{'}'}"
            f"QListWidget:disabled{'{'}background-color: {globs.GREY};{'}'}"
        )
        self.list_widget_scenario.setSizeAdjustPolicy(QtW.QAbstractScrollArea.AdjustToContents)  # type: ignore
        self.list_widget_scenario.setAutoScrollMargin(10)
        self.list_widget_scenario.setEditTriggers(
            QtW.QAbstractItemView.DoubleClicked | QtW.QAbstractItemView.EditKeyPressed | QtW.QAbstractItemView.SelectedClicked  # type: ignore
        )
        self.list_widget_scenario.setDragDropMode(QtW.QAbstractItemView.DragDrop)  # type: ignore
        self.list_widget_scenario.setDefaultDropAction(QtC.Qt.TargetMoveAction)  # type: ignore
        self.list_widget_scenario.setSelectionBehavior(QtW.QAbstractItemView.SelectItems)  # type: ignore
        self.list_widget_scenario.setSelectionRectVisible(False)

        self.vertical_layout_scenario.addWidget(self.list_widget_scenario)

        self.horizontal_layout_main.addLayout(self.vertical_layout_scenario)

        self.vertical_layout_menu = QtW.QVBoxLayout()
        self.vertical_layout_menu.setSpacing(0)
        self.vertical_layout_menu.setObjectName("verticalLayout_menu")

        self.horizontal_layout_main.addLayout(self.vertical_layout_menu)

        self.vertical_layout_main = QtW.QVBoxLayout()
        self.vertical_layout_main.setObjectName("verticalLayout_21")
        self.stacked_widget = QtW.QStackedWidget(self.central_widget)
        self.stacked_widget.setObjectName("stackedWidget")
        self.stacked_widget.setFrameShadow(QtW.QFrame.Plain)  # type: ignore
        self.stacked_widget.setLineWidth(0)

        self.vertical_layout_main.addWidget(self.stacked_widget)

        self.status_bar_progress_bar = QtW.QStatusBar(window)
        window.setStatusBar(self.status_bar_progress_bar)

        self.frame_progress_bar = QtW.QFrame(self.central_widget)
        self.horizontal_layout_progress_bar = QtW.QHBoxLayout(self.frame_progress_bar)
        self.horizontal_layout_progress_bar.setObjectName("horizontalLayout_progress_bar")
        self.label_status = QtW.QLabel(self.central_widget)
        self.label_status.setObjectName("label_Status")
        self.label_status.setFont(font)
        self.horizontal_layout_progress_bar.addWidget(self.label_status)

        self.progress_bar = QtW.QProgressBar(self.central_widget)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setStyleSheet(
            f"QProgressBar{'{'}border: 1px solid {globs.WHITE};border-radius: 10px;text-align: center;color: {globs.WHITE};{'}'}\n"
            f"QProgressBar::chunk{'{'}background-color: {globs.LIGHT}; border-radius: 10px;{'}'}"
        )
        self.progress_bar.setValue(0)
        self.progress_bar.setFont(font)
        self.horizontal_layout_progress_bar.addWidget(self.progress_bar)

        self.vertical_layout_main.addWidget(self.frame_progress_bar)

        self.horizontal_layout_start_buttons = QtW.QHBoxLayout()
        self.horizontal_layout_start_buttons.setObjectName("horizontalLayout_2")

        self.status_bar = StatusBar(window)
        self.horizontal_layout_start_buttons.addWidget(self.status_bar.label)
        globs.LOGGER.addHandler(self.status_bar)

        self.push_button_start_single = QtW.QPushButton(self.central_widget)
        self.push_button_start_single.setObjectName("pushButton_start_single")
        self.push_button_start_single.setMinimumSize(QtC.QSize(100, 40))
        self.push_button_start_single.setMaximumSize(QtC.QSize(16777215, 40))
        icon32 = QtG.QIcon()
        icon32.addFile(f"{globs.FOLDER}/icons/Start.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        self.push_button_start_single.setIcon(icon32)
        self.push_button_start_single.setIconSize(QtC.QSize(24, 24))

        self.horizontal_layout_start_buttons.addWidget(self.push_button_start_single)

        self.push_button_start_multiple = QtW.QPushButton(self.central_widget)
        self.push_button_start_multiple.setObjectName("pushButton_start_multiple")
        self.push_button_start_multiple.setMinimumSize(QtC.QSize(100, 40))
        self.push_button_start_multiple.setMaximumSize(QtC.QSize(16777215, 40))
        icon33 = QtG.QIcon()
        icon33.addFile(
            f"{globs.FOLDER}/icons/Start_multiple.svg",
            QtC.QSize(),
            QtG.QIcon.Normal,  # type: ignore
            QtG.QIcon.Off,  # type: ignore
        )
        self.push_button_start_multiple.setIcon(icon33)
        self.push_button_start_multiple.setIconSize(QtC.QSize(24, 24))

        self.horizontal_layout_start_buttons.addWidget(self.push_button_start_multiple)

        self.push_button_cancel = QtW.QPushButton(self.central_widget)
        self.push_button_cancel.setObjectName("pushButton_Cancel")
        self.push_button_cancel.setMinimumSize(QtC.QSize(100, 40))
        self.push_button_cancel.setMaximumSize(QtC.QSize(16777215, 40))
        icon34 = QtG.QIcon()
        icon34.addFile(f"{globs.FOLDER}/icons/Exit.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        self.push_button_cancel.setIcon(icon34)
        self.push_button_cancel.setIconSize(QtC.QSize(24, 24))

        self.horizontal_layout_start_buttons.addWidget(self.push_button_cancel)

        self.vertical_layout_main.addLayout(self.horizontal_layout_start_buttons)

        self.horizontal_layout_main.addLayout(self.vertical_layout_main)

        window.setCentralWidget(self.central_widget)
        self.menubar = QtW.QMenuBar(window)
        self.menubar.setObjectName("menubar")
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtC.QRect(0, 0, 1226, 30))
        self.menubar.setStyleSheet(
            f"QMenuBar::item{'{'}background-color: {globs.DARK};{'}'}\n"
            f"QMenuBar::item:pressed{'{'}background-color: {globs.LIGHT};{'}'}\n"
            f"QMenuBar::item:selected{'{'}background-color: {globs.LIGHT};{'}'}\n"
        )
        self.menubar.setNativeMenuBar(True)
        self.menu_file = QtW.QMenu(self.menubar)
        self.menu_file.setObjectName("menuFile")
        self.menu_file.setStyleSheet(
            f"QtG.QAction::icon {'{'} background-color:{globs.LIGHT};selection-background-color: {globs.LIGHT};{'}'}\n"
            f"*{'{'}	background-color: {globs.DARK};{'}'}\n"
            f"*:hover{'{'}background-color: {globs.LIGHT};{'}'}"
        )
        self.menu_file.setTearOffEnabled(False)
        self.menu_calculation = QtW.QMenu(self.menubar)
        self.menu_calculation.setObjectName("menuCalculation")
        self.menu_calculation.setFont(font)
        self.menu_settings = QtW.QMenu(self.menubar)
        self.menu_settings.setObjectName("menuSettings")
        self.menu_language = QtW.QMenu(self.menu_settings)
        self.menu_language.setObjectName("menuLanguage")
        self.menu_language.setEnabled(True)
        icon35 = QtG.QIcon()
        icon35.addFile(f"{globs.FOLDER}/icons/Language.svg", QtC.QSize(), QtG.QIcon.Normal, QtG.QIcon.Off)  # type: ignore
        icon35.addFile(
            f"{globs.FOLDER}/icons/Language_Inv.svg",
            QtC.QSize(),
            QtG.QIcon.Active,  # type: ignore
            QtG.QIcon.Off,  # type: ignore
        )
        self.menu_language.setIcon(icon35)
        self.menu_scenario = QtW.QMenu(self.menubar)
        self.menu_scenario.setObjectName("menuScenario")
        window.setMenuBar(self.menubar)
        self.tool_bar = QtW.QToolBar(window)
        self.tool_bar.setObjectName("toolBar")
        self.tool_bar.setStyleSheet(
            f"QAction::icon {'{'} background-color:{globs.LIGHT};selection-background-color: {globs.LIGHT};{'}'}\n"
            f"*{'{'}	background-color: {globs.DARK};{'}'}\n"
            f"*:hover{'{'}background-color: {globs.LIGHT};{'}'}"
        )
        self.tool_bar.setMovable(False)
        window.addToolBar(QtC.Qt.TopToolBarArea, self.tool_bar)  # type: ignore

        self.menubar.addAction(self.menu_file.menuAction())
        self.menubar.addAction(self.menu_calculation.menuAction())
        self.menubar.addAction(self.menu_scenario.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menu_file.addAction(self.action_new)
        self.menu_file.addAction(self.action_save)
        self.menu_file.addAction(self.action_save_as)
        self.menu_file.addAction(self.action_open)
        self.menu_file.setFont(font)
        self.menu_calculation.addAction(self.action_start_multiple)
        self.menu_calculation.addAction(self.action_start_single)
        self.menu_settings.addAction(self.menu_language.menuAction())
        self.menu_settings.setFont(font)
        self.menu_scenario.addAction(self.action_update_scenario)
        self.menu_scenario.addAction(self.action_add_scenario)
        self.menu_scenario.addAction(self.action_delete_scenario)
        self.menu_scenario.addAction(self.action_rename_scenario)
        self.menu_scenario.setFont(font)
        self.tool_bar.addAction(self.action_new)
        self.tool_bar.addAction(self.action_save)
        self.tool_bar.addAction(self.action_save_as)
        self.tool_bar.addAction(self.action_open)
        self.tool_bar.addAction(self.action_start_single)
        self.tool_bar.addAction(self.action_start_multiple)
        self.tool_bar.addAction(self.action_update_scenario)
        self.tool_bar.addAction(self.action_add_scenario)
        self.tool_bar.addAction(self.action_delete_scenario)
        self.tool_bar.addAction(self.action_rename_scenario)

        self.button_rename_scenario.clicked.connect(self.action_rename_scenario.trigger)
        self.push_button_cancel.clicked.connect(window.close)
        self.push_button_start_multiple.clicked.connect(self.action_start_multiple.trigger)
        self.push_button_add_scenario.clicked.connect(self.action_add_scenario.trigger)
        self.push_button_delete_scenario.clicked.connect(self.action_delete_scenario.trigger)
        self.push_button_save_scenario.clicked.connect(self.action_update_scenario.trigger)
        self.list_widget_scenario.itemDoubleClicked.connect(self.action_rename_scenario.trigger)
        self.push_button_start_single.clicked.connect(self.action_start_single.trigger)

        set_default_font(self.list_widget_scenario)

        set_default_font(self.push_button_save_scenario, bold=True)
        set_default_font(self.push_button_add_scenario, bold=True)
        set_default_font(self.push_button_delete_scenario, bold=True)
        set_default_font(self.button_rename_scenario, bold=True)
        set_default_font(self.push_button_cancel, bold=True)
        set_default_font(self.push_button_start_single, bold=True)
        set_default_font(self.push_button_start_multiple, bold=True)
        set_default_font(self.menu_scenario)
        set_default_font(self.menu_calculation)
        set_default_font(self.menu_file)
        set_default_font(self.menu_settings)
        set_default_font(self.menu_language)
        set_default_font(self.menubar)
        set_default_font(self.list_widget_scenario)
        set_default_font(self.status_bar.label)

        self.stacked_widget.setCurrentIndex(0)
        QtC.QMetaObject.connectSlotsByName(window)

        window.setWindowTitle(gui_name)
        self.action_new.setText("New")
        # if QT_CONFIG(tooltip)
        self.action_new.setToolTip("Create new project file")
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.action_new.setShortcut("Ctrl+N")
        # endif // QT_CONFIG(shortcut)
        self.action_save.setText("Save")
        # if QT_CONFIG(shortcut)
        self.action_save.setShortcut("Ctrl+S")
        # endif // QT_CONFIG(shortcut)
        self.action_open.setText("Open")
        # if QT_CONFIG(shortcut)
        self.action_open.setShortcut("Ctrl+O")
        # endif // QT_CONFIG(shortcut)
        self.action_open_add.setText("Open as appending")
        # if QT_CONFIG(shortcut)
        self.action_open_add.setShortcut("Ctrl+A")
        # endif // QT_CONFIG(shortcut)
        self.action_start_multiple.setText("Calculate all scenarios")
        # if QT_CONFIG(shortcut)
        self.action_start_multiple.setShortcut("Ctrl+R")
        # endif // QT_CONFIG(shortcut)
        self.action_update_scenario.setText("Update scenario")
        # if QT_CONFIG(shortcut)
        self.action_update_scenario.setShortcut("Ctrl+Shift+S")
        # endif // QT_CONFIG(shortcut)
        self.action_add_scenario.setText("Add scenario")
        # if QT_CONFIG(shortcut)
        self.action_add_scenario.setShortcut("Ctrl+Shift+A")
        # endif // QT_CONFIG(shortcut)
        self.action_delete_scenario.setText("Delete scenario")
        # if QT_CONFIG(shortcut)
        self.action_delete_scenario.setShortcut("Ctrl+Shift+D")
        # endif // QT_CONFIG(shortcut)
        self.action_save_as.setText("Save As")
        # if QT_CONFIG(shortcut)
        self.action_save_as.setShortcut("F12")
        # endif // QT_CONFIG(shortcut)
        self.action_rename_scenario.setText("Rename scenario")
        # if QT_CONFIG(shortcut)
        self.action_rename_scenario.setShortcut("Ctrl+Shift+R")
        # endif // QT_CONFIG(shortcut)
        self.action_start_single.setText("Calculate current scenario")
        # if QT_CONFIG(shortcut)
        self.action_start_single.setShortcut("Ctrl+Shift+R")
        # endif // QT_CONFIG(shortcut)
        self.push_button_save_scenario.setText("Update scenario")
        self.push_button_add_scenario.setText("Add scenario")
        self.push_button_delete_scenario.setText("Delete scenario")
        self.button_rename_scenario.setText("Rename scenario")

        __sorting_enabled = self.list_widget_scenario.isSortingEnabled()
        self.list_widget_scenario.setSortingEnabled(False)
        ___qlistwidgetitem = self.list_widget_scenario.item(0)
        ___qlistwidgetitem.setText("Scenario: 1")
        self.list_widget_scenario.setSortingEnabled(__sorting_enabled)
        self.label_status.setText("Progress: ")
        self.push_button_start_single.setText("Calculate current scenario")
        self.push_button_start_multiple.setText("Calculate all scenarios")
        self.push_button_cancel.setText("Exit")
        self.menu_file.setTitle("File")
        self.menu_calculation.setTitle("Calculation")
        self.menu_settings.setTitle("Settings")
        self.menu_language.setTitle("Language")
        self.menu_scenario.setTitle("Scenario")
        self.tool_bar.setWindowTitle("toolBar")
        self.status_bar_progress_bar.addPermanentWidget(self.frame_progress_bar, 1)
        self.status_bar_progress_bar.hide()
        # hide toolbar if MAC
        if system() == "Darwin":  # pragma: no cover
            self.tool_bar.hide()
