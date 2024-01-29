import tkinter as tk
from tkinter import filedialog
import time
import os

def read_template(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def julday(month, day, year, hour):
    """
    Calculate the Julian day for a given date and time.

    Parameters:
    - month: Integer, month (1-12).
    - day: Integer, day of the month.
    - year: Integer, year.
    - hour: Float, hour of the day (0-23).

    Returns:
    - Float, Julian day.
    """
    # Check for valid input
    if not (1 <= month <= 12):
        raise ValueError("Invalid month. Month should be between 1 and 12.")
    if not (1 <= day <= 31):
        raise ValueError("Invalid day. Day should be between 1 and 31.")
    if year < 1:
        raise ValueError("Invalid year. Year should be a positive integer.")
    if not (0 <= hour < 24):
        raise ValueError("Invalid hour. Hour should be between 0 and 23.")

    # Handle the special cases of January and February
    if month <= 2:
        month += 12
        year -= 1

    # Formula to calculate the Julian day
    A = year // 100
    B = 2 - A + A // 4
    julian_day = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5 + hour / 24.0

    return julian_day
    
def caldat(jd):
    """
    Convert a Julian date to calendar date components.

    Parameters:
    - jd: Float, Julian date.

    Returns:
    - Dictionary with keys "year", "month", "day", "hour", "minute", "second".
    """
    jd = jd + 0.5  # Adjust to start at noon
    Z = int(jd)
    F = jd - Z

    A = Z
    if Z < 2299161:
        A = Z
    else:
        alpha = int((Z - 1867216.25) / 36524.25)
        A = Z + 1 + alpha - int(alpha / 4)

    B = A + 1524
    C = int((B - 122.1) / 365.25)
    D = int(365.25 * C)
    E = int((B - D) / 30.6001)

    day = B - D - int(30.6001 * E) + F
    month = E - 1 if E <= 13.5 else E - 13
    year = C - 4715 if month > 2.5 else C - 4716

    # Extract hours, minutes, and seconds
    hour = int((F * 24) % 24)
    minute = int((F * 24 * 60) % 60)
    second = int((F * 24 * 60 * 60) % 60)

    return {
        "year": year,
        "month": month,
        "day": int(day),
        "hour": hour,
        "minute": minute,
        "second": second
    }

def update_template(contents, year, month, day, ssn, ssn_w, qfe, qfe_w):
    day_w = day + 3

    # Find line indices for 'LABEL', 'MONTH', 'SUNSPOT'
    line_sel_label = [i for i, line in enumerate(contents) if 'LABEL' in line]
    line_sel_month = [i for i, line in enumerate(contents) if 'MONTH' in line]
    line_sel_sunspot = [i for i, line in enumerate(contents) if 'SUNSPOT' in line]

    months = [' ', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Calculate Julian date and update label_str_w
    jd = julday(month, day, year, 0)
    result = caldat(jd + 6.0)
    month2, day2, year2 = result["month"], result["day"], result["year"] % 100
    label_str_w = f"{day:02d}/{month:02d}/{year % 100:02d}-{day2:02d}/{month2:02d}/{year2:02d}"

    #print(jd)
    #print(result)

    for i in range(len(line_sel_label)):
        # Update LABEL lines
        str_o = contents[line_sel_label[i]]
        b = str_o.find('-')
        meth = 1 if b > 0 else 0
        pos = str_o.find(':')
        str_n = str_o + '   '

        if meth:
            str_n = str_n[:pos + 2] + label_str_w
        else:
            str_n = str_n[:pos + 2] + f"{day:02d}/{months[month]:3}/{year % 100:02d}"

        contents[line_sel_label[i]] = str_n

        # Update MONTH lines
        str_o = contents[line_sel_month[i]]
        day_d = day_w if meth else day
        month_str = f"{year:04d}{month:02d}.{day_d:02d}"
        pos = str_o.find('.')
        str_n = str_n[:pos - 6] + month_str

        contents[line_sel_month[i]] = str_n

        # Update SUNSPOT lines
        str_o = contents[line_sel_sunspot[i]]
        print(str_o)
        ssn_str = f"{ssn_w:.0f}{qfe_w:.1f}" if meth else f"{ssn:.0f}{qfe:.1f}"
        print(ssn_str)
        pos = str_o.find('.')
        str_n = str_n[:pos - 3] + ssn_str

        contents[line_sel_sunspot[i]] = str_n
        print(str_n)
        print(str_o)

        return contents


def file_from_date(code, year, month, day):
    # Format the date components as strings with leading zeros
    year_str = str(year).zfill(4)
    month_str = str(month).zfill(2)
    day_str = str(day).zfill(2)

    # Combine the components to form the filename
    filename = f"{code}_{year_str}{month_str}{day_str}.txt"

    # Optionally, specify a directory path if needed
    directory = "C:\\itshfbc\\run"
    filepath = os.path.join(directory, filename)

    return filepath


def write_template(filename, contents):
    with open(filename, 'w') as file:
        file.write(contents)

def exec_file(input_file, output_file):
    # Perform the execution logic here
    # This is just a placeholder; replace it with your actual execution code
    with open(input_file, 'r') as infile:
        content = infile.read()
        # Perform some processing on the content if needed

    # Specify the output directory and form the output file path
    output_directory = "C:\\itshfbc\\run"
    output_filepath = os.path.join(output_directory, output_file)

    # Write the processed content to the output file
    with open(output_filepath, 'w') as outfile:
        outfile.write(content)

    return output_filepath


def hf_pred_wid_open(pstate):
    file_path = filedialog.askopenfilename(filetypes=[("INP Files", "*.inp")])
    contents = read_template(file_path)
    code = os.path.splitext(os.path.basename(file_path))[0][-3:]

    pstate['file'] = file_path
    pstate['code'] = code
    pstate['contents'] = contents

    print_w(pstate, f"Opened {pstate['file']}")
    pstate['code_i'].set(code)
    pstate['make_button']['state'] = tk.NORMAL
    pstate['exec_button']['state'] = tk.DISABLED

def hf_pred_wid_make_file(pstate):
    contents = pstate['contents']
    update_template(contents, pstate['d_year'], pstate['d_month'], pstate['d_day'],
                    pstate['ssn'], pstate['ssn_w'], pstate['qfe'], pstate['qfe_w'])

    tt = time.time()
    year, month, day, _, _, _ = time.gmtime(tt)
    filename = f"{pstate['code']}{year:04d}{month:02d}{day:02d}.inp"
    write_template(filename, contents)
    pstate['exec_file'] = filename
    pstate['exec_button']['state'] = tk.NORMAL
    print_w(pstate, f"File written {pstate['exec_file']}")

def hf_pred_wid_day_menu(pstate, event):
    pstate['d_day'] = pstate['d_days'][event]
    print(pstate)

def hf_pred_wid_month_menu(pstate, event):
    pstate['d_month'] = pstate['d_months'][event]

def hf_pred_wid_year_menu(pstate, event):
    pstate['d_year'] = pstate['d_years'][event]

def hf_pred_wid_values(pstate, event):
    temp_str = pstate['values'].get()
    if event.widget == pstate['ssn_i']:
        pstate['ssn'] = temp_str
    elif event.widget == pstate['qfe_i']:
        pstate['qfe'] = temp_str
    elif event.widget == pstate['ssn_w_i']:
        pstate['ssn_w'] = temp_str
    elif event.widget == pstate['qfe_w_i']:
        pstate['qfe_w'] = temp_str
    elif event.widget == pstate['code_i']:
        pstate['code'] = temp_str

def hf_pred_wid_execute(pstate):
    exec_file(pstate['exec_file'])
    out_file = f"c:/itshfbc/run/{os.path.basename(pstate['exec_file'])}"
    print_w(pstate, f"File {pstate['exec_file']} moved to c:/itshfbc/run/")
    print_w(pstate, f"Output in {out_file}")

def hf_pred_wid_done(pstate, root):
    root.destroy()

def hf_pred_wid_cleanup(pstate):
    pstate['contents'] = None
    print('done')

def print_w(pstate, text_string):
    pstate['text'].insert(tk.END, text_string + '\n')

def create_widgets(master, pstate):
    frame_date = tk.Frame(master)
    frame_date.pack()

    year_menu = tk.OptionMenu(frame_date, *pstate['d_years'], command=lambda x: hf_pred_wid_year_menu(pstate, x))
    year_menu.pack()

    # Create other widgets here...

if __name__ == "__main__":
    root = tk.Tk()

    pstate = {
        'file': '',
        'code': '',
        'contents': None,
        'd_years': [str(i) for i in range(2000, 2021)],
        # Add other attributes...
    }

    create_widgets(root, pstate)
    pstate['make_button'] = tk.Button(root, text="Make file", state=tk.DISABLED, command=lambda: hf_pred_wid_make_file(pstate))
    pstate['make_button'].pack()

    pstate['exec_button'] = tk.Button(root, text="Execute", state=tk.DISABLED, command=lambda: hf_pred_wid_execute(pstate))
    pstate['exec_button'].pack()

    pstate['text'] = tk.Text(root, width=50, height=10)
    pstate['text'].pack()

    pstate['values'] = tk.StringVar()

    pstate['ssn_i'] = tk.Entry(root, textvariable=pstate['values'])
    pstate['ssn_i'].pack()

    # Add other widgets...

    pstate['d_day'] = 0
    pstate['d_month'] = 0
    pstate['d_year'] = 0

    root.mainloop()
