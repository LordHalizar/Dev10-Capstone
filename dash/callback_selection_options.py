import pandas as pd


class VideoGameSelectionOptions:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def _unpack_column(self, column: str, new_name: str) -> pd.DataFrame:
        rows = self.df.copy()
        rows[column] = rows[column].fillna('').str.split(', ')
        rows = rows.explode(column).rename(columns={column: new_name})
        return rows.loc[rows[new_name] != ''].copy()

    def _unpacked_selection_options(self, column: str, new_name: str) -> list[str]:

        options = self._unpack_column(column=column, new_name=new_name)

        return sorted({
            option.strip()
            for option in options[new_name]
            if isinstance(option, str) and option.strip()
        })

    def genre_selection_options(self) -> list[str]:
        return self._unpacked_selection_options(column='genres', new_name='genre')

    def publisher_selection_options(self) -> list[str]:
        return self._unpacked_selection_options(column='publishers', new_name='publisher')