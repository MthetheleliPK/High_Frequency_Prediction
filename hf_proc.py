import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import tkinter as tk
from tkinter import filedialog

def read_out(filename, out_str, lines):
    # Read the entire file into a list of strings
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Join the list of strings into a single string
    out_str = ''.join(lines)

    return out_str, lines

def find_match(out_str, search_str, line_sel, col_gt=0):
    if col_gt is None:
        col_gt = 0

    line_sel = np.array([])
    lines = len(out_str)
    for i in range(lines):
        b = out_str[i].find(search_str)
        if b > col_gt:
            line_sel = np.append(line_sel, i)
    line_sel = line_sel.astype(int)

def legend_bad(pos):
    plt.plot([0, 1], [0, 1], 'w-')  # No data plot to create an empty canvas
    plt.fill_between([0, 1], 0, 1, color='w')  # Fill with white to clear the canvas
    plt.text(pos[0], pos[1] - 0.05, 'Comm !Cdifficult', color='black', ha='left', va='center')

def legend_hf(label, colr, sym, pos, rev=False, sel_freq=None):
    if sel_freq is None:
        sel_freq = np.arange(len(label)) + 1

    lab = np.array(label)
    col = np.array(colr)
    syms = np.array(sym)
    s_freq = np.array(sel_freq)
    if rev:
        lab = lab[::-1]
        col = col[::-1]
        syms = syms[::-1]
        s_freq = s_freq[::-1]

    step = 1 / 14.0
    plt.plot([0, 1], [0, 1], 'w-')  # No data plot to create an empty canvas
    plt.fill_between([0, 1], 0, 1, color='w')  # Fill with white to clear the canvas

    for j in range(len(lab)):
        i = np.where(s_freq == 1)[0][0]
        plt.plot([0.0, 0.3], (i + 1) * step * np.array([1, 1]), color=col[i], linewidth=2)
        plt.plot([0.15, 0.15], (i + 1) * step * np.array([1, 1]), color=col[i], marker=syms[i])
        plt.text(0.325, (i + 0.75) * step, lab[i], fontsize=15)

def check_title(title):
    code = title.split(':')
    if code[0] == 'MUSINA_MASVINGO_ZW':
        code[0] = 'MUSINA_MASVINGO'
    # ... (additional replacements)

    title = ':'.join(code)

def decode_record(out_str, line_sel, rec_no, sel_freq, draw0, draw1, draw2, title):
    if sel_freq is None:
        sel_freq = np.arange(12) + 1

    page1 = line_sel[rec_no]
    page2 = line_sel[rec_no + 1]
    page3 = line_sel[rec_no + 2]

    title = out_str[page1 + 3].strip()
    b = title.find('AZI')
    title = title[:b].strip()

    check_title(title)

    proc_str = out_str[page1:page3 + 1]

    find_match(proc_str, 'FREQ', ll_sel)
    freqs = proc_str[ll_sel]

    find_match(proc_str, 'ANGLE', ll_sel)
    angles = proc_str[ll_sel]

    if len(ll_sel) > 12:
        angles = angles[np.arange(12) * 2]  # remove the angler fields

    find_match(proc_str, 'SNR', ll_sel, col_gt=65)
    snrs = proc_str[ll_sel]

    t = np.zeros(12, dtype=int)
    angle = np.zeros((13, 12), dtype=float)
    snr = np.zeros((13, 12), dtype=float)
    freq = np.array([f.split()[1] for f in freqs])
    freq[0] = 'MUF'

    for i in range(12):
        t[i] = int(freqs[i].split()[0])
        angle[i + 1, :] = [float(a.split()[0]) for a in angles[i].split()]
        snr[i + 1, :] = [float(s.split()[0]) for s in snrs[i].split()]

    t = np.concatenate(([0], t))
    angle[0, :] = angle[0, :]
    snr[0, :] = snr[0, :]

    labels = out_str[page3 + 11].strip()
    values = out_str[page3 + 13:page3 + 36 + 1]

    ut, ltt, fot, hpf, esmuf, muf, luf = np.zeros(24), np.zeros(24), np.zeros(24), np.zeros(24), np.zeros(24), np.zeros(
        24), np.zeros(24)

    for i in range(24):
        v2 = [float(v) for v in values[i].split()]
        ut[i], ltt[i], fot[i], hpf[i], esmuf[i], muf[i], luf[i] = v2

    if len(draw0) > 0:
        plt.figure(draw0)
    else:
        plt.figure(0)

    plot_muf(ut, muf, luf, hpf, fot, title)

    if len(draw1) > 0:
        plt.figure(draw1)
    else:
        plt.figure(1)

    plot_hf(t, snr, freq, sel_freq, title, 'SNR!C (dB)')

    if len(draw2) > 0:
        plt.figure(draw2)
    else:
        plt.figure(2)

    plot_hf(t, angle, freq, sel_freq, title, 'Take-off!C Angle!C  (deg)')

