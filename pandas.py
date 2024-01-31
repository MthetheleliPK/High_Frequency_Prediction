import os
from typing import Any

class FileProcessing:
    def __init__(self, filepath: str) -> None:
        self.file_path = os.path.join(os.getcwd(), filepath)
        self.file_content: str = ""

    def read_file_content(self):
        # TODO: This reads the file content and probably load it to memory
        with open(self.file_path, 'r') as file:
            self.file_content = file.read()
            

    def search_for_field(self, fieldname: str, new_value: Any = None) -> Any:
        # TODO: This function searches the field supplied and replaces it's value
        for line in self.file_content.split("\n"):
            if line.startswith(fieldname):
                print(line.split(' ')[-1])

    #def update_file(self, fieldname : str, new_Value : str):
        # TODO: Updated original file with new content or creates a new file and replace the old one
        #for line in self.file_content.split("\n"):
        
        #    if line.startswith(fieldname):
        #        line.split(' ')[-1]
        #        line = line.replace(fieldname, new_Value)
        #        print(line.split(' ')[-1])


_obj = FileProcessing('template_spa.inp')

_obj.read_file_content()
_obj.search_for_field("LABEL")
_obj.search_for_field("MONTH")
_obj.search_for_field("SUNSPOT")

#_obj.update_file("LABEL", "2024/01/30")