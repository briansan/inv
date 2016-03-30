package edu.villanova.ece.inv2.model;

/**
 * Created by bk on 7/27/15.
 */
public class Location {

    int id;
    String building;
    String room;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getBuilding() {
        return building;
    }

    public void setBuilding(String building) {
        this.building = building;
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }


    @Override
    public String toString() {
        return this.building + " " + this.room;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj.getClass() == Location.class) {
            Location l = (Location)obj;
            if (l.getId() == this.getId())
                return true;
            if (l.getBuilding() == this.getBuilding())
                if (l.getRoom() == this.getRoom())
                    return true;
        }
        return false;
    }

}
