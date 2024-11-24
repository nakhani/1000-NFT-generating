# NFT Generator

NFT Generator is a Python application that allows you to generate unique NFT images by combining various layers from different subfolders. The application includes a graphical user interface (GUI) built with PySide6.

## Features
- Select a source directory containing subfolders with layout images.
- Select an output directory to save the generated NFT images.
- Input the number of image which should be generated.
- Generates unique NFT images by combining random layers.
- Ensures only PNG images are processed.
- Alerts the user if invalid files (non-PNG) are found in the subfolders.

## Requirements
- Python 3.x
- Required Python libraries:
  - Pillow
  - OpenCV
  - PySide6

## Installation
1. Clone this repository to your local machine:
    ```bash
    git clone https://github.com/nakhani/NFT-generating.git
    ```

2. Navigate to the project directory:
    ```bash
    cd NFT-generating
    ```

3. Install the required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the application:
    ```bash
    python NFT.py
    ```

2. Use the GUI to select the source directory containing your layout images and the output directory to save the generated NFT images.

3. Input the number of images which you want to be generated.

4. Click the "Start Process" button to generate 1000 unique NFT images.

## File Structure
- **NFT.py**: The main Python script containing the GUI and image generation logic.
- **requirements.txt**: A file listing the required Python libraries.

## Example
```plaintext
source_directory/
├── background/
│   ├── background_1.png
│   ├── background_2.png
│   └── ...
├── bod/
│   ├── bod_1.png
│   ├── bod_2.png
│   └── ...
├── body/
│   ├── body_1.png
│   ├── body_2.png
│   └── ...
├── eye/
│   ├── eye_1.png
│   ├── eye_2.png
│   └── ...
├── hat/
│   ├── hat_1.png
│   ├── hat_2.png
│   └── ...
├── mouth/
│   ├── mouth_1.png
│   ├── mouth_2.png
│   └── ...
└── access/
    ├── access_1.png
    ├── access_2.png
    └── ...
