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
import edu.villanova.ece.inv2.model.Asset;
import edu.villanova.ece.inv2.manager.DataManager;
import edu.villanova.ece.inv2.model.User;

/**
 * Created by bk on 8/4/15.
 */
public class UserArrayAdapter extends ArrayAdapter<User>
{
    private static class Cell {
        private TextView uname_label;
        private TextView fname_label;
    }

    public UserArrayAdapter(Context ctxt, int res, ArrayList<User> items) {
        super(ctxt, res, items);
    }

    public View getView(int pos, View v, ViewGroup p) {
        Cell cell;
        User i = getItem(pos);

        if (v==null) {
            v = LayoutInflater.from(this.getContext()).inflate(R.layout.list_item_no_img, p, false);
            cell = new Cell();

            cell.uname_label = (TextView)v.findViewById(R.id.top_label_1);
            cell.fname_label = (TextView)v.findViewById(R.id.bottom_label);

            v.setTag(cell);
        } else {
            cell = (Cell)v.getTag();
        }

        cell.uname_label.setText(i.toString());
        cell.fname_label.setText(i.getFname()+ " "+i.getLname());
        return v;
    }

}
