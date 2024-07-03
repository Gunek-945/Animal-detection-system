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

1. With the virtual environment active, you can install the [requirements.txt](https://github.com/Gunek-945/Animal-detection-system/blob/main/requirements.txt) file given in the repository in the same project directory. Then run the following command-

   ```
   pip install -r requirements.txt
   ```

This will install all the packages listed in the `requirements.txt` file into your virtual environment.

   

## Part 1: Dataset Collection and Pre-processing
### Dataset Collection
The first step in this project is to collect a dataset of images that will be used to train and evaluate the animal detection model. The dataset should contain a diverse set of animal images, covering a wide range of species, poses, and environmental conditions.

To build the dataset, you can utilize publicly available image datasets, such as:
- [Roboflow Universe](https://roboflow.com/)

Alternatively, you can also collect your own images using web scraping techniques or by taking photographs yourself. If you choose to collect your own images you can use the following steps for image scrapping using a pip module.

- Step 1:
- 
