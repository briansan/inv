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
import edu.villanova.ece.inv2.model.Label;
import edu.villanova.ece.inv2.model.Location;

/**
 * Created by bk on 8/6/15.
 */
public class LocationInfoActivity extends BIActivity implements DataManager.ModificationDelegate,
        AdapterView.OnItemSelectedListener, AssetListFragment.Delegate {

    //
    // constants
    private static final String TAG = "LocationInfoActivity";
    private static final String DEFAULT_BUTTON_TEXT = "Select from list";

    //
    // state
    private boolean editing;
    private boolean showingAssets;
    //
    // ui
    private ViewSwitcher build_switcher;
    private ViewSwitcher room_switcher;

    private TextView build_tv;
    private TextView room_tv;

    private Spinner build_spinner;
    private EditText room_et;

    private AssetListFragment frag;

    //
    // model
    Location location;

    //
    // interface
    @Override
    public int tl_icon() {
        return this.editing ? R.drawable.ic_close_white_36dp : R.drawable.ic_keyboard_backspace_white_36dp;
    }

    @Override
    public String tm_label() {
        return this.editing ? this.location == null ? "Add Location" : "Edit Location" : "Location Info";
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
        if (this.editing && this.location != null) {
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
        if (AuthManager.userCanModifySubentity())
            new AlertDialog.Builder(this)
                    .setIcon(R.drawable.ic_delete_white_36dp)
                    .setTitle("Delete")
                    .setMessage("Are you sure that you want to delete this location?")
                    .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            DataManager.sharedManager().rmLocation(location);
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
        if (frag == null) frag = AssetListFragment.newInstance(this.location);
        ft.replace(R.id.fragment, frag);
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
        build_switcher.showNext();
        room_switcher.showNext();
        this.update();
    }

    @Override
    public void init() {
        super.init();
        this.setContentView(R.layout.activity_location_info);

        // initialize ui references
        build_spinner = (Spinner) findViewById(R.id.build_spinner);
        room_et = (EditText) findViewById(R.id.room_et);

        build_tv = (TextView) findViewById(R.id.build_tv);
        room_tv  = (TextView) findViewById(R.id.room_tv);

        build_switcher = (ViewSwitcher) findViewById(R.id.build_switcher);
        room_switcher  = (ViewSwitcher) findViewById(R.id.room_switcher);

        //
        // set the onclick for the add button or hide it
        // depending on permissions
        Button build_b = (Button)findViewById(R.id.add_build_b);
        if (AuthManager.checkAuth(AuthManager.LabelModify)) {
            build_b.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Label.addLabel(LocationInfoActivity.this,Label.LocationBuilding.class);
                }
            });
        } else {
            build_b.setVisibility(View.INVISIBLE);
        }
    }

    @Override
    public void start() {
        super.start();

        // check if an item was specified
        Intent i = getIntent();
        int id = i.getIntExtra("Location", 0);

        // initialize ui fields if item exists
        if (id != 0) {
            this.location = DataManager.sharedManager().getLocation(id);
        } else {
            this.setEditing(true);
        }
    }

    public boolean checkFields() {
        // check user input
        String building, room;
        building = build_spinner.getSelectedItem().toString();
        room = room_et.getText().toString();

        boolean build_empty = building.equals(DEFAULT_BUTTON_TEXT);
        boolean room_empty = room.length() == 0;

        if (build_empty || room_empty) {
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

        if (this.location != null) {
            DataManager dm = DataManager.sharedManager();

            build_spinner.setSelection(dm.getBuildingStrings().indexOf(location.getBuilding()));
            build_tv.setText(location.getBuilding());

            room_et.setText(location.getRoom());
            room_tv.setText(location.getRoom());
        } else {
            build_spinner.setPrompt(DEFAULT_BUTTON_TEXT);
        }

        //
        // initialize spinner data
        ArrayAdapter<String> build_arrayAdapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_item,
                DataManager.sharedManager().getBuildingStrings());

        build_spinner.setAdapter(build_arrayAdapter);
    }

    public void showEditPrompt() {
        Toast t = Toast.makeText(this,"Click the top-right button to edit this location",Toast.LENGTH_SHORT);
        t.show();
    }

    private void save() {
        if (this.checkFields()) {
            // get ui fields
            String building, room;
            building = build_spinner.getSelectedItem().toString();
            room = room_et.getText().toString();

            // set the item
            Location y = this.location != null ? this.location : new Location();
            y.setBuilding(building);
            y.setRoom(room);

            // post it to the datamanager
            DataManager.sharedManager().setModDelegate(this);
            DataManager.sharedManager().saveLocation(y);
        }
    }

    @Override
    public void saveSuccess(Object i) {
        this.location = (Location)i;
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
