# Should be python3.6. Some of the ispaq code uses depricated stuff that doesn't work in 3.9
FROM python

RUN apt update
RUN apt install -y python3-pip
RUN apt install -y r-base
RUN apt install cython

RUN pip3 install numpy==1.19.5
RUN pip3 install pandas
RUN pip3 install obspy==1.2.2
RUN pip3 install rpy2==3.1.0

RUN mkdir ispaq
RUN git clone https://github.com/iris-edu/ispaq.git
RUN cd ispaq
RUN pip3 install .
RUN ispaq -I

ENTRYPOINT ispaq