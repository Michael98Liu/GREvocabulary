gsutil rm -r gs://gre-words/input/*
python downloadLog.py
gsutil cp -r ./log/*.log gs://gre-words/input/
./triggerPipelineWordScore.sh	
./triggerPipelineWordsPerUser.sh
rm ./log/*