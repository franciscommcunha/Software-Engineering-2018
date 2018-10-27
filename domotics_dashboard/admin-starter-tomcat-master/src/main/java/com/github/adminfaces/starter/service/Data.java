package com.github.adminfaces.starter.service;

import com.github.adminfaces.starter.tables.Temperature;
import com.github.adminfaces.starter.tables.Humidity;
import com.github.adminfaces.starter.tables.CO2;
import com.github.adminfaces.starter.tables.Movement;
import com.github.adminfaces.starter.tables.Energy;
import java.io.Serializable;
import com.github.adminfaces.starter.tables.Event;
import java.io.IOException;
import java.io.Serializable;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;
import javax.faces.bean.SessionScoped;

/**
 *
 * @author ritasantiago
 */
@ManagedBean(name = "data", eager=true)
@SessionScoped
@RequestScoped
public class Data implements Serializable{
    private static final Logger LOGGER = Logger.getLogger( Data.class.getName() );

    static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";
    static final String DB_URL = "jdbc:postgresql://postgres/domotics";
    //static final String DB_URL = "jdbc:postgresql://deti-engsoft-01.ua.pt:5555/domotics";
    static final String USER = "postgres";
    static final String PASS = "secret";
    
    String local, room, appliance, hour;
    int value;
    
    public Connection getConnection() throws ClassNotFoundException{
        Connection conn = null;
        try{
            Class.forName("org.postgresql.Driver");
            conn = DriverManager.getConnection(DB_URL,USER,PASS);
            
        }catch(SQLException e ){}
        
        return conn;
    }
    
    public List<Temperature> getTemperatures() throws ClassNotFoundException, IOException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT * FROM temperature;";
        List<Temperature> records = new ArrayList<>();
        ArrayList<String> tmpString = new ArrayList<>();
        
