import os, requests
import pkgutil

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtUiTools import QUiLoader

from .constants import APP_NAME, APP_VERSION, APP_GHAPI_URL, ABOUT_TEXT, BUILD_INFO
from .constants import DAVIDOTEK_KOFI_URL, PROTONUPQT_GITHUB_URL
from .util import config_theme, apply_dark_theme
from .util import open_webbrowser_thread


class PupguiAboutDialog(QObject):

    def __init__(self, parent=None):
        super(PupguiAboutDialog, self).__init__(parent)
        self.parent = parent

        self.load_ui()
        self.setup_ui()
        self.ui.show()

        self.ui.setFixedSize(self.ui.size())

    def load_ui(self):
        data = pkgutil.get_data(__name__, 'resources/ui/pupgui2_aboutdialog.ui')
        ui_file = QDataStream(QByteArray(data))
        loader = QUiLoader()
        self.ui = loader.load(ui_file.device())

    def setup_ui(self):
        self.ui.setWindowTitle(APP_NAME + ' ' + APP_VERSION)

        translator_text = QApplication.instance().translate('translator-text', 'Translated by DavidoTek')

        self.ui.lblAppIcon.setPixmap(QIcon.fromTheme('net.davidotek.pupgui2').pixmap(QSize(96, 96)))

        self.ui.lblAboutTranslator.setText(translator_text)
        self.ui.lblAboutVersion.setTextFormat(Qt.RichText)
        self.ui.lblAboutVersion.setOpenExternalLinks(True)
        self.ui.lblAboutVersion.setText(ABOUT_TEXT)

        self.ui.lblBuildInfo.setText(BUILD_INFO)
        
        try:
            p = QPixmap()
            p.loadFromData(pkgutil.get_data(__name__, 'resources/img/kofi_button_blue.png'))
            self.ui.btnDonate.setIcon(QIcon(p))
            self.ui.btnDonate.setIconSize(p.rect().size())
            self.ui.btnDonate.setFlat(True)
        finally:
            self.ui.btnDonate.setText('')
        self.ui.btnDonate.clicked.connect(self.btn_donate_clicked)

        self.ui.btnGitHub.clicked.connect(self.btn_github_clicked)

        self.ui.comboColorTheme.addItems([self.tr('light'), self.tr('dark'), self.tr('system (restart required)')])
        self.ui.comboColorTheme.setCurrentIndex(['light', 'dark', 'system', None].index(config_theme()))

        self.ui.btnClose.clicked.connect(self.btn_close_clicked)
        self.ui.btnAboutQt.clicked.connect(self.btn_aboutqt_clicked)
        self.ui.btnCheckForUpdates.clicked.connect(self.btn_check_for_updates_clicked)
        self.ui.comboColorTheme.currentIndexChanged.connect(self.combo_color_theme_current_index_changed)

        if os.getenv('APPIMAGE') is None:
            self.ui.btnCheckForUpdates.setVisible(False)

    def combo_color_theme_current_index_changed(self):
        config_theme(['light', 'dark', 'system'][self.ui.comboColorTheme.currentIndex()])
        apply_dark_theme(QApplication.instance())

    def btn_close_clicked(self):
        self.ui.close()

    def btn_aboutqt_clicked(self):
        QMessageBox.aboutQt(self.parent)
    
    def btn_donate_clicked(self):
        open_webbrowser_thread(DAVIDOTEK_KOFI_URL)
    
    def btn_github_clicked(self):
        open_webbrowser_thread(PROTONUPQT_GITHUB_URL)

    def btn_check_for_updates_clicked(self):
        releases = requests.get(APP_GHAPI_URL + '?per_page=1').json()
        if len(releases) == 0:
            return
        newest_release = releases[0]
        v_current = self.tag_name_to_version(APP_VERSION)
        v_newest = self.tag_name_to_version(newest_release['tag_name'])
        if (10000 * int(v_current[0]) + 100 * int(v_current[1]) + int(v_current[2])) < (10000 * int(v_newest[0]) + 100 * int(v_newest[1]) + int(v_newest[2])):
            QMessageBox.information(self.ui, self.tr('Update available'),
            self.tr('There is a newer version available.\nYou are running {APP_VERSION} but {newest_version} is available.')
            .format(APP_VERSION='v' + APP_VERSION, newest_version=newest_release['tag_name']))
            open_webbrowser_thread(newest_release['html_url'])
        else:
            QMessageBox.information(self.ui, self.tr('Up to date'), self.tr('You are running the newest version!'))

    def tag_name_to_version(self, tag_name : str):
        tag_name = tag_name.replace('v', '')
        vers = tag_name.split('.')
        if len(vers) != 3:
            return [0, 0, 0]
        return vers
