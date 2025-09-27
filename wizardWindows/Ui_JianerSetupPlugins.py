# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'JianerSetupPlugins.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (CardWidget, ComboBox, IndeterminateProgressBar, LargeTitleLabel,
    LineEdit, PopUpAniStackedWidget, PrimaryPushButton, PushButton,
    ScrollArea, StrongBodyLabel, SubtitleLabel, TitleLabel,
    ToolButton)
from wizardWindows import JianerSetupWizard_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(798, 634)
        Form.setMinimumSize(QSize(650, 465))
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.PopUpAniStackedWidget = PopUpAniStackedWidget(Form)
        self.PopUpAniStackedWidget.setObjectName(u"PopUpAniStackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout = QVBoxLayout(self.page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.spacer)

        self.widget = QWidget(self.page)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 88))
        self.horizontalLayout_2 = QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.LargeTitleLabel = LargeTitleLabel(self.widget)
        self.LargeTitleLabel.setObjectName(u"LargeTitleLabel")
        font = QFont()
        font.setFamilies([u"HarmonyOS Sans SC Medium"])
        font.setPointSize(30)
        font.setBold(False)
        self.LargeTitleLabel.setFont(font)

        self.horizontalLayout_2.addWidget(self.LargeTitleLabel)


        self.verticalLayout.addWidget(self.widget)

        self.SubtitleLabel_5 = SubtitleLabel(self.page)
        self.SubtitleLabel_5.setObjectName(u"SubtitleLabel_5")
        font1 = QFont()
        font1.setFamilies([u"HarmonyOS Sans SC Medium"])
        font1.setPointSize(14)
        font1.setBold(False)
        self.SubtitleLabel_5.setFont(font1)

        self.verticalLayout.addWidget(self.SubtitleLabel_5)

        self.ScrollArea = ScrollArea(self.page)
        self.ScrollArea.setObjectName(u"ScrollArea")
        self.ScrollArea.setFrameShadow(QFrame.Raised)
        self.ScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 760, 440))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer_31 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_31, 3, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_4)

        self.wikiButton = PushButton(self.scrollAreaWidgetContents)
        self.wikiButton.setObjectName(u"wikiButton")

        self.horizontalLayout_7.addWidget(self.wikiButton)

        self.horizontalSpacer_3 = QSpacerItem(5, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.marketButton = PushButton(self.scrollAreaWidgetContents)
        self.marketButton.setObjectName(u"marketButton")

        self.horizontalLayout_7.addWidget(self.marketButton)

        self.ComboBox = ComboBox(self.scrollAreaWidgetContents)
        self.ComboBox.setObjectName(u"ComboBox")

        self.horizontalLayout_7.addWidget(self.ComboBox)

        self.horizontalSpacer_7 = QSpacerItem(178, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)

        self.SearchBox = LineEdit(self.scrollAreaWidgetContents)
        self.SearchBox.setObjectName(u"SearchBox")

        self.horizontalLayout_7.addWidget(self.SearchBox)

        self.SearchButton = ToolButton(self.scrollAreaWidgetContents)
        self.SearchButton.setObjectName(u"SearchButton")

        self.horizontalLayout_7.addWidget(self.SearchButton)

        self.horizontalSpacer_8 = QSpacerItem(5, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_8)


        self.gridLayout.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)

        self.verticalSpacer_30 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_30, 0, 0, 1, 1)

        

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 0, 1, 1)

        self.LoadingBar = IndeterminateProgressBar(self.scrollAreaWidgetContents)
        self.LoadingBar.setObjectName(u"LoadingBar")

        self.gridLayout.addWidget(self.LoadingBar, 2, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.ScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.ScrollArea)

        self.PopUpAniStackedWidget.addWidget(self.page)

        self.horizontalLayout.addWidget(self.PopUpAniStackedWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u7b80\u513f - \u63d2\u4ef6\u4e2d\u5fc3", None))
        self.LargeTitleLabel.setText(QCoreApplication.translate("Form", u"IntelliMarkets \u63d2\u4ef6\u4e2d\u5fc3", None))
        self.SubtitleLabel_5.setText(QCoreApplication.translate("Form", u"    \u5728\u6b64\u5904\uff0c\u53d1\u6325\u7b80\u513f\u7684\u65e0\u9650\u53ef\u80fd", None))
        self.wikiButton.setText(QCoreApplication.translate("Form", u"Wiki", None))
        self.marketButton.setText(QCoreApplication.translate("Form", u"\u2728 \u524d\u5f80 \u667a\u6167\u5e02\u573a", None))
        self.ComboBox.setText(QCoreApplication.translate("Form", u"\u7b5b\u9009\uff1a\u5df2\u5b89\u88c5", None))
        # retranslateUi

