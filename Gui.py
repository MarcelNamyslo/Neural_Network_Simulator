
import sys
import networkx as nx
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt 
from PyQt5.QtWidgets import QApplication,QDesktopWidget, QMainWindow, QDialog,QTextEdit, QFrame,QHBoxLayout, QVBoxLayout, QTabWidget,QLineEdit, QPushButton, QWidget, QInputDialog, QVBoxLayout, QLabel,QApplication, QMainWindow, QPushButton, QVBoxLayout,QMessageBox, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ConfigDialog import ConfigDialog
from  visualization import ANNGraph
from InputPairsDialog import InputPairsDialog
from Predict_dialog import Predict_dialog
import NN
from PyQt5.QtGui import QIcon

class GraphVisualizerApp(QMainWindow):
    def __init__(self):
        self.Farbe1 = "#f0fff0"
        
        self.Farbe3 = "#"
        super().__init__()
        screen = QApplication.primaryScreen()
        size = screen.size()
        self.setWindowTitle("Graph Visualizer")
        self.setGeometry(int(size.width() * 0.20), int(size.height()* 0.18), 1200, 800)
        self.setStyleSheet(f"background-color: {self.Farbe1}; color: #003e19;")

        self.graph_widgets = []

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.info_widget = QLabel("Welcome to the Graph Visualizer!")
        
        self.info_widget.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.info_widget)

        self.tab_widget = QTabWidget(self)
        self.layout.addWidget(self.tab_widget)

        self.add_tab_button = QPushButton("Create a new Network!")
        self.add_tab_button.clicked.connect(self.add_tab)
        self.tab_widget.addTab(self.add_tab_button, "Main")

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

        icon = QIcon("NN/Predict_dialog.py")  # Replace with the actual path to your icon file
        self.setWindowIcon(icon)
    
    
    """
    add a new tab with a new network
    """
    def add_tab(self):
        tab_name = Name_Dialog.get_text(self)
        if tab_name:
            new_tab_index = self.tab_widget.count() - 1
            new_tab_widget = GraphConfigurationWidget()
            self.graph_widgets.append(new_tab_widget)
            self.tab_widget.insertTab(new_tab_index, new_tab_widget, tab_name)
            self.tab_widget.setCurrentIndex(new_tab_index)

"""
widget to configurate your network and it layers and number of Neurons
"""
class GraphConfigurationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        self.alpha_label = QLabel()
        self.layout.addWidget(self.alpha_label)
        self.beta_label = QLabel()
        self.layout.addWidget(self.beta_label)
       
        

        self.graph_tab_widget = GraphTabWidget(self)  # Create a GraphTabWidget
        #self.graph_tab_widget.setStyleSheet("background-color: lightgray;")
        self.layout.addWidget(self.graph_tab_widget)

        self.setLayout(self.layout)
        self.input_dialog = ConfigDialog(layers = None, parent=self)
        self.input_dialog.exec_()
        
    def create_graph(self, alpha, beta, topology):
        print("your number: ", topology)
        self.alpha_label.setText(f"Alpha: {alpha}")
        self.beta_label.setText(f"Beta: {beta}")
        net = NN.Network(topology, float(alpha), float(beta))
        self.graph_tab_widget.create_graph(net, labels = True)  


class GraphTabWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
      
        self.Farbe2 = "#689c97"
        self.Farbe3 = "#072a24"
        self.parent_widget = parent
        self.graph = nx.Graph()

        self.input_pairs = []
        self.inputs_to_predict = (int, int)
        self.focused_layer = 0


        self.layout = QVBoxLayout(self)
    
        # Canvas and inputs
        self.canvas_and_input_layout = QHBoxLayout()
        self.canvas = FigureCanvas(plt.figure(figsize=(5, 5)))
        self.canvas_and_input_layout.addWidget(self.canvas, 80)

        self.inputs_and_prediction_layout = QVBoxLayout()
        self.input_pairs_label = QLabel(self)
        self.input_pairs_label.setText("inputs:")
        self.prediction_label = QLabel(self)
        self.prediction_label.setText("prediction:")
        self.inputs_and_prediction_layout.addWidget(self.input_pairs_label)
        self.inputs_and_prediction_layout.addWidget(self.prediction_label)

        self.canvas_and_input_layout.addLayout(self.inputs_and_prediction_layout, 20)
        self.layout.addLayout(self.canvas_and_input_layout)

        self.define_inputs_button = QPushButton("define inputs", self)
        self.define_inputs_button.setStyleSheet(f"background-color: {self.Farbe2}; color: white;")
        self.define_inputs_button.clicked.connect(self.define_inputs)
       

        self.layout.addWidget(self.define_inputs_button)

        self.change_topology_button = QPushButton("change_topology", self)
        self.change_topology_button.clicked.connect(self.change_topology)
        self.change_topology_button.setStyleSheet(f"background-color: {self.Farbe2}; color: white;")
        self.layout.addWidget(self.change_topology_button)

        button_layout = QHBoxLayout()

        self.one_step_forward_button = QPushButton("forward propagate one step", self)
        self.one_step_forward_button.clicked.connect(self.forward_propagate_one_step)
        self.one_step_forward_button.setStyleSheet(f"background-color: {self.Farbe2}; color: white;")
        button_layout.addWidget(self.one_step_forward_button)

        self.one_step_backward_button = QPushButton("backward propagate one step", self)
        self.one_step_backward_button.clicked.connect(self.backward_propagate_one_step)
        self.one_step_backward_button.setStyleSheet(f"background-color: {self.Farbe2}; color: white;")
        button_layout.addWidget(self.one_step_backward_button)

        self.layout.addLayout(button_layout)

        button_layout = QHBoxLayout()

        self.forwardpropagate_button = QPushButton("forward propagate", self)
        self.forwardpropagate_button.clicked.connect(self.forword_propagate)
        self.forwardpropagate_button.setStyleSheet(f"background-color: {self.Farbe2}; color: white;")
        button_layout.addWidget(self.forwardpropagate_button)

        self.backwardpropagate_button = QPushButton("backward propagate ", self)
        self.backwardpropagate_button.clicked.connect(self.backward_propagate)
        self.backwardpropagate_button.setStyleSheet(f"background-color: {self.Farbe2}; color: white;")
        button_layout.addWidget(self.backwardpropagate_button)
        self.layout.addLayout(button_layout)

        self.backwardpropagate_button = QPushButton("Train Network ", self)
        self.backwardpropagate_button.clicked.connect(self.train_network)
        self.backwardpropagate_button.setStyleSheet(f"background-color: {self.Farbe2}; color: white;")
        self.layout.addWidget(self.backwardpropagate_button)

        self.backwardpropagate_button = QPushButton("predict ", self)
        self.backwardpropagate_button.clicked.connect(self.predict)
        self.backwardpropagate_button.setStyleSheet(f"background-color: {self.Farbe2}; color: white;")
        self.layout.addWidget(self.backwardpropagate_button)

    
    def define_inputs(self):
        self.input_pairs_dialog = InputPairsDialog(self)
        self.input_pairs_dialog.exec_()

    def setinputs(self, input_pairs):
        self.input_pairs = input_pairs
        self.network_input = []
        self.network_output = []
        for item in input_pairs:
            self.network_input.append(item[0])
            self.network_output.append(item[1])

        self.network_output
        input_text = "\n".join([f"{i + 1}. input: ({item[0][0]}, {item[0][1]})  \t   output: ({item[1][0]}, {item[1][1]}) \n" for i, item in enumerate(input_pairs)])
        
        self.input_pairs_label.setText(input_text)
        self.network.setInput(input_pairs[0][0])
        
        self.create_graph(self.network, labels=False)
        
        label_pos= self.focus(self.focused_layer)
        nx.draw_networkx_labels(self.graph, pos= label_pos, font_size=10, font_color='black', ax = self.ax)
        self.canvas.draw()

    def focus(self, layer):
        focus_layer= []
        #nx.draw(self.graph, pos=self.annGraph.pos, with_labels=True, node_size=1000, font_size=10, cmap=plt.cm.RdYlBu, node_color=self.annGraph.node_colors, ax=self.ax)
        special_node_pos = self.annGraph.pos.copy()
        focus_node_size= []
        
        for lay in range(len(self.annGraph.Network.layers)):
            if lay == layer:
                for node in self.annGraph.Network.layers[lay]:
                    focus_layer.append(str(node.id))
                    
        for node_id in focus_layer:
            x, y = special_node_pos[node_id]
            if node_id == 0 or node_id == 1 :
                special_node_pos[node_id] = (x - 0.15, y)
            else:
                special_node_pos[node_id] = (x + 0.02, y)
            focus_node_size.append(1500)
        
        nx.draw_networkx_nodes(self.graph, special_node_pos, nodelist=focus_layer, node_size=focus_node_size, node_color='lightsalmon', edgecolors='black',ax=self.ax )

        label_offset = [0.0, 0.0]
        label_pos = self.annGraph.pos.copy()
        for node in focus_layer:
            if node in special_node_pos:
                special_node_x, special_node_y = special_node_pos[node]
                label_pos[node] = (special_node_x + label_offset[0], special_node_y + label_offset[1])
                
        return label_pos
    
        # Draw the label for node C
        #nx.draw_networkx_labels(self.graph, pos= label_pos, font_size=10, font_color='black')
        #plt.show()


    def change_topology(self):
        self.graph.clear()  # Clear the graph
        self.canvas.figure.clear()  # Clear the canvas
        self.canvas.draw()
        self.configDialog = ConfigDialog(layers = self.network.topology, parent= self.parent_widget)
        self.configDialog.exec_()
        

    def create_graph(self, network ,labels):
        self.network= network
        self.graph.clear()  # Clear the existing graph
        self.annGraph = ANNGraph(network)  # Create the new graph
        self.graph = self.annGraph.graph
        pos = nx.spring_layout(self.graph)
        self.ax = self.canvas.figure.add_subplot(111)
        self.cid = self.canvas.mpl_connect('button_press_event',  self.annGraph.on_node_click)
        nx.draw(self.graph, self.annGraph.pos, with_labels=labels, node_size=1000, font_size=10,node_color= self.annGraph.node_colors, ax=self.ax )
        self.canvas.draw()

    def forward_propagate_one_step(self):
        self.canvas.figure.clear()
        self.network.one_step_feedForward()
        self.focused_layer = self.focused_layer +1
        self.create_graph(self.network, labels= False)
        label_pos= self.focus(self.focused_layer)
        nx.draw_networkx_labels(self.graph, pos= label_pos, font_size=10, font_color='black', ax = self.ax)
        self.canvas.draw()
    
    def forword_propagate(self):
        self.canvas.figure.clear()
        self.network.feedForword()
        self.focused_layer = len(self.network.layers) -1
        self.create_graph(self.network, labels= False)
        label_pos= self.focus(self.focused_layer)
        nx.draw_networkx_labels(self.graph, pos= label_pos, font_size=10, font_color='black', ax = self.ax)
        self.canvas.draw()
    
    def backward_propagate_one_step(self):
        self.canvas.figure.clear()
        self.network.one_step_backPropagate(self.input_pairs[0][1])
        self.focused_layer = self.focused_layer -1
        self.create_graph(self.network, labels= False)
        label_pos= self.focus(self.focused_layer)
        nx.draw_networkx_labels(self.graph, pos= label_pos, font_size=10, font_color='black', ax = self.ax)
        self.canvas.draw()

    def backward_propagate(self):
        self.canvas.figure.clear()
        self.network.backPropagate(self.input_pairs[0][1])
        self.focused_layer = 0
        self.create_graph(self.network, labels= False)
        label_pos= self.focus(self.focused_layer)
        nx.draw_networkx_labels(self.graph, pos= label_pos, font_size=10, font_color='black', ax = self.ax)
        self.canvas.draw()

    def train_network(self):
        self.network.train_network(self.network_input, self.network_output)
        self.canvas.figure.clear()
        self.create_graph(self.network, labels= True)
    
    def predict(self):
        self.predict_dialog = Predict_dialog(parent=self)
        self.predict_dialog.exec_()

        predicted_output = self.network.predict(self.inputs_to_predict[0], self.inputs_to_predict[1])

        input_text = f"Input you gave     \t   {(self.inputs_to_predict)} \n \nPredicted Output:   \t   ({(predicted_output[0])}, {(predicted_output[1])}) "
        self.prediction_label.setText(input_text)
        a = predicted_output

