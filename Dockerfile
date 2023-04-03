FROM gumtreediff/gumtree
RUN mkdir /src && mkdir /src/scratch && mkdir /src/scratch/left && mkdir /src/scratch/right

WORKDIR /src
COPY * .

RUN 'pip install requirements.txt'

# Need to pip install requirements
# Ensure correct python version is installed

# Change syntactic similarity to reflect lack of docker

ENTRYPOINT ["python -m clustering"]