# Animal-detection-system

## Installation

It's recommended to set up a virtual environment for this project to keep the dependencies isolated from your system's global Python installation. Follow the steps below to get started:

### Create a Virtual Environment

1. Open a terminal or command prompt.
2. Navigate to the root directory of your project.
3. Create a new virtual environment using the following command: <br>
   ```python -m venv env ``` (Replce env with the name you want to give to your environment)

This will create a new directory called `env` in your project directory, which will contain the Python interpreter and all the installed packages.

4. Activate the virtual environment:

- On Windows:
  ```
  env\Scripts\activate
  ```
- On macOS or Linux:
  ```
  source env/bin/activate
  ```

You should see `(env)` at the beginning of your terminal prompt, indicating that the virtual environment is active.

### Install Dependencies

With the virtual environment active, you can install the [requirements.txt](https://github.com/Gunek-945/Animal-detection-system/blob/main/requirements.txt) file given in the repository in the same project directory. Then run the following command-

   ```
   pip install -r requirements.txt
   ```

This will install all the packages listed in the `requirements.txt` file into your virtual environment.

   

## Part 1: Pre Processing
### Dataset Collection
The first step in this project is to collect a dataset of images that will be used to train and evaluate the animal detection model. The dataset should contain a diverse set of animal images, covering a wide range of species, poses, and environmental conditions.

To build the dataset, you can utilize publicly available image datasets, such as:
- [Roboflow Universe](https://roboflow.com/)

Alternatively, you can also collect your own images using web scraping techniques or by taking photographs yourself. If you choose to collect your own images you can use `image_scraping.py` in the `Pre Processing` folder of the repository or click [here](https://github.com/Gunek-945/Animal-detection-system/blob/main/Pre%20processing/image_scraping.py).


For the sake of this project, you can access this [Google drive link](https://drive.google.com/drive/folders/1PLJYTyymfM-SYSsdJt0_QDFtjVH04Yka?usp=sharing) for the images I used to build my dataset.


### Data Augmentation

Data augmentation is a crucial step in this project to increase the diversity and size of the training dataset. By applying various transformations to the existing images, we can create new, synthetic data that can help the model generalize better and improve its performance. You can run autoomatic augmentation on your dataset images using the `augmentation.py` file in the `Pre Processing` folder of the repository or you can also access the python file by clicking [here](https://github.com/Gunek-945/Animal-detection-system/blob/main/Pre%20processing/augmentation.py).

> **Note:** The augmented images will be stored on your local device.

After augmenting the images, we are done with `PART 1` and we can proceed to uploading these images to Roboflow for annotations in `PART 2`.







