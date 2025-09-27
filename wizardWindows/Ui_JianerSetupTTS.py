# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'JianerSetupTTS.ui'
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

from qfluentwidgets import (CardWidget, ComboBox, EditableComboBox, IconWidget,
    LargeTitleLabel, LineEdit, PopUpAniStackedWidget, SmoothScrollArea,
    StrongBodyLabel, SubtitleLabel, TitleLabel)
from wizardWindows import JianerSetupWizard_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(820, 875)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 782, 655))
        self.verticalLayout_2 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.StrongBodyLabel_2 = StrongBodyLabel(self.scrollAreaWidgetContents)
        self.StrongBodyLabel_2.setObjectName(u"StrongBodyLabel_2")
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(14)
        font2.setBold(True)
        self.StrongBodyLabel_2.setFont(font2)

        self.verticalLayout_2.addWidget(self.StrongBodyLabel_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 5, 0, 1, 1)

        self.Edit_Icon_Settings_2 = CardWidget(self.scrollAreaWidgetContents)
        self.Edit_Icon_Settings_2.setObjectName(u"Edit_Icon_Settings_2")
        self.Edit_Icon_Settings_2.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_4 = QHBoxLayout(self.Edit_Icon_Settings_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_7 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_7)

        self.IconWidget_3 = IconWidget(self.Edit_Icon_Settings_2)
        self.IconWidget_3.setObjectName(u"IconWidget_3")
        self.IconWidget_3.setEnabled(True)
        self.IconWidget_3.setMinimumSize(QSize(40, 40))
        self.IconWidget_3.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_4.addWidget(self.IconWidget_3)

        self.horizontalSpacer_8 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalSpacer_28 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_28)

        self.TitleLabel_3 = TitleLabel(self.Edit_Icon_Settings_2)
        self.TitleLabel_3.setObjectName(u"TitleLabel_3")
        self.TitleLabel_3.setMaximumSize(QSize(16777215, 50))
        font3 = QFont()
        font3.setFamilies([u"HarmonyOS Sans SC"])
        font3.setPointSize(21)
        font3.setBold(False)
        self.TitleLabel_3.setFont(font3)

        self.verticalLayout_4.addWidget(self.TitleLabel_3)

        self.SubtitleLabel_3 = SubtitleLabel(self.Edit_Icon_Settings_2)
        self.SubtitleLabel_3.setObjectName(u"SubtitleLabel_3")
        font4 = QFont()
        font4.setFamilies([u"HarmonyOS Sans SC"])
        font4.setPointSize(12)
        font4.setBold(False)
        self.SubtitleLabel_3.setFont(font4)
        self.SubtitleLabel_3.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_3.setScaledContents(False)
        self.SubtitleLabel_3.setWordWrap(True)

        self.verticalLayout_4.addWidget(self.SubtitleLabel_3)

        self.verticalSpacer_29 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_29)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.voiceColor = EditableComboBox(self.Edit_Icon_Settings_2)
        self.voiceColor.setObjectName(u"voiceColor")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.voiceColor.sizePolicy().hasHeightForWidth())
        self.voiceColor.setSizePolicy(sizePolicy)
        self.voiceColor.setMaximumSize(QSize(250, 33))

        self.horizontalLayout_4.addWidget(self.voiceColor)

        self.horizontalSpacer_12 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_12)


        self.gridLayout.addWidget(self.Edit_Icon_Settings_2, 0, 0, 1, 1)

        self.verticalSpacer_14 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer_14, 4, 0, 1, 1)

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
        self.TitleLabel_2.setFont(font3)

        self.verticalLayout_3.addWidget(self.TitleLabel_2)

        self.SubtitleLabel_2 = SubtitleLabel(self.Edit_Icon_Settings)
        self.SubtitleLabel_2.setObjectName(u"SubtitleLabel_2")
        self.SubtitleLabel_2.setFont(font4)
        self.SubtitleLabel_2.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_2.setScaledContents(False)
        self.SubtitleLabel_2.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.SubtitleLabel_2)

        self.verticalSpacer_27 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_27)


        self.horizontalLayout_3.addLayout(self.verticalLayout_3)

        self.ttsRate = ComboBox(self.Edit_Icon_Settings)
        self.ttsRate.setObjectName(u"ttsRate")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ttsRate.sizePolicy().hasHeightForWidth())
        self.ttsRate.setSizePolicy(sizePolicy1)
        self.ttsRate.setMinimumSize(QSize(0, 0))
        self.ttsRate.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_3.addWidget(self.ttsRate)

        self.horizontalSpacer_11 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_11)


        self.gridLayout.addWidget(self.Edit_Icon_Settings, 1, 0, 1, 1)

        self.Edit_Icon_Settings_3 = CardWidget(self.scrollAreaWidgetContents)
        self.Edit_Icon_Settings_3.setObjectName(u"Edit_Icon_Settings_3")
        self.Edit_Icon_Settings_3.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_5 = QHBoxLayout(self.Edit_Icon_Settings_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_9 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_9)

        self.IconWidget_4 = IconWidget(self.Edit_Icon_Settings_3)
        self.IconWidget_4.setObjectName(u"IconWidget_4")
        self.IconWidget_4.setEnabled(True)
        self.IconWidget_4.setMinimumSize(QSize(40, 40))
        self.IconWidget_4.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_5.addWidget(self.IconWidget_4)

        self.horizontalSpacer_10 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_10)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_30 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_30)

        self.TitleLabel_4 = TitleLabel(self.Edit_Icon_Settings_3)
        self.TitleLabel_4.setObjectName(u"TitleLabel_4")
        self.TitleLabel_4.setMaximumSize(QSize(16777215, 50))
        self.TitleLabel_4.setFont(font3)

        self.verticalLayout_5.addWidget(self.TitleLabel_4)

        self.SubtitleLabel_4 = SubtitleLabel(self.Edit_Icon_Settings_3)
        self.SubtitleLabel_4.setObjectName(u"SubtitleLabel_4")
        self.SubtitleLabel_4.setFont(font4)
        self.SubtitleLabel_4.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_4.setScaledContents(False)
        self.SubtitleLabel_4.setWordWrap(True)

        self.verticalLayout_5.addWidget(self.SubtitleLabel_4)

        self.verticalSpacer_31 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_31)


        self.horizontalLayout_5.addLayout(self.verticalLayout_5)

        self.ttsVolume = ComboBox(self.Edit_Icon_Settings_3)
        self.ttsVolume.setObjectName(u"ttsVolume")
        sizePolicy1.setHeightForWidth(self.ttsVolume.sizePolicy().hasHeightForWidth())
        self.ttsVolume.setSizePolicy(sizePolicy1)
        self.ttsVolume.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_5.addWidget(self.ttsVolume)

        self.horizontalSpacer_13 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_13)


        self.gridLayout.addWidget(self.Edit_Icon_Settings_3, 2, 0, 1, 1)

        self.Edit_Icon_Settings_4 = CardWidget(self.scrollAreaWidgetContents)
        self.Edit_Icon_Settings_4.setObjectName(u"Edit_Icon_Settings_4")
        self.Edit_Icon_Settings_4.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_6 = QHBoxLayout(self.Edit_Icon_Settings_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalSpacer_14 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_14)

        self.IconWidget_5 = IconWidget(self.Edit_Icon_Settings_4)
        self.IconWidget_5.setObjectName(u"IconWidget_5")
        self.IconWidget_5.setEnabled(True)
        self.IconWidget_5.setMinimumSize(QSize(40, 40))
        self.IconWidget_5.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_6.addWidget(self.IconWidget_5)

        self.horizontalSpacer_15 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_15)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_33 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_33)

        self.TitleLabel_5 = TitleLabel(self.Edit_Icon_Settings_4)
        self.TitleLabel_5.setObjectName(u"TitleLabel_5")
        self.TitleLabel_5.setMaximumSize(QSize(16777215, 50))
        self.TitleLabel_5.setFont(font3)

        self.verticalLayout_6.addWidget(self.TitleLabel_5)

        self.SubtitleLabel_6 = SubtitleLabel(self.Edit_Icon_Settings_4)
        self.SubtitleLabel_6.setObjectName(u"SubtitleLabel_6")
        self.SubtitleLabel_6.setFont(font4)
        self.SubtitleLabel_6.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_6.setScaledContents(False)
        self.SubtitleLabel_6.setWordWrap(True)

        self.verticalLayout_6.addWidget(self.SubtitleLabel_6)

        self.verticalSpacer_34 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_34)


        self.horizontalLayout_6.addLayout(self.verticalLayout_6)

        self.ttsPitCh = ComboBox(self.Edit_Icon_Settings_4)
        self.ttsPitCh.setObjectName(u"ttsPitCh")
        sizePolicy1.setHeightForWidth(self.ttsPitCh.sizePolicy().hasHeightForWidth())
        self.ttsPitCh.setSizePolicy(sizePolicy1)
        self.ttsPitCh.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_6.addWidget(self.ttsPitCh)

        self.horizontalSpacer_16 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_16)


        self.gridLayout.addWidget(self.Edit_Icon_Settings_4, 3, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.SmoothScrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.SmoothScrollArea)

        self.PopUpAniStackedWidget.addWidget(self.page)

        self.horizontalLayout.addWidget(self.PopUpAniStackedWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u7b80\u513f - \u8bbe\u7f6e\u6846\u67b6", None))
        self.LargeTitleLabel.setText(QCoreApplication.translate("Form", u"\u6587\u672c\u8f6c\u8bed\u97f3\u56de\u590d\u8bbe\u7f6e", None))
        self.SubtitleLabel_5.setText(QCoreApplication.translate("Form", u"    \u8bbe\u7f6e\u5f53\u542f\u7528TTS\u56de\u590d\u4e4b\u540e\uff0c\u8bed\u97f3\u56de\u590d\u7684\u76f8\u5173\u8bbe\u7f6e", None))
        self.StrongBodyLabel_2.setText(QCoreApplication.translate("Form", u"    EdgeTTS", None))
        self.TitleLabel_3.setText(QCoreApplication.translate("Form", u"\u97f3\u8272", None))
        self.SubtitleLabel_3.setText(QCoreApplication.translate("Form", u"\u4ee5\u4ec0\u4e48\u7c7b\u578b\u7684\u89d2\u8272\u58f0\u97f3\u6717\u8bfbAI\u56de\u590d\u7684\u6587\u672c", None))
        self.TitleLabel_2.setText(QCoreApplication.translate("Form", u"\u8bed\u901f", None))
        self.SubtitleLabel_2.setText(QCoreApplication.translate("Form", u"\u8bbe\u7f6e\u6717\u8bfbAI\u56de\u590d\u7684\u8bed\u901f\u500d\u6570", None))
        self.TitleLabel_4.setText(QCoreApplication.translate("Form", u"\u97f3\u91cf", None))
        self.SubtitleLabel_4.setText(QCoreApplication.translate("Form", u"\u8bbe\u7f6e\u6717\u8bfbAI\u56de\u590d\u7684\u97f3\u91cf\u5927\u5c0f\u500d\u6570", None))
        self.TitleLabel_5.setText(QCoreApplication.translate("Form", u"\u97f3\u8c03", None))
        self.SubtitleLabel_6.setText(QCoreApplication.translate("Form", u"\u8bbe\u7f6e\u6717\u8bfbAI\u56de\u590d\u7684\u97f3\u8c03\u9ad8\u4f4e\u500d\u6570", None))
    # retranslateUi

