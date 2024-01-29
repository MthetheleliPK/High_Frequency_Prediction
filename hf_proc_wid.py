import tkinter as tk

from hf_pred import print_w

def hf_proc_wid(Group=0):
    if len(Group) == 0:
        Group = 0

    root = tk.Tk()

    tlb = tk.Frame(root)
    tlb.pack(side=tk.TOP)

    clb1 = tk.Frame(tlb)
    clb1.grid(row=6)

    clb = tk.Frame(tlb)
    clb.grid(column=6)

    # create a place to draw logo
    d_logo = tk.Canvas(clb1, width=264, height=88)
    d_logo.grid(row=0, column=0, padx=5, pady=5)

    slb = tk.Frame(clb1)
    slb.grid(row=2)

    flb = tk.Frame(slb)
    flb.grid(column=3)

    st = tk.Button(flb, text='File', command=lambda: hf_proc_wid_file())
    st.grid(row=0, column=0)
    st = tk.Button(flb, text='Done', command=lambda: hf_proc_wid_done())
    st.grid(row=0, column=1)
    st = tk.Button(flb, text='Back', command=lambda: hf_proc_wid_back())
    st.grid(row=0, column=2)
    st = tk.Button(flb, text='Skip', command=lambda: hf_proc_wid_skip())
    st.grid(row=0, column=3)
    st = tk.Button(flb, text='Write/Next', command=lambda: hf_proc_wid_write())
    st.grid(row=0, column=4)
    st = tk.Button(flb, text='Refresh', command=lambda: hf_proc_wid_refresh())
    st.grid(row=0, column=5)

    blb = tk.Frame(slb)
    blb.grid(row=2, pady=5)

    id0 = tk.Button(blb, text='F1', command=lambda: hf_proc_wid_f1())
    id0.grid(row=0, column=0)
    st = tk.Button(blb, text='F2', command=lambda: hf_proc_wid_f1())
    st.grid(row=0, column=1)
    st = tk.Button(blb, text='F3', command=lambda: hf_proc_wid_f1())
    st.grid(row=0, column=2)
    st = tk.Button(blb, text='F4', command=lambda: hf_proc_wid_f1())
    st.grid(row=0, column=3)
    st = tk.Button(blb, text='F5', command=lambda: hf_proc_wid_f1())
    st.grid(row=0, column=4)
    st = tk.Button(blb, text='F6', command=lambda: hf_proc_wid_f1())
    st.grid(row=0, column=5)
    st = tk.Button(blb, text='F7', command=lambda: hf_proc_wid_f1())
    st.grid(row=0, column=6)
    st = tk.Button(blb, text='F8', command=lambda: hf_proc_wid_f1())
    st.grid(row=0, column=7)
    st = tk.Button(blb, text='F9', command=lambda: hf_proc_wid_f1())
    st.grid(row=0, column=8)
    st = tk.Button(blb, text='F10', command=lambda: hf_proc_wid_f1())
    st.grid(row=0, column=9)
    st = tk.Button(blb, text='F11', command=lambda: hf_proc_wid_f1())
    st.grid(row=0, column=10)
    st = tk.Button(blb, text='F12', command=lambda: hf_proc_wid_f1())
    st.grid(row=0, column=11)

    text = tk.Text(slb, width=85, height=18, wrap=tk.WORD)
    text.grid(row=1, pady=5)

    draw1 = tk.Canvas(tlb, width=550, height=425)
    draw1.grid(row=0, column=0, padx=5, pady=5)

    draw0 = tk.Canvas(tlb, width=550, height=425)
    draw0.grid(row=0, column=1, padx=5, pady=5)

    draw2 = tk.Canvas(tlb, width=550, height=425)
    draw2.grid(row=0, column=2, padx=5, pady=5)

    root.mainloop()

def hf_proc_wid_file(event):
    pstate = event.top.get_uvalue()
    read_file(pstate)
    print_w(event.top, pstate["filename"])
    print_w(event.top, 'records = ' + str(pstate["records"]))
    process_record(pstate)
    print_w(event.top, 'processed rec = ' + str(pstate["rec"] + 1) + ' / ' + str(pstate["records"]))


def hf_proc_wid_done():
    # Your code for the 'Done' button event

def hf_proc_wid_back():
    pstate = event.top.get_uvalue()
    pstate["rec"] -= 1
    if pstate["rec"] < 0:
        pstate["rec"] = 0
    pstate["sel_freq"] = [i+1 for i in range(12)]
    for i in range(12):
        event.widget_control(pstate["id0"] + i, set_button=True)
    process_record(pstate)
    print_w(event.top, 'processed rec = ' + str(pstate["rec"] + 1) + ' / ' + str(pstate["records"]))

def hf_proc_wid_skip():
    pstate = event.top.get_uvalue()
    pstate["rec"] += 1
    if pstate["rec"] > pstate["records"] - 1:
        pstate["rec"] = pstate["records"] - 1
    pstate["sel_freq"] = [i+1 for i in range(12)]
    for i in range(12):
        event.widget_control(pstate["id0"] + i, set_button=True)
    process_record(pstate)
    print_w(event.top, 'processed rec = ' + str(pstate["rec"] + 1) + '

def hf_proc_wid_write():
     pstate = event.top.get_uvalue()

    event.wset(pstate["draw_id0"])
    img0 = Image.open('path_to_your_image0.png')  # Replace with your path
    event.wset(pstate["draw_id1"])
    img1 = Image.open('path_to_your_image1.png')  # Replace with your path
    event.wset(pstate["draw_id2"])
    img2 = Image.open('path_to_your_image2.png')  # Replace with your path

    title = pstate["title"]
    dirname = os.path.dirname(pstate["filename"]) + '/output/'

    if not os.path.exists(dirname):
        print_w(event.top, 'making directory ' + dirname)
        os.makedirs(dirname)

    file = title.split(':')[0].strip()
    file = os.path.join(dirname, file)

    file1 = file + '_muf.png'
    img0.save(file1)
    file2 = file + '_snr.png'
    img1.save(file2)
    file3 = file + '_angle.png'
    img2.save(file3)

    text = 'Output image written to ' + dirname
    print_w(event.top, text)
    print_w(event.top, file1)
    print_w(event.top, file2)
    print_w(event.top, file3)

    pstate["rec"] += 1
    if pstate["rec"] > pstate["records"] - 1:
        pstate["rec"] = pstate["records"] - 1
    pstate["sel_freq"] = [i+1 for i in range(12)]
    for i in range(12):
        event.widget_control(pstate["id0"] + i, set_button=True)
    process_record(pstate)
    print_w(event.top, 'processed rec = ' + str(pstate["rec"] + 1) + '

def hf_proc_wid_refresh():
    pstate = event.top.get_uvalue()
    pstate["sel_freq"] = [i+1 for i in range(12)]
    for i in range(12):
        event.widget_control(pstate["id0"] + i, set_button=True)
    process_record(pstate)
    print_w(event.top, 'processed rec = ' + str(pstate["rec"] + 1) + '

def hf_proc_wid_f1():
    # Your code for the 'F1' button event

# Call the main function
hf_proc_wid()
