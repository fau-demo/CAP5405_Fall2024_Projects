import os
import shutil
from tqdm import tqdm
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

class DatasetDownloader:
    def __init__(self, base_path: str = "datasets"):
        """
        initialize the datasetdownloader.
        
        args:
            base_path (str): base directory to store all datasets
        """
        self.base_path = base_path
        self.api = KaggleApi()
        self.image_extensions = ('.jpg')  # what counts as an "image"
        
    def _create_dataset_directory(self, dataset_name: str) -> str:
        """
        create the directory structure for a dataset.
        """
        dataset_path = os.path.join(self.base_path, dataset_name)
        images_path = os.path.join(dataset_path, "images")
        os.makedirs(images_path, exist_ok=True)
        return dataset_path

    def _extract_images(self, zip_path: str, dataset_path: str):
        """
        extract images from the downloaded zip file to the dataset directory.        
        """
        images_path = os.path.join(dataset_path, "images")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # get list of all files in the zip
            files = [f for f in zip_ref.namelist() if f.lower().endswith(self.image_extensions)]
            
            print(f"extracting {len(files)} images...")
            # First extract all files to a temporary directory
            temp_dir = os.path.join(dataset_path, "temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            for file in tqdm(files):
                zip_ref.extract(file, temp_dir)
            
            # Move all images to the images directory
            for root, _, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith(self.image_extensions):
                        src_path = os.path.join(root, file)
                        dst_path = os.path.join(images_path, file)
                        shutil.move(src_path, dst_path)
            
            # Clean up temporary directory
            shutil.rmtree(temp_dir)

    def download_dataset(self, dataset_url: str):
        """
        download a dataset from kaggle using the dataset url.
        
        args:
            dataset_url (str): kaggle dataset url or dataset reference (e.g., 'username/dataset-name') 
        """
        # extract username and dataset name from url if full url is provided
        if "kaggle.com/datasets/" in dataset_url:
            dataset_ref = dataset_url.split("kaggle.com/datasets/")[1].strip('/')
        else:
            dataset_ref = dataset_url.strip('/')
            
        try:
            # create dataset directory
            dataset_name = dataset_ref.split('/')[-1]
            dataset_path = self._create_dataset_directory(dataset_name)
            
            print(f"downloading dataset: {dataset_ref}")
            
            # download the dataset
            self.api.dataset_download_files(
                dataset_ref,
                path=dataset_path,
                unzip=False
            )
            
            # extract images from the downloaded zip
            zip_path = os.path.join(dataset_path, f"{dataset_name}.zip")
            if os.path.exists(zip_path):
                self._extract_images(zip_path, dataset_path)
                # clean up zip file
                os.remove(zip_path)
                print(f"successfully downloaded and extracted images to {os.path.join(dataset_path, 'images')}")
            else:
                print(f"error: downloaded file not found at {zip_path}")
                
        except Exception as e:
            print(f"error downloading dataset: {str(e)}")
            if "404" in str(e):
                print("dataset not found. please check the dataset url or reference.")

    def duplicate_check(self, dataset_url: str):
        """
        check if a dataset is already downloaded as a subfolder and return its name and image count
        args:
            dataset_url (str): kaggle dataset url or dataset reference (e.g., 'username/dataset-name') 
        returns:
            tuple: (bool, str, int) - whether the dataset exists, the dataset name, and the number of images
        """

        if "kaggle.com/datasets/" in dataset_url:
            dataset_ref = dataset_url.split("kaggle.com/datasets/")[1].strip('/')
        else:
            dataset_ref = dataset_url.strip('/')
            
        dataset_name = dataset_ref.split('/')[-1]
        dataset_path = os.path.join(self.base_path, dataset_name)
        images_path = os.path.join(dataset_path, "images")
        
        if os.path.exists(dataset_path) and os.path.isdir(dataset_path):
            if os.path.exists(images_path) and os.path.isdir(images_path):
                # count number of image files
                image_count = len([
                    f for f in os.listdir(images_path) 
                    if os.path.isfile(os.path.join(images_path, f)) and f.lower().endswith(self.image_extensions)
                ])
                return True, dataset_name, image_count
            return True, dataset_name, 0
        return False, dataset_name, 0