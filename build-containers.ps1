cd Clustering
docker build . -t sidprasad/wfe-clustering:latest
docker push sidprasad/wfe-clustering:latest

cd ../ChaffEval
docker build . -t sidprasad/chaff-eval:latest
docker push sidprasad/chaff-eval:latest

cd ../FeatureVectorExamination
docker build . -t sidprasad/fv-eval:latest
docker push . -t sidprasad/fv-eval:latest

cd ..
