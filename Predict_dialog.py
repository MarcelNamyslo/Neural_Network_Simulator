import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class Predict_dialog(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.parent_widget = parent
        self.setWindowTitle("Tuple Input Dialog")

        self.value1_label = QLabel("Enter value 1 (between 0 and 1):")
        self.value1_input = QLineEdit(self)

        self.value2_label = QLabel("Enter value 2 (between 0 and 1):")
        self.value2_input = QLineEdit(self)

        self.submit_button = QPushButton("Predict Tuple: ", self)
        self.submit_button.clicked.connect(self.create_tuple)

        layout = QVBoxLayout()
        layout.addWidget(self.value1_label)
        layout.addWidget(self.value1_input)
        layout.addWidget(self.value2_label)
        layout.addWidget(self.value2_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def create_tuple(self):
        value1 = self.value1_input.text()
        value2 = self.value2_input.text()

        try:
            value1 = int(value1)
            value2 = int(value2)

            if 0 <= value1 <= 1 and 0 <= value2 <= 1:
                result_tuple = (value1, value2)
                self.parent_widget.inputs_to_predict = result_tuple
                #QMessageBox.information(self, "Tuple Created", f"Tuple created: {result_tuple}")
                print("Tuple created:", result_tuple)
                self.accept()
                
            else:
                QMessageBox.warning(self, "Invalid Values", "Values must be between 0 and 1.")
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numeric values.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Predict_dialog()
    dialog.exec_()
