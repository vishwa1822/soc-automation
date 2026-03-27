import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from logprocessor import LogProcessor


class BatchAnalyzer:

    def __init__(self):

        self.processor = LogProcessor()


    def process_single_log(self, log):

        return self.processor.process_log(log)


    def analyze_file(self, file_path):

        df = pd.read_csv(file_path)

        logs = df.to_dict(orient="records")

        results = []

        # parallel processing
        with ThreadPoolExecutor(max_workers=4) as executor:

            results = list(
                executor.map(self.process_single_log, logs)
            )

        return results