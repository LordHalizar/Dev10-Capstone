import os
import pandas as pd

os.chdir(os.path.dirname(__file__))

xl_df = pd.read_excel(r'data\excel\VideoGames_Sales.xlsx')

xl_df = xl_df.drop(columns=['developer', 'critic_score', 'total_sales(mil)', 'pal_sales(mil)', 'other_sales(mil)'])
xl_df['release_date'] = xl_df['release_date'].dt.year
xl_df = xl_df.rename(columns={'release_date': 'release_year'})
xl_df = xl_df.dropna()
print("excel data: \n")
xl_df.info()
xl_year_counts = xl_df['release_year'].sort_values().value_counts()
print(xl_year_counts)
print()

csv_df = pd.read_csv(r'data\csv\Video_Games.csv')
csv_df = csv_df.drop(columns=['Developer', 'User_Count', 'User_Score', 'Critic_Count', 'Critic_Score', 'index', 'EU_Sales', 'Other_Sales', 'Global_Sales', 'Rating'])
csv_df = csv_df.dropna()
print("csv data: \n")
csv_df.info()
csv_year_counts = csv_df['Year_of_Release'].sort_values().value_counts()
print(csv_year_counts)
print()

# vgcsv_df = pd.read_csv(r'data\csv\vgsales.csv')
# vgcsv_df = vgcsv_df.drop(columns=['User_Score', 'Unnamed: 0', 'Critic_Score', 'Rank', 'PAL_Sales', 'Other_Sales', 'Global_Sales', 'Developer'])
# vgcsv_df = vgcsv_df.dropna()
# print("vgcsv data: \n")
# vgcsv_df.info()
# vgcsv_year_counts = vgcsv_df['Year'].sort_values().value_counts()
# print(vgcsv_year_counts)
# print()