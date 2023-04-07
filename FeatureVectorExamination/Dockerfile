FROM python
RUN mkdir /src
ENV OUTDATED_IGNORE=1
WORKDIR /src
COPY * .

# Need to pip install requirements
# Ensure correct python version is installed
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-m", "largest_clusters"]
