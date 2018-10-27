package com.github.adminfaces.starter.service;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.Properties;
import java.util.regex.Pattern;
import com.github.adminfaces.starter.infra.security.*;
import java.io.IOException;
import org.apache.kafka.common.serialization.Serdes;
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsConfig;
import org.apache.kafka.streams.kstream.KStream;
import org.apache.kafka.streams.kstream.KStreamBuilder;

public class Notifications{
    static ArrayList<String> temp = new ArrayList<>();
    static ArrayList<String> co2 = new ArrayList<>();
    static ArrayList<String> hum = new ArrayList<>();
    static ArrayList<String> mov = new ArrayList<>();
    static ArrayList<String> en = new ArrayList<>();
    
    private static int nTmp;
    private static final int MAX_TMP = 25;
    private static final int MIN_TMP = 10;
    private static int nCO2;
    private static final int MAX_CO2 = 900;
    private static final int MIN_CO2 = 300;
    private static int nHum;
    private static final int MAX_HUM = 90;
    private static final int MIN_HUM = 10;
    private static String nMov;
    private static int nEn;
    private static final int MAX_EN = 2200;
    
    public static void main(String[] args) throws IOException{
        Properties props = new Properties();
        props.put(StreamsConfig.APPLICATION_ID_CONFIG, "notificationConsumer");
        props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "kafka:9092");
        //props.put(StreamsConfig.BOOTSTRAP_SERVERS_CONFIG, "deti-engsoft-01.ua.pt:9092");
        props.put(StreamsConfig.DEFAULT_KEY_SERDE_CLASS_CONFIG, Serdes.String().getClass());
        props.put(StreamsConfig.DEFAULT_VALUE_SERDE_CLASS_CONFIG, Serdes.String().getClass());

        KStreamBuilder builder = new KStreamBuilder();
        KStream<String, String> textLines = builder.stream("SensorsNotifications");
        textLines.foreach((String key, String value) -> {
            switch (key) {
                case "temperature":
                    temp.add(value.split(Pattern.quote("|"))[1]);
                    try{nTmp = notifyTemp(temp);}catch(IOException e){}
                    break;
                    
                case "co2":
                    co2.add(value.split(Pattern.quote("|"))[1]);
                    try{nCO2 = notifyCO2(co2);}catch(IOException e){}
                    break;
                    
                case "humidity":
                    hum.add(value.split(Pattern.quote("|"))[1]);
                    try{nHum = notifyHum(hum);}catch(IOException e){}
                    break;
                    
                case "movement":
                    mov.add(value.split(Pattern.quote("|"))[1]);
                    try{nMov = notifyMov(mov);}catch(IOException e){}
                    break;
                    
                case "energy":
                    en.add(value.split(Pattern.quote("|"))[1]);
                    try{nEn = notifyEn(en);}catch(IOException e){}
                    break;
                    
                default:
                    break;
            }
        });
        
        KafkaStreams streams = new KafkaStreams(builder, props);
        streams.start();

        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }
    
    public static int notifyTemp(ArrayList<String> list) throws IOException{
        Iterator<String> itr = list.iterator();
        
        int val = 0;
        while(itr.hasNext()){
            val += Integer.parseInt(itr.next());
            if(val > MAX_TMP-1) TemperatureNotification.temperatureHigh();
            else if(val < MIN_TMP+1) TemperatureNotification.temperatureLow();
        }
        return val;
    }
    
    public static int notifyHum(ArrayList<String> list) throws IOException{
        Iterator<String> itr = list.iterator();
        
        int val = 0;
        while(itr.hasNext()){
            val += Integer.parseInt(itr.next());
            if(val > MAX_HUM-1) HumidityNotification.humidityHigh();
            else if(val < MIN_HUM+1) HumidityNotification.humidityLow();
        }
        return val;
    }
    
    public static int notifyCO2(ArrayList<String> list) throws IOException{
        Iterator<String> itr = list.iterator();
        
        int val = 0;
        while(itr.hasNext()){
            val += Integer.parseInt(itr.next());
            if(val > MAX_CO2-10) CO2Notification.co2High();
            else if(val < MIN_CO2+10) CO2Notification.co2Low();
        }
        return val;
    }
    
    public static String notifyMov(ArrayList<String> list) throws IOException{
        Iterator<String> itr = list.iterator();
        
        String val = "";
        while(itr.hasNext()){
            val += itr.next();
            if(!val.equals(null)) MovementNotification.movementDetected();
        }
        return val;
    }
    
    public static int notifyEn(ArrayList<String> list) throws IOException{
        Iterator<String> itr = list.iterator();
        
        int val = 0;
        while(itr.hasNext()){
            val += Integer.parseInt(itr.next());
            if(val > MAX_EN-10) EnergyNotification.energyHigh();
        }
        return val;
    }
}


