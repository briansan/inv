package edu.villanova.ece.inv.model;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.widget.EditText;

import com.breadtech.breadinterface.BIActivity;

import java.util.Timer;
import java.util.TimerTask;

import edu.villanova.ece.inv.manager.DataManager;

/**
 * Created by bk on 7/27/15.
 */
public class Label {
    String name;
    int id;

    public Label() {
        this.id = 0;
        this.name = "null";
    }
    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    @Override
    public String toString() {
        return this.name;
    }

    public static void addLabel(final BIActivity caller, final Class type) {

        final EditText et = new EditText(caller);
        new AlertDialog.Builder(caller)
                .setTitle("Add Label")
                .setView(et)
                .setPositiveButton("Add", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        Label cat = new Label();
                        cat.setName(et.getText().toString());
                        DataManager.sharedManager().addLabel(cat, type);
                        // refresh the list a second after the click
                        (new Timer()).schedule(new TimerTask() {
                            @Override
                            public void run() {

                                caller.runOnUiThread(new Runnable() {
                                    @Override
                                    public void run() {
                                        caller.update();
                                    }
                                });
                            }
                        }, 1000);
                    }
                })
                .setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                })
                .show();
    }

    public static class ItemCategory extends Label {}
    public static class LocationBuilding extends Label {
        public LocationBuilding() {
            this.id = 0;
            this.name = "null";
        }
    }
    public static class ItemManufacturer extends Label {}

}
