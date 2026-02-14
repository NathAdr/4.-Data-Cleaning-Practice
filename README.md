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
Third, we want to change the data type from string to int using pandas method, we can access it use to_numeric and the data will be int.
```
df['spend'] = pd.to_numeric(df['spend'])
```

## 3. CATEGORICAL TYPOS
We make a correction map for typo categorical that already identified using unique(). From the code, we know there are many typos, such as
Tik_tok, Gogle, Facebok, etc. The idea was, use dictionary map for example {'Facebok':'Facebook'} and goes to all the categorical. After that,
we will replace the old one with the map by using replace method with this syntax:
```
df['channel'] = df['channel'].replace(cleanup_map)
```

## 5. MIXED BOOLEAN 
The idea was same like categorical typos, we make a map for the all boolean that already identified. 1, '1', Yes, Y are True and 0, '0', No, N are False.
Then use map() to apply it. The syntax something like this:
```
df['active'] = df['active'].map(bool_map).fillna(False).astype(bool)
```
The reason of using map() instead replace() was to change everything that ambigous like for example 'maybe' or 'nah' it will converted
to NaN. Also, to avoid NaN we use fillna(False), the NaN data will automaticlly become False. For the astype(), we want to make sure all the data are boolean type.

## 6. DATE PARSING
We want to make sure all the date data are actually date with correct format. We don't want to have many date format or wrong type. So we use pd.to_datetime
to change all the data to datetime format data. The syntax was:
```
df['start_date'] = pd.to_datetime(df['start_date'], errors="coerce")
```
To handle the wrong data, we can make sure use errors="coerce". It will change the data to NaT (Not a Time). 

## 7. LOGICAL HANDLING
There are 2 that we want to check. First, about the ratio between clicks data and impressions data. Data will make sense if the clicks < impressions.
The reason was clicks is how many was clicked and impressions is how many the ads is displayed. We check it with writing this syntax:
```
impossible_mask = df['clicks'] > df['impressions']
```
Second, about the time travel for the campaign. We check the end date and start date. We don't want the end date < start date.
```
time_travel_mask = df['end_date'] < df['start_date']
```
```
df[time_travel_mask, 'end_date'] = df.loc[time_travel_mask, 'start_date'] + pd.Timedelta(days = 30)
```
Basicly, it will add 30 days to the end_date which contained in time_travel_mask. So the data will be ok because not less than start_date.

## 8. OUTLIER HANDLING
We don't want extreme outlier in our data because it will ruin the data for analyze. So to handling the oulier, we use IQR method. First, we search the Q3 and Q1
then IQR. After that, we make a variable called upper_limit to make a boundary for outlier data. In the code, we assume the upper limit was Q3 + (3 * IQR). So
the outlier will be df['spend'] that bigger than upper_limit. Next, the outlier data we change with upper_limit data.
```
df.loc[outlier_mask, ['spend']] = upper_limit
```

## 9. STRING PARSING & NEW COLUMN
We want to know the season of the campaign was with new column, so it will become more easier to see and understand it. Just need to extract from campaign_name,
the result are gonna like: 'Summer', 'Winter', etc.
```
df['season'] = df['campaign_name'].str.extract(r'Q\d_([^_]+)_')
```

This is my learn journey to know and understand how to proper and good in cleaning data. I know this is only some of basic and simple handling and cleaning. 
There are still many bigger problem and much harder than this and there are many rooms for improvement to clean this data, like 'conversions' and 'campaign_tag' column. 
So, I openly accept if there any recommendation, suggestion for this code and explaination and if there any industrial or company actual dataset with bigger data 
that I can get to learn clean it. For the next study, maybe I will use kaggle dataset or else. Thank you if you read this code documentation, 
I appreciate it! I hope it's useful for us.

![Demo](https://media1.tenor.com/m/N7UC9giNRbEAAAAC/kitten-cute.gif)




