# Traffic.py

This project is aimed to train the AI-agent with a neural network to recognize road signs. I was given two datasets which is called 'gtsrb' and a smaller one 'gtsrb-small'. During the development process, the code was tested on the smaller one. Then, tested on the larger set. 

First off, I loaded the data from the dataset as independent from the os. Then used the loaded data on the network. Here is where the things get experimental:

At the first attemp, there were only one single convolutional and pooling layers. And the result was innaccurate because the agent couldn't recognize the variations due to the being of more sensitive to the variations.
At the second try, I added two more convolutional and pooling layers to train data as being less sensitive to the different versions of the same datapoint. Obviously, the result was more satisfying and accurate.

The main problem is the train the AI agent in a reasonable way to recognize the changes during the process of the same data. 