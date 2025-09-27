# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'JianerSetupAI.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (CardWidget, ComboBox, IconWidget, LargeTitleLabel,
    LineEdit, PopUpAniStackedWidget, SubtitleLabel, TitleLabel)
from wizardWindows import JianerSetupWizard_rc

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(824, 615)
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

        self.verticalSpacer_32 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_32)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.Edit_Icon_Settings_4 = CardWidget(self.page)
        self.Edit_Icon_Settings_4.setObjectName(u"Edit_Icon_Settings_4")
        self.Edit_Icon_Settings_4.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_8 = QHBoxLayout(self.Edit_Icon_Settings_4)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_21 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_21)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalSpacer_37 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_37)

        self.TitleLabel_7 = TitleLabel(self.Edit_Icon_Settings_4)
        self.TitleLabel_7.setObjectName(u"TitleLabel_7")
        self.TitleLabel_7.setMaximumSize(QSize(16777215, 50))
        font2 = QFont()
        font2.setFamilies([u"HarmonyOS Sans SC"])
        font2.setPointSize(21)
        font2.setBold(False)
        self.TitleLabel_7.setFont(font2)

        self.verticalLayout_8.addWidget(self.TitleLabel_7)

        self.SubtitleLabel_8 = SubtitleLabel(self.Edit_Icon_Settings_4)
        self.SubtitleLabel_8.setObjectName(u"SubtitleLabel_8")
        font3 = QFont()
        font3.setFamilies([u"HarmonyOS Sans SC"])
        font3.setPointSize(12)
        font3.setBold(False)
        self.SubtitleLabel_8.setFont(font3)
        self.SubtitleLabel_8.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_8.setScaledContents(False)
        self.SubtitleLabel_8.setWordWrap(True)

        self.verticalLayout_8.addWidget(self.SubtitleLabel_8)

        self.verticalSpacer_38 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_38)


        self.horizontalLayout_8.addLayout(self.verticalLayout_8)

        self.LineEdit_6 = LineEdit(self.Edit_Icon_Settings_4)
        self.LineEdit_6.setObjectName(u"LineEdit_6")
        self.LineEdit_6.setMaximumSize(QSize(330, 33))

        self.horizontalLayout_8.addWidget(self.LineEdit_6)

        self.horizontalSpacer_22 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_22)


        self.gridLayout.addWidget(self.Edit_Icon_Settings_4, 2, 0, 1, 1)

        self.Edit_Icon_Settings_5 = CardWidget(self.page)
        self.Edit_Icon_Settings_5.setObjectName(u"Edit_Icon_Settings_5")
        self.Edit_Icon_Settings_5.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_9 = QHBoxLayout(self.Edit_Icon_Settings_5)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_23 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_23)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalSpacer_39 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_39)

        self.TitleLabel_8 = TitleLabel(self.Edit_Icon_Settings_5)
        self.TitleLabel_8.setObjectName(u"TitleLabel_8")
        self.TitleLabel_8.setMaximumSize(QSize(16777215, 50))
        self.TitleLabel_8.setFont(font2)

        self.verticalLayout_9.addWidget(self.TitleLabel_8)

        self.SubtitleLabel_9 = SubtitleLabel(self.Edit_Icon_Settings_5)
        self.SubtitleLabel_9.setObjectName(u"SubtitleLabel_9")
        self.SubtitleLabel_9.setFont(font3)
        self.SubtitleLabel_9.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_9.setScaledContents(False)
        self.SubtitleLabel_9.setWordWrap(True)

        self.verticalLayout_9.addWidget(self.SubtitleLabel_9)

        self.verticalSpacer_40 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_40)


        self.horizontalLayout_9.addLayout(self.verticalLayout_9)

        self.DeepSeekeyEdit = LineEdit(self.Edit_Icon_Settings_5)
        self.DeepSeekeyEdit.setObjectName(u"DeepSeekeyEdit")
        self.DeepSeekeyEdit.setMaximumSize(QSize(330, 33))

        self.horizontalLayout_9.addWidget(self.DeepSeekeyEdit)

        self.horizontalSpacer_24 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_24)


        self.gridLayout.addWidget(self.Edit_Icon_Settings_5, 3, 0, 1, 1)

        self.SubtitleLabel_6 = SubtitleLabel(self.page)
        self.SubtitleLabel_6.setObjectName(u"SubtitleLabel_6")
        self.SubtitleLabel_6.setFont(font3)
        self.SubtitleLabel_6.setTextFormat(Qt.AutoText)
        self.SubtitleLabel_6.setScaledContents(False)
        self.SubtitleLabel_6.setWordWrap(True)

        self.gridLayout.addWidget(self.SubtitleLabel_6, 4, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.Edit_Icon_Settings = CardWidget(self.page)
        self.Edit_Icon_Settings.setObjectName(u"Edit_Icon_Settings")
        self.Edit_Icon_Settings.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_3 = QHBoxLayout(self.Edit_Icon_Settings)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
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

        self.LineEdit = LineEdit(self.Edit_Icon_Settings)
        self.LineEdit.setObjectName(u"LineEdit")
        self.LineEdit.setMaximumSize(QSize(330, 33))

        self.horizontalLayout_3.addWidget(self.LineEdit)

        self.horizontalSpacer_11 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_11)


        self.gridLayout.addWidget(self.Edit_Icon_Settings, 1, 0, 1, 1)

        self.Edit_Icon_Settings_6 = CardWidget(self.page)
        self.Edit_Icon_Settings_6.setObjectName(u"Edit_Icon_Settings_6")
        self.Edit_Icon_Settings_6.setMaximumSize(QSize(16777215, 120))
        self.horizontalLayout_10 = QHBoxLayout(self.Edit_Icon_Settings_6)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_25 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_25)

        self.IconWidget_8 = IconWidget(self.Edit_Icon_Settings_6)
        self.IconWidget_8.setObjectName(u"IconWidget_8")
        self.IconWidget_8.setEnabled(True)
        self.IconWidget_8.setMinimumSize(QSize(40, 40))
        self.IconWidget_8.setMaximumSize(QSize(40, 40))

        self.horizontalLayout_10.addWidget(self.IconWidget_8)

        self.horizontalSpacer_26 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_26)

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

        self.verticalSpacer_42 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_42)


        self.horizontalLayout_10.addLayout(self.verticalLayout_10)

        self.ComboBox = ComboBox(self.Edit_Icon_Settings_6)
        self.ComboBox.setObjectName(u"ComboBox")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ComboBox.sizePolicy().hasHeightForWidth())
        self.ComboBox.setSizePolicy(sizePolicy)

        self.horizontalLayout_10.addWidget(self.ComboBox)

        self.horizontalSpacer_27 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_27)


        self.gridLayout.addWidget(self.Edit_Icon_Settings_6, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.PopUpAniStackedWidget.addWidget(self.page)

        self.horizontalLayout.addWidget(self.PopUpAniStackedWidget)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"\u7b80\u513f - \u8bbe\u7f6eAI\u529f\u80fd", None))
        self.LargeTitleLabel.setText(QCoreApplication.translate("Form", u"Artificial Intelligence \u8bbe\u7f6e", None))
        self.SubtitleLabel_5.setText(QCoreApplication.translate("Form", u"    \u914d\u7f6e \u7b80\u513f \u7684 AI\u529f\u80fd\u3002", None))
        self.TitleLabel_7.setText(QCoreApplication.translate("Form", u"Gemini Key", None))
        self.SubtitleLabel_8.setText(QCoreApplication.translate("Form", u"\u4f7f\u7528 Google \u7684 Gemini \u670d\u52a1\u6240\u5fc5\u987b\u8981\u6c42\u7684 API Key\u3002", None))
        self.LineEdit_6.setText("")
        self.TitleLabel_8.setText(QCoreApplication.translate("Form", u"DeepSeek Key", None))
        self.SubtitleLabel_9.setText(QCoreApplication.translate("Form", u"\u4f7f\u7528 DeepSeek \u670d\u52a1\u6240\u5fc5\u987b\u8981\u6c42\u7684 API Key\u3002", None))
        self.DeepSeekeyEdit.setText("")
        self.SubtitleLabel_6.setText(QCoreApplication.translate("Form", u"    \u6682\u65f6\u53ef\u4ee5\u7559\u7a7a\uff0c\u4f46\u662f\u5728\u4f7f\u7528AI\u5bf9\u8bdd\u65f6\u4f1a\u76f4\u63a5\u62a5\u9519", None))
        self.TitleLabel_2.setText(QCoreApplication.translate("Form", u"OpenAI Key", None))
        self.SubtitleLabel_2.setText(QCoreApplication.translate("Form", u"\u4f7f\u7528 OpenAI \u7684 ChatGPT \u670d\u52a1\u6240\u5fc5\u987b\u8981\u6c42\u7684 API Key\u3002", None))
        self.LineEdit.setText("")
        self.TitleLabel_9.setText(QCoreApplication.translate("Form", u"\u9ed8\u8ba4\u6a21\u578b", None))
        self.SubtitleLabel_10.setText(QCoreApplication.translate("Form", u"\u673a\u5668\u4eba\u6bcf\u6b21\u542f\u52a8\u65f6\u7684\u9ed8\u8ba4\u542f\u7528\u7684AI\u6a21\u578b", None))
    # retranslateUi

