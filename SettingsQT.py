#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-
# generated by wxGlade 0.3.5.1 on Thu Apr 21 12:10:56 2005

# Papagayo-NG, a lip-sync tool for use with several different animation suites
# Original Copyright (C) 2005 Mike Clifton
# Contact information at http://www.lostmarble.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
import os
import platform
import shutil
from functools import partial

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
from PySide2.QtGui import QDesktopServices
import PySide2.QtWidgets as QtWidgets

from PySide2.QtUiTools import QUiLoader as uic
from PySide2.QtCore import QFile

import utilities
from utilities import *

original_colors = {"wave_fill_color": QtGui.QColor(162, 205, 242),
                   "wave_line_color": QtGui.QColor(30, 121, 198),
                   "frame_color": QtGui.QColor(192, 192, 192),
                   "frame_text_color": QtGui.QColor(64, 64, 64),
                   "playback_fill_color": QtGui.QColor(209, 102, 121),
                   "playback_line_color": QtGui.QColor(128, 0, 0),
                   "phrase_fill_color": QtGui.QColor(205, 242, 162),
                   "phrase_line_color": QtGui.QColor(121, 198, 30),
                   "word_fill_color": QtGui.QColor(242, 205, 162),
                   "word_line_color": QtGui.QColor(198, 121, 30),
                   "phoneme_fill_color": QtGui.QColor(231, 185, 210),
                   "phoneme_line_color": QtGui.QColor(173, 114, 146),
                   "bg_fill_color": QtGui.QColor(255, 255, 255)}


