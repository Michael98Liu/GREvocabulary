1. Download the credentials file and set the path
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
e.g. export GOOGLE_APPLICATION_CREDENTIALS="/Users/yana/Documents/classes/Senior2018/LargeScaleWeb/GREWordApp/credentials.json"
2. Download JDK and set up JAVA_HOME
export PATH=/Users/yana/Documents/classes/Senior2018/LargeScaleWeb/GREWordApp/apache-maven-3.6.0/bin:$PATH

3. Download and install http://maven.apache.org/install.html
Run on DataFlow: 
mvn -Pdataflow-runner compile exec:java \
      -Dexec.mainClass=org.apache.beam.examples.WordDifficultyScore \
      -Dexec.args="--project=gre-words-app \
      --stagingLocation=gs://gre-words/staging/ \
      --output=gs://gre-words/output \
      --runner=DataflowRunner"

mvn -Pdataflow-runner compile exec:java \
      -Dexec.mainClass=org.apache.beam.examples.UserRelativePerf \
      -Dexec.args="--project=gre-words-app \
      --stagingLocation=gs://gre-words/staging/ \
      --output=gs://gre-words/output \
      --runner=DataflowRunner"

Run locally:
mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.WordDifficultyScore -Dexec.args="--output=./output/"

mvn compile exec:java -Dexec.mainClass=org.apache.beam.examples.UserRelativePerf -Dexec.args="--output=./output/"
