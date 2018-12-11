package org.apache.beam.examples;

import com.sun.javafx.image.impl.IntArgb;
import org.apache.beam.examples.common.ExampleUtils;
import org.apache.beam.sdk.Pipeline;
import org.apache.beam.sdk.io.TextIO;
import org.apache.beam.sdk.metrics.Counter;
import org.apache.beam.sdk.metrics.Distribution;
import org.apache.beam.sdk.metrics.Metrics;
import org.apache.beam.sdk.options.Default;
import org.apache.beam.sdk.options.Description;
import org.apache.beam.sdk.options.PipelineOptions;
import org.apache.beam.sdk.options.PipelineOptionsFactory;
import org.apache.beam.sdk.options.Validation.Required;
import org.apache.beam.sdk.transforms.Count;
import org.apache.beam.sdk.transforms.DoFn;
import org.apache.beam.sdk.transforms.MapElements;
import org.apache.beam.sdk.transforms.PTransform;
import org.apache.beam.sdk.transforms.ParDo;
import org.apache.beam.sdk.transforms.GroupByKey;
import org.apache.beam.sdk.transforms.SimpleFunction;
import org.apache.beam.sdk.values.KV;
import org.apache.beam.sdk.values.PCollection;

import java.util.HashSet;
import java.time.Instant;

public class UserRelativePerf {
  public static final long dayinMillis = 86400L;

  /**
   * Concept #2: You can make your pipeline assembly code less verbose by defining your DoFns
   * statically out-of-line. This DoFn tokenizes lines of text into individual words; we pass it to
   * a ParDo in the pipeline.
   */
  static class ExtractWordsFn extends DoFn<String, KV<String, String>> {
    private final Counter emptyLines = Metrics.counter(ExtractWordsFn.class, "emptyLines");
    private final Distribution lineLenDist =
            Metrics.distribution(ExtractWordsFn.class, "lineLenDistro");

    @ProcessElement
    public void processElement(@Element String element, OutputReceiver<KV<String, String>> receiver) {
      lineLenDist.update(element.length());
      if (element.trim().isEmpty()) {
        emptyLines.inc();
      }

      // Split the line into words.
      String[] words = element.split(" ");

      Character verdict = words[2].charAt(0);
      long timestamp = Long.parseLong(words[3]);
      long now = Instant.now().toEpochMilli()/1000L;
      if(verdict == 'c' && (now - timestamp < dayinMillis)) {
        receiver.output(KV.of(words[0], words[1]));
      }
    }
  }


  static class MakeScoresFn extends DoFn<KV<String, Iterable<String>>, KV<String, Integer>> {

    @ProcessElement
    public void processElement(@Element KV<String, Iterable<String>> element, OutputReceiver<KV<String, Integer>> receiver) {

      String key = element.getKey();
      Iterable<String> values = element.getValue();

      HashSet<String> distinctWords = new HashSet<>();
      for(String word : values) {
        distinctWords.add(word);
      }

      receiver.output(KV.of(key, distinctWords.size()));
    }
  }

  /** A SimpleFunction that converts a Word and Count into a printable string. */
  public static class FormatAsTextFn extends SimpleFunction<KV<String, Integer>, String> {
    @Override
    public String apply(KV<String, Integer> input) {
      return input.getKey() + " " + input.getValue();
    }
  }

  /**
   * A PTransform that converts a PCollection containing lines of text into a PCollection of
   * formatted word counts.
   *
   * <p>Concept #3: This is a custom composite transform that bundles two transforms (ParDo and
   * Count) as a reusable PTransform subclass. Using composite transforms allows for easy reuse,
   * modular testing, and an improved monitoring experience.
   */
  public static class CountWords
          extends PTransform<PCollection<String>, PCollection<KV<String, Integer>>> {
    @Override
    public PCollection<KV<String, Integer>> expand(PCollection<String> lines) {

      // Convert lines of text into individual words.
      PCollection<KV<String, String>> words = lines.apply(ParDo.of(new ExtractWordsFn()));


      // Count the number of times each word occurs.
      PCollection<KV<String, Iterable<String>>> wordResults = words.apply(GroupByKey.create());
      PCollection<KV<String, Integer>> wordScores = wordResults.apply(ParDo.of(new MakeScoresFn()));

      return wordScores;
    }
  }

  /**
   * Options supported by {@link UserRelativePerf}.
   *
   * <p>Concept #4: Defining your own configuration options. Here, you can add your own arguments to
   * be processed by the command-line parser, and specify default values for them. You can then
   * access the options values in your pipeline code.
   *
   * <p>Inherits standard configuration options.
   */
  public interface WordCountOptions extends PipelineOptions {

    /**
     * By default, this example reads from a public dataset containing the text of King Lear. Set
     * this option to choose a different input file or glob.
     */
    @Description("Path of the file to read from")
    @Default.String("gs://gre-words/input/*")
    String getInputFile();

    void setInputFile(String value);

    /** Set this required option to specify where to write the output. */
    @Description("Path of the file to write to")
    @Required
    String getOutput();

    void setOutput(String value);
  }

  static void runWordCount(WordCountOptions options) {
    Pipeline p = Pipeline.create(options);

    // Concepts #2 and #3: Our pipeline applies the composite CountWords transform, and passes the
    // static FormatAsTextFn() to the ParDo transform.
    p.apply("ReadLines", TextIO.read().from(options.getInputFile()))
            .apply(new CountWords())
            .apply(MapElements.via(new FormatAsTextFn()))
            .apply("WriteCounts", TextIO.write().to(options.getOutput()));

    p.run().waitUntilFinish();
  }

  public static void main(String[] args) {
    WordCountOptions options =
            PipelineOptionsFactory.fromArgs(args).withValidation().as(WordCountOptions.class);

    runWordCount(options);
  }
}
