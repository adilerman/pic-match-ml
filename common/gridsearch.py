from itertools import product
import pandas as pd
import multiprocessing
from common.score_folder import score_folder, score_sift


class SiftGridSearch:
    def __init__(self, input_path, grid, output_path, y_test):
        self.folder_path = input_path
        self.grid = grid
        self.output_path = output_path
        self.y_test = y_test

    def process_combination(self, combination):
        matches = score_folder(self.folder_path, combination)
        score = score_sift(matches, self.y_test)
        combination.update(score)
        print(f"Finished combination \n{combination}")
        return pd.DataFrame.from_dict(combination, orient='index')

    def run(self):
        combinations = self.get_combinations()
        pool = multiprocessing.Pool(processes=8)
        # Use the pool to map the process_combination function to each combination
        df = pool.map(self.process_combination, combinations)

        # Close the pool and wait for all processes to finish
        pool.close()
        pool.join()

        self.output(df)

    def get_combinations(self):
        param_names = list(self.grid.keys())
        param_values = list(self.grid.values())
        param_combinations = list(product(*param_values))

        combinations = []
        for params in param_combinations:
            combination = dict(zip(param_names, params))
            combinations.append(combination)

        return combinations

    def output(self, df):
        df.to_csv(self.output_path, index=False)