def plot_muf(ut, muf, luf, hpf, fot, title):
    plt.clf()
    plt.figure(0)
    t2 = np.arange(0, 24.1, 0.1)
    col = [[0, 64, 96, 10]]
    plt.plot(ut, hpf, color=col[0], marker='o', markersize=8, linewidth=2, label='HPF')
    z = spline(ut, hpf, t2)
    plt.plot(t2, z, color=col[0], linewidth=2)

    plt.plot(ut, muf, color=col[0], marker='s', markersize=8, label='MUF')
    z = spline(ut, muf, t2)
    plt.plot(t2, z, color=col[0], linewidth=2)

    plt.plot(ut, fot, color=col[0], marker='^', markersize=8, label='FOT')
    z = spline(ut, fot, t2)
    plt.plot(t2, z, color=col[0], linewidth=2)

    b = np.where(luf > 0)[0]
    sym_s = -1 if len(b) == 24 else 1
    if len(b) > 1:
        plt.plot(ut[b], luf[b], color=col[0], marker='v', markersize=8 * sym_s)
    b = np.where(luf <= 0)[0]
    if len(b) > 0:
        for i in range(len(b)):
            x1 = ut[b[i]] - 0.5
            x2 = x1 + 1.0
            if b[i] == 0:
                x1 = 0
            if x2 > 24:
                x2 = 24
            y1, y2 = plt.ylim()
            plt.fill_between([x1, x1, x2, x2], [y1, y2, y2, y1], color='w', alpha=0.5)

    legend_bad([0.895, 0.85, 0.945, 0.9])
    plt.legend(loc='upper left')
    plt.xlabel('UT (h)')
    plt.ylabel('MHz')
    plt.title(title)

def plot_hf(t, sig, freq, sel_freq, title, ytitle):
    plt.clf()
    plt.figure(1)
    sym = [1, 2, 4, 5, 6, 7, 1, 2, 4, 5, 6, 7]
    col = np.arange(12) * 16
    plt.plot([0, 1], [0, 1], 'w-')  # No data plot to create an empty canvas
    plt.fill_between([0, 1], 0, 1, color='w')  # Fill with white to clear the canvas

    plt.plot(t, sig[:, 0], color='k', marker='o', markersize=8, linewidth=2, label='SNR!C (dB)')
    plt.ylim([0, max(sig) + 5])
    plt.xticks(np.arange(0, 24, 6), [0, 4, 8, 12, 16, 20, 24])
    plt.grid(True, linestyle='--', alpha=0.7)

    plt.title(title)
    plt.xlabel('UT (h)')
    plt.ylabel(ytitle)
    plt.legend(loc='upper left')

    t2 = np.arange(0, 24.1, 0.1)

    for i in range(12):
        if sel_freq[i] == 1:
            plt.plot(t, sig[:, i], color=col[i], marker=sym[i], label=freq[i])
            z = spline(t, sig[:, i], t2)
            plt.plot(t2, z, color=col[i], linewidth=2)

    legend_hf(freq, col, sym, [0.895, 0.12, 0.99, 0.9], rev=True, sel_freq=sel_freq[:i + 1])

def main():
    root = tk.Tk()
    filename = filedialog.askopenfilename(filetypes=[('All Files', '*.*')])
    out_str, lines = [], []
    read_out(filename, out_str, lines)
    line_sel = np.arange(0, len(out_str), 3)
    rec_no = 0
    sel_freq = np.arange(12) + 1
    draw0, draw1, draw2 = 0, 1, 2
    title = ""
    decode_record(out_str, line_sel, rec_no, sel_freq, draw0, draw1, draw2, title)
    plt.show()

if __name__ == "__main__":
    main()