class topology_Dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Input Dialog")
        self.setMinimumWidth(500)

class Name_Dialog(QDialog):
    def __init__(self, parent=None, type = str):
        super().__init__(parent)
        self.setWindowTitle("Input Dialog")
        self.setMinimumWidth(300)
        
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Enter the name of the tab")
        self.layout.addWidget(self.label)
       
        self.text_input = QLineEdit()
        self.layout.addWidget(self.text_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept_input)
        self.layout.addWidget(self.ok_button)
        
    def accept_input(self):
        user_input = self.text_input.text()
        if user_input:
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Enter the name of the tab", QMessageBox.Ok)
    
    def get_text(parent=None, type = str):
        dialog = Name_Dialog(parent, type)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            return dialog.text_input.text()
        return None
    
class Input_Dialog(QDialog):
    def __init__(self, parent=None, type = str):
        super().__init__(parent)
        self.setWindowTitle("Input Dialog")
        self.setMinimumWidth(300)
        
        self.layout = QVBoxLayout(self)

        self.label = QLabel("Enter the name of the tab")
        self.layout.addWidget(self.label)
       
        self.text_input = QLineEdit()
        self.layout.addWidget(self.text_input)
        
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept_input)
        self.layout.addWidget(self.ok_button)
        
    def accept_input(self):
        user_input = self.text_input.text()
        if user_input:
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Enter the name of the tab", QMessageBox.Ok)
    
    def get_text(parent=None, type = str):
        dialog = Name_Dialog(parent, type)
        result = dialog.exec_()
        if result == QDialog.Accepted:
            return dialog.text_input.text()
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphVisualizerApp()
    window.show()
    sys.exit(app.exec_())
