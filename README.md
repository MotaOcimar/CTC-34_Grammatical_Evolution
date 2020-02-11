# CTC-34 Grammatical Evolution

This is a programming assignment for our Automata and Formal Languages class. We used the genetic algorithm to derive the best expression that, given eight parameters measured from a concrete block, would estimete its strength.

To run the program that loads the data and finds the best expresion, create an Anaconda virtual environment with the following command:
```
conda env create -f requirements.yml
```

Then, run the program with the following command:

```
ptyhon main.py
```

We have also created a neural network, using Tensorflow and Keras, to compare its perfomance with the derived expression in finding the concrete strenght. All the definitions of the neural network and its code is available within the folder ```NeuralNetwork```. To execute the neural network, use the file ```NN-Test.ipynb``` on that folder.
