#!/usr/bin/env python3
import logging
import shutil
import subprocess
import sys
import os

class BaseInstaller():
    def install(self):
        raise NotImplementedError();


class GenericCopyInstaller(BaseInstaller):
    """
    Copies from local path to destination path.
    Expect that local_back_path is existing dir.
    """
    def __init__(self, local_path,
                 destination_path,
                 backup_name,
                 local_backup_path, logger):
        self.local_path = local_path
        self.backup_name = backup_name
        self.destination_path = destination_path
        self.local_backup_path = local_backup_path
        self.logger =  logger

    def install(self):
        if not self._base_directory_exists():
            self.logger.warning("directory: %s does not exist, will create it",
                                 self._get_base_directory())
            self._create_base_directory()

        if self._exists():
            self.logger.warning("%s exists, will backup it to %s",
                                self.destination_path,
                                self._get_backup_path())
            self._backup()

        self._install()

    def _get_base_directory(self):
        return os.path.dirname(self.destination_path)

    def _base_directory_exists(self):
        return os.path.exists(self._get_base_directory())

    def _create_base_directory(self):
        return os.makedirs(self._get_base_directory())

    def _exists(self):
        return os.path.exists(self.destination_path)

    def _install(self):
        raise NotImplementedError()

    def _get_backup_path(self):
        return os.path.join(self.local_backup_path, self.backup_name)

    def _backup(self):
        raise NotImplementedError()


class FileCopyInstaller(GenericCopyInstaller):
    def __init__(self, file_local_path,
                 file_destination_path,
                 file_backup_name,
                 local_backup_path, logger):
        super(FileCopyInstaller, self).__init__(file_local_path,
                                                file_destination_path,
                                                file_backup_name,
                                                local_backup_path, logger)

    def _install(self):
        shutil.copy(self.local_path, self.destination_path)

    def _backup(self):
        shutil.copy(self.destination_path, self._get_backup_path())

class DirectoryCopyInstaller(GenericCopyInstaller):
    def __init__(self, directory_local_path,
                 directory_destination_path,
                 directory_backup_name,
                 local_backup_path, logger):
        super(DirectoryCopyInstaller, self).__init__(directory_local_path,
                                                     directory_destination_path,
                                                     directory_backup_name,
                                                     local_backup_path, logger)

    def _install(self):
        if os.path.exists(self.destination_path):
            shutil.rmtree(self.destination_path)
        shutil.copytree(self.local_path, self.destination_path)

    def _backup(self):
        if os.path.exists(self._get_backup_path()):
            shutil.rmtree(self._get_backup_path())
        shutil.copytree(self.destination_path, self._get_backup_path())

class VimInstaller(BaseInstaller):
    """
    Copies vimrc from local path to destination path.
    Install Plug plugin manager with instructions from
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

class TmuxInstaller:
    """
    Copies tmux.conf from local path to destination path.
    Expect that local_back_path is existing dir.
    """
    def __init__(self, tmuxconf_local_path,
                 tmuxconf_destination_path,
                 tmuxconf_backup_name,
                 tpm_local_path,
                 tpm_destination_path,
                 tpm_backup_name,
                 local_backup_path, logger):
        self.tmux_conf_installer = FileCopyInstaller(tmuxconf_local_path,
                                                     tmuxconf_destination_path,
                                                     tmuxconf_backup_name,
                                                     local_backup_path, logger)
        self.tpm_installer = DirectoryCopyInstaller(tpm_local_path,
                                                    tpm_destination_path,
                                                    tpm_backup_name,
                                                    local_backup_path, logger)

    def install(self):
        self.tmux_conf_installer.install()
        self.tpm_installer.install()

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
    TPM_LOCAL_PATH = "./third_party/tpm"
    TPM_BACKUP_NAME = "tpm"
    TPM_DESTINATION_PATH = "{HOME}/.tmux/plugins/tpm"
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
        self.TPM_DESTINATION_PATH = \
            self.TPM_DESTINATION_PATH.format(HOME=os.environ["HOME"])
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
                                            self.TPM_LOCAL_PATH,
                                            self.TPM_DESTINATION_PATH,
                                            self.TPM_BACKUP_NAME,
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
