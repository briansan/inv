package com.breadtech.breadinterface;

import android.app.Activity;
import android.app.Fragment;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;

import edu.villanova.ece.inv2.R;

public class BIActivity extends FragmentActivity implements ButtonLayout, Lifecycle {

    //
    // instance variables
    //
    protected Button tl, tm, tr, bl, bm, br;

    //
    // breadinterface button layout
    //

    @Override
    public int tl_icon() { return 0; }
    @Override
    public int tm_icon() { return 0; }
    @Override
    public int tr_icon() { return 0; }
    @Override
    public int bl_icon() { return 0; }
    @Override
    public int bm_icon() { return 0; }
    @Override
    public int br_icon() { return 0; }

    //
    // button labels
    @Override
    public String tl_label() { return ""; }
    @Override
    public String tm_label() { return ""; }
    @Override
    public String tr_label() { return ""; }
    @Override
    public String bl_label() { return ""; }
    @Override
    public String bm_label() { return ""; }
    @Override
    public String br_label() { return ""; }

    //
    // button clicked responses

    @Override
    public void tl_clicked() {}
    @Override
    public void tm_clicked() {}
    @Override
    public void tr_clicked() {}
    @Override
    public void bl_clicked() {}
    @Override
    public void bm_clicked() {}
    @Override
    public void br_clicked() {}

    //
    // the inner button onclick listener class definition
    //
    private class TopLeftButtonOnClickListener implements View.OnClickListener {
        @Override
        public void onClick( View v ) {
            tl_clicked();
        }
    }
    private class TopMiddleButtonOnClickListener implements View.OnClickListener {
        @Override
        public void onClick( View v ) {
            tm_clicked();
        }
    }
    private class TopRightButtonOnClickListener implements View.OnClickListener {
        @Override
        public void onClick( View v ) {
            tr_clicked();
        }
    }
    private class BottomLeftButtonOnClickListener implements View.OnClickListener {
        @Override
        public void onClick( View v ) {
            bl_clicked();
        }
    }
    private class BottomMiddleButtonOnClickListener implements View.OnClickListener {
        @Override
        public void onClick( View v ) {
            bm_clicked();
        }
    }
    private class BottomRightButtonOnClickListener implements View.OnClickListener {
        @Override
        public void onClick( View v ) {
            br_clicked();
        }
    }

    //
    // breadinterface lifecycle
    //
    @Override
    public void init()
    {
    }
    @Override
    public void start() {
        // set the handles
        this.tl = (Button)this.findViewById(R.id.tl);
        this.tm = (Button)this.findViewById(R.id.tm);
        this.tr = (Button)this.findViewById(R.id.tr);
        this.bl = (Button)this.findViewById(R.id.bl);
        this.bm = (Button)this.findViewById(R.id.bm);
        this.br = (Button)this.findViewById(R.id.br);

        // set the button clicks
        if (this.tl != null) this.tl.setOnClickListener( new TopLeftButtonOnClickListener());
        if (this.tm != null) this.tm.setOnClickListener( new TopMiddleButtonOnClickListener());
        if (this.tr != null) this.tr.setOnClickListener( new TopRightButtonOnClickListener());
        if (this.bl != null) this.bl.setOnClickListener( new BottomLeftButtonOnClickListener());
        if (this.bm != null) this.bm.setOnClickListener( new BottomMiddleButtonOnClickListener());
        if (this.br != null) this.br.setOnClickListener( new BottomRightButtonOnClickListener());
    }

    @Override
    public void resume() { this.update(); }

    @Override
    public void update()
    {
        // setting the button content here
        if (this.tl != null) this.tl.setText( this.tl_label() );
        if (this.tm != null) this.tm.setText( this.tm_label() );
        if (this.tr != null) this.tr.setText( this.tr_label() );
        if (this.bl != null) this.bl.setText( this.bl_label() );
        if (this.bm != null) this.bm.setText( this.bm_label() );
        if (this.br != null) this.br.setText( this.br_label() );

        // try to set the icons
        this.tl.setBackgroundResource(this.tl_icon());
        this.tm.setBackgroundResource(this.tm_icon());
        this.tr.setBackgroundResource(this.tr_icon());
        this.bl.setBackgroundResource(this.bl_icon());
        this.bm.setBackgroundResource(this.bm_icon());
        this.br.setBackgroundResource(this.br_icon());
    }

    @Override
    public void clear() {}
    @Override
    public void pause() {}
    @Override
    public void stop() {}

    @Override
    public void cleanup()
    {
        this.tl = this.tm = this.tr = this.bl = this.bm = this.br = null;
    }

    //
    // activity lifecycle (implemented to inject BI lifecycle methods)
    //

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_bi);

        this.init();
    }

    @Override
    protected void onStart() {
        super.onStart();
        this.start();
    }

    @Override
    protected void onResume() {
        super.onResume();
        this.resume();
    }

    @Override
    protected void onPause() {
        super.onPause();
        this.pause();
    }

    @Override
    protected void onStop() {
        super.onStop();
        this.stop();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        this.cleanup();
    }


}
