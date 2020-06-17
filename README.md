# financial-technical-analysis-using-NN
Using a Convolutional Neural Network to perform technical analysis on stock prices in order to predict the trend.

The dataset is composed of 30 days window of stock prices and technical indicators (SMA, EMA, MACD, ROC, bollinger bands, stochastic oscillators) plotted as 64x64 RGB pictures. 

The model used is a simplified XCeption model.

This project is a work in progress, so far the  accuracy on the trainning set reaches 90% but does not go higher than 50% on the validation set ... so overfitting

Futur work:
1. Work on the model:
  - Tunning of the the XCeption model
  - Investigate other well known CV models (ResNet)
  - Investiage Convolution layers taking into account the coordinate of the pixel (CoordConv): as we are dealing with time-series the location (e.g.left or right of the picture) of the pixel matters wich is not the case when trying to recognize a hot dog

2. Work on the dataset
  - Use other technical indicators
  - Change the plot type for the time serie : Reccurence Plot, Markov Transition Field, Gramian Angular Field


All feedbacks are welcome
