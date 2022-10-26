import tkinter as tk
import tkinter.filedialog as tkfd
from tkinter import ttk
import os

import numpy as np
import pandas as pd
import os
import re

def confirmClobber(output_filename):
    """ Pop a message box to get confirmation that an existing file can be overwritten

        Returns
        -------
        bool: ``True`` if user confirms overwrite (or if filename does not exist), ``False`` if user cancels overwrite
    """
    if not os.path.isfile(output_filename):
        return True
    confirmtxt = "The output filename you selected already exists.\n\nAre you sure you want to overwrite the file?"
    if tk.messagebox.askokcancel("Close", confirmtxt, default="cancel", icon="warning"):
        return True
    return False 

def grLoadDf(filename):
    if filename.lower().endswith("csv"):
        df = pd.read_csv(filename, dtype=str) 
    elif filename.lower().endswith("xlsx"):
        df = pd.read_excel(filename, dtype=str)
    else:
        raise RuntimeError("Cannot load dataframe - unknown filetype: " + filename)
    return df


def grPrepareTestRecords(file_or_dir, event_name, instrument, dictColumns, dictFXLookup, fxs_override=None):
    
    # decide if file_or_dir is a folder or not. 
    # Create a list of filenames (even if its just a filename), then process files in list. 
    file_list = []
    if os.path.isfile(file_or_dir):
        file_list = ([file_or_dir])
    elif os.path.isdir(file_or_dir):
        # get all files in dir
        if fxs_override != None:
            raise RuntimeException("Cannot provide fxsID when using a directory.")
        for f in os.scandir(file_or_dir):
            if (f.is_file() and (f.name.endswith("xlsx") or f.name.endswith("csv"))):
                file_list.append(os.path.join(file_or_dir, f.name))

    # dict for mapping FXS ID to TRAX ID
    #dfLookup = readGrExport(lookup_filename)
    #dictLookup = dict(zip(dfLookup.iloc[:,0], dfLookup.iloc[:,1])) 

    # dict for renaming columns
    #column_dict = dict(zip(old_columns, new_columns))

    # Now get records for each file in list 
    bigdf = None
    for f in file_list:
        print("\nInput file %s" % f)
        df = grLoadDf(f)
        fxs = None
        if fxs_override==None:
            # expect file basename to look like NNNNNN-NNN*
            m=re.match(r"(\d{6}-\d{3}).*", os.path.basename(f))
            if m == None:
                raise RuntimeError("Leading chars of filename must be in FXS format e.g. NNNNNN-NNNwhatever.csv")
            else:
                fxs = m.group(1)
                print("FXS from filename: %s" % fxs)

        else:
            fxs = fxs_override
                
        if fxs in dictFXLookup:
            studyid = dictFXLookup[fxs]
            print("FXS/TRAX ID: %s/%s" % (fxs, studyid))
        else:
            studyid = '000'
            print("FXS not found in lookup table, use 000: %s/%s" % (fxs, studyid))
            #raise RuntimeError("FXS not found in lookup table: " + fxs)
            #continue

        df2 = df[dictColumns.keys()]
        df3 = df2.rename(columns=dictColumns)
        df4 = df3[~df3['test_record_num'].isna()].copy()

        # don't forget to add key columns
        # TODO: HARD CODED KEY COLUMN NAME study_id
        # DJS NO, USE "dem_trax_subj_id", taken from filename or maybe command line
        # DJS NO AGAIN, use study_id and dem_trax_subj_id
        df4.insert(0, "study_id", studyid)
        df4.insert(1, "dem_trax_subj_id", fxs)


        # and don't forget to add the 'redcap_repeat_instance' column and its friend 'redcap_event_name'
        # We use 'new' for the redcap_repeat_instance. The event name has to come with the folder name 
        # as input. 
        df4.insert(2, "redcap_event_name", event_name)
        df4.insert(3, "redcap_repeat_instrument", instrument)
        df4.insert(4, "redcap_repeat_instance", "new")

        # and insert the filename
        df4.insert(5, 'input_filename', os.path.basename(f))

        # Assign testtype based on contents of 'comments'
        df4.insert(6, 'testtype', 5)
        df4.loc[df4.condition_comments.str.contains("control", na=False), 'testtype'] = 1
        df4.loc[df4.condition_comments.str.contains("light", na=False), 'testtype'] = 2
        df4.loc[df4.condition_comments.str.contains("loaded", na=False), 'testtype'] = 3
          
        if bigdf is None:
            bigdf = df4
        else:
            bigdf = pd.concat((bigdf, df4))
    
    return bigdf

