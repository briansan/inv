package edu.villanova.ece.inv.activity;

import android.app.Fragment;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.content.Intent;

import com.breadtech.breadinterface.BIActivity;

import java.util.Stack;

import edu.villanova.ece.inv.R;
import edu.villanova.ece.inv.fragment.AssetListFragment;
import edu.villanova.ece.inv.fragment.BuildingListFragment;
import edu.villanova.ece.inv.fragment.CategoryListFragment;
import edu.villanova.ece.inv.fragment.InvListFragment;
import edu.villanova.ece.inv.fragment.ItemListFragment;
import edu.villanova.ece.inv.fragment.ManufacturerListFragment;
import edu.villanova.ece.inv.manager.AuthManager;
import edu.villanova.ece.inv.model.Asset;
import edu.villanova.ece.inv.manager.DataManager;
import edu.villanova.ece.inv.model.Inventory;
import edu.villanova.ece.inv.model.Item;
import edu.villanova.ece.inv.model.Label;
import edu.villanova.ece.inv.model.Location;
import edu.villanova.ece.inv.model.User;

/**
 * Created by bk on 8/5/15.
 */
public class ListActivity extends BIActivity implements ItemListFragment.Delegate, AssetListFragment.Delegate,
        InvListFragment.Delegate, CategoryListFragment.Delegate, ManufacturerListFragment.Delegate,
        BuildingListFragment.Delegate
{
    //
    // constants
    public static final String TAG = "ListActivity";

    //
    // mode enum definition
    public static class Mode {
        public static final int ItemByCategory = 0;
        public static final int AssetByLocation = 1;
        public static final int AssetByItem = 2;
        public static final int AssetByUser = 3;
        public static final int InvByAsset = 4;
        public static final int InvByUser  = 5;
        public static final int ItemCategory     = 6;
        public static final int ItemManufacturer = 7;
        public static final int LocationBuilding = 8;
    }

    //
    // instance variables
    private int mode;
    private Object ref;
    private Stack<Integer> modeHistory;
    private Stack<Object> refHistory;

    //
    // ui
    @Override
    public int tl_icon() {
        return R.drawable.ic_keyboard_backspace_white_36dp;
    }

    @Override
    public void tl_clicked() {
        //
        // check the history
        if (this.modeHistory.empty())
            this.finish();
        else {
            //
            // if it's not empty, pop the values and update
            this.mode = this.modeHistory.pop();
            this.ref = this.refHistory.pop();
            this.update();
        }
    }

    @Override
    public String bm_label() {
        return this.ref != null ? this.ref.toString() : "";
    }

    @Override
    public String tm_label() {
        String y = "";
        switch (this.mode) {
            case Mode.ItemByCategory:
                y = "Items by Category";
                break;
            case Mode.AssetByLocation:
                y = "Assets by Location";
                break;
            case Mode.AssetByItem:
                y = "Assets by Item";
                break;
            case Mode.AssetByUser:
                y = "Assets by User";
                break;
            case Mode.InvByAsset:
                y = "Inventory Log of Asset";
                break;
            case Mode.InvByUser:
                y = "Inventory Log by User";
                break;
            case Mode.ItemCategory:
                y = "Item Categories";
                break;
            case Mode.ItemManufacturer:
                y = "Item Manufacturers";
                break;
            case Mode.LocationBuilding:
                y = "Location Buildings";
                break;
        }
        return y;
    }

    @Override
    public int br_icon() {
        return (this.mode == Mode.ItemCategory || this.mode == Mode.ItemManufacturer ||
                this.mode == Mode.LocationBuilding) && AuthManager.checkAuth(AuthManager.LabelModify)
                ? R.drawable.ic_add_white_36dp: 0 ;
    }

    @Override
    public void br_clicked() {
        if (AuthManager.checkAuth(AuthManager.LabelModify)) {
            if (this.mode == Mode.ItemCategory) {
                Label.addLabel(this, Label.ItemCategory.class);
            } else if (this.mode == Mode.ItemManufacturer) {
                Label.addLabel(this, Label.ItemManufacturer.class);
            } else if (this.mode == Mode.LocationBuilding) {
                Label.addLabel(this, Label.LocationBuilding.class);
            }
        }
    }

    @Override
    public void init() {
        super.init();

        // initialize the navigation stacks
        modeHistory = new Stack<Integer>();
        refHistory = new Stack<Object>();

        Intent i = getIntent();
        this.mode = i.getIntExtra("Mode",1);
    }


    @Override
    public void update() {
        FragmentManager fm = getFragmentManager();
        FragmentTransaction ft = fm.beginTransaction();
        Fragment frag = null;

        Intent i = getIntent();
        switch( this.mode ) {
            case Mode.ItemByCategory:
                String cat = i.getStringExtra("Category");
                this.ref = cat;
                frag = ItemListFragment.newInstance(cat);
                break;
            case Mode.AssetByLocation:
                int loc_id = i.getIntExtra("Location", 1);
                Location loc = DataManager.sharedManager().getLocationMap().get(loc_id);
                this.ref = loc;
                frag = AssetListFragment.newInstance(loc);
                break;
            case Mode.AssetByItem:
                int item_id = i.getIntExtra("Item", 1);
                Item item = DataManager.sharedManager().getItemMap().get(item_id);
                this.ref = item;
                frag = AssetListFragment.newInstance(item);
                break;
            case Mode.AssetByUser:
                String uid = i.getStringExtra("User");
                User user = DataManager.sharedManager().getUser(uid);
                this.ref = user;
                frag = AssetListFragment.newInstance(user);
                break;
            case Mode.InvByAsset:
                String tag = i.getStringExtra("Asset");
                Asset asset = DataManager.sharedManager().getAsset(tag);
                this.ref = asset;
                frag = InvListFragment.newInstance(asset);
                break;
            case Mode.InvByUser:
                String uid2 = i.getStringExtra("User");
                User u = DataManager.sharedManager().getUser(uid2);
                this.ref = u;
                frag = InvListFragment.newInstance(u);
                break;

            case Mode.ItemCategory:
                frag = CategoryListFragment.newInstance();
                break;
            case Mode.ItemManufacturer:
                frag = ManufacturerListFragment.newInstance();
                break;
            case Mode.LocationBuilding:
                frag = BuildingListFragment.newInstance();
                break;
        }
        ft.replace(R.id.fragment, frag);
        ft.commit();

        super.update();
    }

    @Override
    public void didSelectItem(Item item) {
        //
        // store history
        modeHistory.push(this.mode);
        refHistory.push(this.ref);

        //
        // display item info
        Intent i = new Intent(this,ItemInfoActivity.class);
        i.putExtra("Item", item.getId());
        startActivity(i);

        /*
        this.mode = Mode.AssetByItem;
        this.update();
        */
    }

    @Override
    public void didSelectAsset(Asset asset) {
        //
        // store history
        modeHistory.push(this.mode);
        refHistory.push(this.ref);

        //
        //
        Intent i = getIntent();
        i.putExtra("Asset", asset.tag_ece);
        this.mode = Mode.InvByAsset;
        this.update();
    }

    @Override
    public void didSelectInv(Inventory inv) {
        Intent i = new Intent(this, InvInfoActivity.class);
        i.putExtra("Inv",inv.getId());
        this.startActivity(i);
    }

    @Override
    public void didSelectItemCategory(String name) {

    }

    @Override
    public void didSelectItemManufacturer(String name) {

    }

    @Override
    public void didSelectLocationBuilding(String name) {

    }
}
