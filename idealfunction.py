import numpy as np

class IdealFunctionFinder:
    def __init__(self, train_df, ideal_df):
        self.train_df = train_df
        self.ideal_df = ideal_df
        self.deviations = None
        self.min_deviation_indices = None
        self.ideal_functions = None

    def calculate_deviations(self):
        # Create a list to store the deviations
        deviations = []

        # Iterate over the columns in the training dataset (excluding 'x')
        for col in self.train_df.columns[1:]:
            # Create a list to store the deviations for the current column
            col_deviations = []
            
            # Iterate over the ideal columns
            for ideal_col in self.ideal_df.columns[1:]:
                # Calculate the deviation using least squares
                deviation = np.sum((self.train_df[col] - self.ideal_df[ideal_col]) ** 2)
                
                # Append the deviation to the list
                col_deviations.append(deviation)
            
            # Store the deviations for the current column
            deviations.append(col_deviations)

        # Convert the deviations to a NumPy array
        self.deviations = np.array(deviations)
        print(deviation)

    def find_ideal_functions(self):
        if self.deviations is None:
            self.calculate_deviations()

        # Find the indices of the ideal functions with the least deviation for each column
        self.min_deviation_indices = np.argmin(self.deviations, axis=1)

        # Extract the corresponding column names of the ideal functions
        self.ideal_functions = self.ideal_df.columns[self.min_deviation_indices + 1]

    def print_ideal_functions(self):
        if self.ideal_functions is None:
            self.find_ideal_functions()

        # Print the ideal functions for each column
        for i, col in enumerate(self.train_df.columns[1:]):
            ideal_function = self.ideal_functions[i]
            deviation = self.deviations[i, self.min_deviation_indices[i]]
            print(f"Ideal function for {col} is {ideal_function}")
            print(f"Deviation: {deviation}")
            print()

# Example usage:
# Assuming you have 'train_df' and 'ideal_df' DataFrames already defined
# ideal_finder = IdealFunctionFinder(train_df, ideal_df)
# ideal_finder.print_ideal_functions()
