package edu.villanova.ece.inv.activity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ViewSwitcher;

import com.breadtech.breadinterface.BIActivity;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import java.text.SimpleDateFormat;
import java.util.Date;

import edu.villanova.ece.inv.R;
import edu.villanova.ece.inv.manager.AuthManager;
import edu.villanova.ece.inv.manager.DataManager;
import edu.villanova.ece.inv.model.Asset;
import edu.villanova.ece.inv.model.Inventory;
import edu.villanova.ece.inv.model.Location;
import edu.villanova.ece.inv.model.User;

/**
 * Created by bk on 8/6/15.
 */
public class InvInfoActivity extends BIActivity implements DataManager.ModificationDelegate,
        AdapterView.OnItemSelectedListener {

    //
    // constants
    private static final String TAG = "InvInfoActivity";
    private static final String DEFAULT_BUTTON_TEXT = "Select from list";

    //
    // state
    private boolean editing;
    private boolean showingAssets;
    //
    // ui
    private ViewSwitcher who_switcher;
    private ViewSwitcher what_switcher;
    /* when is only a text view */
    private ViewSwitcher where_switcher;
    private ViewSwitcher how_switcher;

    private TextView who_tv;
    private TextView what_tv;
    private TextView when_tv;
    private TextView where_tv;
    private TextView how_tv;

    private Spinner who_spinner;
    private EditText what_et;
    /* when is only a text view */
    private Spinner where_spinner;
    private Spinner how_spinner;

    private SimpleDateFormat df;

    //
    // model
    Inventory inv;

    //
    // interface
    @Override
    public int tl_icon() {
        return this.editing ? R.drawable.ic_close_white_36dp : R.drawable.ic_keyboard_backspace_white_36dp;
    }

    @Override
    public String tm_label() {
        return this.editing ? this.inv == null ? "Add Inventory Record" : "Edit Inventory Record" : "Inventory Record";
    }

    @Override
    public int tr_icon() {
        return AuthManager.checkAuth(AuthManager.EntityModifyWorld) || (AuthManager.userCanModifyEntity() && this.editing)
                ? this.editing ? R.drawable.ic_done_white_36dp : R.drawable.ic_edit_white_36dp
                : 0;
    }

    @Override
    public int bl_icon() {
        return AuthManager.userCanModifyEntityWorld() ? R.drawable.ic_delete_white_36dp : 0;
    }

    //
    // functionality
    @Override
    public void tl_clicked() {
        if (this.editing && this.inv != null) {
            this.setEditing(false);
        } else
            finish();
    }

    @Override
    public void tr_clicked() {
        if (AuthManager.userCanModifyEntityWorld() || (AuthManager.userCanModifyEntity() && this.editing) )
            if (this.editing)
                this.save();
            else
                this.setEditing(true);
    }

    @Override
    public void bl_clicked() {
        if (AuthManager.userCanModifyEntityWorld())
            new AlertDialog.Builder(this)
                    .setIcon(R.drawable.ic_delete_white_36dp)
                    .setTitle("Delete")
                    .setMessage("Are you sure that you want to delete this inventory record?")
                    .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            DataManager.sharedManager().rmInv(inv);
                        }
                    })
                    .setNegativeButton("No", null)
                    .show();
    }

    public void setEditing( boolean editing ) {
        this.editing = editing;
        who_switcher.showNext();
        what_switcher.showNext();
        where_switcher.showNext();
        how_switcher.showNext();
        this.update();
    }

    @Override
    public void init() {
        super.init();
        this.setContentView(R.layout.activity_inv_info);

        // initialize ui references
        who_spinner = (Spinner) findViewById(R.id.who_spinner);
        what_et     = (EditText) findViewById(R.id.what_et);
        where_spinner = (Spinner) findViewById(R.id.where_spinner);
        how_spinner   = (Spinner) findViewById(R.id.how_spinner);

        who_tv   = (TextView) findViewById(R.id.who_tv);
        what_tv  = (TextView) findViewById(R.id.what_tv);
        when_tv  = (TextView) findViewById(R.id.when_tv);
        where_tv   = (TextView) findViewById(R.id.where_tv);
        how_tv  = (TextView) findViewById(R.id.how_tv);

        who_switcher  = (ViewSwitcher) findViewById(R.id.who_switcher);
        what_switcher = (ViewSwitcher) findViewById(R.id.what_switcher);
        where_switcher = (ViewSwitcher) findViewById(R.id.where_switcher);
        how_switcher   = (ViewSwitcher) findViewById(R.id.how_switcher);

        // initialize spinner data
        ArrayAdapter<User> who_arrayAdapter = new ArrayAdapter<User>(this,
                android.R.layout.simple_spinner_item,
                DataManager.sharedManager().getUsers());
        ArrayAdapter<Location> where_arrayAdapter = new ArrayAdapter<Location>(this,
                android.R.layout.simple_spinner_item,
                DataManager.sharedManager().getLocations());
        ArrayAdapter<String> how_arrayAdapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_item,
                Asset.Status.all);

        who_spinner.setAdapter(who_arrayAdapter);
        where_spinner.setAdapter(where_arrayAdapter);
        how_spinner.setAdapter(how_arrayAdapter);

        // set on click
        what_et.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                IntentIntegrator scanner = new IntentIntegrator(InvInfoActivity.this);
                scanner.initiateScan();
            }
        });

        df = new SimpleDateFormat("MM/dd/yyyy hh:mm");
    }

    public void onActivityResult(int requestCode, int resultCode, Intent intent) {

        //
        // returning from the barcode scanner
        IntentResult scanner = IntentIntegrator.parseActivityResult(requestCode,resultCode,intent);
        if (scanner != null) {
            String ece_tag = scanner.getContents();
            if (ece_tag == null || ece_tag.length() == 0) return;
            this.what_et.setText(ece_tag);
            this.setEditing(true);
        }
    }

    @Override
    public void start() {
        super.start();

        // check if an item was specified
        Intent i = getIntent();
        int id = i.getIntExtra("Inv", 0);

        // initialize ui fields if item exists
        if (id != 0) {
            this.inv = DataManager.sharedManager().getInv(id);
        } else {
            this.setEditing(true);
        }
    }

    public boolean checkFields() {
        // check user input
        String ece_tag = what_et.getText().toString();
        Asset a = DataManager.sharedManager().getAsset(ece_tag);
        if (a == null) {
            new AlertDialog.Builder(this)
                    .setIcon(R.drawable.abc_ic_clear_mtrl_alpha)
                    .setTitle("Not Found")
                    .setMessage("This asset was not found.")
                    .setNegativeButton("OK", null)
                    .show();
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

        if (this.inv != null) {
            DataManager dm = DataManager.sharedManager();

            who_spinner.setSelection(dm.getUsers().indexOf(inv.getWho().getUid()));
            who_tv.setText(inv.getWho().toString());

            what_et.setText(inv.getWhat().getTag_ece());
            what_tv.setText(inv.getWhat().getTag_ece());

            when_tv.setText(df.format(inv.getWhen()));

            where_spinner.setSelection(dm.getLocations().indexOf(inv.getWhere()));
            where_tv.setText(inv.getWhere().toString());

            how_spinner.setSelection(Asset.Status.all.indexOf(inv.getHow().toString()));
            how_tv.setText(inv.getHow().toString());
        } else {
            //
            // initialize add inv fields

            // who: the logged in user, when: now, how: available
            who_spinner.setSelection(DataManager.sharedManager().getUsers().indexOf(AuthManager.getUser()));
            when_tv.setText(df.format(new Date()));
            how_spinner.setSelection(1);

            // initialize what and where if the ecetag was supplied to the activity
            Intent i = getIntent();
            String ece_tag = i.getStringExtra("Asset");
            if (ece_tag != null)  {
                Asset a = DataManager.sharedManager().getAsset(ece_tag);
                what_et.setText(ece_tag);
                where_spinner.setSelection(
                        DataManager.sharedManager().getLocations().indexOf(a));
            }

        }

        // disable the who spinner if the user does not have permission to modify all invs
        if (!AuthManager.checkAuth(AuthManager.EntityModifyWorld)) {
            who_spinner.setEnabled(false);
        }
    }

    public void showEditPrompt() {
        Toast t = Toast.makeText(this,"Click the top-right button to edit this Inventory Record",Toast.LENGTH_SHORT);
        t.show();
    }

    private void save() {
        if (this.checkFields()) {
            try {
                // get ui fields
                User who = (User) who_spinner.getSelectedItem();
                Asset what = DataManager.sharedManager().getAsset(what_et.getText().toString());
                Date when = df.parse(when_tv.getText().toString());
                Location where = (Location) where_spinner.getSelectedItem();
                Asset.Status how = Asset.Status.valueOf((String) how_spinner.getSelectedItem());

                // set the item
                Inventory y = this.inv != null ? this.inv : new Inventory();
                y.setWho(who.getUid());
                y.setWhat(what.getTag_ece());
                y.setWhen(when.getTime() / 1000);
                y.setWhere(where.getId());
                y.setHow(how);

                // post it to the datamanager
                DataManager.sharedManager().setModDelegate(this);
                DataManager.sharedManager().saveInv(y);
            }
            catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    @Override
    public void saveSuccess(Object i) {
        this.inv = (Inventory)i;
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
