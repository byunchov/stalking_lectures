import pandas as pd
import numpy as np
import re
from zipfile import ZipFile
from os import walk
import json


ALLOWED_FILE_EXTENTIONS = ('.xls','.xlsx', '.ods', '.odf' ,'.odt', '.csv')


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

    def __init__(self, upload_path):
        self.upload_path = upload_path

        self.student_results = None
        self.system_logs = None

        self.results_df = []
        self.logs_df = []

        self.err_log = [] #TODO

        self.init_data_from_file()


    def init_data_from_file(self):
        for content in walk(self.upload_path):

            #Check if there are any files in the current dir
            if content[2]:
                # if there are files, loop through all and check if they are of the allowed types
                for item in content[2]:
                    data_file = f'{content[0]}/{item}'

                    if item.endswith('.zip'):
                        self.handle_zip_file(data_file)
                    elif item.endswith(ALLOWED_FILE_EXTENTIONS):
                        self.handle_data_file(data_file)

        if self.results_df and self.logs_df:
            self.student_results = pd.concat(self.results_df).sort_values(by='ID', ascending=True)
            self.system_logs = pd.concat(self.logs_df)

            del self.results_df
            del self.logs_df


    def handle_zip_file(self, path_to_file):
        with ZipFile(path_to_file) as input_archive:
            for item in input_archive.namelist():
                if item.endswith(ALLOWED_FILE_EXTENTIONS):
                    with input_archive.open(item) as data_file:
                        self.handle_data_file(data_file)


    def handle_data_file(self, path_to_file):
        df = pd.read_csv(path_to_file) if str(path_to_file).endswith('.csv') else pd.read_excel(path_to_file)

        if 'ID' and 'Result' in df.columns:
            self.results_df.append(df)
            print('Result file found! Appending DF to list.')
        elif 'Event' and 'Component' in df.columns:
            df['User ID'] = df['Description'].apply(lambda x: np.int32(re.sub(r"[\D]+",' ', x).strip().split()[0]))
            self.logs_df.append(df)
            print('Log file found! Appending DF to list.')
        else:
            print('Nothing found!')


    def calculate_central_tendency(self, selector):
        if self.student_results is not None and self.system_logs is not None:
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
            uploded_files_stats['median'] = np.median(uploded_files)

            return json.dumps(uploded_files_stats, cls=NpEncoder)

        else:
            return json.dumps({ 'error': 'Nothing to be displayed!' })

    def calculate_all(self):
        result = {}
        result['status'] = 200
        result['central_tendency'] = (json.loads(self.calculate_central_tendency("all")))
        return json.dumps(result, cls=NpEncoder)
