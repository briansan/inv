package edu.villanova.ece.inv.adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.ArrayList;

import edu.villanova.ece.inv.R;
import edu.villanova.ece.inv.model.Asset;
import edu.villanova.ece.inv.model.Item;

/**
 * Created by bk on 8/4/15.
 */
public class AssetArrayAdapter extends ArrayAdapter<Asset>
{
    private static class Cell {
        private TextView tag_label;
        private TextView item_label;
        private TextView location_label;
    }

    public AssetArrayAdapter( Context ctxt, int res, ArrayList<Asset> items ) {
        super(ctxt, res, items);
    }

    public View getView(int pos, View v, ViewGroup p) {
        Cell cell;
        Asset i = getItem(pos);

        if (v==null) {
            v = LayoutInflater.from(this.getContext()).inflate(R.layout.list_item_no_img, p, false);
            cell = new Cell();

            cell.tag_label = (TextView)v.findViewById(R.id.top_label_1);
            cell.location_label = (TextView)v.findViewById(R.id.bottom_label);

            v.setTag(cell);
        } else {
            cell = (Cell)v.getTag();
        }

        cell.tag_label.setText(i.toString());
        cell.location_label.setText(i.getStatus().toString());

        return v;
    }

}