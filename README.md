# Bone Fracture Detection with YOLOv8 and Streamlit

This repository contains a Streamlit web application for bone fracture detection using YOLOv8. Follow the instructions below to run the application.

## Prerequisites

- Python 3.9 
- Git
- 

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/imadarsh9686/bone_fracture_detection.git

2. Navigate to the project directory:

   ```bash
   cd your-repo

3. Create a conda environment (optional but recommended):
   
   ```bash
   conda create --name your_env_name python=3.9.18

4. Activate the conda environment:

   ```bash
   conda activate your_env_name

5. Install the required Python packages:

   ```bash
   pip install -r requirements.txt

## Running the Application

## 1. Detecting Fractures in a Single Image
1. Make sure your virtual environment is activated.

2. Run the following command to start the Streamlit app:
   
   ```bash
      streamlit run app.py

3. Open your web browser and go to http://localhost:8501.
4. Upload an X-ray image and click the "Detect" button to view the fracture detection results.

## 2. Creating a CSV File of Fracture Predictions in a Folder

1. Follow steps 1-4 from the "Detecting Fractures in a Single Image" section.

2. Navigate to the "Image Folder Detection" page in the Streamlit app.

3. Enter the path of the folder containing X-ray images.

4. Click the "Detect in Folder" button to generate a CSV file with detection results.


