package edu.villanova.ece.inv.model;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import edu.villanova.ece.inv.manager.DataManager;

/**
 * Created by bk on 7/27/15.
 */
public class Inventory {
    int id;
    String who;
    String what;
    long when;
    int where;
    int how;

    private static DataManager dm = DataManager.sharedManager();

    public int  getId() {return id;}
    public void setId(int id) {this.id = id;}
    public Location getWhere() {return dm.getLocation(where);}
    public void     setWhere(int where) {this.where = where;}
    public User getWho() {return dm.getUser(who);}
    public void setWho(String who) {this.who = who;}
    public Asset getWhat() {return dm.getAsset(what);}
    public void  setWhat(String what) {this.what = what;}
    public Date getWhen() {return new Date(when*1000);}
    public void setWhen(long when) {this.when = when;}
    public Asset.Status getHow() {return Asset.Status.fromInt(how);}
    public void setHow(Asset.Status how) {this.how = Asset.Status.toInt(how);}

    @Override
    public String toString() {
        return getWhat().getTag_ece() +  " by " + getWho().toString() + " as " + getHow().toString();
    }
}
