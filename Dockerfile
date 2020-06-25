FROM tensorflow/tensorflow:nightly

RUN apt-get install -y screen
RUN apt-get install -y git
RUN apt-get install -y zip unzip
RUN pip install jupyter -U && pip install jupyterlab
RUN pip install pandas
RUN pip install matplotlib
RUN pip install seaborn
RUN pip install mplfinance
RUN pip install sklearn
RUN pip install numpy
RUN pip install pydot
RUN pip install graphviz
RUN pip install xgboost
RUN pip install ta
RUN pip install pyts
RUN pip3 install opencv-contrib-python
RUN pip install pillow

EXPOSE 8888
ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]
