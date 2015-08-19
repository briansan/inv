package com.breadtech.breadinterface;

/**
 * Created by bk on 12/12/14.
 */
public interface ButtonLayout
{
    //
    // button icons
    public int tl_icon();
    public int tm_icon();
    public int tr_icon();
    public int bl_icon();
    public int bm_icon();
    public int br_icon();

    //
    // button labels
    public String tl_label();
    public String tm_label();
    public String tr_label();
    public String bl_label();
    public String bm_label();
    public String br_label();

    //
    // button clicked responses
    public void tl_clicked();
    public void tm_clicked();
    public void tr_clicked();
    public void bl_clicked();
    public void bm_clicked();
    public void br_clicked();
}
