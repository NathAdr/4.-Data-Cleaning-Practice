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
