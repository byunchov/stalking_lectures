import pandas as pd
import numpy as np
import re
from zipfile import ZipFile
from os import walk
import json


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)


class PlatformDataAnalyser():

    def __init__(self, content_dir):
        self.content_dir = content_dir
        self.allowed_file_extentions = ('.xls','.xlsx', '.ods', '.odf' ,'.odt', '.csv')

    def handle_individual_files(self):
        results_df = []
        logs_df = []

        for content in walk(self.content_dir):
            if content[2]:
                for item in content[2]:
                    if item.endswith(self.allowed_file_extentions):
                        data_file = f'{content[0]}/{item}'
                        if data_file.endswith(self.allowed_file_extentions[-1]):                    
                            df = pd.read_csv(data_file)
                        else:
                            df = pd.read_excel(data_file)

                        if 'ID' and 'Result' in df.columns:
                            results_df.append(df)
                            print('Result file found! Appending DF to list.')
                        elif 'Event' and 'Component' in df.columns:
                            df['User ID'] = df['Description'].apply(lambda x: np.int32(re.sub(r"[\D]+",' ', x).strip().split()[0]))
                            logs_df.append(df)
                            print('Log file found! Appending DF to list.')
                        else:
                            print('Nothing found!')
        
        if results_df and logs_df:
            student_results = pd.concat(results_df).sort_values(by='ID', ascending=True)
            system_logs = pd.concat(logs_df)

            del results_df
            del logs_df
            
            return (student_results, system_logs)
        else:
            return (None, None)

    def calculate_central_tendency(self, selector):
        student_results, system_logs = self.handle_individual_files()

        if not student_results.empty and not system_logs.empty:
            from statistics import mode

            if selector == 'all':
                selector = ''

            event_context = f'Assignment: Качване на Упр. {selector}'
            event_name = 'Submission created.'

            filtered_data = system_logs[system_logs['Event context'].str.contains(event_context) & (system_logs['Event name'] == event_name)]['Description']
            
            uploded_files = np.empty_like(filtered_data, dtype=int)

            for index, item in enumerate(filtered_data):
                val = re.sub(r"[\D]+",' ', item).strip()
                uploded_files[index] = np.fromstring(val, dtype=np.int32, sep=' ')[1]

            uploded_files.sort()

            uploded_files_stats = {}

            #mode
            uploded_files_stats['mode'] = mode(uploded_files)

            #average
            uploded_files_stats['mean'] = round(np.mean(uploded_files), 3)

            #meadian
            uploded_files_stats['median'] = int(np.median(uploded_files))

            return json.dumps(uploded_files_stats, cls=NpEncoder)
        
        else:
            return json.dumps({ 'error': 'Nohing to be dispaleyd!' })
