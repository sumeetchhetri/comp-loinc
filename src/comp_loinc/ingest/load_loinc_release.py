import subprocess
import os
import shutil
from pathlib import Path
from os.path import dirname


PROJECT_DIR = Path(dirname(dirname(dirname(dirname(__file__)))))
SRC_DIR = os.path.join(PROJECT_DIR, 'src')
DATA_DIR = os.path.join(PROJECT_DIR, 'data')


class LoadLoincRelease(object):
    def __init__(self, filepath):
        self.filepath = filepath
        self.unzip_loinc_release()
        self.move_files()

    def get_release_filename(self):
        release_files = [x for x in os.listdir(self.filepath) if x.endswith('.zip')]
        if len(release_files) == 1 and release_files[0].endswith('.zip'):
            return release_files.pop()
        else:
            raise Exception('More than one file in release directory.')

    def unzip_loinc_release(self):
        filename = self.get_release_filename()
        subprocess.call(['unzip', "-o", f"{self.filepath}/{filename}", '-d', f"{self.filepath}/extracted"])

    def move_files(self):
        filename = self.get_release_filename()
        extracted_files = f"{self.filepath}/extracted/{filename.replace('.zip', '')}"
        lpl = f"{extracted_files}/AccessoryFiles/PartFile/LoincPartLink_Primary.csv"
        shutil.move(lpl, f"{DATA_DIR}/code_files/LoincPartLink_Primary.csv")
        loinc_csv = f"{extracted_files}/LoincTable/Loinc.csv"
        shutil.move(loinc_csv, f"{DATA_DIR}/code_files/Loinc.csv")
