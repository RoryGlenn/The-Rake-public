import datetime
import os


class ErrorLog():
    def __init__(self):
        self.directory_path = os.getcwd() + "\\logs\\error_logs"
        self.file_path = self.directory_path + "\\" + str(datetime.date.today()) + ".txt"


    def directory_create(self):
        """Create directory if it does not exist"""
        try:
            if not os.path.exists(self.directory_path):
                os.mkdir(self.directory_path)
        except Exception as e:
            print(e)


    def file_create(self):
        """Create a file if it does not exist"""
        try:
            if not os.path.exists(self.file_path):
                file = open(self.file_path, "w+")
                file.close()
            
            with open(self.file_path, 'a') as file:
                file.write("\n=========================================================================================\n")
        except Exception as e:
            print(e)


    def write(self, text):
        """Writes to the end of the log file"""
        try:
            with open(self.file_path, 'a') as file:
                file.write(f"{text}\n")
        except Exception as e:
            print(e)
