import os
import random
from PIL import Image
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NFT Generator")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Select the folder containing your layout images:")
        layout.addWidget(self.label)

        self.select_source_button = QPushButton("Select Source Directory")
        self.select_source_button.clicked.connect(self.select_source_directory)
        layout.addWidget(self.select_source_button)

        self.label_output = QLabel("Select the folder to save outputs:")
        layout.addWidget(self.label_output)

        self.select_output_button = QPushButton("Select Output Directory")
        self.select_output_button.clicked.connect(self.select_output_directory)
        layout.addWidget(self.select_output_button)

        self.process_button = QPushButton("Start Process")
        self.process_button.clicked.connect(self.start_process)
        layout.addWidget(self.process_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.source_directory = ""
        self.output_directory = ""

    def select_source_directory(self):
        self.source_directory = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        self.label.setText(f"Source directory: {self.source_directory}")

    def select_output_directory(self):
        self.output_directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        self.label_output.setText(f"Output directory: {self.output_directory}")

    def start_process(self):
        if not self.source_directory:
            self.label.setText("Please select a source directory first.")
            return
        if not self.output_directory:
            self.label_output.setText("Please select an output directory first.")
            return

        layers = {}
        invalid_files = {}
        for subfolder in os.listdir(self.source_directory):
            subfolder_path = os.path.join(self.source_directory, subfolder)
            if os.path.isdir(subfolder_path):
                files = os.listdir(subfolder_path)
                png_files = [file for file in files if file.lower().endswith('.png')]
                non_png_files = [file for file in files if not file.lower().endswith('.png')]
                if png_files:
                    layers[subfolder] = png_files
                if non_png_files:
                    invalid_files[subfolder] = non_png_files

        if invalid_files:
            invalid_files_message = "Invalid files found:\n"
            for folder, files in invalid_files.items():
                invalid_files_message += f"{folder}: {', '.join(files)}\n"
            print(invalid_files_message)
            QMessageBox.critical(self, "Invalid Files", f"Invalid files found. Please upload only PNG images.\n\n{invalid_files_message}")
            self.label.setText("Invalid files found. Please upload only PNG images.")
            return

        if not layers:
            self.label.setText("No valid PNG image folders found. Please check your source directory.")
            return

        lsid = set()
        for i in range(1, 1001):
            while True:
                selected_layers = {layer: random.choice(layers[layer]) for layer in layers}
                combination = ''.join(selected_layers.values())
                if combination not in lsid:
                    lsid.add(combination)
                    break

            images = {layer: Image.open(os.path.join(self.source_directory, layer, selected_layers[layer])) for layer in selected_layers}
            base_image = next(iter(images.values())).convert('RGBA')

            for layer_image in list(images.values())[1:]:
                layer_image = layer_image.convert('RGBA')
                base_image.paste(layer_image, (0, 0), layer_image)

            output_path_png = os.path.join(self.output_directory, f"{i}.png")
            base_image.save(output_path_png)

        print(len(lsid))
        print("Process completed")
        self.label_output.setText("Process completed.")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
