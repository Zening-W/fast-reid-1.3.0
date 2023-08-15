import os
import random
import shutil

# Paths
image_folder = "datasets\AIC19\image_train"
output_folder = "datasets\\AIC19\\new_sets"

# List and shuffle images
image_filenames = os.listdir(image_folder)
random.shuffle(image_filenames)

# Split percentages
train_ratio = 0.75
test_ratio = 0.20
query_ratio = 0.05

# Calculate split sizes
num_images = len(image_filenames)
num_train = int(train_ratio * num_images)
num_test = int(test_ratio * num_images)
num_query = int(query_ratio * num_images)

# Create output folders
train_folder = os.path.join(output_folder, "train")
test_folder = os.path.join(output_folder, "test")
query_folder = os.path.join(output_folder, "query")
for folder in [train_folder, test_folder, query_folder]:
    os.makedirs(folder, exist_ok=True)

# Copy images
for i, filename in enumerate(image_filenames):
    dest_folder = train_folder if i < num_train else (test_folder if i < num_train + num_test else query_folder)
    dest_path = os.path.join(dest_folder, filename)
    shutil.copy(os.path.join(image_folder, filename), dest_path)
