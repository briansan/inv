package edu.villanova.ece.inv.adapter;

import android.content.Context;
import android.view.View;
import android.view.ViewGroup;
import android.view.LayoutInflater;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.util.ArrayList;

import edu.villanova.ece.inv.R;
import edu.villanova.ece.inv.model.Item;

/**
 * Created by bk on 7/28/15.
 */
public class ItemArrayAdapter extends ArrayAdapter<Item>
{
    private static class Cell {
        private TextView cat_label;
        private TextView man_label;
        private TextView model_label;
    }

    public ItemArrayAdapter( Context ctxt, int res, ArrayList<Item> items ) {
        super(ctxt, res, items);
    }

    public View getView(int pos, View v, ViewGroup p) {
        Cell cell;
        Item i = getItem(pos);

        if (v==null) {
            v = LayoutInflater.from(this.getContext()).inflate(R.layout.list_item_no_img, p, false);
            cell = new Cell();

            cell.man_label = (TextView)v.findViewById(R.id.top_label_1);
            cell.cat_label = (TextView)v.findViewById(R.id.bottom_label);

            v.setTag(cell);
        } else {
            cell = (Cell)v.getTag();
        }

        cell.man_label.setText(i.getManufacturer() + " " + i.getModel());
        cell.cat_label.setText(i.getCategory());

        return v;
    }

}
