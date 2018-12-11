cd analytics-jobs
mvn -Pdataflow-runner compile exec:java \
      -Dexec.mainClass=org.apache.beam.examples.WordDifficultyScore \
      -Dexec.args="--project=gre-words-app \
      --stagingLocation=gs://gre-words/staging \
      --output=gs://gre-words/output/wordScore/ \
      --runner=DataflowRunner"
cd ..
gsutil cp -r gs://gre-words/output/wordScore ./output/
python uploadScriptWordsScore.py
rm -rf ./output/wordScore