if (__name__ == '__main__'):
    import sys

    # get path of this script
    script_folder = os.path.dirname(os.path.realpath(__file__))
    column_names_file = os.path.join(script_folder, 'data', 'column_names.csv')
    lookup_file = os.path.join(script_folder, 'data', 'FX_ID_TRAX_ID_List.xlsx')
    print("This script lives in %s\nExpecting these input files:\nColumn names: %s\nFX/TRAX List: %s\n" % (script_folder, column_names_file, lookup_file))
    
    # load columns
    cdf = grLoadDf(column_names_file)
    dictColumns = dict(zip(cdf.iloc[:,0], cdf.iloc[:,1])) 
    ldf = grLoadDf(lookup_file)
    dictFXLookup = dict(zip(ldf.iloc[:,0], ldf.iloc[:,1])) 

    if len(sys.argv) == 4:
        print(sys.argv[1])
        print(sys.argv[2])
        df = grPrepareTestRecords(sys.argv[1], sys.argv[2], "gaitrite_data_entry", dictColumns, dictFXLookup)
        print("Writing %d records to output file %s\n" % (len(df), sys.argv[3]))
        df.to_csv(sys.argv[3])
    else:
        window = tk.Tk()
        input_folder=tk.StringVar()
        output_filename = tk.StringVar()
        window.title("Create RedCap import for GaitRite data")
        window.geometry('460x150')


        # Input folder
        lbl = tk.Label(window, text="Input Folder:", width=15)
        lbl.grid(row=0, column=0, ipadx=1, ipady=1, sticky='E')
        entryInputFolder = tk.Label(window, textvariable=input_folder, width=40)
        entryInputFolder.grid(row=0, column=1, ipadx=1, ipady=1, sticky='W')


        # called when "Select" button (for folder/file) is pressed
        def select_clicked():
            input_folder.set(tkfd.askdirectory(mustexist=True))
            print('Dirname set to %s\n' % input_folder.get())

        # Now the button itself        
        btn = tk.Button(window, text="Select", command=select_clicked)
        btn.grid(row=0, column=2, ipadx=1, ipady=1, sticky='E')


        # event name
        eventName = tk.StringVar();
        lblEvent = tk.Label(window, text='Event Name:', width=15)
        lblEvent.grid(row=1, column=0, ipadx=1, ipady=1, sticky='E')
        entryEventName = tk.Entry(window, width=40, textvariable=eventName)
        entryEventName.grid(row=1, column=1, ipadx=1, ipady=1, sticky='W')

        
        # output file label
        olbl = tk.Label(window, text="Output file:", width=15)
        olbl.grid(row=2, column=0, ipadx=1, ipady=1, sticky='E')
        oflbl = tk.Label(window, textvariable=output_filename, width=40)
        oflbl.grid(row=2, column=1, ipadx=1, ipady=1, sticky='W')

        def output_file_select_clicked():
            output_filename.set(tkfd.asksaveasfilename(initialdir=r"C:\work\rivera", filetypes=[("csv file", "*.csv")], defaultextension=".csv"))

        # output file select        
        obtn = tk.Button(window, text="Select", command=output_file_select_clicked)
        obtn.grid(row=2, column=2, ipadx=1, ipady=1)

#=======================================

        # go button
        def goClicked():
            print("Input file %s event %s\n" % (input_folder.get(), eventName.get()))
            if len(input_folder.get())==0:
                tk.messagebox.showwarning(title="Input error", message="Please select an input folder")
                return
            elif len(output_filename.get())==0:
                tk.messagebox.showwarning(title="Input error", message="Please select an output file")
                return
            elif len(entryEventName.get())==0:
                tk.messagebox.showwarning(title="Input error", message="Please enter an event name")
                return

            if confirmClobber(output_filename.get()):
                df = grPrepareTestRecords(input_folder.get(), eventName.get(), "gaitrite_data_entry", dictColumns, dictFXLookup)
                print("Writing %d records to output file %s\n" % (len(df), output_filename.get()))
                df.to_csv(output_filename.get())
                # clear dialog
                input_folder.set("")
                output_filename.set("")

        btnGo = tk.Button(window, text='Process GaitRite data & Generate RedCap import file', command=goClicked)
        btnGo.grid(row=3, columnspan=3)

        window.mainloop()
