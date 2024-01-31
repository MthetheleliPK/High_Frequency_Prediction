import os
from typing import Any

class FileProcessing:
    def __init__(self, filepath: str) -> None:
        self.file_path = os.path.join(os.getcwd(), filepath)
        self.file_content: str = ""

    def read_file_content(self):
        with open(self.file_path, 'r') as file:
            self.file_content = file.read()
            return self.file_content


    def search_for_field(self, fieldname: str, new_value: Any = None, new_value2: Any = None) -> Any:
        
        for line in self.file_content.split("\n"):
            if line.startswith(fieldname):
                print(line.split(' ')[-1])  
                line.replace(line.split(' ')[-1], str(new_value)) 
                file += line + "\n"
        with open(self.file_path, 'w') as file:
            file.write(file)
                # if new_value is not None:
                #     if new_value2 is not None:
                #         self.update_file(fieldname, new_value, new_value2)
                # else:
                #     self.update_file(fieldname, new_value)
               
    def update_file(self, fieldname: str, new_value: Any, new_value2: Any) -> None:
        new_content = ""
        for line in self.file_content.split("\n"):
            if line.startswith(fieldname):
                line = line.replace(line.split(' ')[-1], str(new_value))
                while(new_value2):
                    line = line.replace(line.split(' ')[-2], str(new_value2))
            new_content += line + "\n"

        with open(self.file_path, 'w') as file:
            file.write(new_content)

# Example usage
_obj = FileProcessing('template_spa.inp')

_obj.read_file_content()
_obj.search_for_field("LABEL", "2024/01/30")
# _obj.search_for_field("MONTH", "4")
# _obj.search_for_field("SUNSPOT", "123.7", "4.9")
