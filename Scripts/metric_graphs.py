import os
import matplotlib.pyplot as plt
import numpy as np

# Function to parse a text file and extract average values for each metric
def parse_text_file(file_path):
    metric_values = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
        metric = None
        for line in lines:
            line = line.strip()
            if line.startswith('Average:'):
                metric_values[metric] = float(line.split(':')[1].strip())
            elif line.endswith(':'):
                metric = line[:-1]
    return metric_values

# Directory containing the text files
directory = 'Evaluation/Manual_Evaluation/Fair_Comparison_70'

# Create a directory to save plots
plots_directory = os.path.join(directory, 'Plots')
os.makedirs(plots_directory, exist_ok=True)

# Mapping between custom names and file names
custom_names_mapping = {
    'Conventional': 'conventional80.txt',
    'Conventional \n Sentence Tagged': 'conventional_80_sentence_tags_NoOE_1.txt',
    'Mixtral Prompt Engineered': 'mixtral_80_Edited.txt',
    'Mixtral Prompt Engineered \n Sentence Tagged': 'mixtral_80_tagged_NoOE_Edited.txt',
    'Mixtral Fine-tuned': 'output_80_Mixtral_Transformer_Finetuned_Fixed_Edited.txt',
    'Mixtral Fine-tuned \n Sentence Tagged': 'output_80_sentence_tags_NoOE_Fixed_Edited.txt',
    'Starline Fine-tuned': 'output_Vanilla_Untagged_80_Edited.txt',
    'Starling Fine-tuned \n Sentence Tagged': 'output_SentenceVanilla_Sentence_80_NoOE_Edited.txt',
    'Starling Prompt Engineered': 'output_80_Starling_Untagged_Edited.txt',
    'Starling Prompt Engineered \n Sentence Tagged': 'output_80_Starling_Sentence_Tagged_Edited.txt',
}

# Group custom names by category
categories = {
    'Conventional': ['Conventional', 'Conventional \n Sentence Tagged'],
    'Mixtral Prompt Engineered': ['Mixtral Prompt Engineered', 'Mixtral Prompt Engineered \n Sentence Tagged'],
    'Mixtral Fine-tuned': ['Mixtral Fine-tuned', 'Mixtral Fine-tuned \n Sentence Tagged'],
    'Starling Prompt Egnineered': ['Starling Prompt Engineered', 'Starling Prompt Engineered \n Sentence Tagged'],
    'Starling Fine-tuned': ['Starline Fine-tuned', 'Starling Fine-tuned \n Sentence Tagged']
}

# Initialize dictionaries to store average values for each metric
metric_avgs = {
    'Precision': {},
    'Recall': {},
    'F1-score': {},
    'Jaro-Winkler Similarity': {},
    'Bonus Precision': {},
    'Bonus Recall': {},
    'Bonus F1-score': {},
    'Bonus Precision and Recall F1 Score': {}
}

# Iterate through each text file in the directory
for custom_name, file_name in custom_names_mapping.items():
    file_path = os.path.join(directory, file_name)
    metric_values = parse_text_file(file_path)
    for metric, value in metric_values.items():
        if metric in metric_avgs:
            metric_avgs[metric][custom_name] = value

# Plotting each metric on its own plot and save the plot
# Plotting each metric on its own plot and save the plot
# Plotting each metric on its own plot and save the plot
for metric, values in metric_avgs.items():
    plt.figure(figsize=(10, 6))
    plt.xlabel('Models')
    plt.ylabel('Average Value')
    plt.title(metric)
    
    # Plot bars for each category
    x_positions = np.arange(len(custom_names_mapping))
    all_category_positions = []
    for category, names in categories.items():
        category_values = {name: values[name] for name in names if name in values}
        if category_values:
            category_positions = [x_positions[list(custom_names_mapping.keys()).index(name)] for name in names]
            all_category_positions.extend(category_positions)
            plt.bar(category_positions, category_values.values(), label=category)
    
    plt.xticks(sorted(all_category_positions), custom_names_mapping.keys(), rotation=45, fontsize='small')
    plt.legend()
    plt.tight_layout()
    plot_file_path = os.path.join(plots_directory, f'{metric}_plot.png')
    plt.savefig(plot_file_path)
    plt.close()

print("Plots saved successfully!")

