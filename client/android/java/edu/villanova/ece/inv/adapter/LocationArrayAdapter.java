package edu.villanova.ece.inv.adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.HashMap;

import edu.villanova.ece.inv.R;
import edu.villanova.ece.inv.model.Asset;
import edu.villanova.ece.inv.manager.DataManager;
import edu.villanova.ece.inv.model.Location;

/**
 * Created by bk on 8/4/15.
 */
public class LocationArrayAdapter extends ArrayAdapter<Location>
{
    private static class Cell {
        private TextView building_label;
        private TextView room_label;
        private TextView count_label;
    }

    public LocationArrayAdapter( Context ctxt, int res, ArrayList<Location> items ) {
        super(ctxt, res, items);
    }

    public View getView(int pos, View v, ViewGroup p) {
        Cell cell;
        Location i = getItem(pos);

        if (v==null) {
            v = LayoutInflater.from(this.getContext()).inflate(R.layout.list_item_no_img, p, false);
            cell = new Cell();

            cell.building_label = (TextView)v.findViewById(R.id.top_label_1);
            cell.count_label = (TextView)v.findViewById(R.id.bottom_label);

            v.setTag(cell);
        } else {
            cell = (Cell)v.getTag();
        }

        cell.building_label.setText(i.toString());
        HashMap<Location,ArrayList<Asset>> map = DataManager.sharedManager().getLocationAssetMap();
        cell.count_label.setText(""+map.get(i).size()+" Assets");

        return v;
    }

}
