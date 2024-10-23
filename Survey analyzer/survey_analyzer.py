import pandas as pd 
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import json


class SurveyAnalyzer:
    def __init__(self):
        """
        Initializes the SurveyAnalyzer with an empty DataFrame and an empty dictionary for analysis results.
        """
        self.df = None
        self.analysis_results = {}

    def import_data(self, filename):
        """
        Import data from a CSV file using pandas.
        """
        try:
            self.df = pd.read_csv(filename)
            print(f"Successfully imported {len(self.df)} responses.")
            return True
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return False
        except pd.errors.EmptyDataError:
            print(f"Error: File '{filename}' is empty.")
            return False
        except Exception as e:
            print(f"Error importing data: {str(e)}")
            return False

    def analyze_data(self):
        """
        Analyze the survey data using pandas functionality.
        """
        if self.df is None or self.df.empty:
            return "No data to analyze."

        self.analysis_results = {
            "response_count": len(self.df),
            "questions": {}
        }

        # Analyze each column
        for column in self.df.columns:
            column_data = self.df[column]
            
            analysis = {
                "response_count": len(column_data),
                "unique_responses": len(column_data.unique()),
                "missing_values": column_data.isnull().sum(),
                "response_distribution": column_data.value_counts().to_dict()
            }

            if pd.api.types.is_numeric_dtype(column_data):
                analysis.update({
                    "mean": round(column_data.mean(), 2),
                    "median": round(column_data.median(), 2),
                    "std_dev": round(column_data.std(), 2),
                    "min": column_data.min(),
                    "max": column_data.max(),
                    "quartiles": {
                        "25%": round(column_data.quantile(0.25), 2),
                        "50%": round(column_data.quantile(0.50), 2),
                        "75%": round(column_data.quantile(0.75), 2)
                    }
                })

            self.analysis_results["questions"][column] = analysis

    def generate_visualizations(self, output_folder="survey_visualizations"):
        """
        Generate visualizations for the survey data.
        """
        if self.df is None or self.df.empty:
            return "No data to visualize."

        Path(output_folder).mkdir(exist_ok=True)

        for column in self.df.columns:
            plt.figure(figsize=(10, 6)) 
            
            if pd.api.types.is_numeric_dtype(self.df[column]):
                self.df[column].hist()
                plt.title(f'Distribution of {column}')
                plt.xlabel(column)
                plt.ylabel('Frequency')
            else:
                self.df[column].value_counts().plot(kind='bar')
                plt.title(f'Response Distribution for {column}')
                plt.xlabel(column)
                plt.ylabel('Count')
            
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f'{output_folder}/{column}_analysis.png')
            plt.close()

    def export_results(self, filename):
        """
        Export analysis results to a JSON file.
        """
        try:
            def convert_to_serializable(obj):
                type_conversion = {
                    np.int64: int,
                    np.int32: int,
                    np.float64: float,
                    np.float32: float,
                    np.bool_: bool,
                }
                if isinstance(obj, tuple(type_conversion.keys())):
                    return type_conversion[type(obj)](obj)
                if isinstance(obj, dict):
                    return {key: convert_to_serializable(value) for key, value in obj.items()}
                if isinstance(obj, (list, tuple)):
                    return [convert_to_serializable(item) for item in obj]
                return obj
            
            serializable_results = convert_to_serializable(self.analysis_results)

            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(serializable_results, file, indent=4)
            print(f"Results successfully exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting results: {str(e)}")
            return False

    def get_summary_statistics(self):
        """
        Get a brief summary of the analysis.
        """
        if self.df is None:
            return "No data loaded."
        
        return {
            "Total Responses": len(self.df),
            "Questions": len(self.df.columns),
            "Complete Responses": len(self.df.dropna()),
            "Columns": list(self.df.columns)
        }


def main():
    analyzer = SurveyAnalyzer()
    
    while True:
        print("\nSurvey Data Analyzer")
        print("1. Import CSV file")
        print("2. Analyze data")
        print("3. Generate visualizations")
        print("4. Export results")
        print("5. Show summary statistics")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ")

        options = {
            '1': lambda: analyzer.import_data(input("Enter CSV filename: ")),
            '2': lambda: (analyzer.analyze_data(), print("\nAnalysis complete!")),
            '3': lambda: (
                (output_folder := input("Enter output folder name (default: survey_visualizations): ") or "survey_visualizations"),
                analyzer.generate_visualizations(output_folder),
                print(f"\nVisualizations saved in {output_folder} folder!")
            ),
            '4': lambda: (
                (output_file := input("Enter output filename (e.g., results.json): ")),
                analyzer.export_results(output_file),
                print(f"Results exported to {output_file}")
            ),
            '5': lambda: (
                print("\nSummary Statistics:"), 
                print("\n".join(f"{key}: {value}" for key, value in analyzer.get_summary_statistics().items()))
            ),
            '6': lambda: (print("Thank you for using Survey Data Analyzer!"), exit())
        }

        if choice in options:
            options[choice]()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
