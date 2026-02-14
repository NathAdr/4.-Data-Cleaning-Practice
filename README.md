In this data cleaning practice, I watched and learnt from youtube channel called "Lore So What". 
This is the video link: https://www.youtube.com/watch?v=NeJKaolLQqU . For the dataset, you can download from here:
https://drive.google.com/drive/folders/135-0Mi2697S0-1INCyfPb03qc2EgQPvt

So, there are 9 part for cleaning the data and I will explain my understanding.

## 1. HEAD CLEANING
If you already download the dataset and saw it. You will realize some of the column name have different format and duplicated column,
like ' Campaign_id' has a space before the text and the other column 'Campaign_name' no have space, etc. We want to clean that format and want to lowercase
like 'spend', 'campaign_id', etc. We using string method called strip, lower, and replace. Strip for deleting the space after and before the text, 
lower for lowering the capital letter, and replace for changing the space with something we set, in this case we want the space change to '_'. 
For example, 'campaign id' to 'campaign_id'. 

Because this is python, we just need to write this: 
```
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
```
For the duplicated column, we use ~, duplicated and loc. This is something new too for me. So, the syntax:
```
df = df.loc[:, ~df.columns.duplicated()]
```
duplicated() is from pandas library. df.columns.duplicated() will outputing something like ['False', 'False', 'True', 'False']. 
The 'True' output is a duplicate column from the previous column. After that, because we used ~ it reverse the boolean output.
'True' become 'False' and 'False' become 'True'. With df.loc[: , ], we only take all the 'True' output and the duplicated will gone.

## 2. TYPE CONVERSION & CURRENCY CLEANING
We use 'spend' column, some of the data have '$' sign. We need to delete the dollar sign and change the type of data from string to int 
because we will use the column for analyze it later. 

First syntax, we make a variable to save the dirty data. We searching data that has dollar sign use contains method. 
This syntax use to locate data later using df.loc[] to assuring there are dirty data.
```
dirty_mask_spend = df['spend'].astype(str).str.contains(r\'$')
```
Second syntax, we replace the dollar sign with '' none using replace method. It will change from '$400' to '400'. But, importantly the
data type still string not int.
```
df['spend'] = df['spend'].astype(str).str.replace(r'[^\d.-]','',regex=True)
```
Third, we want to change the data type from string to int using pandas method, we can access it to_numeric and the data will be int.
```
df['spend'] = pd.to_numeric(df['spend'])
```












