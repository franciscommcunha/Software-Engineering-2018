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
import static com.github.adminfaces.starter.bean.SmokeChartView.DB_URL;
import javax.annotation.PostConstruct;
import java.io.Serializable;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.faces.bean.ManagedBean;
import org.primefaces.model.chart.Axis;
import org.primefaces.model.chart.AxisType;
import org.primefaces.model.chart.BarChartModel;
import org.primefaces.model.chart.HorizontalBarChartModel;
import org.primefaces.model.chart.ChartSeries;
 
@ManagedBean
public class EnergyChartView implements Serializable {
 
    private BarChartModel barModel;
    static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";
    static final String DB_URL = "jdbc:postgresql://postgres/domotics";
    //static final String DB_URL = "jdbc:postgresql://deti-engsoft-01.ua.pt:5555/domotics";

    static final String USER = "postgres";
    static final String PASS = "secret";
 
    @PostConstruct
    public void init() {
        try{
            createBarModels();
        }catch(ClassNotFoundException | SQLException e){}
    }
 
    public BarChartModel getBarModel() {
        return barModel;
    }
    
    private Connection getConnection() throws ClassNotFoundException{
        Connection conn = null;
        try{
            Class.forName("org.postgresql.Driver");
            conn = DriverManager.getConnection(DB_URL,USER,PASS);
            
        }catch(SQLException e){}
        
        return conn;
    }
    
    private List<Integer> findValueByAppliance(String applianceID) throws ClassNotFoundException, SQLException{
        Connection dbConnection = null;
        PreparedStatement preparedStatement = null;
        String selectSQL = "SELECT value FROM energy WHERE appliance = ?;";
        List<Integer> values = new ArrayList<>();
        ResultSet rs = null;
        try {
            dbConnection = getConnection();
            preparedStatement = dbConnection.prepareStatement(selectSQL);
            preparedStatement.setString(1, applianceID);
            preparedStatement.execute();
            rs = preparedStatement.getResultSet();
            
            while (rs.next()) {
                int value = rs.getInt(1);
                values.add(value);
            }
        } catch (SQLException e) {} 
        finally {
            if (dbConnection != null) {
                dbConnection.close();
            }
        }
        return values;
    }
 
    private BarChartModel initBarModel() throws ClassNotFoundException, SQLException {
        BarChartModel model = new BarChartModel();
        String rooms[] = {"Kitchen, Living Room, Room 1, Room 2"};
        
        String TV = "tv";
        List<Integer> allTVValues = findValueByAppliance(TV);
        String LAMPS = "luz_quarto";
        List<Integer> allLampsValues = findValueByAppliance(LAMPS);
        String HEATER = "aquecedor";
        List<Integer> allHeaterValues = findValueByAppliance(HEATER);
        String FRIDGER = "frigorifico";
        List<Integer> allFridgerValues = findValueByAppliance(FRIDGER);
        
        ChartSeries tv = new ChartSeries();
        tv.setLabel(TV);
        for(int i = 0; i< allTVValues.size(); i++){
            for (int j = i; j< rooms.length; j++){
                tv.set(rooms[j], allTVValues.get(i));
            }
        }
        
        ChartSeries lamp = new ChartSeries();
        lamp.setLabel(LAMPS);
        for(int i = 0; i< allLampsValues.size(); i++){
            for (int j = i; j< rooms.length; j++){
                lamp.set(rooms[j], allLampsValues.get(i));
            }
        }
        
        ChartSeries heater = new ChartSeries();
        heater.setLabel(HEATER);
        for(int i = 0; i< allHeaterValues.size(); i++){
            for (int j = i; j< rooms.length; j++){
                heater.set(rooms[j], allHeaterValues.get(i));
            }
        }
        
        ChartSeries fridger = new ChartSeries();
        fridger.setLabel(FRIDGER);
        for(int i = 0; i< allFridgerValues.size(); i++){
            fridger.set("Kitchen", allFridgerValues.get(i));
        }
 
        model.addSeries(tv);
        model.addSeries(lamp);
        model.addSeries(heater);
        model.addSeries(fridger);
         
        return model;
    }
     
    private void createBarModels() throws ClassNotFoundException, SQLException {
        createBarModel();
    }
     
    private void createBarModel() throws ClassNotFoundException, SQLException {
        barModel = initBarModel();
         
        barModel.setTitle("Energy Chart");
        barModel.setLegendPosition("ne");
         
        Axis xAxis = barModel.getAxis(AxisType.X);
        xAxis.setLabel("House Divisions");
         
        Axis yAxis = barModel.getAxis(AxisType.Y);
        yAxis.setLabel("Energy (W/h)");
        yAxis.setMin(0);
        yAxis.setMax(500);
        yAxis.setTickInterval("100");
    }
}
