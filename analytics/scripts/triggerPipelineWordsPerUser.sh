cd analytics-jobs
mvn -Pdataflow-runner compile exec:java \
      -Dexec.mainClass=org.apache.beam.examples.UserRelativePerf \
      -Dexec.args="--project=gre-words-app \
      --stagingLocation=gs://gre-words/staging/ \
      --output=gs://gre-words/output/wordsPerUser/ \
      --runner=DataflowRunner"
cd ..
gsutil cp -r gs://gre-words/output/wordsPerUser /Users/yana/Documents/classes/Senior2018/LargeScaleWeb/GREWordApp/GREvocabulary/analytics/scripts/output/
python uploadScriptWordsPerUser.py
rm -rf /Users/yana/Documents/classes/Senior2018/LargeScaleWeb/GREWordApp/GREvocabulary/analytics/scripts/output/wordsPerUser