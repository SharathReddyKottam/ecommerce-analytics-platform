import kaggle
import os

def download_data():
    print("Downloading ecommerce dataset from Kaggle...")
    os.makedirs('data', exist_ok=True)
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(
        'carrie1/ecommerce-data',
        path='data/',
        unzip=True
    )
    print("Dataset downloaded successfully!")

if __name__ == "__main__":
    download_data()