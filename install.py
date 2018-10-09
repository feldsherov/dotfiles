#!/usr/bin/env python3
import logging
import shutil
import os


class Installer():
    LOCAL_BACKUP_PATH = "./dotbackups"
    VIMRC_LOCAL_PATH = "./vimrc"
    VIMRC_BACKUP_NAME = "vimrc"
    VIMRC_DESTINATION_PATH = "{HOME}/.vimrc"

    def __init__(self, logger=None, verbosity=logging.INFO):
        self.logger =  logging.getLogger(__name__) if logger is None else logger
        self.logger.setLevel(verbosity)

        self.VIMRC_DESTINATION_PATH = self.VIMRC_DESTINATION_PATH.format(HOME=os.environ["HOME"])

    def install(self):
        self._common_setup()
        self._install_vim()

    def _common_setup(self):
        if not os.path.exists(self.LOCAL_BACKUP_PATH):
            os.makedirs(self.LOCAL_BACKUP_PATH)

    def _install_vim(self):
        if self._vimrc_exists():
            self.logger.warn("vimrc: %s exists, will backup it to %s", self.VIMRC_DESTINATION_PATH, self._get_vimrc_backup_path())
            self._backup_vimrc()

        self._install_vimrc()

    def _install_vimrc(self):
        shutil.copy(self.VIMRC_LOCAL_PATH, self.VIMRC_DESTINATION_PATH)

    def _vimrc_exists(self):
        return os.path.exists(self.VIMRC_DESTINATION_PATH)

    def _get_vimrc_backup_path(self):
        return os.path.join(self.LOCAL_BACKUP_PATH, self.VIMRC_BACKUP_NAME)

    def _backup_vimrc(self):
        shutil.copy(self.VIMRC_DESTINATION_PATH, self._get_vimrc_backup_path())

if __name__ == "__main__":
    installer = Installer()
    installer.install()
