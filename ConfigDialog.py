
import sys
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSpinBox

class ConfigDialog(QDialog):
    def __init__(self, layers, parent=None):
        super().__init__(parent)
        self.parent_widget = parent

        self.layers = layers

        self.setStyleSheet("background-color: #f0fff0; color: black;")
        self.dataEntered = pyqtSignal(str, str, list)
        self.setWindowTitle("Neural Network Configuration")
        screen = QApplication.primaryScreen()
        size = screen.size()
        width = self.width
        height = self.height
        #self.setGeometry(int(size.width() * 0.40), int(size.height()* 0.28), width, height)
        self.layout = QVBoxLayout()

        self.alpha_label = QLabel("Alpha:")
        self.alpha_input = QLineEdit()
        self.alpha_input.setText("0.015")

        self.beta_label = QLabel("Beta:")
        self.beta_input = QLineEdit()
        self.beta_input.setText("0.09")

        alpha_beta_layout = QHBoxLayout()
        alpha_beta_layout.addWidget(self.alpha_label)
        alpha_beta_layout.addWidget(self.alpha_input)
        alpha_beta_layout.addWidget(self.beta_label)
        alpha_beta_layout.addWidget(self.beta_input)

        self.layout.addLayout(alpha_beta_layout)

        self.layer_inputs_layout = QVBoxLayout()  # Container for layer inputs
        self.neuron_inputs = []
        self.layers_label = QLabel("Number of Layers:")
        self.layers_input = QSpinBox()
        self.layers_input.setMinimum(1)
        self.layers_input.valueChanged.connect(self.update_layer_inputs)
        self.number_of_layers = self.layers_input.value()
        self.layer_inputs_layout.addWidget(self.layers_label)
        self.layer_inputs_layout.addWidget(self.layers_input)

        if self.layers != None:
            self.update = True
            i = 1
            for layer in self.layers:
                layer_label = QLabel(f"Layer {i} Neurons:")
                
                
                layer_input = QSpinBox()
                layer_input.setValue(layer)
                if i == 1:
                    layer_input.setValue(2)  # Set an initial value
                    layer_input.setEnabled(False)
                self.neuron_inputs.append((layer_label, layer_input))
                self.layer_inputs_layout.addWidget(layer_label)
                self.layer_inputs_layout.addWidget(layer_input)
                i= i+1
        else:
            self.update = False
            layer_label = QLabel(f"Layer {1} Neurons:")
            layer_input = QSpinBox()
          
            layer_input.setValue(2)  # Set an initial value
            layer_input.setEnabled(False)
            self.neuron_inputs.append((layer_label, layer_input))
            self.layer_inputs_layout.addWidget(layer_label)
            self.layer_inputs_layout.addWidget(layer_input)

        



        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.send_inputs)

        # Add layer inputs layout and OK button layout to the main layout
        self.layout.addLayout(self.layer_inputs_layout)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)

    def update_layer_inputs(self, new_value):
        previous_value = self.number_of_layers
        if new_value > previous_value:
            for layer in range(previous_value + 1, new_value + 1):
                
                layer_label = QLabel(f"Layer {layer} Neurons:")
                layer_input = QSpinBox()
                layer_input.setMinimum(1)
                    
                self.neuron_inputs.append((layer_label, layer_input))
                self.layer_inputs_layout.addWidget(layer_label)
                self.layer_inputs_layout.addWidget(layer_input)

            self.number_of_layers = new_value
            self.adjustSize()
        elif new_value < previous_value:
            for _ in range(previous_value, new_value, -1):
                removed_label, removed_input = self.neuron_inputs.pop()
                removed_label.deleteLater()
                removed_input.deleteLater()

            self.adjustSize()
            self.number_of_layers = new_value
    
    def send_inputs(self):
        # This method is called when the "OK" button is clicked

        # Gather the entered data
        alpha = self.alpha_input.text()
        beta = self.beta_input.text()
        layer_data = []

        for neuron_label, neuron_input in self.neuron_inputs:
            layer_neuron_count = neuron_input.value()
            layer_data.append(layer_neuron_count)

        # Display the gathered data
        print("Alpha:", alpha)
        print("Beta:", beta)
        print("Layer Neuron Counts:", layer_data)
        try:    
    
            self.parent_widget.create_graph(alpha, beta, layer_data)
            self.accept()

        except ValueError:
            pass    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = ConfigDialog()
    dialog.exec_()
