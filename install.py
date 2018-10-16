#!/usr/bin/env python3
import logging
import shutil
import subprocess
import sys
import os

class BaseInstaller():
    def install(self):
        raise NotImplementedError();

class FileCopyInstaller(BaseInstaller):
    """
    Copies file from local path to destination path.
    Expect that local_back_path is existing dir.
    """
    def __init__(self, file_local_path,
                 file_destination_path,
                 file_backup_name,
                 local_backup_path, logger):
        self.file_local_path = file_local_path
        self.file_backup_name = file_backup_name
        self.file_destination_path = file_destination_path
        self.local_backup_path = local_backup_path
        self.logger =  logger

    def install(self):
        if not self._base_directory_exists():
            self.logger.warn("directory: %s does not exist, will create it",
                             self._get_base_directory())
            self._create_base_directory()

        if self._file_exists():
            self.logger.warn("file: %s exists, will backup it to %s",
                             self.file_destination_path,
                             self._get_file_backup_path())
            self._backup_file()

        self._install_file()

    def _get_base_directory(self):
        return os.path.dirname(self.file_destination_path)

    def _base_directory_exists(self):
        return os.path.exists(self._get_base_directory())

    def _create_base_directory(self):
        return os.makedirs(self._get_base_directory())

    def _file_exists(self):
        return os.path.exists(self.file_destination_path)

    def _install_file(self):
        shutil.copy(self.file_local_path, self.file_destination_path)


    def _get_file_backup_path(self):
        return os.path.join(self.local_backup_path, self.file_backup_name)

    def _backup_file(self):
        shutil.copy(self.file_destination_path, self._get_file_backup_path())


class VimInstaller(BaseInstaller):
    """
    Copies vimrc from local path to destination path.
    Install Plug plugin manager with instaructions from
    https://github.com/junegunn/vim-plug
    Expect that local_back_path is existing dir.
    """
    def __init__(self,
                 vimrc_local_path,
                 vimrc_destination_path,
                 vimrc_backup_name,
                 plugvim_local_path,
                 plugvim_destination_path,
                 plugvim_backup_name,
                 local_backup_path, logger):
        self.copy_vimrc_installer = FileCopyInstaller(
                vimrc_local_path,
                vimrc_destination_path,
                vimrc_backup_name,
                local_backup_path, logger)
        self.copy_plugvim_installer = FileCopyInstaller(
                plugvim_local_path,
                plugvim_destination_path,
                plugvim_backup_name,
                local_backup_path, logger)

    def install(self):
        self.copy_vimrc_installer.install()
        self.copy_plugvim_installer.install()

class TmuxInstaller(FileCopyInstaller):
    """
    Copies tmux.conf from local path to destination path.
    Expect that local_back_path is existing dir.
    """
    def __init__(self, tmuxconf_local_path,
                 tmuxconf_destination_path,
                 tmuxconf_backup_name,
                 local_backup_path, logger):
        FileCopyInstaller.__init__(self, tmuxconf_local_path,
                                   tmuxconf_destination_path,
                                   tmuxconf_backup_name,
                                   local_backup_path, logger)

class ZshInstaller(FileCopyInstaller):
    """
    Copies zshrc from local path to destination path.
    Expect that local_back_path is existing dir.
    """
    def __init__(self, zshrc_local_path,
                 zshrc_destination_path,
                 zshrc_backup_name,
                 local_backup_path, logger):
        FileCopyInstaller.__init__(self, zshrc_local_path,
                                   zshrc_destination_path,
                                   zshrc_backup_name,
                                   local_backup_path, logger)

class Installer():
    LOCAL_BACKUP_PATH = "./dotbackups"
    VIMRC_LOCAL_PATH = "./vimrc"
    VIMRC_BACKUP_NAME = "vimrc"
    VIMRC_DESTINATION_PATH = "{HOME}/.vimrc"
    PLUGVIM_LOCAL_PATH = "third_party/vim-plug/plug.vim"
    PLUGVIM_BACKUP_NAME = "plug.vim"
    PLUGVIM_DESTINATION_PATH = "{HOME}/.vim/autoload/plug.vim"
    TMUXCONF_LOCAL_PATH = "./tmux.conf"
    TMUXCONF_BACKUP_NAME = "tmux.conf"
    TMUXCONF_DESTINATION_PATH = "{HOME}/.tmux.conf"
    ZSHRC_LOCAL_PATH = "./zshrc"
    ZSHRC_BACKUP_NAME = "zshrc"
    ZSHRC_DESTINATION_PATH = "{HOME}/.zshrc"

    def __init__(self, logger=None, verbosity=logging.INFO):
        self.logger =  logging.getLogger(__name__) if logger is None else logger
        self.logger.setLevel(verbosity)

        self.VIMRC_DESTINATION_PATH = \
            self.VIMRC_DESTINATION_PATH.format(HOME=os.environ["HOME"])
        self.PLUGVIM_DESTINATION_PATH = \
            self.PLUGVIM_DESTINATION_PATH.format(HOME=os.environ["HOME"])
        self.vim_installer = VimInstaller(self.VIMRC_LOCAL_PATH,
                                          self.VIMRC_DESTINATION_PATH,
                                          self.VIMRC_BACKUP_NAME,
                                          self.PLUGVIM_LOCAL_PATH,
                                          self.PLUGVIM_DESTINATION_PATH,
                                          self.PLUGVIM_BACKUP_NAME,
                                          self.LOCAL_BACKUP_PATH,
                                          self.logger)

        self.TMUXCONF_DESTINATION_PATH = \
            self.TMUXCONF_DESTINATION_PATH.format(HOME=os.environ["HOME"])
        self.tmux_installer = TmuxInstaller(self.TMUXCONF_LOCAL_PATH,
                                            self.TMUXCONF_DESTINATION_PATH,
                                            self.TMUXCONF_BACKUP_NAME,
                                            self.LOCAL_BACKUP_PATH,
                                            self.logger)

        self.ZSHRC_DESTINATION_PATH = \
            self.ZSHRC_DESTINATION_PATH.format(HOME=os.environ["HOME"])
        self.zsh_installer = ZshInstaller(self.ZSHRC_LOCAL_PATH,
                                          self.ZSHRC_DESTINATION_PATH,
                                          self.ZSHRC_BACKUP_NAME,
                                          self.LOCAL_BACKUP_PATH,
                                          self.logger)

    def install(self):
        self._common_setup()
        self.vim_installer.install()
        self.tmux_installer.install()
        self.zsh_installer.install()

    def _common_setup(self):
        if subprocess.call(["git", "submodule", "update", "--init", "--recursive"]):
          self.logger.fatal("Can not update submodules.")
          sys.exit(1)

        if not os.path.exists(self.LOCAL_BACKUP_PATH):
            os.makedirs(self.LOCAL_BACKUP_PATH)


if __name__ == "__main__":
    installer = Installer()
    installer.install()
