package com.github.adminfaces.starter.tables;

import java.io.Serializable;
import javax.faces.bean.ManagedBean;
import javax.faces.bean.RequestScoped;

/**
 *
 * @author ritasantiago
 */
@ManagedBean
@RequestScoped
public class CO2 implements Serializable, Comparable<CO2> {
    int id, value;
    String room, hour;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getValue() {
        return value;
    }

    public void setValue(int value) {
        this.value = value;
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }

    public String getHour() {
        return hour;
    }

    public void setHour(String hour) {
        this.hour = hour;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        CO2 other = (CO2) obj;
        if (id == 0) {
            if (other.id != 0)
                return false;
        } else if (equals(id)!=equals(other.id))
            return false;
        return true;
    }
    
    @Override
    public int compareTo(CO2 o) {
        return this.compareTo(o);
    }
    
}
