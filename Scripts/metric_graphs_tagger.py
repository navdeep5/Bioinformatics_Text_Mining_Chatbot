import os
import matplotlib.pyplot as plt

# Function to read metrics from text files
def read_metrics(file_path):
    metrics = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        metric_name = ''
        for line in lines:
            if line.strip() in ['Precision:', 'Recall:', 'F1-score:']:
                metric_name = line.strip()
                metrics[metric_name] = {}
            elif ':' in line:
                key, value = line.strip().split(': ')
                metrics[metric_name][key.strip()] = float(value.strip())
    return metrics

# Function to create graphs
def create_graphs(folder_path):
    metrics_files = os.listdir(folder_path)
    metrics = {file[:-4]: read_metrics(os.path.join(folder_path, file)) for file in metrics_files if file.endswith('.txt')}

    # Plotting
    for metric_name, metric_values in metrics.items():
        plt.figure(figsize=(7, 6))  # Adjust figsize as needed
        plt.title(metric_name)
        # plt.xlabel('Named Entity Recognition Algorithm')
        plt.ylabel('Average Value')
        
        x = list(metric_values.keys())
        y = [metric_values[metric]['Average'] for metric in metric_values]

        bars = plt.bar(range(len(x)), y, color=['blue'])
        plt.xticks(range(len(x)), x, rotation=45)
        
        for i, bar in enumerate(bars):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{y[i]:.2f}', ha='center', va='bottom')

        # Custom labels line
        # plt.legend(labels=[file[:-4] for file in metrics_files], loc='upper left', bbox_to_anchor=(1, 1))
        plt.tight_layout()  # Adjust layout to prevent label cutoff
        plt.show()


# Folder path containing the text files
folder_path = 'Evaluation/Tagger_Evaluation'

# Custom labels for the graphs (corresponding to file names)
custom_labels = ['HTML Tags', 'Sentence Tags']

# Create graphs
create_graphs(folder_path) #, custom_labels)
