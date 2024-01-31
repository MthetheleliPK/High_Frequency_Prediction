import datetime as dt
from fileinput import filename
import shutil
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import numpy as np
from hf_pred import update_template, write_template, exec_file

class HFProcessorApp:
    def __init__(self, master):
        self.master = master
        self.master.title('HF Prediction file generator')

        # Initialize variables
        self.d_years = [str(i) for i in range(2010, 2030)]
        self.d_months = [str(i) for i in range(1, 13)]
        self.d_days = [str(i) for i in range(1, 32)]

        self.ssn = tk.DoubleVar()
        self.qfe = tk.DoubleVar()
        self.ssn_w = tk.DoubleVar()
        self.qfe_w = tk.DoubleVar()
        self.code = tk.StringVar()
        self.file = tk.StringVar()
        self.exec_file = tk.StringVar()

        # Load logo image
        logo_path = "sansalogo.gif"  # Provide the correct path or ensure the image is in the same directory
        logo_image = Image.open(logo_path)
        logo_photo = ImageTk.PhotoImage(logo_image)

        # Create the main layout
        d_logo = tk.Label(self.master, image=logo_photo)
        d_logo.grid(row=0, column=0, columnspan=4)
        d_logo.image = logo_photo  # Keep a reference to prevent garbage collection

        d_base = ttk.Frame(self.master)
        d_base.grid(row=1, column=0)

        ttk.Label(d_base, text='year').grid(row=0, column=0)
        self.year_menu = ttk.Combobox(d_base, values=self.d_years)
        self.year_menu.grid(row=0, column=1)
        self.year_menu.bind("<<ComboboxSelected>>", self.hf_pred_wid_year_menu)

        ttk.Label(d_base, text='month').grid(row=1, column=0)
        self.month_menu = ttk.Combobox(d_base, values=self.d_months)
        self.month_menu.grid(row=1, column=1)
        self.month_menu.bind("<<ComboboxSelected>>", self.hf_pred_wid_month_menu)

        ttk.Label(d_base, text='day').grid(row=2, column=0)
        self.day_menu = ttk.Combobox(d_base, values=self.d_days)
        self.day_menu.grid(row=2, column=1)
        self.day_menu.bind("<<ComboboxSelected>>", self.hf_pred_wid_day_menu)

        o_base = ttk.Frame(self.master)
        o_base.grid(row=1, column=1)
        ttk.Label(o_base, text='Solar Index').grid(row=0, column=0)
        ssn_i = ttk.Entry(o_base, textvariable=self.ssn)
        ssn_i.grid(row=0, column=1)
        ttk.Label(o_base, text='qfe').grid(row=1, column=0)
        qfe_i = ttk.Entry(o_base, textvariable=self.qfe)
        qfe_i.grid(row=1, column=1)
        ttk.Label(o_base, text='Weekly Solar Index').grid(row=2, column=0)
        ssn_w_i = ttk.Entry(o_base, textvariable=self.ssn_w)
        ssn_w_i.grid(row=2, column=1)
        ttk.Label(o_base, text='Weekly qfe').grid(row=3, column=0)
        qfe_w_i = ttk.Entry(o_base, textvariable=self.qfe_w)
        qfe_w_i.grid(row=3, column=1)
        ttk.Label(o_base, text='type').grid(row=4, column=0)
        code_i = ttk.Entry(o_base, textvariable=self.code)
        code_i.grid(row=4, column=1)

        slb = ttk.Frame(self.master)
        slb.grid(row=1, column=2)
        flb = ttk.Frame(slb)
        flb.grid(row=0, column=0)

        ttk.Button(flb, text='Open Template', command=self.hf_pred_wid_open).grid(row=0, column=0)
        make_button = ttk.Button(flb, text='Make file', command=self.hf_pred_wid_make_file)
        make_button.grid(row=0, column=1)
        exec_button = ttk.Button(flb, text='Execute', command=self.hf_pred_wid_execute)
        exec_button.grid(row=0, column=2)
        ttk.Button(flb, text='Done', command=self.hf_pred_wid_done).grid(row=0, column=3)

        self.text_widget = tk.Text(slb, wrap='word', width=50, height=6)
        self.text_widget.grid(row=1, column=0)


    def hf_pred_wid_f1(self, index):
        self.sel_freq[index] = 1 - self.sel_freq[index]
        self.process_record()

    def hf_pred_wid_year_menu(self, event):
        self.d_year = self.d_years[self.year_menu.current()]

    def hf_pred_wid_month_menu(self, event):
        self.d_month = self.d_months[self.month_menu.current()]

    def hf_pred_wid_day_menu(self, event):
        self.d_day = self.d_days[self.day_menu.current()]
        print(self.d_day)

        #return self.d_day

    def hf_pred_wid_values(event, pstate):
        # Toggle the line connection
        pstate_data = event.top.get_uvalue()  # Get the data structure stored with the top widget
        temp_str = event.id.get_value()  # Get the value in the box

        if event.id == pstate_data.ssn_i:
            pstate_data.ssn = temp_str
        elif event.id == pstate_data.qfe_i:
            pstate_data.qfe = temp_str
        elif event.id == pstate_data.ssn_w_i:
            pstate_data.ssn_w = temp_str
        elif event.id == pstate_data.qfe_w_i:
            pstate_data.qfe_w = temp_str
        elif event.id == pstate_data.code_i:
            pstate_data.code = temp_str

    def hf_pred_wid_open(self):
        file_path = filedialog.askopenfilename(filetypes=[('Template files', '*.inp')])
        if file_path:
            with open(file_path, 'r') as file:
                contents = file.readlines()
            self.file.set(file_path)
            print(file_path)
            code = os.path.basename(file_path).split('.')[0][-3:]
            print(code)
            self.code = code
            self.text_widget.insert(tk.END, f'Opened {file_path}\n')
            self.contents = contents

    def hf_pred_wid_make_file(self):
        #contents = ''  # Implement reading template contents here
        contents = update_template(self.contents, self.d_year, self.d_month, self.d_day, self.ssn, self.ssn_w,
                             self.qfe, self.qfe_w)
        #tt = 123456789  # Replace with actual systime function (replace with the current time)
        #month, day, year, n_hour = 1,12, 2024, 0  # Replace with actual caldat function
        filename = self.file_from_date()# self.code, self.d_year, self.d_month, self.d_day))
        print(filename)
        write_template(filename, contents)
        #self.exec_file.set(filename)
        self.text_widget.insert(tk.END, f'File written {filename}\n')

    #def hf_pred_wid_execute(self):
    #    output_file = os.path.basename(self.exec_file.get())
    #    output_filepath = self.exec_file.get()  # assuming you want to get the value of the StringVar
    #    self.text_widget.insert(tk.END, f'File {self.exec_file.get()} moved to C:\\itshfbc\\run\\ \n')
    #    self.text_widget.insert(tk.END, f'Output in {output_filepath}\n')

    #def hf_pred_wid_execute(event):
    #    pstate = event.widget.master.get_uvalue()
    #    hf_pred.exec_file(pstate['exec_file'])
    #    hf_pred.print_w(event.widget.master, f"File {pstate['exec_file']} moved to c:\\itshfbc\\run\\")
    #    hf_pred.print_w(event.widget.master, f"Output in {pstate['exec_file']}_out")

    def hf_pred_wid_execute(self):
        #output_file = os.path.basename(self.exec_file.get())
        filename = self.file_from_date()
        output_filepath = exec_file(filename)  # assuming you want to get the value of the StringVar
        self.text_widget.insert(tk.END, f'File {self.exec_file.get()} moved to C:\\itshfbc\\run\\ \n')
        self.text_widget.insert(tk.END, f'Output in {output_filepath}\n')

    # def hf_pred_wid_execute(self, event, pstate):
    # # Assuming pstate is an object with attributes exec_file and out_file
    #     exec_file = getattr(filename)
    #     out_file = getattr(pstate, 'out_file', None)

    #     if exec_file and out_file:
    #         # Assuming event.top is equivalent to a text widget
    #         event.top.insert("end", f'File {exec_file} moved to c:\\itshfbc\\run\\\n')
    #         event.top.insert("end", f'Output in {out_file}\n')

    # def move_file(source_path, destination_path):
    #     """
    #     Move a file from the source_path to the destination_path.

    #     Parameters:
    #     - source_path (str): Path to the source file.
    #     - destination_path (str): Path to the destination folder.

    #     Returns:
    #     - str: Path to the moved file.
    #     """
    #     #source_path = "C:\\C:\Users\pkhumalo\Desktop\Phumlani_Khumalo\New Python Code"
    #     try:
    #         # Use shutil.move to move the file
    #         moved_file_path = shutil.move(source_path, destination_path)
    #         print(f"File moved successfully to: {moved_file_path}")
    #         return moved_file_path
    #     except Exception as e:
    #         print(f"Error: {e}")
    #         return None
    
    def hf_pred_wid_done(self):
        root.destroy()

    # def exec_file(self, input_file, output_file):
    #     # Perform the execution logic here
    #     # This is just a placeholder; replace it with your actual execution code
    #     with open(input_file, 'r') as infile:
    #         content = infile.read()
    #         # Perform some processing on the content if needed

    #     # Specify the output directory and form the output file path
    #     output_directory = "C:\\itshfbc\\run"
    #     output_filepath = os.path.join(output_directory, output_file)

    #     # Write the processed content to the output file
    #     with open(output_filepath, 'w') as outfile:
    #         outfile.write(content)

    #     return output_filepath
    
    def file_from_date(self):
        # Format the date as a string
        date_str = dt.datetime(int(self.d_year), int(self.d_month), int(self.d_day)).strftime('%Y%m%d')

        # Create the filename using the specified format
        filename = f'ar{date_str}{self.code}.inp'

        return filename

    def update_template(self, contents, d_year, d_month, d_day, ssn, ssn_w, qfe, qfe_w):
        parms = f"Year: {d_year}\nMonth: {d_month}\nDay: {d_day}\nSSN: {ssn}\nSSN Weekly: {ssn_w}\nQFE: {qfe}\nQFE Weekly: {qfe_w}"
        #print(parms)
        filename = self.file_from_date()
        print(filename)
        
        #update_template(contents, d_day, d_year, d_month, ssn, ssn_w, qfe, qfe_w)
        #write_template(self,filename)

        return contents

    #def file_from_date(self):
    #    # Format the date as a string
    #    date_str = datetime(self.d_year, self.d_month, self.d_day).strftime('%Y%m%d')

        # Create the filename using the specified format
    #    filename = f'ar{date_str}{self.code}.inp'

    #    return filename

    #def write_template(self, filename):
    #    with open(filename, 'w') as file:
    #        file.writelines(self.contents)

# Create the main window
root = tk.Tk()
app = HFProcessorApp(root)

# Start the Tkinter event loop
root.mainloop()
