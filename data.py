import pandas as pd
import numpy as np

df = pd.read_csv('marketing_campaign_data_messy.csv')
print(f'Loaded dataset: {df.shape[0]} rows , {df.shape[1]} columns') #mau liat seberapa banyak data dalam baris kolom

#Head (columns) cleaning
print(df.columns.tolist())
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_') #nama kolom yang ada spasi dihapus, diganti, dihurufkecilkan
print('FIX')
print(df.columns.tolist())

#Type conversion & currency cleaning
dirty_spend_mask = df['spend'].astype(str).str.contains(r'\$') 
print(df.loc[dirty_spend_mask, ['campaign_id', 'spend']].head(3))
df['spend'] = df['spend'].astype(str).str.replace(r'[^\d.-]','',regex=True) #menghilangkan simbol dollar pada data karena data spend harus berupa numerik untuk diolah
df['spend'] = pd.to_numeric(df['spend'])
print('FIX')
print(df.loc[dirty_spend_mask, ['campaign_id', 'spend']].head(3))

#Categorical typos
print(df['channel'].unique())
cleanup_map = { #untuk data kategorikal menggunakan map yang dibuat lalu direplace
  'Facebok':'Facebook',
  'Tik_Tok':'TikTok',
  'Insta_gram':'Instagram',
  'E-mail':'Email',
  'Gogle':'Google Ads',
  'N/A':np.nan
}
df['channel'] = df['channel'].replace(cleanup_map)
print('FIX')
print(df['channel'].unique())

#Mixed boolean
print(df['active'].unique())
bool_map = { #menggunakan map juga lalu direplace
  'Y':True,
  'Yes':True,
  '1':True,
  1:True,
  'No':False,
  'N':False,
  '0':False,
  0:False
}
df['active'] = df['active'].map(bool_map).fillna(False).astype(bool)
print('FIX')
print(df['active'].unique())

#Date parsing
print(df['start_date'].dtype) #cek tipe data 

df['start_date'] = pd.to_datetime(df['start_date'], errors="coerce") 
df['end_date'] = pd.to_datetime(df['end_date'], dayfirst=True, errors="coerce") #benerin dg diubah ke format datetime

print('FIX')
print(df['start_date'].dtype)

df = df.loc[:, ~df.columns.duplicated()] #hapus kolom duplikat yaitu clicks
print(df.columns.tolist())

#-- bbrp handling
#jml click > jml impresi (ini seharusnya g mungkin terjadi)
impossible_mask = df['clicks'] > df['impressions']
print(df.loc[impossible_mask, ['campaign_id', 'clicks', 'impressions']].head(3))

#time travel; end date < start date (ini seharusnya g mungkin terjadi)
time_travel_mask = df['end_date'] < df['start_date']
print(df.loc[time_travel_mask, ['campaign_id', 'start_date', 'end_date']].head(3))

df.loc[time_travel_mask, 'end_date'] = df.loc[time_travel_mask, 'start_date'] + pd.Timedelta(days=30)
print('FIX')
print(df.loc[time_travel_mask, ['campaign_id', 'start_date', 'end_date']].head(3))

#outlier handling

#string parsing