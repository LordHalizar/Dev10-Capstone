import pandas as pd


class VideoGameDataFrames:
    def __init__(self, df: pd.DataFrame, sales_regions: list[str] | None = None):
        self.df = df.copy()
        self.sales_regions = (
            sales_regions
            if sales_regions is not None
            else ['na_sales', 'jp_sales']
        )

    def _source_df(self, df: pd.DataFrame | None = None) -> pd.DataFrame:
        return self.df if df is None else df

    def _unpack_column(self, df: pd.DataFrame, column: str, new_name: str) -> pd.DataFrame:
        rows = df.copy()
        rows[column] = rows[column].fillna('').str.split(', ')
        rows = rows.explode(column).rename(columns={column: new_name})
        return rows.loc[rows[new_name] != ''].copy()

    def _unpacked_genres_df(self, df: pd.DataFrame | None = None) -> pd.DataFrame:
        source = self._source_df(df)
        return self._unpack_column(df=source, column='genres', new_name='genre')

    def _unpacked_publishers_df(self, df: pd.DataFrame | None = None) -> pd.DataFrame:
        source = self._source_df(df)
        return self._unpack_column(df=source, column='publishers', new_name='publisher')

    def _combine_numeric_columns(self, df: pd.DataFrame, columns: list[str], new_name: str) -> pd.DataFrame:
        result = df.copy()
        result[new_name] = result[columns].fillna(0).sum(axis=1)
        return result

    def _combine_sales_regions(self, df: pd.DataFrame | None = None) -> pd.DataFrame:
        source = self._source_df(df)
        return self._combine_numeric_columns(df=source, columns=self.sales_regions, new_name='sales')

    def _sales_by_year_column_df(self, df: pd.DataFrame, column: str):
        sales_agg = {
            region: (region, 'sum')
            for region in self.sales_regions
        }

        df = (
            df
            .groupby(['release_year', column], as_index=False)
            .agg(**sales_agg)
        )
        return df

    def sales_by_year_genre_df(self) -> pd.DataFrame:
        df = self._unpacked_genres_df()
        return self._sales_by_year_column_df(df=df, column='genre')

    def sales_by_year_platform_df(self) -> pd.DataFrame:
        return self._sales_by_year_column_df(df=self.df, column='platform_name')

    def sales_by_year_publisher_df(self) -> pd.DataFrame:
        df = self._unpacked_publishers_df()
        return self._sales_by_year_column_df(df=df, column='publisher')

    def animated_sales_by_year_genre_df(self) -> pd.DataFrame:
        source = self._unpacked_genres_df()
        source[self.sales_regions] = source[self.sales_regions].fillna(0)

        source = source.dropna(subset=['release_year', 'genre'])

        totals = self._sales_by_year_column_df(df=source, column='genre')

        years = sorted(totals['release_year'].unique())
        genres = sorted(totals['genre'].unique())

        full_index = pd.MultiIndex.from_product(
            [years, genres],
            names=['release_year', 'genre']
        )

        return (
            totals.set_index(['release_year', 'genre'])
            .reindex(full_index, fill_value=0)
            .reset_index()
        )