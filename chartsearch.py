import pandas as pd
from typing import List, Optional, Union 
class ArcaeaChartFilter:
    def __init__(self, csvpath):
        self.ogcharts=pd.read_csv(csvpath)
        self.filteredcharts=self.ogcharts.copy()
    
    def reset(self):
        self.filteredcharts=self.ogcharts.copy()
    
    def difficulty(self, diffname:Union[str, List[str]]):
        if isinstance(diffname, str):
            diffname=[diffname]
        self.filteredcharts=self.filteredcharts[self.filteredcharts['Difficulty'].isin(diffname)]
        return self
    
    def level(self, levels:Union[str, int, List[Union[str, int]]]):
        if not isinstance(levels, list):
            levels=[levels]
        levels = [str(lv) for lv in levels]
        self.filteredcharts=self.filteredcharts[self.filteredcharts['Lv'].astype(str).isin(levels)]
        return self
    
    def min_level(self, min_level: Union[str, int]):
        def level_to_float(lv):
            lv_str = str(lv)
            if '+' in lv_str:
                return float(lv_str.replace('+', '.7'))
            return float(lv_str)
        
        min_val = level_to_float(min_level)
        self.df_filtered = self.df_filtered[
            self.df_filtered['Lv'].apply(level_to_float) >= min_val
        ]
        return self

    def max_level(self, max_level: Union[str, int]):
        def level_to_float(lv):
            lv_str = str(lv)
            if '+' in lv_str:
                return float(lv_str.replace('+', '.5'))
            return float(lv_str)
        
        max_val = level_to_float(max_level)
        self.df_filtered = self.df_filtered[
            self.df_filtered['Lv'].apply(level_to_float) <= max_val
        ]
        return self
    def cc(self, cc_values: Union[float, List[float]]):
        if not isinstance(cc_values, list):
            cc_values = [cc_values]
        self.df_filtered = self.df_filtered[self.df_filtered['CC'].isin(cc_values)]
        return self
    
    def min_cc(self, min_cc: float):
        self.df_filtered = self.df_filtered[self.df_filtered['CC'] >= min_cc]
        return self
    
    def max_cc(self, max_cc: float):
        self.df_filtered = self.df_filtered[self.df_filtered['CC'] <= max_cc]
        return self
    
    def cc_range(self, min_cc: float, max_cc: float):
        self.df_filtered = self.df_filtered[
            (self.df_filtered['CC'] >= min_cc) & (self.df_filtered['CC'] <= max_cc)
        ]
        return self
    
    def song(self, song_names: Union[str, List[str]], exact: bool = True):
        if isinstance(song_names, str):
            song_names = [song_names]
        
        if exact:
            self.df_filtered = self.df_filtered[self.df_filtered['Song'].isin(song_names)]
        else:
            pattern = '|'.join(song_names)
            self.df_filtered = self.df_filtered[
                self.df_filtered['Song'].str.contains(pattern, case=False, na=False)
            ]
        return self
    
    def song_contains(self, search_term: str):
        self.df_filtered = self.df_filtered[
            self.df_filtered['Song'].str.contains(search_term, case=False, na=False)
        ]
        return self
    
    def artist(self, artist_names: Union[str, List[str]], exact: bool = True):
        if isinstance(artist_names, str):
            artist_names = [artist_names]
        
        if exact:
            self.df_filtered = self.df_filtered[self.df_filtered['Artist'].isin(artist_names)]
        else:
            pattern = '|'.join(artist_names)
            self.df_filtered = self.df_filtered[
                self.df_filtered['Artist'].str.contains(pattern, case=False, na=False)
            ]
        return self
    
    def artist_contains(self, search_term: str):
        self.df_filtered = self.df_filtered[
            self.df_filtered['Artist'].str.contains(search_term, case=False, na=False)
        ]
        return self
    
    def designer(self, designer_names: Union[str, List[str]], exact: bool = True):
        if isinstance(designer_names, str):
            designer_names = [designer_names]
        
        if exact:
            self.df_filtered = self.df_filtered[self.df_filtered['Chart designer'].isin(designer_names)]
        else:
            pattern = '|'.join(designer_names)
            self.df_filtered = self.df_filtered[
                self.df_filtered['Chart designer'].str.contains(pattern, case=False, na=False)
            ]
        return self
    
    def designer_contains(self, search_term: str):
        self.df_filtered = self.df_filtered[
            self.df_filtered['Chart designer'].str.contains(search_term, case=False, na=False)
        ]
        return self
    
    def version(self, versions: Union[str, List[str]]):
        if isinstance(versions, str):
            versions = [versions]
        self.df_filtered = self.df_filtered[self.df_filtered['Version'].isin(versions)]
        return self
    
    def min_notes(self, min_notes: int):
        self.df_filtered = self.df_filtered[self.df_filtered['Notes'].astype(int) >= min_notes]
        return self
    
    def max_notes(self, max_notes: int):
        self.df_filtered = self.df_filtered[self.df_filtered['Notes'].astype(int) <= max_notes]
        return self
    
    def notes_range(self, min_notes: int, max_notes: int):
        notes = self.df_filtered['Notes'].astype(int)
        self.df_filtered = self.df_filtered[(notes >= min_notes) & (notes <= max_notes)]
        return self
    
    def sort_by(self, column: str, ascending: bool = True):
        self.df_filtered = self.df_filtered.sort_values(column, ascending=ascending)
        return self
    
    def get(self, limit: Optional[int] = None) -> pd.DataFrame:
        if limit:
            return self.df_filtered.head(limit)
        return self.df_filtered
    
    def count(self) -> int:
        return len(self.df_filtered)
    
    def to_csv(self, output_path: str):
        self.df_filtered.to_csv(output_path, index=False)
        return self
    
    def print_summary(self, max_rows: int = 10):
        print(f"Total results: {self.count()}")
        print("\n" + "="*80 + "\n")
        
        pd.set_option('display.max_rows', max_rows)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        
        print(self.df_filtered.to_string(index=False))
        
        if self.count() > max_rows:
            print(f"\n... and {self.count() - max_rows} more results")