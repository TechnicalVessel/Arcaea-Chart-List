import sys
try:
    import pandas as pd
except ImportError:
    print("pandas library required. Install with: 'pip install pandas'")
    sys.exit()
from typing import List, Optional, Union 
from random import randint
import time

class ArcaeaChartFilter:
    def __init__(self, csvpath=None):
        if csvpath==None:
            self.ogcharts=pd.read_csv("arcaea_chart_list.csv")
        else:
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
        self.filteredcharts = self.filteredcharts[
            self.filteredcharts['Lv'].apply(level_to_float) >= min_val
        ]
        return self

    def max_level(self, max_level: Union[str, int]):
        def level_to_float(lv):
            lv_str = str(lv)
            if '+' in lv_str:
                return float(lv_str.replace('+', '.5'))
            return float(lv_str)
        
        max_val = level_to_float(max_level)
        self.filteredcharts = self.filteredcharts[
            self.filteredcharts['Lv'].apply(level_to_float) <= max_val
        ]
        return self
    def cc(self, cc_values: Union[float, List[float]]):
        if not isinstance(cc_values, list):
            cc_values = [cc_values]
        self.filteredcharts = self.filteredcharts[self.filteredcharts['CC'].isin(cc_values)]
        return self
    
    def min_cc(self, min_cc: float):
        self.filteredcharts = self.filteredcharts[self.filteredcharts['CC'] >= min_cc]
        return self
    
    def max_cc(self, max_cc: float):
        self.filteredcharts = self.filteredcharts[self.filteredcharts['CC'] <= max_cc]
        return self
    
    def cc_range(self, min_cc: float, max_cc: float):
        self.filteredcharts = self.filteredcharts[
            (self.filteredcharts['CC'] >= min_cc) & (self.filteredcharts['CC'] <= max_cc)
        ]
        return self
    
    def song(self, song_names: Union[str, List[str]], exact: bool = True):
        if isinstance(song_names, str):
            song_names = [song_names]
        
        if exact:
            self.filteredcharts = self.filteredcharts[self.filteredcharts['Song'].isin(song_names)]
        else:
            pattern = '|'.join(song_names)
            self.filteredcharts = self.filteredcharts[
                self.filteredcharts['Song'].str.contains(pattern, case=False, na=False)
            ]
        return self
    
    
    def song_contains(self, search_term: str):
        self.filteredcharts = self.filteredcharts[
            self.filteredcharts['Song'].str.contains(search_term, case=False, na=False)
        ]
        return self
    
    def artist(self, artist_names: Union[str, List[str]], exact: bool = True):
        if isinstance(artist_names, str):
            artist_names = [artist_names]
        
        if exact:
            self.filteredcharts = self.filteredcharts[self.filteredcharts['Artist'].isin(artist_names)]
        else:
            pattern = '|'.join(artist_names)
            self.filteredcharts = self.filteredcharts[
                self.filteredcharts['Artist'].str.contains(pattern, case=False, na=False)
            ]
        return self
    
    def artist_contains(self, search_term: str):
        self.filteredcharts = self.filteredcharts[
            self.filteredcharts['Artist'].str.contains(search_term, case=False, na=False)
        ]
        return self
    
    def designer(self, designer_names: Union[str, List[str]], exact: bool = True):
        if isinstance(designer_names, str):
            designer_names = [designer_names]
        
        if exact:
            self.filteredcharts = self.filteredcharts[self.filteredcharts['Chart designer'].isin(designer_names)]
        else:
            pattern = '|'.join(designer_names)
            self.filteredcharts = self.filteredcharts[
                self.filteredcharts['Chart designer'].str.contains(pattern, case=False, na=False)
            ]
        return self
    
    def designer_contains(self, search_term: str):
        self.filteredcharts = self.filteredcharts[
            self.filteredcharts['Chart designer'].str.contains(search_term, case=False, na=False)
        ]
        return self
    
    def version(self, versions: Union[str, List[str]]):
        if isinstance(versions, str):
            versions = [versions]
        self.filteredcharts = self.filteredcharts[self.filteredcharts['Version'].isin(versions)]
        return self
    
    def min_notes(self, min_notes: int):
        self.filteredcharts = self.filteredcharts[self.filteredcharts['Notes'].astype(int) >= min_notes]
        return self
    
    def max_notes(self, max_notes: int):
        self.filteredcharts = self.filteredcharts[self.filteredcharts['Notes'].astype(int) <= max_notes]
        return self
    
    def notes_range(self, min_notes: int, max_notes: int):
        notes = self.filteredcharts['Notes'].astype(int)
        self.filteredcharts = self.filteredcharts[(notes >= min_notes) & (notes <= max_notes)]
        return self
    
    def sort_by(self, column: str, ascending: bool = True):
        self.filteredcharts = self.filteredcharts.sort_values(column, ascending=ascending)
        return self
    
    def get(self, limit: Optional[int] = None) -> pd.DataFrame:
        if limit:
            return self.filteredcharts.head(limit)
        return self.filteredcharts
    
    def count(self) -> int:
        return len(self.filteredcharts)
    
    def to_csv(self, output_path: str):
        self.filteredcharts.to_csv(output_path, index=False)
        return self
    
    def print_summary(self, max_rows: int = 10):
        print(f"Total results: {self.count()}")
        print("\n" + "="*80 + "\n")
        
        pd.set_option('display.max_rows', max_rows)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        
        print(self.filteredcharts.to_string(index=False))
        
        if self.count() > max_rows:
            print(f"\n... and {self.count() - max_rows} more results")
    
    def Score(self, song, difficulty, exact=True):
        try:
            import keyboard
        except ImportError:
            print("keyboard library required. Install with: 'pip install keyboard'")
            return None
        
        rank_thresholds = {
            'PM': 10000000,
            'EX+': 9900000,
            'EX': 9800000,
            'AA': 9500000,
            'A': 9200000,
            'B': 8900000,
            'C': 8600000,
            'D': 0
        }
        
        if isinstance(song, str):
            song = [song]
        if exact:
            temp = self.ogcharts[self.ogcharts['Song'].isin(song)]
        else:
            pattern = '|'.join(song)
            temp = self.ogcharts[
                self.ogcharts['Song'].str.contains(pattern, case=False, na=False)
            ]
        if isinstance(difficulty, str):
            difficulty = [difficulty]
        temp = temp[temp['Difficulty'].isin(difficulty)]

        if temp.empty:
            return {'Status': 'Chart not found'}
        
        row = temp.iloc[0]
        notecount = int(row['Notes'])
        purescore = 10000000 / notecount
        purecount = 0
        playrating=0.00
        mod=None
        def display_score():
            total_score = int(purecount * purescore)
            lost_from_input = purecount
            current_lost = notecount - lost_from_input
            if(total_score>9800000 and total_score<10000000):
                mod=1.0+((total_score-9800000)/200000)
            elif(total_score==10000000):
                mod=2
            else:
                mod=(total_score-9800000)/300000
            playrating=round(max(float(row['CC'])+mod, 0.0), 2)
            print(f"\r\033[KScore: {total_score:,} | Pure: {purecount} | Lost: {current_lost} (Max notes: {notecount}) | Potential Rating: {playrating}", end='', flush=True)
        
        print("\n" + "="*80)
        print(f"Song: {row['Song']} | Difficulty: {row['Difficulty']} | Notes: {notecount}")
        print("="*80)
        print("Controls:")
        print("  Right Arrow        : +1 Pure")
        print("  Left Arrow         : -1 Pure")
        print("  Ctrl+Right         : +100 Pure")
        print("  Ctrl+Left          : -100 Pure")
        print("  Shift+Right        : Max Pure")
        print("  Shift+Left         : 0 Pure")
        print("  Q                  : Quit")
        print("="*80 + "\n")
        
        try:
            while True:
                display_score()
                
                if keyboard.is_pressed('shift+right'):
                    purecount = notecount
                    time.sleep(0.15)  
                    
                elif keyboard.is_pressed('shift+left'):
                    purecount = 0
                    time.sleep(0.15)  
                    
                elif keyboard.is_pressed('ctrl+right'):
                    purecount = min(purecount + 100, notecount)
                    time.sleep(0.15)  
                    
                elif keyboard.is_pressed('ctrl+left'):
                    purecount = max(0, purecount - 100)
                    time.sleep(0.15)  
                    
                elif keyboard.is_pressed('right'):
                    purecount += 1
                    if purecount > notecount:
                        purecount = notecount
                    time.sleep(0.15)  
                    
                elif keyboard.is_pressed('left'):
                    purecount = max(0, purecount - 1)
                    time.sleep(0.15)  

                elif keyboard.is_pressed('q'):
                    print("\n\nQuitting score calculator...")
                    break

                time.sleep(0.01)
                
        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
        
        total_score = int(purecount * purescore)
        return {
            'Song': row['Song'],
            'Difficulty': row['Difficulty'],
            'Total_Score': total_score,
            'Pure_Count': purecount,
            'Lost_Count': notecount - (purecount)
        }
acf=ArcaeaChartFilter()
acf.Score("Testify", "Beyond")