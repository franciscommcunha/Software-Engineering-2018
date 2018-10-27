/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.github.adminfaces.starter.bean;

/**
 *
 * @author raquelramos
 */
 
import javax.annotation.PostConstruct;
import java.io.Serializable;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;
import java.util.Set;
import javax.faces.bean.ManagedBean;
import org.primefaces.model.chart.Axis;
import org.primefaces.model.chart.AxisType;
import org.primefaces.model.chart.LineChartModel;
import org.primefaces.model.chart.LineChartSeries;
 
@ManagedBean
public class SmokeChartView implements Serializable {
 
    private LineChartModel lineModel1;
    static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";
    static final String DB_URL = "jdbc:postgresql://postgres/domotics";
    //static final String DB_URL = "jdbc:postgresql://deti-engsoft-01.ua.pt:5555/domotics";

    static final String USER = "postgres";
    static final String PASS = "secret";
     
    @PostConstruct
    public void init() {
        try{
            createLineModels();
        }catch(ClassNotFoundException | SQLException e){}
    }
 
    public LineChartModel getLineModel1() {
        return lineModel1;
    }
     
    private void createLineModels() throws ClassNotFoundException, SQLException {
        lineModel1 = initLinearModel();
        lineModel1.setTitle("CO2 Levels Chart");
        lineModel1.setLegendPosition("e");
        Axis xAxis = lineModel1.getAxis(AxisType.X);
        xAxis.setMin(0);
        xAxis.setMax(24);
        xAxis.setTickInterval("1");
        xAxis.setLabel("Hours");
        Axis yAxis = lineModel1.getAxis(AxisType.Y);
        yAxis.setMin(300);
        yAxis.setMax(900);
        yAxis.setTickInterval("150");
        yAxis.setLabel("CO2 Levels (ppm)");
    }
     
    private Connection getConnection() throws ClassNotFoundException{
        Connection conn = null;
        try{
            Class.forName("org.postgresql.Driver");
            conn = DriverManager.getConnection(DB_URL,USER,PASS);
            
        }catch(SQLException e){}
        
        return conn;
    }
    
    private Map<Integer, Integer> findValueByRoom(String roomID) throws ClassNotFoundException, SQLException {
        Connection dbConnection = null;
        PreparedStatement preparedStatement = null;
        String selectSQL = "SELECT value, hour FROM co2 WHERE room = ?;";
        Map<Integer, Integer> values = new HashMap<>();
        ResultSet rs = null;
        try {
            dbConnection = getConnection();
            preparedStatement = dbConnection.prepareStatement(selectSQL);
            preparedStatement.setString(1, roomID);
            preparedStatement.execute();
            rs = preparedStatement.getResultSet();
            
            while (rs.next()){
                int value = rs.getInt(1);
                int h = Integer.parseInt(rs.getString(2));
                values.put(value, h);
            }
        } catch (SQLException e) {} 
        finally {
            if (dbConnection != null) {
                dbConnection.close();
            }
        }
        return values;
    }
     
    private LineChartModel initLinearModel() throws ClassNotFoundException, SQLException {
        LineChartModel model = new LineChartModel();
        
        LineChartSeries series1 = new LineChartSeries();
        String kitchen = "cozinha";
        series1.setLabel(kitchen);
        Map<Integer,Integer> allKitchenValues = findValueByRoom(kitchen);
        Set keysK = allKitchenValues.keySet();
        
        for(Iterator i = keysK.iterator(); i.hasNext();){
            int key = (Integer) i.next();
            int value = allKitchenValues.get(key);
            series1.set(value, key);
        }
 
        LineChartSeries series2 = new LineChartSeries();
        String livingRoom = "sala";
        series2.setLabel(livingRoom);
        Map<Integer,Integer> allLivings = findValueByRoom(livingRoom);
        Set keysL = allLivings.keySet();
        
        for(Iterator i = keysL.iterator(); i.hasNext();){
            int key = (Integer) i.next();
            int value = allLivings.get(key);
            series2.set(value, key);
        }
        
        LineChartSeries series3 = new LineChartSeries();
        String bedRoom1 = "quarto1";
        series3.setLabel(bedRoom1);
        Map<Integer,Integer> allBed1 = findValueByRoom(bedRoom1);
        Set keysR1 = allBed1.keySet();
        
        for(Iterator i = keysR1.iterator(); i.hasNext();){
            int key = (Integer) i.next();
            int value = allBed1.get(key);
            series3.set(value, key);
        }
        
        LineChartSeries series4 = new LineChartSeries();
        String bedRoom2 = "quarto2";
        series4.setLabel(bedRoom2);
        Map<Integer,Integer> allBed2 = findValueByRoom(bedRoom2);
        Set keysR2 = allBed2.keySet();
        
        for(Iterator i = keysR2.iterator(); i.hasNext();){
            int key = (Integer) i.next();
            int value = allBed2.get(key);
            series4.set(value, key);
        }
 
        model.addSeries(series1);
        model.addSeries(series2);
        model.addSeries(series3);
        model.addSeries(series4);
         
        return model;
    }
}
