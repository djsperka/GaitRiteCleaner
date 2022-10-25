import tkinter as tk
import tkinter.filedialog as tkfd
from tkinter import ttk
import os

import numpy as np
import pandas as pd
import os
import re



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

    # load columns
    cdf = grLoadDf("data/column_names.csv")
    dictColumns = dict(zip(cdf.iloc[:,0], cdf.iloc[:,1])) 
    ldf = grLoadDf("data/FX_ID_TRAX_ID_List.xlsx")
    dictFXLookup = dict(zip(ldf.iloc[:,0], ldf.iloc[:,1])) 

    if len(sys.argv) == 4:
        print(sys.argv[1])
        print(sys.argv[2])
        df = grPrepareTestRecords(sys.argv[1], sys.argv[2], "gaitrite_data_entry", dictColumns, dictFXLookup)
        print("Writing %d records to output file %s\n" % (len(df), sys.argv[3]))
        df.to_csv(sys.argv[3])
    else:
        window = tk.Tk()
        filename=tk.StringVar()
        filename.set("None Selected")
        map_filename = tk.StringVar()
        map_filename.set(os.path.join(os.getcwd(), r"data\FX_ID_TRAX_ID_List.xlsx"))
        window.title("Select GaitRite file(s)")
        window.geometry('400x300')


        # first row
        doFolder = tk.IntVar()
        doFolder.set(1)
        lbl = tk.Label(window, text="Folder:")
        lbl.grid(row=0, column=0)
        flbl = tk.Label(window, textvariable=filename, width=60)
        flbl.grid(row=0, column=1)

        # second row
        def chkFolderChanged():
            if (doFolder.get() == 1):
                lbl.config(text='Folder:')
            else:
                lbl.config(text='File:')
        chkFolder = tk.Checkbutton(window, text='Folder?',variable=doFolder, onvalue=1, offvalue=0, command=chkFolderChanged)
        chkFolder.grid(row=1, column=0)

        def select_clicked():
            if doFolder.get() == 0:
                filename.set(tkfd.askopenfilename())
                print('Filename set to %s\n' % filename.get())
            else:
                filename.set(tkfd.askdirectory(mustexist=True))
                print('Dirname set to %s\n' % filename.get())
                
        btn = tk.Button(window, text="Select", command=select_clicked)
        btn.grid(row=1, column=1)

        # event name
        eventName = tk.StringVar();
        lblEvent = tk.Label(window, text='Event Name:')
        lblEvent.grid(row=2, column=0)
        entryEventName = tk.Entry(window, width=20, textvariable=eventName)
        entryEventName.grid(row=2, column=1)

        # go button
        def goClicked():
            print("file %s event %s\n" % (filename.get(), eventName.get()))
            
        btnGo = tk.Button(window, text='Go', command=goClicked)
        btnGo.grid(row=3, column=0)

        window.mainloop()
