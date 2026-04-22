## Streamlit Introduction

Data Science models often need to be shared and presented in an interactive manner for various applications. Streamlit provides a convenient platform to build user-friendly interfaces, allowing practitioners to showcase their machine learning models to a broader audience effectively.

This lab builds upon the previous FastAPI Lab, where we trained a classification model on the Palmer Penguins dataset and served it through a FastAPI backend. In this lab, we will create a clean, user-friendly Streamlit dashboard that connects to the API and allows users to make real-time predictions for penguin species.

## Lab Objective

Before starting this lab, it is recommended that you complete the FastAPI Labs since the model created there will be used here. In this Streamlit lab, you will learn how to connect the trained model with a visual interface and allow users to test predictions interactively.

The goal is to design a dashboard where users can provide input parameters such as bill length, bill depth, flipper length, and body mass, and instantly see the predicted species of the penguin.

## Installing Required Packages

There are two ways to install the necessary packages for this lab.

The first and recommended way is by using the requirements.txt file. This file contains all the libraries needed for the project. You will first create a virtual environment to isolate dependencies, install the required packages inside it, and then activate the environment. This ensures that your project runs in a controlled setup without affecting your global Python libraries.

Alternatively, you can manually install Streamlit, FastAPI, and Uvicorn along with other dependencies using pip. Once the setup is complete, verify the installation by running a simple Streamlit hello app to confirm that Streamlit is properly configured.

## Hello World in Streamlit

To check if Streamlit is correctly installed, you can run a simple hello world dashboard. This command launches a small demo interface on port 8501 and lets you explore how Streamlit components like sliders, charts, and widgets work. This step ensures your environment is ready before building the main penguin prediction app.

## Building the UI Step-by-Step

When designing the dashboard, the structure is divided into two sections — a sidebar for interaction and configuration, and a main body section for displaying results. The sidebar helps users input features or upload a file for predictions, while the main body shows results, backend status, and other important information.

The dashboard checks whether the FastAPI backend is online and responds correctly. If the backend is running, the sidebar shows a success message; if not, it warns the user that the backend is offline. This ensures real-time communication between Streamlit and FastAPI.

Next, users can either manually select measurement values through sliders or upload a JSON file containing input data. The sliders allow fine-tuned control for each feature, such as bill length, bill depth, flipper length, and body mass. The JSON upload feature supports more automated testing by directly providing structured data input.

If the user uploads a valid JSON file, the file content is previewed in the sidebar, confirming that the data has been loaded successfully. If no file is provided, the system will only use slider values. Once inputs are set, the user can click on the Predict button to trigger the prediction request.

## Understanding the Interface Components

Streamlit uses widgets like sliders, file uploaders, and buttons to interact with the user. For instance, the sidebar can include a slider for bill length where users can adjust the value within the dataset’s observed range. Similar sliders are used for bill depth, flipper length, and body mass. This interactive approach allows users to experiment with multiple feature combinations easily.

The file uploader provides an alternative method to enter input data. It ensures that users can test multiple prediction cases in one go. If a JSON file of incorrect format is uploaded, Streamlit automatically alerts the user with a warning, preventing invalid submissions.

When the Predict button is pressed, Streamlit sends a POST request to the FastAPI endpoint. The FastAPI server takes this input, runs the trained model, and returns the predicted penguin species as a numeric class which is then displayed as its corresponding label such as Adelie, Chinstrap, or Gentoo.

## Displaying the Prediction

The main body of the dashboard is used to display results. It contains the title, a placeholder for prediction, and various UI elements for dynamic updates. Once a prediction is made, Streamlit shows the species name in a green success box. If the backend connection fails or the model file is missing, an error or warning box is displayed instead.

The app includes simple spinner animations and toast notifications for better user experience. These small interactions help indicate progress when the model is processing predictions, preventing users from thinking the app has frozen.

If the trained model file is not found in the FastAPI directory, the dashboard displays a clear message reminding users to run the training script first. This avoids confusion and ensures all components are properly connected before testing.

## Running the Application

To execute the lab, you must run both the FastAPI backend and the Streamlit frontend. First, navigate to the FastAPI directory and start the backend using Uvicorn. This will launch the server and confirm the startup completion message. Once the backend is running, open a new terminal window, activate your virtual environment, navigate to the Streamlit directory, and run the dashboard using the Streamlit command. The dashboard will automatically open in your default browser.

If you see “Backend offline” in the sidebar, it means the Streamlit app cannot connect to FastAPI. Make sure the FastAPI server is still running on port 8000 and check the URL configuration in your Streamlit script.

Once both applications are connected, you can test predictions by adjusting slider values or uploading a JSON file. The model will then output one of the three penguin species based on the measurements provided.

## Additional Information

The dashboard you just created is a single-page application. However, Streamlit allows you to expand it into a multi-page structure where each page can show different sections, such as model details, dataset statistics, or analysis charts. You can do this by adding files in a folder named “pages” following Streamlit’s naming convention like 1_Home, 2_About, and so on.

To run the FastAPI server, always use the Uvicorn command with reload enabled. This makes sure that any change in the code is reflected instantly without restarting the server manually.

The Streamlit app runs locally by default, but you can deploy it online on Streamlit Community Cloud or connect it with a public server to make it accessible remotely. This makes it easier to demonstrate your model predictions to others interactively.

## Summary

In this lab, we successfully built an end-to-end machine learning application using FastAPI and Streamlit. The FastAPI backend hosts a trained model on the Penguins dataset, while Streamlit provides a visual interface for testing the model with various inputs. The app checks backend connectivity, accepts user input through sliders or files, and displays real-time predictions.

This hands-on lab demonstrates how to bridge backend model deployment with an interactive dashboard, providing a complete workflow from data to deployment. It showcases how easy it is to create real-time applications where machine learning meets user experience — turning models into accessible tools for exploration and understanding.
