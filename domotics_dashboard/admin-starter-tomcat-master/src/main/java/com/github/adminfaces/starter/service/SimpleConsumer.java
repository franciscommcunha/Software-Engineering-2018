// https://kafka.apache.org/11/documentation/streams/developer-guide/dsl-api.html

package com.github.adminfaces.starter.service;

import java.util.ArrayList;
import java.util.Iterator;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KStreamBuilder;
import java.util.Properties;
import java.util.regex.Pattern;

public class SimpleConsumer {
    
    static ArrayList<String> temp = new ArrayList<>();
    static ArrayList<String> co2 = new ArrayList<>();
    static ArrayList<String> hum = new ArrayList<>();
    static ArrayList<String> mov = new ArrayList<>();
    static ArrayList<String> en = new ArrayList<>();
    
    private static double avgTemp;
    private static double avgCO2;
    private static double avgHum;
    private static double avgMov;
    private static double avgEn;
    
    private static String LastTemp;
    private static String LastCO2;
    private static String LastHum;
    private static String LastMov;
    private static String LastEn;
    
    public static void main(final String[] args) throws Exception {
        
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "avgConsumer"); // id of config, can be anything
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092"); // servers
        //props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "deti-engsoft-01.ua.pt:9092"); // servers
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        KStreamBuilder builder = new KStreamBuilder();
        KStream<String, String> textLines = builder.stream("SensorsValues"); // topic name
        
        textLines.foreach((String key, String value) -> {
            switch (key) {
                case "temperature":
                    temp.add(value.split(Pattern.quote("|"))[1]); 
                    LastTemp = getLastTemp(); // get the last received value
                    System.out.println("Last Temperature: " + LastTemp);
                    avgTemp = average(temp);
                    System.out.println("Average temp: "+ getAvgTemp() );
                    break;
                    
                case "co2":
                    co2.add(value.split(Pattern.quote("|"))[1]);
                    LastCO2 = getLastCO2();
                    System.out.println("Last CO2: " + LastCO2);
                    avgCO2 = average(co2);
                    System.out.println("Average CO2: "+ getAvgCO2() );
                    break;
                    
                case "humidity":
                    hum.add(value.split(Pattern.quote("|"))[1]);
                    LastHum = getLastHum();
                    System.out.println("Last HUM: " + LastHum);
                    avgHum = average(hum);
                    System.out.println("Average HUM: "+ getAvgHum() );
                    break;
                    
                case "movement":
                    mov.add(value.split(Pattern.quote("|"))[1]);
                    LastMov = getLastMov();
                    System.out.println("Last MOV: " + LastMov);
                    avgMov = average(mov);
                    System.out.println("Average Mov: "+ getAvgMov() );
                    break;
                    
                case "energy":
                    en.add(value.split(Pattern.quote("|"))[1]);
                    LastEn = getLastEn();
                    System.out.println("Last EN: " + LastEn);
                    avgEn = average(en);
                    System.out.println("Average EN: "+ getAvgEn() );
                    break;
                    
                default:
                    break;
            }
        });
        
        KafkaStreams streams = new KafkaStreams(builder, props);
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
    
    private static double average(ArrayList<String> list) {
        Iterator<String> itr = list.iterator();
        
        double val = 0;
        while (itr.hasNext()) {
            val += Double.parseDouble(itr.next());
        }
        return (val / list.size() );
    }
    
    public static String getLastTemp() {  return temp.get(temp.size() - 1); }
    
    public static String getLastCO2() {  return co2.get(co2.size() - 1); }
    
    public static String getLastHum() {  return hum.get(hum.size() - 1); }
    
    public static String getLastMov() {  return mov.get(mov.size() - 1); }
    
    public static String getLastEn() {  return en.get(en.size() - 1); }
    
    public static double getAvgTemp() { return avgTemp; }
    
    public static double getAvgCO2() { return avgCO2; }
    
    public static double getAvgHum() { return avgHum; }
    
    public static double getAvgMov() { return avgMov; }
    
    public static double getAvgEn() { return avgEn; }
}