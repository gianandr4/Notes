import pyperclip
import pandas as pd

x = '''https://quickchart.io/chart?bkg=white&c={type:%27bar%27,data:{labels:
[1997,2001,2002,2003,2004,2005,2006,2007,2009,2012,2014,2015,2016,2017,2018,2019,2020,2021,2000,2008,2010,2011,2013,1991,1996,1999,1986,1994,1995,1987,1988,1992,1993,1998,1989]
,datasets:[{label:%27Citations_Per_Year%27,data:
[214,462,948,976,993,547,558,523,721,662,228,431,325,250,227,191,91,24,353,601,786,831,508,0,40,391,21,47,25,7,91,157,39,203,0]
}]}}'''

x = '''
https://quickchart.io/chart?bkg=white&c={type:%27bar%27,data:{labels:
[1997,2001,2002,2003,2004,2005,2006,2007,2009,2012,2014,2015,2016,2017,2018,2019,2020,2021,2000,2008,2010,2011,2013,1991,1996,1999,1986,1994,1995,1987,1988,1992,1993,1998,1989]
,datasets:[{label:%27Citations_Per_Year%27,data:
[214,462,948,976,993,547,558,523,721,662,228,431,325,250,227,191,91,24,353,601,786,831,508,0,40,391,21,47,25,7,91,157,39,203,0]
}]}}
'''






'''

https://quickchart.io/chart?bkg=white&c={type:%27bar%27,data:{labels:
[1984,1997,2001,2002,2003,2004,2005,2006,2007,2009,2012,2014,2015,2016,2017,2018,2019,2020,2021,2000,2008,2010,2011,2013,1991,1996,1999,1986,1994,1995,1987,1988,1992,1993,1998,1989]
,datasets:[{label:%27Publications_Per_Year%27,data:
[2,17,27,18,24,12,14,17,13,5,21,18,36,40,38,29,27,25,21,3,8,14,15,14,2,4,5,1,4,1,1,2,1,1,5,3]
}]}}


'''

while True:
    try:
        ("GETTING CLIPBOARD")
        original = pyperclip.waitForNewPaste()
        x= original

        x = x.replace(r'https://quickchart.io/chart?bkg=white&c={type:%27bar%27,data:{labels:','')
        x = x.replace(r',datasets:[{label:%27Citations_Per_Year%27,data:','')
        x = x.replace(r',datasets:[{label:%27Publications_Per_Year%27,data:','')
        x = x.replace(r'}]}}','')

        x = x.replace('][','],[')
        x = "["+x+"]"
        x = eval(x)

        year = x[0]
        old_year = str(x[0]).replace(' ','')
        values = x[1]
        old_values = str(x[1]).replace(' ','')


        x = list(zip(x[0], x[1]))

        df = pd.DataFrame(x).sort_values(by=0)

        new_year = str(df[0].to_list()).replace(' ','')
        new_values = str(df[1].to_list()).replace(' ','')

        original = original.replace(old_year, new_year)
        original = original.replace(old_values, new_values)

        print("PASTE")

        pyperclip.copy(original)
        # pyperclip.paste()

    except:continue

