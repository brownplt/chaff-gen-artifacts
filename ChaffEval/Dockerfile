FROM python
RUN mkdir /src
ENV OUTDATED_IGNORE=1
WORKDIR /src
COPY * .
ADD DocDiff-Chaffs /src/DocDiff-Chaffs
ADD Nile-Chaffs /src/Nile-Chaffs
ADD Filesystem-Chaffs /src/Filesystem-Chaffs

# Need to pip install requirements
# Ensure correct python version is installed
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-m", "chaff_eval"]
