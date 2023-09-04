import math
import numpy as np

class Connection:
    def __init__(self, connectedNeuron):
        self.connectedNeuron = connectedNeuron
        self.weight = np.random.normal()
        self.dWeight = 0.0


class Neuron:
    #eta = 0.2
    #alpha = 0.01
    eta = 0.09
    alpha = 0.015

    def __init__(self, layer, id):
        self.id = id
        self.dendrons = []
        self.error = 0.0
        self.gradient = 0.0
        self.output = 0.0
        if layer is None:
            pass
        else:
            for neuron in layer:
                con = Connection(neuron)
                self.dendrons.append(con)

    def addError(self, err):
        self.error = self.error + err

    def sigmoid(self, x):
        return 1 / (1 + math.exp(-x * 1.0))

    def dSigmoid(self, x):
        return x * (1.0 - x)

    def setError(self, err):
        self.error = err

    def setOutput(self, output):
        self.output = output

    def getOutput(self):
        return self.output

    def feedForword(self):
        sumOutput = 0
        if len(self.dendrons) == 0:
            return
        for dendron in self.dendrons:
            sumOutput = sumOutput + float(dendron.connectedNeuron.getOutput()) * dendron.weight
        self.output = self.sigmoid(sumOutput)

    def backPropagate(self):
        self.gradient = self.error * self.dSigmoid(self.output);
        for dendron in self.dendrons:
            dendron.dWeight = Neuron.eta * (
            dendron.connectedNeuron.output * self.gradient) + self.alpha * dendron.dWeight;
            dendron.weight = dendron.weight + dendron.dWeight;
            dendron.connectedNeuron.addError(dendron.weight * self.gradient);
        self.error = 0;


class Network:
    def __init__(self, topology, alpha, eta):
        self.layers = []
        self.topology = topology
        id = 0
        self.feed_forward_iterations = 1
        Neuron.alpha = alpha
        Neuron.eta = eta
        for numNeuron in topology:
            layer = []
            for i in range(numNeuron):
                if (len(self.layers) == 0):
                    layer.append(Neuron(None, id))
                    id = id +1
                else:
                    layer.append(Neuron(self.layers[-1], id))
                    id = id +1
            #layer.append(Neuron(None,id))
            #id = id +1
            #layer[-1].setOutput(1)
            self.layers.append(layer)

    def setInput(self, inputs):
        for i in range(len(inputs)):
            self.layers[0][i].setOutput(inputs[i])

    def feedForword(self):
        for layer in self.layers[1:]:
            for neuron in layer:
                neuron.feedForword();
        self.feed_forward_iterations = len(self.topology)
    
    def one_step_feedForward(self):
        for neuron in self.layers[self.feed_forward_iterations]:
                neuron.feedForword();

    def backPropagate(self, target):
        for i in range(len(target)):
            self.layers[-1][i].setError(target[i] - self.layers[-1][i].getOutput())
        for layer in self.layers[::-1]:
            for neuron in layer:
                neuron.backPropagate()

    def getError(self, target):
        err = 0
        for i in range(len(target)):
            e = (target[i] - self.layers[-1][i].getOutput())
            err = err + e ** 2
        err = err / len(target)
        err = math.sqrt(err)
        return err

    def getResults(self):
        output = []
        for neuron in self.layers[-1]:
            output.append(neuron.getOutput())
        output.pop()
        return output

    def getThResults(self):
        output = []
        for neuron in self.layers[-1]:
            o = neuron.getOutput()
            if (o > 0.5):
                o = 1
            else:
                o = 0
            output.append(o)
        return output
    
    def get_neuron_by_id(self, id):
        for layer in range(len(self.layers)):
            for neuron in range(len(self.layers[layer])):
                if self.layers[layer][neuron].id == id:
                    return self.layers[layer][neuron]

    
    def train_network(self, inputs, outputs):
        trained = False
        while not trained:

            err = 0
           
            for i in range(len(inputs)):
                self.setInput(inputs[i])
                self.feedForword()
                self.backPropagate(outputs[i])
                err = err + self.getError(outputs[i])
            print("error: ", err)
            if err < 0.5:
                trained = True
                

        #while True:
            #a = input("type 1st input :")
            #b = input("type 2nd input :")
            #self.setInput([a, b])
            #self.feedForword()
            #print(self.getThResults())
    
    def predict(self, a, b):
        self.setInput([a, b])
        self.feedForword()
        results= (self.getThResults())
        return results

def main():
    topology = []
    topology.append(2)
    topology.append(3)
    topology.append(2)
    net = Network(topology)
    #net.run_network()
    Neuron.eta = 0.09
    Neuron.alpha = 0.015
    inputs = [[0, 0], [0, 1], [1, 0], [1, 1]]
    outputs = [[0, 0], [1, 0], [1, 0], [0, 1]]
    net.train_network(inputs, outputs)
    #net.setInput(inputs[0])
    net.train_network()

    

if __name__ == '__main__':
    main()