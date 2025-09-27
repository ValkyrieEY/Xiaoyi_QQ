# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'JianerSetupOthers.ui'
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

from qfluentwidgets import (CardWidget, IconWidget, LargeTitleLabel, LineEdit,
    PlainTextEdit, PopUpAniStackedWidget, SmoothScrollArea, SubtitleLabel,
    TitleLabel)
from wizardWindows import JianerSetupWizard_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(884, 645)
        Form.setMinimumSize(QSize(650, 465))
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.PopUpAniStackedWidget = PopUpAniStackedWidget(Form)
        self.PopUpAniStackedWidget.setObjectName(u"PopUpAniStackedWidget")
        self.PopUpAniStackedWidget.setMinimumSize(QSize(0, 0))
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 846, 427))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.Edit_Icon_Settings_5 = CardWidget(self.scrollAreaWidgetContents)
        self.Edit_Icon_Settings_5.setObjectName(u"Edit_Icon_Settings_5")
        self.Edit_Icon_Settings_5.setMaximumSize(QSize(16777215, 120))
        self.horizontalLayout_9 = QHBoxLayout(self.Edit_Icon_Settings_5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_23 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_23)

        self.IconWidget_8 = IconWidget(self.Edit_Icon_Settings_5)
        self.IconWidget_8.setObjectName(u"IconWidget_8")
        self.IconWidget_8.setEnabled(True)
        self.IconWidget_8.setMinimumSize(QSize(40, 40))
        self.IconWidget_8.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_9.addWidget(self.IconWidget_8)

        self.horizontalSpacer_24 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_24)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalSpacer_39 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_39)

        self.TitleLabel_8 = TitleLabel(self.Edit_Icon_Settings_5)
        self.TitleLabel_8.setObjectName(u"TitleLabel_8")
        self.TitleLabel_8.setMaximumSize(QSize(16777215, 50))
        font2 = QFont()
        font2.setFamilies([u"HarmonyOS Sans SC"])
        font2.setPointSize(21)
        font2.setBold(False)
        self.TitleLabel_8.setFont(font2)

        self.verticalLayout_9.addWidget(self.TitleLabel_8)

        self.SubtitleLabel_9 = SubtitleLabel(self.Edit_Icon_Settings_5)
        self.SubtitleLabel_9.setObjectName(u"SubtitleLabel_9")
        font3 = QFont()
        font3.setFamilies([u"HarmonyOS Sans SC"])
        font3.setPointSize(12)
        font3.setBold(False)
        self.SubtitleLabel_9.setFont(font3)
        self.SubtitleLabel_9.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_9.setScaledContents(False)
        self.SubtitleLabel_9.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.SubtitleLabel_9)

        self.SubtitleLabel_11 = SubtitleLabel(self.Edit_Icon_Settings_5)
        self.SubtitleLabel_11.setObjectName(u"SubtitleLabel_11")
        self.SubtitleLabel_11.setFont(font3)
        self.SubtitleLabel_11.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_11.setScaledContents(False)
        self.SubtitleLabel_11.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.SubtitleLabel_11)

        self.verticalSpacer_40 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_40)


        self.horizontalLayout_9.addLayout(self.verticalLayout_9)

        self.NiceWords = PlainTextEdit(self.Edit_Icon_Settings_5)
        self.NiceWords.setObjectName(u"NiceWords")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.NiceWords.sizePolicy().hasHeightForWidth())
        self.NiceWords.setSizePolicy(sizePolicy)
        self.NiceWords.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_9.addWidget(self.NiceWords)

        self.horizontalSpacer_25 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_25)


        self.gridLayout.addWidget(self.Edit_Icon_Settings_5, 1, 0, 1, 1)

        self.Edit_Icon_Settings = CardWidget(self.scrollAreaWidgetContents)
        self.Edit_Icon_Settings.setObjectName(u"Edit_Icon_Settings")
        self.Edit_Icon_Settings.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_3 = QHBoxLayout(self.Edit_Icon_Settings)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.IconWidget_2 = IconWidget(self.Edit_Icon_Settings)
        self.IconWidget_2.setObjectName(u"IconWidget_2")
        self.IconWidget_2.setEnabled(True)
        self.IconWidget_2.setMinimumSize(QSize(40, 40))
        self.IconWidget_2.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_3.addWidget(self.IconWidget_2)

        self.horizontalSpacer_6 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalSpacer_26 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_26)

        self.TitleLabel_2 = TitleLabel(self.Edit_Icon_Settings)
        self.TitleLabel_2.setObjectName(u"TitleLabel_2")
        self.TitleLabel_2.setMaximumSize(QSize(16777215, 50))
        self.TitleLabel_2.setFont(font2)

        self.verticalLayout_3.addWidget(self.TitleLabel_2)

        self.SubtitleLabel_2 = SubtitleLabel(self.Edit_Icon_Settings)
        self.SubtitleLabel_2.setObjectName(u"SubtitleLabel_2")
        self.SubtitleLabel_2.setFont(font3)
        self.SubtitleLabel_2.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_2.setScaledContents(False)
        self.SubtitleLabel_2.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.SubtitleLabel_2)

        self.verticalSpacer_27 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_27)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.SloganText = LineEdit(self.Edit_Icon_Settings)
        self.SloganText.setObjectName(u"SloganText")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.SloganText.sizePolicy().hasHeightForWidth())
        self.SloganText.setSizePolicy(sizePolicy1)
        self.SloganText.setMaximumSize(QSize(16777215, 33))

        self.horizontalLayout_3.addWidget(self.SloganText)

        self.horizontalSpacer_11 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_11)


        self.gridLayout.addWidget(self.Edit_Icon_Settings, 0, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 0, 1, 1)

        self.Edit_Icon_Settings_6 = CardWidget(self.scrollAreaWidgetContents)
        self.Edit_Icon_Settings_6.setObjectName(u"Edit_Icon_Settings_6")
        self.Edit_Icon_Settings_6.setMaximumSize(QSize(16777215, 120))
        self.horizontalLayout_10 = QHBoxLayout(self.Edit_Icon_Settings_6)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_26 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_26)

        self.IconWidget_9 = IconWidget(self.Edit_Icon_Settings_6)
        self.IconWidget_9.setObjectName(u"IconWidget_9")
        self.IconWidget_9.setEnabled(True)
        self.IconWidget_9.setMinimumSize(QSize(40, 40))
        self.IconWidget_9.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_10.addWidget(self.IconWidget_9)

        self.horizontalSpacer_27 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_27)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalSpacer_41 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_41)

        self.TitleLabel_9 = TitleLabel(self.Edit_Icon_Settings_6)
        self.TitleLabel_9.setObjectName(u"TitleLabel_9")
        self.TitleLabel_9.setMaximumSize(QSize(16777215, 50))
        self.TitleLabel_9.setFont(font2)

        self.verticalLayout_10.addWidget(self.TitleLabel_9)

        self.SubtitleLabel_10 = SubtitleLabel(self.Edit_Icon_Settings_6)
        self.SubtitleLabel_10.setObjectName(u"SubtitleLabel_10")
        self.SubtitleLabel_10.setFont(font3)
        self.SubtitleLabel_10.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_10.setScaledContents(False)
        self.SubtitleLabel_10.setWordWrap(True)

        self.verticalLayout_10.addWidget(self.SubtitleLabel_10)

        self.SubtitleLabel_12 = SubtitleLabel(self.Edit_Icon_Settings_6)
        self.SubtitleLabel_12.setObjectName(u"SubtitleLabel_12")
        self.SubtitleLabel_12.setFont(font3)
        self.SubtitleLabel_12.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_12.setScaledContents(False)
        self.SubtitleLabel_12.setWordWrap(True)

        self.verticalLayout_10.addWidget(self.SubtitleLabel_12)

        self.verticalSpacer_42 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_42)


        self.horizontalLayout_10.addLayout(self.verticalLayout_10)

        self.PokeWords = PlainTextEdit(self.Edit_Icon_Settings_6)
        self.PokeWords.setObjectName(u"PokeWords")
        sizePolicy.setHeightForWidth(self.PokeWords.sizePolicy().hasHeightForWidth())
        self.PokeWords.setSizePolicy(sizePolicy)
        self.PokeWords.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_10.addWidget(self.PokeWords)

        self.horizontalSpacer_28 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_28)


        self.gridLayout.addWidget(self.Edit_Icon_Settings_6, 2, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.SmoothScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.SmoothScrollArea)

        self.PopUpAniStackedWidget.addWidget(self.page)

        self.horizontalLayout.addWidget(self.PopUpAniStackedWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u7b80\u513f - \u8bbe\u7f6e\u57fa\u672c\u4fe1\u606f", None))
        self.LargeTitleLabel.setText(QCoreApplication.translate("Form", u"\u5176\u4ed6\u4fe1\u606f\u8bbe\u7f6e", None))
        self.SubtitleLabel_5.setText(QCoreApplication.translate("Form", u"    \u8bbe\u7f6e QQ\u673a\u5668\u4eba \u7684\u4e00\u4e9b\u5176\u4ed6\u5c0f\u529f\u80fd", None))
        self.TitleLabel_8.setText(QCoreApplication.translate("Form", u"\u7b80\u513f\u771f\u68d2", None))
        self.SubtitleLabel_9.setText(QCoreApplication.translate("Form", u"\u5f53\u7528\u6237\u5938\u8d5e\u673a\u5668\u4eba\u7684\u65f6\u5019\uff0c\u673a\u5668\u4eba\u5e94\u8be5\u5982\u4f55\u56de\u590d", None))
        self.SubtitleLabel_11.setText(QCoreApplication.translate("Form", u"\u4e00\u884c\u4e00\u4e2a\u7b54\u6848\uff0c\u4e0d\u8981\u91cd\u590d\u586b\u5199", None))
        self.TitleLabel_2.setText(QCoreApplication.translate("Form", u"Slogan", None))
        self.SubtitleLabel_2.setText(QCoreApplication.translate("Form", u"\u673a\u5668\u4eba\u7684\u53e3\u53f7\u3002", None))
        self.SloganText.setText(QCoreApplication.translate("Form", u"\u7b80\u5355 \u53ef\u7231 \u4e2a\u6027 \u5168\u77e5", None))
        self.TitleLabel_9.setText(QCoreApplication.translate("Form", u"\u6233\u4e00\u6233", None))
        self.SubtitleLabel_10.setText(QCoreApplication.translate("Form", u"\u5f53\u7528\u6237\u6233\u4e00\u6233\u673a\u5668\u4eba\u65f6\uff0c\u673a\u5668\u4eba\u5e94\u8be5\u5982\u4f55\u56de\u590d", None))
        self.SubtitleLabel_12.setText(QCoreApplication.translate("Form", u"\u4e00\u884c\u4e00\u4e2a\u7b54\u6848\uff0c\u4e0d\u8981\u91cd\u590d\u586b\u5199", None))
    # retranslateUi

