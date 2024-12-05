## !! please do not upload the dataset to gitlab, simply run this script at 
## local environment and add the containing folder to git ignore

import kagglehub

# Download latest version
path = kagglehub.dataset_download("mohamedbakhet/amazon-books-reviews")

print("Path to dataset files:", path)

# move path to local environment
import shutil
shutil.move(path, "./dataset")