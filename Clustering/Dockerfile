FROM gumtreediff/gumtree
RUN mkdir /src && mkdir /src/scratch && mkdir /src/scratch/left && mkdir /src/scratch/right
ENV CONTAINER=TRUE
WORKDIR /src
COPY * ./

# Need to pip install requirements
# Ensure correct python version is installed
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "-m", "clustering"]
