import numpy as np
from scipy.stats import pearsonr, linregress
from sklearn.metrics import mean_absolute_error, mean_squared_error

class EnhancedAnalysis:
    def __init__(self, visualization_panel):
        self.visualization_panel = visualization_panel


    def perform_analysis(self, predicted_y, actual_y):
        # Calculate metrics directly
        correlation = pearsonr(predicted_y, actual_y)[0]
        slope, intercept, r_value, p_value, std_err = linregress(predicted_y, actual_y)
        mae = mean_absolute_error(actual_y, predicted_y)
        rmse = np.sqrt(mean_squared_error(actual_y, predicted_y))
        mape = np.mean(np.abs((actual_y - predicted_y) / actual_y)) * 100

        # Store and return results
        analysis_results = {
            'Correlation': correlation,
            'Slope': slope,
            'Intercept': intercept,
            'R_value': r_value,
            'P_value': p_value,
            'Std_err': std_err,
            'MAE': mae,
            'RMSE': rmse,
            'MAPE': mape
        }
        return analysis_results


    def calculate_metrics(predicted_y, actual_y):
        # Perform the calculations as before
        correlation = pearsonr(predicted_y, actual_y)[0]
        slope, intercept, r_value, p_value, std_err = linregress(predicted_y, actual_y)
        mae = mean_absolute_error(actual_y, predicted_y)
        rmse = np.sqrt(mean_squared_error(actual_y, predicted_y))
        mape = np.mean(np.abs((actual_y - predicted_y) / actual_y)) * 100

        return correlation, slope, intercept, r_value, p_value, std_err, mae, rmse, mape


    def print_analysis_results(self, analysis_results):
        for fig_idx, results in analysis_results.items():
            print(f"Analysis Results for Figure {fig_idx}:")
            for metric, value in results.items():
                print(f"{metric}: {value:.3f}")
            print("\n")

# Example usage:
# Assuming `visualization_panel` is an instance of the VisualizationPanel class
# analysis = EnhancedAnalysis(visualization_panel)
# results = analysis.perform_analysis()
# analysis.print_analysis_results(results)
