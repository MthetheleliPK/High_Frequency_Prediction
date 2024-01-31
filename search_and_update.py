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


    def search_for_field(self, fieldname: str, new_value: Any = None) -> Any:
        #Check if fieldname is Sunspot and new values are sent as a list
        is_sunspot_list = fieldname == "SUNSPOT" and isinstance(new_value, list)

        #creating readable rows (spliting by the new line character)
        lines = self.file_content.split("\n")

        for line in lines:
            if line.startswith(fieldname):
                if not is_sunspot_list:
                    date = line.split(" ")[-1]
                    self.file_content = self.file_content.replace(date, new_value)
                else:
                    old_sunspot_line = line.split(" ")

                    #extracting sunspot and qfe numbers from the template
                    sunspot_number = old_sunspot_line[-2]
                    qfe_number = old_sunspot_line[-1]

                    #old values to be replaced and spliting two values from an array
                    old_sunspot_qfe = f"{sunspot_number} {qfe_number}"

                    #accessing values from an array
                    sunspot_qfe = f"{new_value[0]} {new_value[1]}"

                    self.file_content = self.file_content.replace(old_sunspot_qfe, sunspot_qfe)

    def update_file(self) -> None:
        with open("new_file.txt", 'w') as file:
            file.write(self.file_content)
            file.close()

# Example usage
_obj = FileProcessing('template_spa.inp')

_obj.read_file_content()
_obj.search_for_field("LABEL", "2024/01/30")
_obj.search_for_field("MONTH", "202401.30")
_obj.search_for_field("SUNSPOT", ["123.", "4.9"])

# Save updated content
_obj.update_file()
