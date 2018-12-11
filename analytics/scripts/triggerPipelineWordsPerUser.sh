cd analytics-jobs
mvn -Pdataflow-runner compile exec:java \
      -Dexec.mainClass=org.apache.beam.examples.UserRelativePerf \
      -Dexec.args="--project=gre-words-app \
      --stagingLocation=gs://gre-words/staging/ \
      --output=gs://gre-words/output/wordsPerUser/ \
      --runner=DataflowRunner"
cd ..
gsutil cp -r gs://gre-words/output/wordsPerUser ./output/
python uploadScriptWordsPerUser.py
rm -rf ./output/wordsPerUser