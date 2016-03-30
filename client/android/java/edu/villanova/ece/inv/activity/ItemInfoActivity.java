package edu.villanova.ece.inv2.activity;

import android.app.AlertDialog;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.content.DialogInterface;
import android.content.Intent;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ViewSwitcher;

import com.breadtech.breadinterface.BIActivity;

import edu.villanova.ece.inv2.R;
import edu.villanova.ece.inv2.fragment.AssetListFragment;
import edu.villanova.ece.inv2.manager.AuthManager;
import edu.villanova.ece.inv2.model.Asset;
import edu.villanova.ece.inv2.manager.DataManager;
import edu.villanova.ece.inv2.model.Item;
import edu.villanova.ece.inv2.model.Label;

/**
 * Created by bk on 8/6/15.
 */
public class ItemInfoActivity extends BIActivity implements DataManager.ModificationDelegate,
        AdapterView.OnItemSelectedListener, AssetListFragment.Delegate {

    //
    // constants
    private static final String TAG = "ItemInfoActivity";
    private static final String DEFAULT_BUTTON_TEXT = "Select from list";

    //
    // state
    private boolean editing;
    private boolean showingAssets;
    //
    // ui
    private ViewSwitcher cat_switcher;
    private ViewSwitcher man_switcher;
    private ViewSwitcher model_switcher;

    private TextView cat_tv;
    private TextView man_tv;
    private TextView model_tv;

    private Spinner man_spinner;
    private Spinner cat_spinner;
    private EditText model_et;

    private AssetListFragment frag;

    //
    // model
    Item item;

    //
    // interface
    @Override
    public int tl_icon() {
        return this.editing ? R.drawable.ic_close_white_36dp : R.drawable.ic_keyboard_backspace_white_36dp;
    }

    @Override
    public String tm_label() {
        return this.editing ? this.item == null ? "Add Item" : "Edit Item" : "Item Info";
    }

    @Override
    public int tr_icon() {
        return AuthManager.checkAuth(AuthManager.SubentityModify) ?
            this.editing ? R.drawable.ic_done_white_36dp : R.drawable.ic_edit_white_36dp :
            0;
    }

    @Override
    public int bl_icon() {
        return AuthManager.userCanModifySubentity() ? R.drawable.ic_delete_white_36dp : 0;
    }

    @Override
    public String bm_label() {
        if (!this.showingAssets && !this.editing) return "Show Assets";
        return "";
    }

    //
    // functionality
    @Override
    public void tl_clicked() {
        if (this.editing && this.item != null) {
            this.setEditing(false);
        } else
            finish();
    }

    @Override
    public void tr_clicked() {
        if (AuthManager.checkAuth(AuthManager.SubentityModify)) {
            if (this.editing)
                this.save();
            else
                this.setEditing(true);
        }
    }

    @Override
    public void bl_clicked() {
        if ( AuthManager.userCanModifySubentity() )
            new AlertDialog.Builder(this)
                    .setIcon(R.drawable.ic_delete_white_36dp)
                    .setTitle("Delete")
                    .setMessage("Are you sure that you want to delete this item?")
                    .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            DataManager.sharedManager().rmItem(item);
                        }
                    })
                    .setNegativeButton("No", null)
                    .show();
    }

    @Override
    public void bm_clicked() {
        if (!this.showingAssets && !this.editing) showAssets();
    }

    private void showAssets() {
        FragmentManager fm = getFragmentManager();
        FragmentTransaction ft = fm.beginTransaction();
        if (frag == null) {
            frag = AssetListFragment.newInstance(this.item);
            ft.add(R.id.fragment, frag);
        } else {
            ft.show(frag);
        }
        ft.commit();

        this.showingAssets = true;
        this.update();
    }

    @Override
    public void didSelectAsset(Asset item) {
        Intent i = new Intent(this, AssetInfoActivity.class);
        i.putExtra("Asset",item.tag_ece);
        this.startActivity(i);
    }

    public void setEditing( boolean editing ) {
        this.editing = editing;
        cat_switcher.showNext();
        man_switcher.showNext();
        model_switcher.showNext();
        this.update();
    }

    @Override
    public void init() {
        super.init();
        this.setContentView(R.layout.activity_item_info);

        //
        // initialize ui references
        cat_spinner = (Spinner) findViewById(R.id.cat_spinner);
        man_spinner = (Spinner) findViewById(R.id.man_spinner);
        model_et = (EditText) findViewById(R.id.model_et);

        cat_tv = (TextView) findViewById(R.id.cat_tv);
        man_tv = (TextView) findViewById(R.id.man_tv);
        model_tv = (TextView) findViewById(R.id.model_tv);

        cat_switcher = (ViewSwitcher) findViewById(R.id.cat_switcher);
        man_switcher = (ViewSwitcher) findViewById(R.id.man_switcher);
        model_switcher = (ViewSwitcher) findViewById(R.id.model_switcher);

        //
        // set the onclick for the add buttons or hide them
        // depending on permissions
        Button add_cat_b = (Button)findViewById(R.id.add_cat_b);
        Button add_man_b = (Button)findViewById(R.id.add_man_b);
        if (AuthManager.checkAuth(AuthManager.LabelModify)) {
            add_cat_b.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Label.addLabel(ItemInfoActivity.this, Label.ItemCategory.class);
                }
            });
            add_man_b.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Label.addLabel(ItemInfoActivity.this, Label.ItemManufacturer.class);
                }
            });
        } else {
            add_cat_b.setVisibility(View.INVISIBLE);
            add_man_b.setVisibility(View.INVISIBLE);
        }
    }

    @Override
    public void start() {
        super.start();

        // check if an item was specified
        Intent i = getIntent();
        int id = i.getIntExtra("Item", 0);

        // initialize ui fields if item exists
        if (id != 0) {
            item = DataManager.sharedManager().getItem(id);
        } else {
            this.setEditing(true);
        }
    }

    public boolean checkFields() {
        // check user input
        String cat, man, model;
        cat = cat_spinner.getSelectedItem().toString();
        man = man_spinner.getSelectedItem().toString();
        model = model_et.getText().toString();

        boolean cat_empty = cat.equals(DEFAULT_BUTTON_TEXT);
        boolean man_empty = man.equals(DEFAULT_BUTTON_TEXT);
        boolean model_empty = model.length() == 0;

        if (cat_empty || man_empty || model_empty) {
            return false;
        }
        return true;
    }

    @Override
    public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {

    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }

    @Override
    public void update() {
        super.update();

        // initialize spinner data
        ArrayAdapter<String> cat_arrayAdapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_item,
                DataManager.sharedManager().getCategoryStrings());
        ArrayAdapter<String> man_arrayAdapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_item,
                DataManager.sharedManager().getManufacturerStrings());

        cat_spinner.setAdapter(cat_arrayAdapter);
        man_spinner.setAdapter(man_arrayAdapter);

        if (item != null) {
            DataManager dm = DataManager.sharedManager();

            cat_spinner.setSelection(dm.getCategoryStrings().indexOf(item.getCategory()));
            cat_tv.setText(item.getCategory());

            man_spinner.setSelection(dm.getManufacturerStrings().indexOf(item.getManufacturer()));
            man_tv.setText(item.getManufacturer());

            model_tv.setText(item.getModel());
            model_et.setText(item.getModel());
        } else {
            cat_spinner.setPrompt(DEFAULT_BUTTON_TEXT);
            man_spinner.setPrompt(DEFAULT_BUTTON_TEXT);
        }
    }

    public void showEditPrompt() {
        Toast t = Toast.makeText(this,"Click the top-right button to edit this item",Toast.LENGTH_SHORT);
        t.show();
    }

    private void save() {
        if (this.checkFields()) {
            // get ui fields
            String cat, man, model;
            cat = cat_spinner.getSelectedItem().toString();
            man = man_spinner.getSelectedItem().toString();
            model = model_et.getText().toString();

            // set the item
            Item y = this.item != null ? this.item : new Item();
            y.setCategory(cat);
            y.setManufacturer(man);
            y.setModel(model);

            // post it to the datamanager
            DataManager.sharedManager().setModDelegate(this);
            DataManager.sharedManager().saveItem(y);
        }
    }

    @Override
    public void saveSuccess(Object i) {
        this.item = (Item)i;
        this.setEditing(false);
    }

    @Override
    public void deleteSuccess(String msg) {
        (Toast.makeText(this,msg,Toast.LENGTH_SHORT)).show();
        finish();
    }

    @Override
    public void saveFailure(int code, String reason) {
        Log.w(TAG, "An error occured while saving " + code + " " + reason);
    }
}
