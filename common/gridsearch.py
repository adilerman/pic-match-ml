from tester import score_folder
from itertools import product


class SiftGridSearch:
    def __init__(self, folder_path, grid, output_path):
        self.folder_path = folder_path
        self.grid = grid
        self.output_path = output_path
        # self.threshold = threshold
        # self.nfeatures = nfeatures
        # self.n_octave_layers = n_octave_layers
        # self.contrast_threshold = contrast_threshold
        # self.edge_threshold = edge_threshold

    def run(self):
        combinations = self.get_combinations()
        for combination in combinations:
            matches = score_folder(self.folder_path, combination)
            score = score_sift(matches, )

    def get_combinations(self):
        param_names = list(self.grid.keys())
        param_values = list(self.grid.values())
        param_combinations = list(product(*param_values))

        combinations = []
        for params in param_combinations:
            combination = dict(zip(param_names, params))
            combinations.append(combination)

        return combinations

    def output(self):

        return


