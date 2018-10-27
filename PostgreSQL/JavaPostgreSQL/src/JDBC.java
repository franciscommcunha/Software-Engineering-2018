import java.sql.*;

/**
 * 
 * @author ritasantiago
 */

/**
 * Before you need to connect to database by terminal using "psql -U postgres 
 * domotics", then type postgre's password (secret).
 */

public class JDBC{
    static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";
    static final String DB_URL = "jdbc:postgresql://localhost/domotics";

    static final String USER = "postgres";
    static final String PASS = "secret";

    public static void main(String[] args){
        Connection conn = null;
        Statement stmt = null;
        ResultSet temperature = null;
        ResultSet co2 = null;
        ResultSet humidity = null;
        ResultSet energy = null;
        ResultSet movement = null;
        try{
            Class.forName("org.postgresql.Driver");
            System.out.println("Connecting to database starts");
            conn = DriverManager.getConnection(DB_URL,USER,PASS);
            System.out.println("Connected to domotics!");

            stmt = conn.createStatement();
            System.out.println("Temperature's table:");
            temperature = selectTemperature(stmt);
            System.out.println("CO2's table:");
            co2 = selectCO2(stmt);
            System.out.println("Humidity's table:");
            humidity = selectHumidity(stmt);
            System.out.println("Energy's table:");
            energy = selectEnergy(stmt);
            System.out.println("Movement's table:");
            movement = selectMovement(stmt);
            
            stmt.close();


        }catch (SQLException | ClassNotFoundException se) {		
        }finally{
            try{
                if(conn != null){
                    conn.close();
                }
            }catch(SQLException se){
            }
        }
    }

    private static ResultSet selectTemperature(Statement stmt){
        ResultSet rs = null;
        try{
            rs = stmt.executeQuery( "SELECT * FROM temperature;" );
            while ( rs.next() ) {
                String room = rs.getString("room");
                int value = rs.getInt("value");
                System.out.println( "ROOM =" +room);
                System.out.println( "VALUE = " + value );
                System.out.println();
            }
            rs.close();
        } catch(Exception e){
             System.err.println( e.getClass().getName()+": "+ e.getMessage() );
             System.exit(0);
        }


        return rs;
    }
    
    private static ResultSet selectCO2(Statement stmt){
        ResultSet rs = null;

        try{
            rs = stmt.executeQuery( "SELECT * FROM CO2;" );
            while ( rs.next() ) {
                String room = rs.getString("room");
                int value = rs.getInt("value");
                System.out.println( "ROOM =" +room);
                System.out.println( "VALUE = " + value );
                System.out.println();
            }
            rs.close();
        }catch ( Exception e ) {
             System.err.println( e.getClass().getName()+": "+ e.getMessage() );
             System.exit(0);
        }

        return rs;
    }

    private static ResultSet selectHumidity(Statement stmt){
        ResultSet rs = null;

        try{
            rs = stmt.executeQuery( "SELECT * FROM humidity;" );
            while ( rs.next() ) {
                String room = rs.getString("room");
                int value = rs.getInt("value");
                System.out.println( "ROOM =" +room);
                System.out.println( "VALUE = " + value );
                System.out.println();
            }
            rs.close();
        }catch ( Exception e ) {
             System.err.println( e.getClass().getName()+": "+ e.getMessage() );
             System.exit(0);
        }

        return rs;
    }
    
    private static ResultSet selectEnergy(Statement stmt){
        ResultSet rs = null;

        try{
            rs = stmt.executeQuery( "SELECT * FROM energy;" );
            while ( rs.next() ) {
                String appliance = rs.getString("appliance");
                int value = rs.getInt("value");
                System.out.println( "APPLIANCE = " + appliance );
                System.out.println( "VALUE = " + value );
                System.out.println();
            }
            rs.close();
        }catch ( Exception e ) {
             System.err.println( e.getClass().getName()+": "+ e.getMessage() );
             System.exit(0);
        }

        return rs;
    }

    private static ResultSet selectMovement(Statement stmt){
        ResultSet rs = null;

        try{
            rs = stmt.executeQuery( "SELECT * FROM movement;" );
            while ( rs.next() ) {
                String local = rs.getString("local");
                System.out.println( "LOCAL = " + local );
                System.out.println();
            }
            rs.close();
        }catch ( Exception e ) {
             System.err.println( e.getClass().getName()+": "+ e.getMessage() );
             System.exit(0);
        }

        return rs;
    }
}