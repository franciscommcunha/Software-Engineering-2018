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
import org.primefaces.model.chart.LineChartModel;
import org.primefaces.model.chart.ChartSeries;
import org.primefaces.model.chart.LineChartSeries;
 
@ManagedBean
public class MovementChartView implements Serializable {
 
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
        lineModel1.setTitle("Movement Chart");
        lineModel1.setLegendPosition("e");
        Axis xAxis = lineModel1.getAxis(AxisType.X);
        xAxis.setMin(0);
        xAxis.setMax(24);
        xAxis.setTickInterval("1");
        xAxis.setLabel("Hours");
        Axis yAxis = lineModel1.getAxis(AxisType.Y);
        yAxis.setMin(-0.5);
        yAxis.setMax(1.5);
        yAxis.setTickInterval("0.5");
        yAxis.setLabel("Movement");
    }
    
    private Connection getConnection() throws ClassNotFoundException{
        Connection conn = null;
        try{
            Class.forName("org.postgresql.Driver");
            conn = DriverManager.getConnection(DB_URL,USER,PASS);
            
        }catch(SQLException e){}
        
        return conn;
    }
    
    private List<Integer> findHourByRoom(String roomID) throws ClassNotFoundException, SQLException {
        Connection dbConnection = null;
        PreparedStatement preparedStatement = null;
        String selectSQL = "SELECT hour FROM movement WHERE local = ?;";
        List<Integer> hours = new ArrayList<>();
        ResultSet rs = null;
        try {
            dbConnection = getConnection();
            preparedStatement = dbConnection.prepareStatement(selectSQL);
            preparedStatement.setString(1, roomID);
            preparedStatement.execute();
            rs = preparedStatement.getResultSet();
            
            while (rs.next()) {
                int hour = Integer.parseInt(rs.getString(1));
                hours.add(hour);
            }
        } catch (SQLException e) {} 
        finally {
            if (dbConnection != null) {
                dbConnection.close();
            }
        }
        return hours;
    }
    
    private Map<String, Integer> countByRoom(String roomID) throws ClassNotFoundException, SQLException{
        Connection dbConnection = null;
        PreparedStatement pst = null;
        String sql = "SELECT local, COUNT(local) AS count_local FROM movement "
                + "GROUP BY local HAVING COUNT(local) > 1 ORDER BY COUNT(local)"
                + "DESC;";
        Map<String, Integer> countLocal = new HashMap<>();
        ResultSet rs = null;
        try{
            dbConnection = getConnection();
            pst = dbConnection.prepareStatement(sql);
            pst.execute();
            rs = pst.getResultSet();
            while(rs.next()){
                countLocal.put(rs.getString(1), rs.getInt(2));
            }
        }catch (SQLException e) {} 
        finally {
            if (dbConnection != null) {
                dbConnection.close();
            }
        }
        return countLocal;
    }
     
    private LineChartModel initLinearModel() throws ClassNotFoundException, SQLException {
        LineChartModel model = new LineChartModel();
        
        String kitchen = "cozinha";
        List<Integer> allKitchenHours = findHourByRoom(kitchen);
        String living = "sala";
        List<Integer> allLivingHours = findHourByRoom(living);
        String room1 = "quarto1";
        List<Integer> allRoom1Hours = findHourByRoom(room1);
        String room2 = "quarto2";
        List<Integer> allRoom2Hours = findHourByRoom(room2);
        
        LineChartSeries series1 = new LineChartSeries();
        series1.setLabel(kitchen);
        for(int i = 0; i<allKitchenHours.size(); i++){
            series1.set(allKitchenHours.get(i), 1);
        }
 
        LineChartSeries series2 = new LineChartSeries();
        series2.setLabel(living);
        for(int i = 0; i<allLivingHours.size(); i++){
            series2.set(allLivingHours.get(i), 1);
        }
        
        LineChartSeries series3 = new LineChartSeries();
        series3.setLabel(room1);
        for(int i = 0; i<allRoom1Hours.size(); i++){
            series3.set(allRoom1Hours.get(i), 1);
        }
       
        LineChartSeries series4 = new LineChartSeries();
        series4.setLabel(room2);
        for(int i = 0; i<allRoom2Hours.size(); i++){
            series4.set(allRoom2Hours.get(i), 1);
        }
        
        model.addSeries(series1);
        model.addSeries(series2);
        model.addSeries(series3);
        model.addSeries(series4);
         
        return model;
    }
    
}