class SettingsWindow:
    def __init__(self):
        self.loader = None
        self.ui = None
        self.ui_file = None
        self.main_window = self.load_ui_widget(os.path.join(get_main_dir(), "rsrc", "settings.ui"))
        self.settings = QtCore.QSettings("Morevna Project", "Papagayo-NG")
        self.main_window.general_2.clicked.connect(self.change_tab)
        self.main_window.graphical_2.clicked.connect(self.change_tab)
        self.main_window.misc_2.clicked.connect(self.change_tab)
        self.main_window.voice_rec.clicked.connect(self.change_tab)
        self.main_window.delete_settings.clicked.connect(self.delete_settings)
        self.main_window.reset_colors.clicked.connect(self.on_reset_colors)
        self.main_window.ffmpeg_delete_button.clicked.connect(self.delete_ffmpeg)
        self.main_window.allo_delete_button.clicked.connect(self.delete_ai_model)
        self.main_window.rhubarb_delete_button.clicked.connect(self.delete_rhubarb)
        self.main_window.accepted.connect(self.accepted)
        for color_button in self.main_window.graphical.findChildren(QtWidgets.QPushButton):
            self.main_window.connect(color_button, QtCore.SIGNAL("clicked()"),
                                     partial(self.open_color_dialog, color_button))
        self.load_settings_to_gui()
        self.main_window.open_app_data_path.clicked.connect(self.open_app_data)
        self.main_window.settings_options.setCurrentIndex(0)
        # self.main_window.setWindowIcon(QtGui.QIcon(os.path.join(get_main_dir(), "rsrc", "window_icon.bmp")))
        # self.main_window.about_ok_button.clicked.connect(self.close)

    def load_ui_widget(self, ui_filename, parent=None):
        loader = uic()
        file = QFile(ui_filename)
        file.open(QFile.ReadOnly)
        self.ui = loader.load(file, parent)
        file.close()
        return self.ui

    def change_tab(self, event=None):
        if self.main_window.graphical_2.isChecked():
            print("Graphics")
            self.main_window.settings_options.setCurrentIndex(1)
        elif self.main_window.general_2.isChecked():
            print("General")
            self.main_window.settings_options.setCurrentIndex(0)
        elif self.main_window.misc_2.isChecked():
            print("Misc")
            self.main_window.settings_options.setCurrentIndex(3)
        elif self.main_window.voice_rec.isChecked():
            print("Voice")
            self.main_window.settings_options.setCurrentIndex(2)

    def delete_settings(self, event=None):
        self.settings.clear()

    def open_color_dialog(self, event=None):
        print(event.text())
        old_color = event.palette().button().color()
        new_color = QtWidgets.QColorDialog().getColor(old_color)
        print(event.objectName())
        self.settings.setValue(event.objectName(), new_color.name())
        style = "background-color: {};\nborder: transparent;".format(new_color.name())
        event.setStyleSheet(style)
        print(old_color)
        print(new_color)

    def open_app_data(self):
        qt_url = QtCore.QUrl(r"file:///" + utilities.get_app_data_path(), QtCore.QUrl.TolerantMode)
        QtGui.QDesktopServices.openUrl(qt_url)

    def delete_ffmpeg(self):
        ffmpeg_binary = "ffmpeg.exe"
        ffprobe_binary = "ffprobe.exe"
        if platform.system() == "Darwin":
            ffmpeg_binary = "ffmpeg"
            ffprobe_binary = "ffprobe"
        ffmpeg_path_old = os.path.join(get_main_dir(), ffmpeg_binary)
        ffprobe_path_old = os.path.join(get_main_dir(), ffprobe_binary)
        if os.path.exists(ffmpeg_path_old):
            os.remove(ffmpeg_path_old)
        if os.path.exists(ffprobe_path_old):
            os.remove(ffprobe_path_old)
        ffmpeg_path_new = os.path.join(utilities.get_app_data_path(), ffmpeg_binary)
        ffprobe_path_new = os.path.join(utilities.get_app_data_path(), ffprobe_binary)
        if os.path.exists(ffmpeg_path_new):
            os.remove(ffmpeg_path_new)
        if os.path.exists(ffprobe_path_new):
            os.remove(ffprobe_path_new)

    def delete_rhubarb(self):
        binary = "rhubarb.exe"
        if platform.system() == "Darwin":
            binary = "rhubarb"
        rhubarb_path = os.path.join(utilities.get_app_data_path(), binary)
        if os.path.exists(rhubarb_path):
            os.remove(rhubarb_path)

    def delete_ai_model(self):
        allosaurus_model_path_old = os.path.join(get_main_dir(), "allosaurus_model")
        allosaurus_model_path_new = os.path.join(utilities.get_app_data_path(), "allosaurus_model")
        if os.path.exists(allosaurus_model_path_old):
            shutil.rmtree(allosaurus_model_path_old)
        if os.path.exists(allosaurus_model_path_new):
            shutil.rmtree(allosaurus_model_path_new)

    def load_settings_to_gui(self):
        self.main_window.fps_value.setValue(int(self.settings.value("LastFPS", 24)))
        self.main_window.lang_id_value.setText(self.settings.value("allo_lang_id", "eng"))
        self.main_window.voice_emission_value.setValue(float(self.settings.value("allo_emission", 1.0)))
        self.main_window.run_allosaurus.setChecked(bool(self.settings.value("run_allosaurus", True)))
        self.main_window.app_data_path.setText(utilities.get_app_data_path())
        self.main_window.app_data_path.home(True)
        for color_button in self.main_window.graphical.findChildren(QtWidgets.QPushButton):
            style = "background-color: {};\nborder: transparent;".format(
                self.settings.value(color_button.objectName(), original_colors[color_button.objectName()]))
            color_button.setStyleSheet(style)

    def on_reset_colors(self):
        for color_name, color_value in original_colors.items():
            self.settings.setValue(color_name, color_value.name())
        for color_button in self.main_window.graphical.findChildren(QtWidgets.QPushButton):
            style = "background-color: {};\nborder: transparent;".format(
                self.settings.value(color_button.objectName(), original_colors[color_button.objectName()]))
            color_button.setStyleSheet(style)

    def accepted(self, event=None):
        self.settings.setValue("LastFPS", self.main_window.fps_value.value())
        self.settings.setValue("allo_lang_id", self.main_window.lang_id_value.text())
        self.settings.setValue("allo_emission", self.main_window.voice_emission_value.value())
        self.settings.setValue("run_allosaurus", int(self.main_window.run_allosaurus.isChecked()))

    def close(self):
        self.main_window.close()
# end of class AboutBox
