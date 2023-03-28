import os
import shutil
import time
from datetime import date


# get source folder content
class ScanDirectory:
    def __init__(self, dir):
        self.files = []
        self.directory = dir

    def get_content(self):
        all_files = os.scandir(self.directory)
        for file in all_files:
            self.files.append(file.name)
        return self.files


# compare folders
class CompareDirectories:
    def __init__(self, source, target):
        self.source = source
        self.target = target
        self.counter = 0
        self.missing = []
        self.deleted = []

    def is_there_a_new_file(self):
        for file in self.source:
            if file in self.target:
                self.counter += 1
            else:
                self.missing.append(file)
        if self.counter == len(self.target) + 1:
            return False
        else:
            return True

    def is_there_a_deleted_file(self):
        for file in self.target:
            if file not in self.source:
                print(file)
                self.deleted.append(file)
                print(self.deleted)


# update modified files
class UpdateFiles:
    def __init__(self, modified_files, deleted_files):
        self.copy_prpmpt = "cp ~/Desktop/source/"
        self.modified_files = modified_files
        self.deleted_files = deleted_files
        self.destination_prompt = " ~/Desktop/target/"
        self.destination_path = "/Users/robertmuresan/Desktop/target/"

    def copy_files(self):
        for file_raw in self.modified_files:
            file = file_raw.replace(" ", "\ ")
            Logchanges().log(f"Copied: {file}")
            prompt = self.copy_prpmpt + file + self.destination_prompt
            print(prompt)
            os.popen(prompt, "r", 1)

    def delete_files(self):
        for file in self.deleted_files:
            Logchanges().log(f"Deleted: {file}")
            print(file)
            print(self.destination_path + file)
            try:
                os.remove(self.destination_path + file)
            except PermissionError:
                print("error")
                shutil.rmtree(self.destination_path + file)


# changes logger
class Logchanges:
    def __init__(self):
        self.f = open("folderSyncLog.txt", "a")
        self.timestamp = f"; timestamp: {str(date.today())}"

    def log(self, action):
        self.f.write(action + self.timestamp + "\n")


# main engine
def main():
    while True:
        source_directory = "/Users/robertmuresan/Desktop/source"
        target_directory = "/Users/robertmuresan/Desktop/target"

        source = ScanDirectory(source_directory).get_content()
        target = ScanDirectory(target_directory).get_content()

        compare = CompareDirectories(source, target)
        compare.is_there_a_deleted_file()
        compare.is_there_a_new_file()

        update = UpdateFiles(compare.missing, compare.deleted)
        update.copy_files()
        update.delete_files()

        print(f"I ran the script at this timestamp: {date.today().}")

        time.sleep(3600)


if __name__ == "__main__":
    main()
