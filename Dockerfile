FROM ufoym/deepo:tensorflow

CMD ["bash"]

# Install Node.js 8 and npm 5
RUN apt-get update
RUN apt-get -y install curl gnupg
RUN curl -sL https://deb.nodesource.com/setup_11.x  | bash -
RUN apt-get -y install nodejs
RUN mkdir /workspace 
WORKDIR /workspace

RUN rm -rf node_modules && npm install

RUN pip3 install tensorflow ipython tensorflow_hub

RUN cd /usr/local/cuda/lib64 \
 && mv stubs/libcuda.so ./ \
 && ln -s libcuda.so libcuda.so.1 \
 && ldconfig
ENV PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
ENV LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
ENV CUDA_HOME=/usr/local/cuda

COPY package.json .
RUN npm install
RUN mkdir /workspace/images

COPY . .
EXPOSE 80
# ENTRYPOINT npm start 