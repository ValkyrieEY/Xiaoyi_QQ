# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'JianerSetupPluginWindow.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QHBoxLayout,
    QSizePolicy, QSpacerItem, QTextBrowser, QVBoxLayout,
    QWidget)

from qfluentwidgets import (LargeTitleLabel, OpacityAniStackedWidget, Pivot, PopUpAniStackedWidget,
    PrimaryPushButton, PushButton, ScrollArea, SegmentedWidget)
from wizardWindows import JianerSetupWizard_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(802, 643)
        Form.setMinimumSize(QSize(650, 465))
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.PopUpAniStackedWidget = PopUpAniStackedWidget(Form)
        self.PopUpAniStackedWidget.setObjectName(u"PopUpAniStackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout = QVBoxLayout(self.page)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.LargeTitleLabel = LargeTitleLabel(self.page)
        self.LargeTitleLabel.setObjectName(u"LargeTitleLabel")

        self.verticalLayout.addWidget(self.LargeTitleLabel)

        self.line = QFrame(self.page)
        self.line.setObjectName(u"line")
        self.line.setStyleSheet(u"color: rgb(95, 95, 95);")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(5)
        self.line.setMidLineWidth(5)
        self.line.setFrameShape(QFrame.HLine)

        self.verticalLayout.addWidget(self.line)

        self.OpacityAniStackedWidget = OpacityAniStackedWidget(self.page)
        self.OpacityAniStackedWidget.setObjectName(u"OpacityAniStackedWidget")
        self.OpacityAniStackedWidget.setLineWidth(0)
        self.IntroPage = QWidget()
        self.IntroPage.setObjectName(u"IntroPage")
        self.verticalLayout_3 = QVBoxLayout(self.IntroPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.ScrollArea = ScrollArea(self.IntroPage)
        self.ScrollArea.setObjectName(u"ScrollArea")
        self.ScrollArea.setMaximumSize(QSize(16777215, 16777215))
        self.ScrollArea.setFrameShape(QFrame.StyledPanel)
        self.ScrollArea.setFrameShadow(QFrame.Raised)
        self.ScrollArea.setLineWidth(0)
        self.ScrollArea.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.ScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 746, 477))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.IntroPageText = QTextBrowser(self.scrollAreaWidgetContents)
        self.IntroPageText.setObjectName(u"IntroPageText")
        font = QFont()
        font.setFamilies([u"HarmonyOS Sans SC"])
        font.setPointSize(13)
        font.setBold(True)
        self.IntroPageText.setFont(font)
        self.IntroPageText.setStyleSheet(u"background: transparent;")
        self.IntroPageText.setFrameShape(QFrame.NoFrame)
        self.IntroPageText.setFrameShadow(QFrame.Sunken)
        self.IntroPageText.setOverwriteMode(False)

        self.verticalLayout_2.addWidget(self.IntroPageText)

        self.verticalSpacer_2 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.ScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.ScrollArea)

        self.OpacityAniStackedWidget.addWidget(self.IntroPage)
        self.DependPage = QWidget()
        self.DependPage.setObjectName(u"DependPage")
        self.verticalLayout_4 = QVBoxLayout(self.DependPage)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.ScrollArea_2 = ScrollArea(self.DependPage)
        self.ScrollArea_2.setObjectName(u"ScrollArea_2")
        self.ScrollArea_2.setFrameShadow(QFrame.Raised)
        self.ScrollArea_2.setWidgetResizable(True)
        self.scrollAreaWidgetContents_2 = QWidget()
        self.scrollAreaWidgetContents_2.setObjectName(u"scrollAreaWidgetContents_2")
        self.scrollAreaWidgetContents_2.setGeometry(QRect(0, 0, 746, 477))
        self.verticalLayout_5 = QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.DependPageText = QTextBrowser(self.scrollAreaWidgetContents_2)
        self.DependPageText.setObjectName(u"DependPageText")
        self.DependPageText.setFont(font)
        self.DependPageText.setStyleSheet(u"background: transparent")
        self.DependPageText.setFrameShape(QFrame.NoFrame)
        self.DependPageText.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_5.addWidget(self.DependPageText)

        self.verticalSpacer_3 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.ScrollArea_2.setWidget(self.scrollAreaWidgetContents_2)

        self.verticalLayout_4.addWidget(self.ScrollArea_2)

        self.OpacityAniStackedWidget.addWidget(self.DependPage)
        self.LicencePage = QWidget()
        self.LicencePage.setObjectName(u"LicencePage")
        self.verticalLayout_7 = QVBoxLayout(self.LicencePage)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.ScrollArea_3 = ScrollArea(self.LicencePage)
        self.ScrollArea_3.setObjectName(u"ScrollArea_3")
        self.ScrollArea_3.setFrameShadow(QFrame.Raised)
        self.ScrollArea_3.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setObjectName(u"scrollAreaWidgetContents_3")
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 746, 477))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.LicencePageText = QTextBrowser(self.scrollAreaWidgetContents_3)
        self.LicencePageText.setObjectName(u"LicencePageText")
        self.LicencePageText.setFont(font)
        self.LicencePageText.setStyleSheet(u"background: transparent;")
        self.LicencePageText.setFrameShape(QFrame.NoFrame)
        self.LicencePageText.setFrameShadow(QFrame.Sunken)
        self.LicencePageText.setOverwriteMode(False)

        self.verticalLayout_6.addWidget(self.LicencePageText)

        self.verticalSpacer_4 = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_6.addItem(self.verticalSpacer_4)

        self.ScrollArea_3.setWidget(self.scrollAreaWidgetContents_3)

        self.verticalLayout_7.addWidget(self.ScrollArea_3)

        self.OpacityAniStackedWidget.addWidget(self.LicencePage)

        self.verticalLayout.addWidget(self.OpacityAniStackedWidget)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.SegmentedWidget = SegmentedWidget(self.page)
        self.SegmentedWidget.setObjectName(u"SegmentedWidget")

        self.horizontalLayout_7.addWidget(self.SegmentedWidget)

        self.horizontalSpacer_7 = QSpacerItem(178, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)

        self.AblitilyButton_2 = PushButton(self.page)
        self.AblitilyButton_2.setObjectName(u"AblitilyButton_2")

        self.horizontalLayout_7.addWidget(self.AblitilyButton_2)

        self.ManageButton_2 = PrimaryPushButton(self.page)
        self.ManageButton_2.setObjectName(u"ManageButton_2")

        self.horizontalLayout_7.addWidget(self.ManageButton_2)

        self.horizontalSpacer_8 = QSpacerItem(5, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_8)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.PopUpAniStackedWidget.addWidget(self.page)

        self.horizontalLayout.addWidget(self.PopUpAniStackedWidget)


        self.retranslateUi(Form)

        self.OpacityAniStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u7b80\u513f - \u63d2\u4ef6\u4e2d\u5fc3", None))
        self.LargeTitleLabel.setText(QCoreApplication.translate("Form", u" Hello World", None))
        self.IntroPageText.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'HarmonyOS Sans SC'; font-size:13pt; font-weight:700; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u6ca1\u6709\u76f8\u5173\u4ecb\u7ecd (README.md)</p></body></html>", None))
        self.DependPageText.setMarkdown(QCoreApplication.translate("Form", u"**\u6ca1\u6709\u76f8\u5173\u4f9d\u8d56 (requirements.txt)**\n"
"\n"
"", None))
        self.DependPageText.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'HarmonyOS Sans SC'; font-size:13pt; font-weight:700; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u6ca1\u6709\u76f8\u5173\u4f9d\u8d56 (requirements.txt)</p></body></html>", None))
        self.LicencePageText.setHtml(QCoreApplication.translate("Form", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'HarmonyOS Sans SC'; font-size:13pt; font-weight:700; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">\u6ca1\u6709\u76f8\u5173\u534f\u8bae (LICENSE)</p></body></html>", None))
        self.AblitilyButton_2.setText(QCoreApplication.translate("Form", u"\u7981\u7528", None))
        self.ManageButton_2.setText(QCoreApplication.translate("Form", u"\u5b89\u88c5", None))
    # retranslateUi

