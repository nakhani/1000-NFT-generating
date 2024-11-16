import os
import random
from PIL import Image
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget, QMessageBox, QLineEdit
from PySide6.QtGui import QPalette, QColor
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("NFT Generator")
        self.setGeometry(300, 300, 400, 200)

        # Set up the dark mode palette
        self.setPalette(self.create_dark_palette())

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

        self.label_number = QLabel("Enter the number of images to generate:")
        layout.addWidget(self.label_number)

        self.number_input = QLineEdit()
        layout.addWidget(self.number_input)

        self.process_button = QPushButton("Start Process")
        self.process_button.clicked.connect(self.start_process)
        layout.addWidget(self.process_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.source_directory = ""
        self.output_directory = ""
        self.max_combinations = 0

        # Apply styling
        self.apply_styles()

    def create_dark_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(18, 18, 18))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(18, 18, 18))
        palette.setColor(QPalette.ToolTipBase, Qt.black)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        return palette

    def apply_styles(self):
        self.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #444444;
                color: #FFFFFF;
                border: 1px solid #555555;
                padding: 8px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
        """)

    def select_source_directory(self):
        self.source_directory = QFileDialog.getExistingDirectory(self, "Select Source Directory")
        self.label.setText(f"Source directory: {self.source_directory}")

    def select_output_directory(self):
        self.output_directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        self.label_output.setText(f"Output directory: {self.output_directory}")

    def start_process(self):
        if not self.source_directory:
            QMessageBox.warning(self, "Selection Error", "Please select a source directory.")
            return
        if not self.output_directory:
            QMessageBox.warning(self, "Selection Error", "Please select an output directory.")
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

        # Calculate the maximum number of combinations
        self.max_combinations = 1
        for files in layers.values():
            self.max_combinations *= len(files)

        try:
            num_images = int(self.number_input.text())
            if num_images > self.max_combinations:
                QMessageBox.warning(self, "Input Error", f"Maximum number you can use is {self.max_combinations}.")
                return
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter a valid number.")
            return

        self.label_output.setText("Processing...")
        QApplication.processEvents()  # This line forces the GUI to update

        lsid = set()
        for i in range(1, num_images + 1):
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
