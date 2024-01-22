import os
import csv
import ultralytics
import streamlit as st
import tempfile
import cv2
import PIL
from ultralytics import YOLO

model_path = 'best1.pt'
model = None  # Define model globally

# Setting page layout
st.set_page_config(
    page_title="Bone Fracture Detection",  # Setting page title
    page_icon="",     # Setting page icon
    layout="wide",      # Setting layout to wide
    initial_sidebar_state="expanded",    # Expanding sidebar by default
)

# Function to load the YOLO model
def load_model():
    global model
    try:
        if model is None:
            model = YOLO(model_path)
    except Exception as ex:
        st.error(f"Unable to load model. Check the specified path: {model_path}")
        st.error(ex)



# Function for the main page
def main_page():
    global model
    st.sidebar.title('Custom Object Detection')
    st.title("Bone Fracture Detection with YOLOv8 and Streamlit")
    st.markdown('''
                :orange[**Upload an xray to detect fracture**]
                ''')

    st.markdown('''
                :orange[**Click :blue[Detect] button and check the result.**]
                '''
                )

    # Creating two columns on the main page
    col1, col2 = st.columns(2)
    col3, col4, col5 = st.columns(3)
    st.divider()

    with col1:
        uploaded_file = st.file_uploader("Choose a file")

    # Adding image to the first column if an image is uploaded
    with col3:
        if uploaded_file:
            # Opening the uploaded image
            uploaded_image = PIL.Image.open(uploaded_file)
            # Adding the uploaded image to the page with a caption
            st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    if model is None:
        load_model()

    if model is not None:
        object_cls = None
        conf = None
        if st.sidebar.button('Detect'):
            results1 = model.predict(uploaded_image)

            if not results1:
                
                st.warning("No objects detected in the image.")
            else:
                for result in results1:
                    boxes = result.boxes
                    for box in boxes:
                        class_id = box.cls[0].item()
                        object_cls = result.names[class_id]
                        prob = round(box.conf[0].item(), 2)
                
                        conf = f"{prob:.0%}"
                
                    res_plotted = result.plot()

                with col4:
                    try:
                        st.image(res_plotted,
                                caption='Detected Image',
                                use_column_width=True,
                                )
                    except Exception as ex:
                        st.write("Error displaying the detected image.")

                with col5:
                    st.markdown('''
                                :orange[**Detection:**]
                                ''')
                    st.header(object_cls)
                    st.markdown('''
                                :orange[**Confidence:**]
                                '''
                                ) 
                    st.subheader(conf)
            

# Function for Page 2
def page2():
    global model
    st.sidebar.title('Just paste the path of the x-ray images folder')
    st.title("CREATE CSV FILE OF FRACTURE PREDICTION.")
    st.markdown('''
                :orange[**Select a folder containing X-ray images to detect fractures.**]
                ''')

    folder_path = st.sidebar.text_input("Enter the folder path:")
    
    object_cls = "Not_Fractured"
    
    conf = "Not_Fractured"
    
    col1, col2 = st.columns(2)
    
    
    if st.sidebar.button("Detect in Folder"):
        
        if model is None:
            load_model()

        if model is not None:
            if os.path.exists(folder_path):
                image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

                if not image_files:
                    st.warning("No valid image files found in the folder.")
                else:
                    results_list = []

                    for image_file in image_files:
                        image_path = os.path.join(folder_path, image_file)
                        uploaded_image = PIL.Image.open(image_path)

                        
                        
                        results = model.predict(uploaded_image)

                        if not results:
                            st.warning("No objects detected in the image.")
                        else:
                            for result in results:
                                boxes = result.boxes
                                for box in boxes:
                                    class_id = box.cls[0].item()
                                    object_cls = result.names[class_id]
                                    prob = round(box.conf[0].item(), 2)
                            
                                    conf = f"{prob:.0%}"
                            
                                res_plotted = result.plot()
                            with col1:
                                results_list.append({"Image": image_file, "Class": object_cls, "Confidence": conf})
          
                                    

                    if results_list:
                        csv_filename = "detection_results.csv"
                        csv_path = os.path.join(os.getcwd(), csv_filename)  # Save in the present working directory
                        with open(csv_path, 'w', newline='') as csvfile:
                            fieldnames = ["Image", "Class", "Confidence"]
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                            writer.writeheader()
                            writer.writerows(results_list)

                        st.success(f"Detection results saved to: {csv_path}")
                    else:
                        st.warning("No valid results to save.")

            else:
                st.warning("Folder path does not exist.")

# Define the page names and corresponding functions
page_names_to_funcs = {
    "Main Page": main_page,
    "Image Folder Detection": page2,
}

# Select a page using the sidebar and call the corresponding function
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
