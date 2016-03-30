package edu.villanova.ece.inv2.adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.HashMap;

import edu.villanova.ece.inv2.R;
import edu.villanova.ece.inv2.manager.DataManager;
import edu.villanova.ece.inv2.model.Item;
import edu.villanova.ece.inv2.model.Label;
import edu.villanova.ece.inv2.model.Location;

/**
 * Created by bk on 8/4/15.
 */
public class BuildingArrayAdapter extends ArrayAdapter<Label.LocationBuilding> {

    private static class Cell {
        private TextView label;
        private TextView count;
    }

    public BuildingArrayAdapter(Context ctxt, int res, ArrayList<Label.LocationBuilding> categories) {
        super(ctxt, res, categories);
    }

    public View getView(int pos, View v, ViewGroup p) {
        Cell cell;
        Label.LocationBuilding i = getItem(pos);

        if (v==null) {
            v = LayoutInflater.from(this.getContext()).inflate(R.layout.list_item_no_img, p, false);
            cell = new Cell();
            cell.label = (TextView)v.findViewById(R.id.top_label_1);
            cell.count = (TextView)v.findViewById(R.id.bottom_label);
            v.setTag(cell);
        } else {
            cell = (Cell)v.getTag();
        }

        cell.label.setText(i.getName());
        HashMap<String,ArrayList<Location>> map = DataManager.sharedManager().getBuildingLocationMap();
        String count = ""+map.get(i.getName()).size()+ " Locations";
        cell.count.setText(count);

        return v;
    }

}
