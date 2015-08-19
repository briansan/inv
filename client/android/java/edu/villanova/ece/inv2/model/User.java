package edu.villanova.ece.inv2.model;

/**
 * Created by bk on 7/27/15.
 */
public class User
{
    public enum Groups {
        NoGroup,
        Student,
        Faculty,
        Operator,
        Admin
    }

    // instance variables
    private long perm, start;
    private Groups grp;
    private String uid;
    private String fname;
    private String lname;
    private String email;
    private String phone;
    private boolean annon;

    public String getLname() {
        return lname;
    }

    public void setLname(String lname) {
        this.lname = lname;
    }

    public Groups getGrp() {
        return grp;
    }

    public void setGrp(Groups grp) {
        this.grp = grp;
    }

    public long getPerm() {
        return perm;
    }

    public void setPerm(long perm) {
        this.perm = perm;
    }

    public long getStart() {
        return start;
    }

    public void setStart(long start) {
        this.start = start;
    }

    public String getUid() {return this.uid;}

    public void setUid(String uname) {
        this.uid = uname;
    }

    public String getFname() {
        return fname;
    }

    public void setFname(String fname) {
        this.fname = fname;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPhone() {
        return phone;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public boolean isAnnon() {
        return annon;
    }

    public void setAnnon(boolean annon) {
        this.annon = annon;
    }

    @Override
    public String toString() {
        return this.uid;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj.getClass() == User.class) {
            User u = (User)obj;
            if (u.getUid().equals(this.getUid()))
                return true;
        }
        return false;
    }
}
