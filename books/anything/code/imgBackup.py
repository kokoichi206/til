#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

class BackupDir:
    PATH = "/tmp/sd"

    @classmethod
    def make(cls):
        os.makedirs(cls.PATH, exist_ok=True)

class Logger:
    FILE = Path(BackupDir.PATH).joinpath("copy.log")

    @classmethod
    def log(cls, message):
        print(message)
        with open(cls.FILE, mode='a+') as f:
            f.write(message + os.linesep)

class ImgBackup:
    backup_target_list = []

    def backup(self):
        BackupDir.make()
        self.__make_backup_list()
        self.__copy()
    
    def __copy(self):
        for target in self.backup_target_list:
            try:
                shutil.copy2(target, BackupDir.PATH)
                Logger.log("Copy " + str(target))
            except PermissionError:
                Logger.log("コピーする権限がありません:" + str(target))

    def __make_backup_list(self):
        all_file_list = []
        for dir, _, files in os.walk(Path.home()):
            for file in files:
                all_file_list.append(Path(dir).joinpath(file))

        for path in all_file_list:
            if self.__is_include_hidden(path):
                continue
            
            if self.__is_img(path):
                self.backup_target_list.append(path)

    def __is_include_hidden(self, path):
        path_parts = Path(path).parts
        for part in path_parts:
            if part.startswith("."):
                return True
        return False
    
    def __is_img(self, path):
        img_ext_list = [".jpeg", ".jpg", ".gif", ".bmp", ".raw"]
        return Path(path).suffix in img_ext_list
    
class Main:
    def run(self):
        img_backup = ImgBackup()
        img_backup.backup()


if __name__ == "__main__":
    main = Main()
    main.run()
