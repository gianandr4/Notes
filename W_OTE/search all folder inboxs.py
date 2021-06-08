

import win32com.client
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
lista=0



for si in range(50):
    try:
        box = outlook.GetDefaultFolder(si)
        ms = box.Items
        if not (len(ms)==0 and len(box.folders)==0):
            lista+=len(ms)
            print(si, box.name,":",len(ms))
###############################################################################
        for sj in range(50):
            try:
                boxx = box.folders[sj]
                mss=boxx.Items
                if not (len(mss)==0 and len(boxx.folders)==0):
                    lista+=len(mss)
                    print("  ",sj, boxx.name,len(mss))
###############################################################################
                for sk in range(50):
                    try:
                        boxxx = boxx.folders[sk]
                        msss=boxxx.Items
                        if not (len(msss)==0 and len(boxxx.folders)==0):
                            lista+=len(msss)
                            print("    ",sk, boxxx.name,len(msss))
###############################################################################
                        for sl in range(50):
                            try:
                                boxxxx = boxxx.folders[sk]
                                mssss=boxxx.Items
                                if not (len(mssss)==0 and len(boxxx.folders)==0):
                                    lista+=len(mssss)
                                    print("      ",sl, boxxxx.name,len(mssss))
                            except:pass
                    except:pass
            except:pass
    except:pass
    