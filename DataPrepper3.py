# %% Takes a two input files that need to be located in same folder as this script. Name the workbook file "workbook"
# %% and name the csv file "data"

import pandas as pd


### Loop the data lines
with open("data.csv", 'r') as temp_f:
    # get No of columns in each line
    col_count = [ len(l.split(",")) for l in temp_f.readlines() ]

### Generate column names  (names will be 0, 1, 2, ..., maximum columns - 1)
column_names = [i for i in range(0, max(col_count))]



### Read csv
df = pd.read_excel("../QuestionnaireDataPrepper_Python/workbook.xlsx", header=None)
df2 = pd.read_csv("../QuestionnaireDataPrepper_Python/data.csv", header=None, delimiter=",", names=column_names)

#%% df1 Prep
#getting name of questionnaire
name = df.iloc[0][0]
name = name[15:]
name = name.rstrip()

#deleting first 2 rows
df = df.iloc[2:]

df.columns = df.iloc[0]
df = df[1:]

#moving AlexID to front
col = df.pop("AlexID")
df.insert(0, col.name, col)

#Dropping from after Alex to Existing Contact
df = df.drop(df.iloc[:, 1:df.columns.get_loc("Existing Contact")+1], axis = 1)

#%%
if 'datetime - time' in df:
    df = df.drop('datetime - time', 1)
if 'Imported' in df:
   df = df.drop('Imported', 1)
   
df['datetime - date'] = pd.to_datetime(df['datetime - date'])
df['date'] = df['datetime - date'].dt.date

## popping date column and putting it where old one is, than dropping old date column
col = df.pop("date")
df.insert(df.columns.get_loc("datetime - date"), col.name, col)
df = df.drop('datetime - date', 1)

#dropping specific edge case columns
if 'Form Key Pass' in df:
    df = df.drop('Form Key Pass', 1)

#%% df2 Prep
#deleting first 2 rows
df2 = df2.iloc[2:]

df2.columns = df2.iloc[0]
df2 = df2[1:]

if 'alexid_17' in df2:
    col = df2.pop("alexid_17")
    
    df2.insert(0, col.name, col)
    df2 = df2.rename(columns = {'alexid_17':'AlexID'})
elif 'alexid_17' in df2:
    col = df2.pop("AlexID")
    df2.insert(0, col.name, col)

df2 = df2.iloc[:,0:df2.columns.get_loc("webform_serial")]



#%%

#list of columns being removed from df2, checking if they exist before removal
if 'id' in df2:
    df2 = df2.drop('id', 1)
if 'is_deceased' in df2:
   df2 = df2.drop('is_deceased', 1) 
if 'actlimitations1_23' in df2:
    df2 = df2.drop('actlimitations1_23', 1)
if 'actlimitations2_24' in df2:
    df2 = df2.drop('actlimitations2_24', 1)
if 'refby_25' in df2:
    df2 = df2.drop('refby_25', 1)
if 'neighb_27' in df2:
    df2 = df2.drop('neighb_27', 1)
if 'popgrp_other_29' in df2:
    df2 = df2.drop('popgrp_other_29', 1)
if 'homelang_other_30' in df2:
    df2 = df2.drop('homelang_other_30', 1)
if 'genderwritein_84' in df2:
    df2 = df2.drop('genderwritein_84', 1)
if 'appt_reminder_88' in df2:
    df2 = df2.drop('appt_reminder_88', 1)
if 'pregnant_89' in df2:
    df2 = df2.drop('pregnant_89', 1)
if 'imm_other_96' in df2:
    df2 = df2.drop('imm_other_96', 1)
if 'indigenousband_97' in df2:
    df2 = df2.drop('indigenousband_97', 1)
if 'indigenoustreaty_98' in df2:
    df2 = df2.drop('indigenoustreaty_98', 1)
if 'abhealth_118' in df2:
    df2 = df2.drop('abhealth_118', 1)
if 'emergencycontact_120' in df2:
    df2 = df2.drop('emergencycontact_120', 1)
if 'emergencyphone_121' in df2:
    df2 = df2.drop('emergencyphone_121', 1)
if 'emergencyrelationship_122' in df2:
    df2 = df2.drop('emergencyrelationship_122', 1)
if 'researchconsent_date_234' in df2:
    df2 = df2.drop('researchconsent_date_234', 1)
if 'researchconsent_status_251' in df2:
    df2 = df2.drop('researchconsent_status_251', 1)
if 'secondlang_262' in df2:
    df2 = df2.drop('secondlang_262', 1)


#%% merge

df = df.dropna(thresh=len(df.columns)-3)
df3 = df.merge(df2, left_on='AlexID', right_on="AlexID")

csvName = 'Processed_'+name+'.csv'

df3.to_csv(csvName, index=False)
