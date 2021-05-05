import pandas as pd
import numpy as np
import re
from zipfile import ZipFile
from os import walk
import json

ALLOWED_EXTENTIONS = ('.xls','.xlsx', '.ods', '.odf' ,'.odt', '.csv')
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
        self.err_log = []
        self.student_results = None
        self.system_logs = None

        status = False
        try:
            if content_dir.endswith(".zip"):
                pass
            else:
                status = self.handle_individual_files()
        except:
            self.err_log.append("[ERR]: Fatar error occured while initializing file data.")

        if not status:
            self.err_log.append("[ERR]: Error occured while initializing data. It's possible that the data of the file doesn't match the requirements.")

    def handle_individual_files(self):
        # returns True if handling is successful, else False`
        results_df = []
        logs_df = []

        for content in walk(self.content_dir):
            if content[2]:
                for item in content[2]:
                    if item.endswith(ALLOWED_EXTENTIONS):
                        data_file = f'{content[0]}/{item}'
                        df = pd.read_csv if data_file.name.endswith('.csv') else pd.read_excel(data_file)

                        if 'ID' and 'Result' in df.columns:
                            results_df.append(df)
                        elif 'Event' and 'Component' in df.columns:
                            df['User ID'] = df['Description'].apply(lambda x: np.int32(re.sub(r"[\D]+",' ', x).strip().split()[0]))
                            logs_df.append(df)
                        else:
                            # TODO: handle error if columns data doesn't match
                            return False

        if results_df and logs_df:
            self.student_results = pd.concat(results_df).sort_values(by='ID', ascending=True)
            self.system_logs = pd.concat(logs_df)

            del results_df
            del logs_df

            return True
        else:
            return False

    def calculate_central_tendency(self, selector):
        # redundant, already checked in initialization
        # if not self.student_results.empty and not self.system_logs.empty:
        from statistics import mode

        if selector == 'all':
            selector = ''

            event_context = f'Assignment: Качване на Упр. {selector}'
            event_name = 'Submission created.'

            filtered_data = self.system_logs[self.system_logs['Event context'].str.contains(event_context) & (self.system_logs['Event name'] == event_name)]['Description']

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