        try{
            Statement stmt = con.createStatement();
            rs = stmt.executeQuery( "SELECT * FROM temperature;" );
            
            while(rs.next()){
                Temperature temp = new Temperature();
                temp.setId(rs.getInt(1));
                temp.setRoom(rs.getString(2));
                temp.setValue(rs.getInt(3));
                tmpString.add(rs.getInt(3) + "");
                temp.setHour(rs.getString(4));
                records.add(temp);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        
        Notifications.notifyTemp(tmpString);
        
        return records;
    }
    
    public double getTempAverage() throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT avg(value) FROM temperature;";
        double average = 0;
        try{
            LOGGER.log( Level.SEVERE, "Connection: " + con.toString(), con );
            pst = con.prepareStatement(stm);
            pst.execute();
            rs = pst.getResultSet();
            while(rs.next()){
                average = rs.getDouble(1);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return roundDoubles(average);//roundDoubles(SimpleConsumer.getAvgTemp());
    }
    
    public Temperature selectTempByRoom(String room) throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT value, hour FROM temperature WHERE room = ?;";
        Temperature x = new Temperature();
        try{
            pst = con.prepareStatement(stm);
            pst.setString(1, room);
            pst.execute();
            rs = pst.getResultSet();
            while(rs.next()){
                x.setValue(rs.getInt(1));
                x.setHour(rs.getString(2));
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return x;
    }
    
    
    public List<Humidity> getHumidity() throws ClassNotFoundException, IOException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT * FROM humidity;";
        List<Humidity> records = new ArrayList<>();
        ArrayList<String> tmpString = new ArrayList<>();
        
        try{
            pst = con.prepareStatement(stm);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                Humidity temp = new Humidity();
                temp.setId(rs.getInt(1));
                temp.setRoom(rs.getString(2));
                temp.setValue(rs.getInt(3));
                tmpString.add(rs.getInt(3) + "");
                temp.setHour(rs.getString(4));
                records.add(temp);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        
        Notifications.notifyHum(tmpString);
        
        return records;
    }
    
    public double getHumAverage() throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT avg(value) FROM humidity;";
        double average = 0;
        try{
            pst = con.prepareStatement(stm);
            pst.execute();
            rs = pst.getResultSet();
            while(rs.next()){
                average = rs.getDouble(1);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return roundDoubles(average);//roundDoubles(SimpleConsumer.getAvgHum());
    }
    
    public Humidity selectHumByRoom(String room) throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT value, hour FROM humidity WHERE room = ?;";
        Humidity x = new Humidity();
        
        try{
            pst = con.prepareStatement(stm);
            pst.setString(1, room);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                x.setValue(rs.getInt(1));
                x.setHour(rs.getString(2));
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return x;
    }
    
    public List<CO2> getCO2() throws ClassNotFoundException, IOException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT * FROM CO2;";
        List<CO2> records = new ArrayList<>();
        ArrayList<String> tmpString = new ArrayList<>();
        
        try{
            pst = con.prepareStatement(stm);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                CO2 temp = new CO2();
                temp.setId(rs.getInt(1));
                temp.setRoom(rs.getString(2));
                temp.setValue(rs.getInt(3));
                tmpString.add(rs.getInt(3) + "");
                temp.setHour(rs.getString(4));
                records.add(temp);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        
        Notifications.notifyCO2(tmpString);
        
        return records;
    }
    
    public double getCO2Average() throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT avg(value) FROM CO2;";
        double average = 0;
        try{
            pst = con.prepareStatement(stm);
            pst.execute();
            rs = pst.getResultSet();
            while(rs.next()){
                average = rs.getDouble(1);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return roundDoubles(average);//roundDoubles(SimpleConsumer.getAvgCO2());
    }
    
    public CO2 selectCO2ById(String room) throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT value, hour FROM co2 WHERE id = ?;";
        CO2 x = new CO2();
        try{
            pst = con.prepareStatement(stm);
            pst.setString(1, room);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                x.setValue(rs.getInt(1));
                x.setHour(rs.getString(2));
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return x;
    }
    
    public List<Energy> getEnergy() throws ClassNotFoundException, IOException{
        Connection con = getConnection();
        String stm = "SELECT * FROM energy;";
        List<Energy> records = new ArrayList<>();
        ArrayList<String> tmpString = new ArrayList<>();
        
        try{
            Statement pst = con.createStatement();
            ResultSet rs = pst.executeQuery(stm);
            
            while(rs.next()){
                Energy temp = new Energy();
                temp.setId(rs.getInt(1));
                temp.setAppliance(rs.getString(2));
                temp.setValue(rs.getInt(3));
                tmpString.add(rs.getInt(3) + "");
                temp.setHour(rs.getString(4));
                records.add(temp);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        
        Notifications.notifyEn(tmpString);
        
        return records;
    }
    
    public double getEnergyAverage() throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT avg(value) FROM energy;";
        double average = 0;
        try{
            pst = con.prepareStatement(stm);
            pst.execute();
            rs = pst.getResultSet();
            while(rs.next()){
                average = rs.getDouble(1);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return average;//SimpleConsumer.getAvgEn();
    }
    
    public List<Energy> getEnergyByAppliance(String appliance) throws ClassNotFoundException{
        Connection con = getConnection();
        ResultSet rs = null;
        PreparedStatement pst = null;
        String stm = "SELECT value, hour FROM energy WHERE appliance = ?;";
        List<Energy> energy = new ArrayList<>();
        try{
            pst = con.prepareStatement(stm);
            pst.setString(1, appliance);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                Energy x = new Energy();
                x.setValue(rs.getInt(1));
                x.setHour(rs.getString(2));
                energy.add(x);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return energy;
    }
    
    public List<Movement> getMovement() throws ClassNotFoundException, IOException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT * FROM movement;";
        List<Movement> records = new ArrayList<>();
        ArrayList<String> tmpString = new ArrayList<>();
        
        try{
            pst = con.prepareStatement(stm);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                Movement temp = new Movement();
                temp.setId(rs.getInt(1));
                temp.setLocal(rs.getString(2));
                tmpString.add(rs.getString(2));
                temp.setHour(rs.getString(3));
                records.add(temp);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        
        Notifications.notifyMov(tmpString);
        
        return records;
    }
    
    public String getMovAverage() throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT local FROM movement GROUP BY local ORDER BY "
                + "COUNT(local) DESC LIMIT 1;";
        String average = "";
        try{
            pst = con.prepareStatement(stm);
            pst.execute();
            rs = pst.getResultSet();
            while(rs.next()){
                average = rs.getString(1);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return average;
        //return SimpleConsumer.getAvgMov();
    }
    
    public List<Movement> getMovByRoom(String room) throws ClassNotFoundException{
        Connection con = getConnection();
        ResultSet rs = null;
        PreparedStatement pst = null;
        String stm = "SELECT hour FROM movement WHERE local = ?;";
        List<Movement> mov = new ArrayList<>();
        try{
            pst = con.prepareStatement(stm);
            pst.setString(1, room);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                Movement x = new Movement();
                x.setHour(rs.getString(1));
                mov.add(x);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return mov;
    }
    
    public List<Event> getEvent() throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT * FROM event;";
        List<Event> records = new ArrayList<>();
        
        try{
            pst = con.prepareStatement(stm);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                Event temp = new Event();
                temp.setId(rs.getInt(1));
                temp.setName(rs.getString(2));
                temp.setEventDate(rs.getString(3));
                temp.setLocation(rs.getString(4));
                records.add(temp);
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return records;
    }
    
    public Event getEventByName(String name) throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "SELECT eventdate, location FROM event WHERE name = ?;";
        Event event = new Event();
        
        try{
            pst = con.prepareStatement(stm);
            pst.setString(1, name);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                event.setEventDate(rs.getString(1));
                event.setLocation(rs.getString(2));
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return event;
    }
    
    public Event insertEvent(String name, Date eventdate, String location) throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "INSERT INTO event (name, eventdate, location) VALUES (?,?,?);";
        Event event = new Event();
        
        try{
            pst = con.prepareStatement(stm);
            pst.setString(1, name);
            pst.setString(2, eventdate.toString());
            pst.setString(3, location);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                event.setName(rs.getString(1));
                event.setEventDate(rs.getString(2));
                event.setLocation(rs.getString(3));
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return event;
    }
    
    public Event updateEventDate(String name, String eventdate) throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "UPDATE event SET eventdate = ? WHERE name = ?;";
        Event event = new Event();
        
        try{
            pst = con.prepareStatement(stm);
            pst.setString(1, eventdate);
            pst.setString(2, name);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                event.setName(rs.getString(1));
                event.setEventDate(rs.getString(2));
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return event;
    }
    
    public Event updateEventLocation(String name, String location) throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "UPDATE event SET location = ? WHERE name = ?;";
        Event event = new Event();
        
        try{
            pst = con.prepareStatement(stm);
            pst.setString(1, location);
            pst.setString(2, name);
            pst.execute();
            rs = pst.getResultSet();
            
            while(rs.next()){
                event.setName(rs.getString(1));
                event.setLocation(rs.getString(2));
            }
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
        return event;
    }
    
    public void deleteEvent(String name) throws ClassNotFoundException{
        ResultSet rs = null;
        PreparedStatement pst = null;
        Connection con = getConnection();
        String stm = "DELETE FROM event WHERE name = ?;";
        
        try{
            pst = con.prepareStatement(stm);
            pst.setString(1, name);
            pst.execute();
            
        }catch(SQLException e){}
        finally{
            try{
                if(con != null){
                    con.close();
                }
            }catch(SQLException se){
            }
        }
    }
    
    private double roundDoubles(double value){
        BigDecimal bd = new BigDecimal(value);
        bd = bd.setScale(2, RoundingMode.HALF_UP);
        return bd.doubleValue();
    }

    public String getLocal() {
        return local;
    }

    public void setLocal(String local) {
        this.local = local;
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }

    public String getAppliance() {
        return appliance;
    }

    public void setAppliance(String appliance) {
        this.appliance = appliance;
    }

    public String getHour() {
        return hour;
    }

    public void setHour(String hour) {
        this.hour = hour;
    }

    public int getValue() {
        return value;
    }

    public void setValue(int value) {
        this.value = value;
    }
}