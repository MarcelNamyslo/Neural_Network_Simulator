import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import NN
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QDialog,QVBoxLayout

class ANNGraph:
    def __init__(self, Network):
        self.Network = Network
        self.graph = nx.DiGraph()
        for layer_idx, layer in enumerate(Network.layers):
            for neuron in layer:
                # Adding nodes with attributes
                
                self.graph.add_node(str(neuron.id), neuron=neuron)

                if layer_idx > 0:
                    for dendron in neuron.dendrons:
                        self.graph.add_edge(str(dendron.connectedNeuron.id), str(neuron.id))

        self.pos = {}
        for layer_idx, layer in enumerate(Network.layers):
            x = layer_idx
            y_spacing = 1.0 / (len(layer) + 1)
            y_offset = (1.0 - y_spacing * len(layer))   # Calculate offset for centering
            for neuron_idx, neuron in enumerate(layer):
                self.pos[str(neuron.id)] = (x, y_offset + neuron_idx * y_spacing)  # Add y_offset

        self.node_colors = [self.pos[node][0] for node in self.graph.nodes()]
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Neural Network Graph')
        self.canvas = self.fig.canvas

        #self.plot_graph()

        self.cid = self.canvas.mpl_connect('button_press_event', self.on_node_click)
        #plt.show()

    def plot_graph(self):
        nx.draw(self.graph, pos=self.pos, with_labels=True, node_size=1000, font_size=10, cmap=plt.cm.RdYlBu, node_color=self.node_colors, ax=self.ax)


    def focus(self, layer):
        focus_layer= []
        #nx.draw(self.graph, pos=self.pos, node_size=1000, font_size=10, cmap=plt.cm.RdYlBu, node_color=self.node_colors, ax=self.ax)
        special_node_pos = self.pos.copy()
        focus_node_size= []
        
        for lay in range(len(self.Network.layers)):
            if lay == layer:
                for node in self.Network.layers[lay]:
                    focus_layer.append(str(node.id))
                    
        for node_id in focus_layer:
            x, y = special_node_pos[node_id]
            special_node_pos[node_id] = (x + 0.04, y)
            focus_node_size.append(1500)
        
        #nx.draw_networkx_nodes(self.graph, special_node_pos, nodelist=focus_layer, node_size=focus_node_size, node_color='yellow', edgecolors='black')

        label_offset = [0.0, 0.0]
        label_pos = self.pos.copy()
        for node in focus_layer:
            if node in special_node_pos:
                special_node_x, special_node_y = special_node_pos[node]
                label_pos[node] = (special_node_x + label_offset[0], special_node_y + label_offset[1])
                

        return label_pos
        # Draw the label for node C
        #nx.draw_networkx_labels(self.graph, pos= label_pos, font_size=10, font_color='black')
        #plt.show()
        

        

      

    def on_node_click(self, event):
        x, y = event.xdata, event.ydata
        clicked_node_id = None
        for node, (node_x, node_y) in self.pos.items():
            distance = ((node_x - x) ** 2 + (node_y - y) ** 2) ** 0.5
            if distance < 0.2:  # Adjust this threshold as needed
                clicked_node_id = node
                break

        if clicked_node_id is not None:
            for node_id, attributes in self.graph.nodes(data=True):
                if node_id == clicked_node_id:
                    clicked_neuron = attributes['neuron']  # Set the clicked_neuron variable

        if clicked_neuron is not None:  # Check if a neuron was clicked                                                                                                           self.pos[node][0] for node in self.graph.nodes()


            neuron_info = (
        "Neuron ID: {}\nGradient: {}\nOutput: {}\nError: {}\nDendrons:\n{}".format(
        clicked_neuron.id,
        clicked_neuron.gradient,
        clicked_neuron.output,
        clicked_neuron.error,
        "\n".join(
            [
                "ID: {}, Weight: {}".format(den.connectedNeuron.id, den.weight)
                for den in clicked_neuron.dendrons
            ]
        ),
    )
)

            
        
        popup = QDialog()
        popup.setWindowTitle("Node Info")
        popup.adjustSize()
        layout = QVBoxLayout()

        label = QLabel(neuron_info, popup)
        layout.addWidget(label)

        popup.setLayout(layout)
        # Create a pop-up window to display neuron information
        popup.exec_()

def main():
    topology = [2, 1, 5,1,4]
    net = NN.Network(topology)
    graph = ANNGraph(net)

    graph.focus(3)
    
if __name__ == '__main__':
    main()
