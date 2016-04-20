package edu.villanova.ece.inv.model;

import android.util.Log;

import java.lang.reflect.Array;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.Locale;

import edu.villanova.ece.inv.manager.DataManager;

/**
 * Created by bk on 7/27/15.
 */
public class Asset {

    public enum Status {
        NoStatus,
        Available,
        Deployed,
        Loaned,
        Disposed;

        public static ArrayList<String> all = new ArrayList<>(Arrays.asList("NoStatus", "Available", "Deployed", "Loaned", "Disposed"));

        public static int toInt(Status x) {
            if (x==NoStatus) return 0;
            if (x==Available) return 1;
            if (x==Deployed) return 2;
            if (x==Loaned) return 3;
            if (x==Disposed) return 4;
            return -1;
        }

        public static Status fromInt(int x) {
            if (x==0) return NoStatus;
            if (x==1) return Available;
            if (x==2) return Deployed;
            if (x==3) return Loaned;
            if (x==4) return Disposed;
            return NoStatus;
        }
    }


    private static DataManager dm = DataManager.sharedManager();

    public String tag_ece, tag_vu, tag_svc, tag_unit, serial;
    public int status;
    public int item;
    public long purchased, inventoried;
    public int home, current;
    public String ip;
    public String comments;
    public float price;
    public String owner, holder;
    public boolean doinv;


    public ArrayList<Inventory> invs; // defaulted to null

    public String getTag_ece() {
        return tag_ece;
    }

    public void setTag_ece(String tag_ece) {
        this.tag_ece = tag_ece;
    }

    public String getTag_vu() {
        return tag_vu;
    }

    public void setTag_vu(String tag_vu) {
        this.tag_vu = tag_vu;
    }

    public String getTag_svc() {
        return tag_svc;
    }

    public void setTag_svc(String tag_svc) {
        this.tag_svc = tag_svc;
    }

    public String getTag_unit() {
        return tag_unit;
    }

    public void setTag_unit(String tag_unit) {
        this.tag_unit = tag_unit;
    }

    public String getSerial() {
        return serial;
    }

    public void setSerial(String serial) {
        this.serial = serial;
    }


    public Status getStatus() {return Status.fromInt(this.status);}
    public void   setStatus(Status status) {this.status = Status.toInt(status);}
    public Item getItem() {return dm.getItem(this.item);}
    public void setItem(int item) {this.item = item;}
    public Date getPurchased() {return new Date(this.purchased*1000);}
    public void setPurchased(Date purchased) {
        this.purchased = purchased.getTime()/1000;
    }

    public Date getInventoried() {
        return new Date(this.inventoried*1000);
    }

    public void setInventoried(Date inventoried) {
        this.inventoried = inventoried.getTime()/1000;
    }

    public Location getHome() { return this.home == 0 ? Location.getNullLocation() : dm.getLocation(this.home);}
    public void     setHome(int home) {this.home = home;}
    public Location getCurrent() { return this.current == 0 ? Location.getNullLocation() : dm.getLocation(current);}
    public void     setCurrent(int current) {this.current = current;}
    public String getIp() {return ip;}
    public void   setIp(String ip) {this.ip = ip;}
    public String getComments() {return comments;}
    public void   setComments(String comments) {this.comments = comments;}
    public float getPrice() {return price;}
    public void  setPrice(float price) {this.price = price;}
    public User getOwner() {return owner == null ? User.getNullUser() : dm.getUser(owner);}
    public void setOwner(String owner) {this.owner = owner;}
    public User getHolder() {return holder == null ? User.getNullUser() : dm.getUser(holder);}
    public void setHolder(String holder) {this.holder = holder;}

    @Override
    public String toString() {
        return this.tag_ece + ": " + this.getItem().getManufacturer() + " " + this.getItem().getModel();
    }

    @Override
    public boolean equals(Object obj) {
        if (obj.getClass() == Asset.class) {
            Asset a = (Asset)obj;
            return a.tag_ece == this.tag_ece;
            // check equality of ece tags
        }
        return false;
    }

}
