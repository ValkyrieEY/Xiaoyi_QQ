# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'JianerSetupWizard.ui'
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

from qfluentwidgets import (CardWidget, ElevatedCardWidget, IconWidget, LargeTitleLabel,
    PopUpAniStackedWidget, SimpleCardWidget, SmoothScrollArea, SubtitleLabel,
    TitleLabel)
from wizardWindows import JianerSetupWizard_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(797, 754)
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
        self.SubtitleLabel_5.setWordWrap(True)

        self.verticalLayout.addWidget(self.SubtitleLabel_5)

        self.verticalSpacer_32 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_32)

        self.SmoothScrollArea = SmoothScrollArea(self.page)
        self.SmoothScrollArea.setObjectName(u"SmoothScrollArea")
        self.SmoothScrollArea.setFrameShadow(QFrame.Raised)
        self.SmoothScrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 759, 821))
        self.verticalLayout_6 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 9, 0, 1, 1)

        self.NormalIconButton_5 = ElevatedCardWidget(self.scrollAreaWidgetContents)
        self.NormalIconButton_5.setObjectName(u"NormalIconButton_5")
        self.NormalIconButton_5.setMaximumSize(QSize(16777215, 110))
        self.horizontalLayout_7 = QHBoxLayout(self.NormalIconButton_5)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_11 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_11)

        self.IconWidget_5 = IconWidget(self.NormalIconButton_5)
        self.IconWidget_5.setObjectName(u"IconWidget_5")
        self.IconWidget_5.setEnabled(True)
        self.IconWidget_5.setMinimumSize(QSize(40, 40))
        self.IconWidget_5.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_7.addWidget(self.IconWidget_5)

        self.horizontalSpacer_12 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_12)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalSpacer_33 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_33)

        self.TitleLabel_5 = TitleLabel(self.NormalIconButton_5)
        self.TitleLabel_5.setObjectName(u"TitleLabel_5")
        self.TitleLabel_5.setMaximumSize(QSize(16777215, 50))
        font2 = QFont()
        font2.setFamilies([u"HarmonyOS Sans SC"])
        font2.setPointSize(21)
        font2.setBold(False)
        self.TitleLabel_5.setFont(font2)

        self.verticalLayout_7.addWidget(self.TitleLabel_5)

        self.SubtitleLabel_7 = SubtitleLabel(self.NormalIconButton_5)
        self.SubtitleLabel_7.setObjectName(u"SubtitleLabel_7")
        font3 = QFont()
        font3.setFamilies([u"HarmonyOS Sans SC"])
        font3.setPointSize(12)
        font3.setBold(False)
        self.SubtitleLabel_7.setFont(font3)
        self.SubtitleLabel_7.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_7.setScaledContents(False)
        self.SubtitleLabel_7.setWordWrap(True)

        self.verticalLayout_7.addWidget(self.SubtitleLabel_7)

        self.verticalSpacer_34 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_34)


        self.horizontalLayout_7.addLayout(self.verticalLayout_7)


        self.gridLayout.addWidget(self.NormalIconButton_5, 7, 0, 1, 1)

        self.NormalIconButton_3 = ElevatedCardWidget(self.scrollAreaWidgetContents)
        self.NormalIconButton_3.setObjectName(u"NormalIconButton_3")
        self.NormalIconButton_3.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_5 = QHBoxLayout(self.NormalIconButton_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_7 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        self.IconWidget_3 = IconWidget(self.NormalIconButton_3)
        self.IconWidget_3.setObjectName(u"IconWidget_3")
        self.IconWidget_3.setEnabled(True)
        self.IconWidget_3.setMinimumSize(QSize(40, 40))
        self.IconWidget_3.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_5.addWidget(self.IconWidget_3)

        self.horizontalSpacer_8 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_8)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_28 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_28)

        self.TitleLabel_3 = TitleLabel(self.NormalIconButton_3)
        self.TitleLabel_3.setObjectName(u"TitleLabel_3")
        self.TitleLabel_3.setMaximumSize(QSize(16777215, 50))
        self.TitleLabel_3.setFont(font2)

        self.verticalLayout_4.addWidget(self.TitleLabel_3)

        self.SubtitleLabel_3 = SubtitleLabel(self.NormalIconButton_3)
        self.SubtitleLabel_3.setObjectName(u"SubtitleLabel_3")
        self.SubtitleLabel_3.setFont(font3)
        self.SubtitleLabel_3.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_3.setScaledContents(False)
        self.SubtitleLabel_3.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.SubtitleLabel_3)

        self.verticalSpacer_29 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_29)


        self.horizontalLayout_5.addLayout(self.verticalLayout_4)


        self.gridLayout.addWidget(self.NormalIconButton_3, 5, 0, 1, 1)

        self.NormalIconButton_2 = ElevatedCardWidget(self.scrollAreaWidgetContents)
        self.NormalIconButton_2.setObjectName(u"NormalIconButton_2")
        self.NormalIconButton_2.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_4 = QHBoxLayout(self.NormalIconButton_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_5 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_5)

        self.IconWidget_2 = IconWidget(self.NormalIconButton_2)
        self.IconWidget_2.setObjectName(u"IconWidget_2")
        self.IconWidget_2.setEnabled(True)
        self.IconWidget_2.setMinimumSize(QSize(40, 40))
        self.IconWidget_2.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_4.addWidget(self.IconWidget_2)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_26 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_26)

        self.TitleLabel_2 = TitleLabel(self.NormalIconButton_2)
        self.TitleLabel_2.setObjectName(u"TitleLabel_2")
        self.TitleLabel_2.setMaximumSize(QSize(16777215, 50))
        self.TitleLabel_2.setFont(font2)

        self.verticalLayout_3.addWidget(self.TitleLabel_2)

        self.SubtitleLabel_2 = SubtitleLabel(self.NormalIconButton_2)
        self.SubtitleLabel_2.setObjectName(u"SubtitleLabel_2")
        self.SubtitleLabel_2.setFont(font3)
        self.SubtitleLabel_2.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_2.setScaledContents(False)
        self.SubtitleLabel_2.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.SubtitleLabel_2)

        self.verticalSpacer_27 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_27)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)


        self.gridLayout.addWidget(self.NormalIconButton_2, 3, 0, 1, 1)

        self.NormalIconButton_4 = ElevatedCardWidget(self.scrollAreaWidgetContents)
        self.NormalIconButton_4.setObjectName(u"NormalIconButton_4")
        self.NormalIconButton_4.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_6 = QHBoxLayout(self.NormalIconButton_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_9 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_9)

        self.IconWidget_4 = IconWidget(self.NormalIconButton_4)
        self.IconWidget_4.setObjectName(u"IconWidget_4")
        self.IconWidget_4.setEnabled(True)
        self.IconWidget_4.setMinimumSize(QSize(40, 40))
        self.IconWidget_4.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_6.addWidget(self.IconWidget_4)

        self.horizontalSpacer_10 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_10)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_30 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_30)

        self.TitleLabel_4 = TitleLabel(self.NormalIconButton_4)
        self.TitleLabel_4.setObjectName(u"TitleLabel_4")
        self.TitleLabel_4.setMaximumSize(QSize(16777215, 50))
        self.TitleLabel_4.setFont(font2)

        self.verticalLayout_5.addWidget(self.TitleLabel_4)

        self.SubtitleLabel_4 = SubtitleLabel(self.NormalIconButton_4)
        self.SubtitleLabel_4.setObjectName(u"SubtitleLabel_4")
        self.SubtitleLabel_4.setFont(font3)
        self.SubtitleLabel_4.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_4.setScaledContents(False)
        self.SubtitleLabel_4.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.SubtitleLabel_4)

        self.verticalSpacer_31 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_31)


        self.horizontalLayout_6.addLayout(self.verticalLayout_5)


        self.gridLayout.addWidget(self.NormalIconButton_4, 4, 0, 1, 1)

        self.NormalIconButton = ElevatedCardWidget(self.scrollAreaWidgetContents)
        self.NormalIconButton.setObjectName(u"NormalIconButton")
        self.NormalIconButton.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_3 = QHBoxLayout(self.NormalIconButton)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_4 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.IconWidget = IconWidget(self.NormalIconButton)
        self.IconWidget.setObjectName(u"IconWidget")
        self.IconWidget.setEnabled(True)
        self.IconWidget.setMinimumSize(QSize(40, 40))
        self.IconWidget.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_3.addWidget(self.IconWidget)

        self.horizontalSpacer_3 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_25 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_25)

        self.TitleLabel = TitleLabel(self.NormalIconButton)
        self.TitleLabel.setObjectName(u"TitleLabel")
        self.TitleLabel.setMaximumSize(QSize(16777215, 50))
        self.TitleLabel.setFont(font2)

        self.verticalLayout_2.addWidget(self.TitleLabel)

        self.SubtitleLabel = SubtitleLabel(self.NormalIconButton)
        self.SubtitleLabel.setObjectName(u"SubtitleLabel")
        self.SubtitleLabel.setFont(font3)
        self.SubtitleLabel.setTextFormat(Qt.AutoText)
        self.SubtitleLabel.setScaledContents(False)
        self.SubtitleLabel.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.SubtitleLabel)

        self.verticalSpacer_24 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_24)


        self.horizontalLayout_3.addLayout(self.verticalLayout_2)


        self.gridLayout.addWidget(self.NormalIconButton, 2, 0, 1, 1)

        self.PluginIconButton = ElevatedCardWidget(self.scrollAreaWidgetContents)
        self.PluginIconButton.setObjectName(u"PluginIconButton")
        self.PluginIconButton.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_8 = QHBoxLayout(self.PluginIconButton)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_13 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_13)

        self.IconWidget_6 = IconWidget(self.PluginIconButton)
        self.IconWidget_6.setObjectName(u"IconWidget_6")
        self.IconWidget_6.setEnabled(True)
        self.IconWidget_6.setMinimumSize(QSize(40, 40))
        self.IconWidget_6.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_8.addWidget(self.IconWidget_6)

        self.horizontalSpacer_14 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_14)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalSpacer_35 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_35)

        self.TitleLabel_6 = TitleLabel(self.PluginIconButton)
        self.TitleLabel_6.setObjectName(u"TitleLabel_6")
        self.TitleLabel_6.setMaximumSize(QSize(16777215, 50))
        self.TitleLabel_6.setFont(font2)

        self.verticalLayout_8.addWidget(self.TitleLabel_6)

        self.SubtitleLabel_8 = SubtitleLabel(self.PluginIconButton)
        self.SubtitleLabel_8.setObjectName(u"SubtitleLabel_8")
        self.SubtitleLabel_8.setFont(font3)
        self.SubtitleLabel_8.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_8.setScaledContents(False)
        self.SubtitleLabel_8.setWordWrap(True)

        self.verticalLayout_8.addWidget(self.SubtitleLabel_8)

        self.verticalSpacer_36 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_36)


        self.horizontalLayout_8.addLayout(self.verticalLayout_8)


        self.gridLayout.addWidget(self.PluginIconButton, 0, 0, 1, 1)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        font4 = QFont()
        font4.setBold(True)
        self.line.setFont(font4)
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)

        self.OtherIconButton = ElevatedCardWidget(self.scrollAreaWidgetContents)
        self.OtherIconButton.setObjectName(u"OtherIconButton")
        self.OtherIconButton.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_9 = QHBoxLayout(self.OtherIconButton)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_15 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_15)

        self.IconWidget_7 = IconWidget(self.OtherIconButton)
        self.IconWidget_7.setObjectName(u"IconWidget_7")
        self.IconWidget_7.setEnabled(True)
        self.IconWidget_7.setMinimumSize(QSize(40, 40))
        self.IconWidget_7.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_9.addWidget(self.IconWidget_7)

        self.horizontalSpacer_16 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_16)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalSpacer_37 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_37)

        self.TitleLabel_7 = TitleLabel(self.OtherIconButton)
        self.TitleLabel_7.setObjectName(u"TitleLabel_7")
        self.TitleLabel_7.setMaximumSize(QSize(16777215, 50))
        self.TitleLabel_7.setFont(font2)

        self.verticalLayout_9.addWidget(self.TitleLabel_7)

        self.SubtitleLabel_9 = SubtitleLabel(self.OtherIconButton)
        self.SubtitleLabel_9.setObjectName(u"SubtitleLabel_9")
        self.SubtitleLabel_9.setFont(font3)
        self.SubtitleLabel_9.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_9.setScaledContents(False)
        self.SubtitleLabel_9.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.SubtitleLabel_9)

        self.verticalSpacer_38 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_38)


        self.horizontalLayout_9.addLayout(self.verticalLayout_9)


        self.gridLayout.addWidget(self.OtherIconButton, 6, 0, 1, 1)


        self.verticalLayout_6.addLayout(self.gridLayout)

        self.SmoothScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.SmoothScrollArea)

        self.SubtitleLabel_6 = SubtitleLabel(self.page)
        self.SubtitleLabel_6.setObjectName(u"SubtitleLabel_6")
        font5 = QFont()
        font5.setFamilies([u"HarmonyOS Sans SC Black"])
        font5.setPointSize(14)
        font5.setBold(False)
        self.SubtitleLabel_6.setFont(font5)

        self.verticalLayout.addWidget(self.SubtitleLabel_6)

        self.PopUpAniStackedWidget.addWidget(self.page)

        self.horizontalLayout.addWidget(self.PopUpAniStackedWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u7b80\u513f - \u8bbe\u7f6e\u5411\u5bfc", None))
        self.LargeTitleLabel.setText(QCoreApplication.translate("Form", u"Ciallo\uff5e(\u2220\u30fb\u03c9< )\u2312\u2605", None))
        self.SubtitleLabel_5.setText(QCoreApplication.translate("Form", u"    \u6b22\u8fce\u52a0\u5165\u7b80\u513f\u7684\u5927\u5bb6\u5ead\uff0c\u7b80\u513f\u662f\u4f60\u6700\u5fe0\u5b9e\u53ef\u7231\u7684\u5973\u670b\u53cb\u5662o(*\u2267\u25bd\u2266)\u30c4", None))
        self.TitleLabel_5.setText(QCoreApplication.translate("Form", u"\u6846\u67b6\u8bbe\u7f6e", None))
        self.SubtitleLabel_7.setText(QCoreApplication.translate("Form", u"\u4e00\u4e9b\u5173\u4e8e\u6846\u67b6\u7684\u914d\u7f6e\u3002", None))
        self.TitleLabel_3.setText(QCoreApplication.translate("Form", u"\u9ad8\u7ea7\u8bbe\u7f6e", None))
        self.SubtitleLabel_3.setText(QCoreApplication.translate("Form", u"\u4e3b\u673a\u5730\u5740\u3001\u7aef\u53e3 \u548c QQ\u673a\u5668\u4eba\u534f\u8bae\u7b49\u3002", None))
        self.TitleLabel_2.setText(QCoreApplication.translate("Form", u"Artificial Intelligence \u8bbe\u7f6e", None))
        self.SubtitleLabel_2.setText(QCoreApplication.translate("Form", u"\u914d\u7f6e \u7b80\u513f \u7684 AI\u529f\u80fd\u3002", None))
        self.TitleLabel_4.setText(QCoreApplication.translate("Form", u"\u9884\u8bbe", None))
        self.SubtitleLabel_4.setText(QCoreApplication.translate("Form", u"\u5168\u65b0\u7684\u89d2\u8272\u626e\u6f14\u540e\u53f0\uff0c\u53ef\u89c6\u5316\u9884\u8bbe\u4fe1\u606f\u4e0e\u4eba\u5458\u7ba1\u7406\uff0c\u65e0\u9650\u5236\u5730\u6dfb\u52a0\u9884\u8bbe\u3002", None))
        self.TitleLabel.setText(QCoreApplication.translate("Form", u"\u57fa\u672c\u4fe1\u606f\u8bbe\u7f6e", None))
        self.SubtitleLabel.setText(QCoreApplication.translate("Form", u"\u8bbe\u7f6e QQ\u673a\u5668\u4eba \u7684\u57fa\u672c\u4fe1\u606f\uff0c\u5982 QQ\u53f7\u3001QQ\u673a\u5668\u4eba\u6635\u79f0\u548c\u89e6\u53d1\u56de\u7b54\u7684\u5173\u952e\u8bcd\u7b49\u3002", None))
        self.TitleLabel_6.setText(QCoreApplication.translate("Form", u"\u63d2\u4ef6\u4e2d\u5fc3", None))
        self.SubtitleLabel_8.setText(QCoreApplication.translate("Form", u"\u62d3\u5bbd\u8fb9\u754c\uff0c\u4e3a\u4f60\u7684\u7b80\u513f\u589e\u6dfb\u65e0\u9650\u53ef\u80fd\u3002", None))
        self.TitleLabel_7.setText(QCoreApplication.translate("Form", u"\u5176\u4ed6\u8bbe\u7f6e", None))
        self.SubtitleLabel_9.setText(QCoreApplication.translate("Form", u"\u673a\u5668\u4eba\u7684 Slogan \uff0c\u6216\u662f\u6233\u4e00\u6233\u3002", None))
        self.SubtitleLabel_6.setText(QCoreApplication.translate("Form", u"    \u8bf7\u6ce8\u610f\uff1a\u9996\u6b21\u4f7f\u7528\u5fc5\u987b\u5b8c\u6210\u5168\u90e8\u8bbe\u7f6e\uff0c\u5426\u5219 QQ\u673a\u5668\u4eba \u5c06\u65e0\u6cd5\u6b63\u5e38\u8fd0\u884c\uff01", None))
    # retranslateUi

