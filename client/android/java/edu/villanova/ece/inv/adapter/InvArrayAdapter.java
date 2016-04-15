package edu.villanova.ece.inv.adapter;

import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Locale;

import edu.villanova.ece.inv.R;
import edu.villanova.ece.inv.model.Asset;
import edu.villanova.ece.inv.model.Inventory;

/**
 * Created by bk on 8/4/15.
 */
public class InvArrayAdapter extends ArrayAdapter<Inventory>
{
    private static class Cell {
        private TextView desc_label;
        private TextView asset_label;
    }

    private static final SimpleDateFormat fmt = new SimpleDateFormat("MM/dd/yyyy hh:mm", Locale.US);

    public InvArrayAdapter(Context ctxt, int res, ArrayList<Inventory> items) {
        super(ctxt, res, items);
    }

    public View getView(int pos, View v, ViewGroup p) {
        Cell cell;
        Inventory i = getItem(pos);

        if (v==null) {
            v = LayoutInflater.from(this.getContext()).inflate(R.layout.list_item_no_img, p, false);
            cell = new Cell();

            cell.desc_label = (TextView)v.findViewById(R.id.top_label_1);
            cell.asset_label = (TextView)v.findViewById(R.id.bottom_label);

            v.setTag(cell);
        } else {
            cell = (Cell)v.getTag();
        }

        cell.desc_label.setText(i.toString());
        cell.asset_label.setText("on " + fmt.format(i.getWhen()) + " in " + i.getWhere().toString());

        return v;
    }

}