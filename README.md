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

   

## Part 1: Pre Processing and preparation of dataset
### Dataset Collection
The first step in this project is to collect a dataset of images that will be used to train and evaluate the animal detection model. The dataset should contain a diverse set of animal images, covering a wide range of species, poses, and environmental conditions.

To build the dataset, you can utilize publicly available image datasets, such as:
- [Roboflow Universe](https://roboflow.com/)

Alternatively, you can also collect your own images using web scraping techniques or by taking photographs yourself. If you choose to collect your own images you can use `image_scraping.py` in the `Pre Processing` folder of the repository or click [here](https://github.com/Gunek-945/Animal-detection-system/blob/main/Pre%20processing/image_scraping.py).


For the sake of this project, you can access this [Google drive link](https://drive.google.com/drive/folders/1PLJYTyymfM-SYSsdJt0_QDFtjVH04Yka?usp=sharing) for the images I used to build my dataset.


### Data Augmentation

Data augmentation is a crucial step in this project to increase the diversity and size of the training dataset. By applying various transformations to the existing images, we can create new, synthetic data that can help the model generalize better and improve its performance. You can run autoomatic augmentation on your dataset images using the `augmentation.py` file in the `Pre Processing` folder of the repository or you can also access the python file by clicking [here](https://github.com/Gunek-945/Animal-detection-system/blob/main/Pre%20processing/augmentation.py).

> **Note:** The augmented images will be stored on your local device.

### Uploading Augmented Images to Roboflow
After applying the data augmentation techniques, you can upload the augmented images to the Roboflow dashboard for further processing and model training. Roboflow provides a convenient way to manage your dataset, including the ability to upload and organize your augmented images.

Here are the steps to upload the augmented images to Roboflow:

1. **Create a Roboflow Account**: If you haven't already, sign up for a Roboflow account at [https://roboflow.com/](https://roboflow.com/).

2. **Create a New Project**: Once logged in, create a new project on the Roboflow dashboard by clicking on the "New Project" button.

3. **Set up the Project**: Give your project a name, select the appropriate dataset type (e.g., Object Detection), and configure any other project settings as needed.

4. **Upload the Augmented Images**: Click on the "Upload" button in your project, and then select the "Upload Images" option. Choose the directory containing your augmented images and click "Upload".

5. **Verify the Upload**: After the upload is complete, you should see the augmented images listed in your Roboflow project. You can inspect the images, add annotations (if needed), and prepare the dataset for training.

>#### Your dataset is now ready for labeling 
    
## Part 2: Labelling of dataset

After uploading the augmented images to Roboflow, the next step is to label and annotate the dataset. Roboflow provides a user-friendly interface and tools to help you with this process.

1. Access the Roboflow Project: Log in to your Roboflow account and navigate to the project where you uploaded the augmented images.
   
2. Start Labeling: In the project, click on the "Annotate" button to start the labeling process. Roboflow supports various annotation types, such as bounding boxes, polygons, and keypoints, depending on your dataset requirements.

3. Label the Images: Examine each image and create the necessary annotations. Roboflow's annotation tools allow you to efficiently label multiple objects within an image.

4. Review and Refine: Regularly review your annotations to ensure they are accurate and consistent. You can use Roboflow's built-in tools to validate, edit, and refine the annotations as needed.
   
5. Manage Annotations: Roboflow provides features to manage your annotations, such as exporting them in various formats (e.g., COCO, Pascal VOC, YOLO) and versioning the dataset.


## Part3: Training YOLOv8 model on Custom Dataset

After completing the dataset labeling and annotation steps in `Part 2`, you are now ready to train the `YOLOv8` model on our custom dataset. This part of the project will guide you through the model training process.

### Prerequisits

Before you begin, ensure that you have the following:

1. Python 3.7 or higher installed on your system.
   
2. The ultralytics library installed. You can install it using pip:
   ```
   pip install ultralytics
   ```
   
3. Your labeled and annotated dataset ready in a format compatible with YOLOv8

### Set up CUDA for GPU Acceleration (Optional)

If you have a `CUDA-enabled GPU`, you can set it up to accelerate the training process. Follow these steps:

1. **Install CUDA toolkit:** Download and install the `CUDA Toolkit` from the NVIDIA website. The version should match the requirements of the ultralytics library.
   
2. **Install CUDA-Enabled PyTorch:** Install a CUDA-enabled version of PyTorch that is compatible with your CUDA Toolkit version. You can use the `pip` command provided on the PyTorch website.
   
3. **Verify the CUDA Installation:** Run the following `Python code` to ensure that CUDA is properly installed and recognized by the ultralytics library:
   ```
   from ultralytics import YOLO
   device = YOLO("yolov8s.pt").device
   print(f"Using device: {device}")
   ```
   If the output shows `"cuda"` as the `device`, your CUDA setup is successful.

### Model Training Steps 

You can follow this [Colab Notebook](https://colab.research.google.com/github/roboflow-ai/notebooks/blob/main/notebooks/train-yolov8-object-detection-on-custom-dataset.ipynb) to train your Model virtually on Google Colab or you can follow the following steps to train it locally:


#### 1. Export the Dataset:

You can use this [dataset]()

or 


You can export your own Roboflow dataset created in the previous part using the code below:

```
!mkdir {HOME}/datasets
%cd {HOME}/datasets

!pip install roboflow --quiet

from roboflow import Roboflow
rf = Roboflow(api_key="YOUR_API_KEY")
project = rf.workspace("roboflow-jvuqo").project("football-players-detection-3zvbc")
dataset = project.version(1).download("yolov8")
```


#### 2. Train the YOLOv8 Model:

1. **Start the Training:** Use the `yolo` command-line tool provided by the ultralytics library to initiate the training process. Enter this command in your terminal-

   ```
   yolo task=detect mode=train model=yolov8s.pt data=dataset.yaml epochs=100 batch=16
   ```
   If you have a `CUDA-enabled GPU`, you can use the device parameter to specify the GPU to use:

   ```
   yolo task=detect mode=train model=yolov8s.pt data=dataset.yaml epochs=100 batch=16 device=0
   ```

2. **Monitor the Training Process:** Keep an eye on the `training progress`, loss values, and other metrics to ensure the model is converging as expected.

3. **Checkpoint and Save the Model:** During the training, the ultralytics library will automatically save checkpoint files at regular intervals. You can also manually save the final trained model for later use.


#### 3. Testing the model on Validation set

   After training, use the trained model to run inference on the validation set to evaluate its performance. You can run training using the `file` [yolov8_custom.py](https://github.com/Gunek-945/Animal-detection-system/blob/main/yolov8_custom.py) in the repository.
   Review the evaluation metrics and identify areas for improvement. You may need to adjust the training parameters, augment the dataset, or fine-tune the model further.

By following these steps, you can train the YOLOv8 model on your custom dataset and evaluate its performance.

## UART Communication with NVIDIA Orin Nano and ESP32 Module

This section describes how to implement UART communication between the NVIDIA Orin Nano and an ESP32 module to control an LED based on object detection results from the YOLOv8 model.

### Overview

The NVIDIA Orin Nano communicates with the ESP32 module via UART (Universal Asynchronous Receiver-Transmitter). Upon detecting a specific object with the YOLOv8 model, a signal is sent to the ESP32 to light up an LED.

### Circuit Setup

1. **Wiring the ESP32 and Orin Nano:**
   - Connect the TX pin of the Orin Nano to the RX pin of the ESP32.
   - Connect the RX pin of the Orin Nano to the TX pin of the ESP32.
   - Connect the GND pin of both the Orin Nano and ESP32 to ensure they share a common ground.

2. **Connecting the LED:**
   - Connect a suitable resistor to the LED to limit current.
   - Connect the anode (positive leg) of the LED to one of the GPIO pins on the ESP32.
   - Connect the cathode (negative leg) of the LED to the ground.

3. **Power Supply:**
   - Ensure that both devices are powered adequately. The ESP32 can be powered via USB or an external source, while the Orin Nano should be connected to a suitable power supply.





   





