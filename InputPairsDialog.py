import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

class InputPairsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.parentWidget = parent
        self.setWindowTitle("Input Output")
        
        self.data_pairs = []
        
        self.layout = QVBoxLayout()
        
        self.pair_layouts = []
        
        self.add_pair_layout()
        
        self.add_button = QPushButton("Add Inputs")
        self.add_button.clicked.connect(self.sendInputs)
        
        self.add_pair_button = QPushButton("Add Another Pair")
        self.add_pair_button.clicked.connect(self.add_pair_layout)
        
        self.layout.addWidget(self.add_pair_button)
        self.layout.addWidget(self.add_button)
        
        self.setLayout(self.layout)
        
    def add_pair_layout(self):
        pair_layout = QHBoxLayout()
    
        label1 = QLabel(f"Input Pair {len(self.pair_layouts) + 1}     ")

        label2 = QLabel(f"(")
        number2_combobox = QComboBox()
        number2_combobox.addItems(["0", "1"])
        
        label3 = QLabel(")   (")
        number3_combobox = QComboBox()
        number3_combobox.addItems(["0", "1"])

        label4 = QLabel(")              Output Pair:    ")

        label5 = QLabel("(")
        number5_combobox = QComboBox()
        number5_combobox.addItems(["0", "1"])

        label6 = QLabel(")   (")
        number6_combobox = QComboBox()
        number6_combobox.addItems(["0", "1"])
        label7 = QLabel(")")
        
        pair_layout.addWidget(label1)
        pair_layout.addWidget(label2)
        pair_layout.addWidget(number2_combobox)
        pair_layout.addWidget(label3)
        pair_layout.addWidget(number3_combobox)
        pair_layout.addWidget(label4)
        pair_layout.addWidget(label5)
        pair_layout.addWidget(number5_combobox)
        pair_layout.addWidget(label6)
        pair_layout.addWidget(number6_combobox)
        pair_layout.addWidget(label7)
        
        self.pair_layouts.append((number2_combobox, number3_combobox, number5_combobox,number6_combobox))
        self.layout.insertLayout(len(self.pair_layouts) - 1, pair_layout)
    
        
    def add_numbers(self):
        pairs_added = False
        
        for pair_layout in self.pair_layouts:
            number1 = int(pair_layout[0].currentText())
            number2 = int(pair_layout[1].currentText())
            input = (number1, number2)

            number3 = int(pair_layout[2].currentText())
            number4 = int(pair_layout[3].currentText())
            output = (number3, number4)

            self.data_pairs.append((input, output))
            pairs_added = True
        
        if pairs_added:
            print("Pairs added:", self.data_pairs)

    def sendInputs(self):
         self.add_numbers()
         self.parentWidget.setinputs(self.data_pairs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = InputPairsDialog()
    dialog.exec_()
