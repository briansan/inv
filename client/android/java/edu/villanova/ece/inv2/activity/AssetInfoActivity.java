package edu.villanova.ece.inv2.activity;

import android.app.AlertDialog;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.CheckBox;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.ViewSwitcher;

import com.breadtech.breadinterface.BIActivity;

import org.apache.http.impl.cookie.DateUtils;

import java.text.NumberFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import edu.villanova.ece.inv2.R;
import edu.villanova.ece.inv2.adapter.ItemArrayAdapter;
import edu.villanova.ece.inv2.adapter.LocationArrayAdapter;
import edu.villanova.ece.inv2.adapter.UserArrayAdapter;
import edu.villanova.ece.inv2.fragment.AssetListFragment;
import edu.villanova.ece.inv2.manager.AuthManager;
import edu.villanova.ece.inv2.manager.DataManager;
import edu.villanova.ece.inv2.model.Asset;
import edu.villanova.ece.inv2.model.Item;
import edu.villanova.ece.inv2.model.Location;
import edu.villanova.ece.inv2.model.User;

/**
 * Created by bk on 8/6/15.
 */
public class AssetInfoActivity extends BIActivity implements DataManager.ModificationDelegate,
        AdapterView.OnItemSelectedListener {

    //
    // constants
    private static final String TAG = "AssetInfoActivity";
    private static final String DEFAULT_BUTTON_TEXT = "Select from list";

    //
    // state
    private boolean editing;
    //
    // ui
    private ViewSwitcher ece_switcher, item_switcher, status_switcher, vu_switcher,
                         unit_switcher, svc_switcher, serial_switcher,
                         price_switcher, purchase_switcher, owner_switcher, home_switcher,
                         ip_switcher, comments_switcher;

    private TextView ece_tv, item_tv, status_tv, lastinv_tv, holder_tv, current_tv, vu_tv,
                     unit_tv, svc_tv, serial_tv, price_tv, purchase_tv, owner_tv, home_tv,
                     ip_tv, comments_tv;

    private Spinner item_spinner, status_spinner, owner_spinner, home_spinner;
    private EditText ece_et, vu_et, unit_et, svc_et, serial_et, price_et, purchase_et, ip_et, comments_et;


    //
    // model
    Asset asset;
    String ece_tag;

    //
    // interface
    @Override
    public int tl_icon() {
        return this.editing ? R.drawable.ic_close_white_36dp : R.drawable.ic_keyboard_backspace_white_36dp;
    }

    @Override
    public String tm_label() {
        return this.editing ? this.asset == null ? "Add Asset" : "Edit Asset" : "Asset Info";
    }

    @Override
    public int tr_icon() {
        boolean isOwner = this.asset == null && AuthManager.getUser().equals(this.asset.getOwner());
        return AuthManager.checkAuth(AuthManager.EntityModifyWorld) || isOwner ?
            this.editing ? R.drawable.ic_done_white_36dp : R.drawable.ic_edit_white_36dp :
            0;
    }

    @Override
    public int bl_icon() {
        return AuthManager.userCanModifyEntityWorld() ? R.drawable.ic_delete_white_36dp : 0;
    }

    @Override
    public String bm_label() {
        if (!this.editing) return "Inventory Log";
        return "";
    }

    @Override
    public int br_icon() {
        return AuthManager.checkAuth(AuthManager.EntityModify) && this.asset != null
                ? R.drawable.ic_add_white_36dp : 0;
    }

    //
    // functionality
    @Override
    public void tl_clicked() {
        if (this.editing && this.asset != null) {
            this.setEditing(false);
        } else
            finish();
    }

    @Override
    public void tr_clicked() {
        boolean isOwner = this.asset != null && AuthManager.getUser().equals(this.asset.getOwner());
        if (AuthManager.checkAuth(AuthManager.EntityModify) || isOwner) {
            if (this.editing)
                this.save();
            else
                this.setEditing(true);
        }
    }

    @Override
    public void bl_clicked() {
        if (AuthManager.userCanModifyEntityWorld())
             new AlertDialog.Builder(this)
                    .setIcon(R.drawable.ic_delete_white_36dp)
                    .setTitle("Delete")
                    .setMessage("Are you sure that you want to delete this asset?")
                    .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                        @Override
                        public void onClick(DialogInterface dialog, int which) {
                            DataManager.sharedManager().rmAsset(asset);
                        }
                    })
                    .setNegativeButton("No", null)
                    .show();
    }

    @Override
    public void bm_clicked() {
        if (!this.editing) showInv();
    }

    @Override
    public void br_clicked() {
        if (this.asset != null && AuthManager.checkAuth(AuthManager.EntityModify)) {
            Intent i = new Intent(this,InvInfoActivity.class);
            i.putExtra("Asset",this.asset.getTag_ece());
            startActivity(i);
        }
    }

    private void showInv() {
        Intent i = new Intent(this,ListActivity.class);
        i.putExtra("Mode",ListActivity.Mode.InvByAsset);
        i.putExtra("Asset",this.asset.tag_ece);
        startActivity(i);
    }

    public void setEditing( boolean editing ) {
        this.editing = editing;
        ece_switcher.showNext();
        item_switcher.showNext();
        status_switcher.showNext();
        vu_switcher.showNext();
        unit_switcher.showNext();
        svc_switcher.showNext();
        serial_switcher.showNext();
        price_switcher.showNext();
        purchase_switcher.showNext();
        owner_switcher.showNext();
        home_switcher.showNext();
        ip_switcher.showNext();
        comments_switcher.showNext();
        this.update();
    }

    private SimpleDateFormat dfmt1, dfmt2;
    private NumberFormat cfmt;

    @Override
    public void init() {
        super.init();
        this.setContentView(R.layout.activity_asset_info);


        dfmt1 = new SimpleDateFormat("MM/dd/yyyy hh:mm", Locale.US);
        dfmt2 = new SimpleDateFormat("MM/dd/yyyy", Locale.US);
        cfmt = NumberFormat.getCurrencyInstance();

        // initialize ui references
        ece_switcher = (ViewSwitcher)findViewById(R.id.ece_switcher);
        item_switcher = (ViewSwitcher)findViewById(R.id.item_switcher);
        status_switcher = (ViewSwitcher)findViewById(R.id.status_switcher);
        vu_switcher = (ViewSwitcher)findViewById(R.id.vu_switcher);
        unit_switcher = (ViewSwitcher)findViewById(R.id.unit_switcher);
        svc_switcher = (ViewSwitcher)findViewById(R.id.svc_switcher);
        serial_switcher = (ViewSwitcher)findViewById(R.id.serial_switcher);
        price_switcher = (ViewSwitcher)findViewById(R.id.price_switcher);
        purchase_switcher = (ViewSwitcher)findViewById(R.id.purchase_switcher);
        owner_switcher = (ViewSwitcher)findViewById(R.id.owner_switcher);
        home_switcher = (ViewSwitcher)findViewById(R.id.home_switcher);
        ip_switcher = (ViewSwitcher)findViewById(R.id.ip_switcher);
        comments_switcher = (ViewSwitcher)findViewById(R.id.comment_switcher);

        ece_tv = (TextView)findViewById(R.id.ece_tv);
        item_tv = (TextView)findViewById(R.id.item_tv);
        status_tv = (TextView)findViewById(R.id.status_tv);
        lastinv_tv = (TextView)findViewById(R.id.lastinv_tv);
        holder_tv = (TextView)findViewById(R.id.holder_tv);
        current_tv = (TextView)findViewById(R.id.current_tv);
        vu_tv = (TextView)findViewById(R.id.vu_tv);
        unit_tv = (TextView)findViewById(R.id.unit_tv);
        svc_tv = (TextView)findViewById(R.id.svc_tv);
        serial_tv = (TextView)findViewById(R.id.serial_tv);
        price_tv = (TextView)findViewById(R.id.price_tv);
        purchase_tv = (TextView)findViewById(R.id.purchase_tv);
        owner_tv = (TextView)findViewById(R.id.owner_tv);
        home_tv = (TextView)findViewById(R.id.home_tv);
        ip_tv = (TextView)findViewById(R.id.ip_tv);
        comments_tv = (TextView)findViewById(R.id.comment_tv);

        item_spinner = (Spinner)findViewById(R.id.item_spinner);
        status_spinner = (Spinner)findViewById(R.id.status_spinner);
        owner_spinner = (Spinner)findViewById(R.id.owner_spinner);
        home_spinner = (Spinner)findViewById(R.id.home_spinner);

        ece_et = (EditText)findViewById(R.id.ece_et);
        vu_et = (EditText)findViewById(R.id.vu_et);
        unit_et = (EditText)findViewById(R.id.unit_et);
        svc_et = (EditText)findViewById(R.id.svc_et);
        serial_et = (EditText)findViewById(R.id.serial_et);
        price_et = (EditText)findViewById(R.id.price_et);
        purchase_et = (EditText)findViewById(R.id.purchase_et);
        ip_et = (EditText)findViewById(R.id.ip_et);
        comments_et = (EditText)findViewById(R.id.comment_et);

        // initialize spinner data
        ArrayAdapter<Item> itemArrayAdapter = new ArrayAdapter<Item>(this,
                android.R.layout.simple_spinner_item, DataManager.sharedManager().getItems());
        ArrayAdapter<String> statusArrayAdapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_item, Asset.Status.all);
        ArrayAdapter<User> userArrayAdapter = new ArrayAdapter<User>(this,
                android.R.layout.simple_spinner_item, DataManager.sharedManager().getUsers());
        ArrayAdapter<Location> locArrayAdapter = new ArrayAdapter<Location>(this,
                android.R.layout.simple_spinner_item, DataManager.sharedManager().getLocations());

        item_spinner.setAdapter(itemArrayAdapter);
        status_spinner.setAdapter(statusArrayAdapter);
        owner_spinner.setAdapter(userArrayAdapter);
        home_spinner.setAdapter(locArrayAdapter);
    }

    @Override
    public void start() {
        super.start();

        // check if an item was specified
        Intent i = getIntent();
        ece_tag = i.getStringExtra("Asset");

        // initialize ui fields if item exists
        if (ece_tag !=  null) {
            asset = DataManager.sharedManager().getAsset(ece_tag);
            if (asset == null) this.setEditing(true);
        } else {
            this.setEditing(true);
        }
    }

    public boolean checkFields() {
        // check user input
        String ece_tag = ece_et.getText().toString();

        boolean model_empty = ece_tag.length() == 0;

        if (model_empty) {
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

        if (asset != null) {
            DataManager dm = DataManager.sharedManager();


            ece_tv.setText(asset.getTag_ece());
            item_tv.setText(asset.getItem() == null ? "" : asset.getItem().toString());
            status_tv.setText(asset.getStatus() == null ? "" : asset.getStatus().toString());
            lastinv_tv.setText(asset.getInventoried() == null ? "Never" : dfmt1.format(asset.getInventoried()));
            holder_tv.setText(asset.getHolder() == null ? asset.getOwner().toString() : asset.getHolder().toString());
            current_tv.setText(asset.getCurrent() == null ? asset.getHome().toString() : asset.getCurrent().toString());
            vu_tv.setText(asset.getTag_vu());
            unit_tv.setText(asset.getTag_unit());
            svc_tv.setText(asset.getTag_svc());
            serial_tv.setText(asset.getSerial());
            price_tv.setText(cfmt.format(asset.getPrice()));
            purchase_tv.setText(asset.getPurchased() == null ? "" : dfmt2.format(asset.getPurchased()));
            owner_tv.setText(asset.getOwner() == null ? "" : asset.getOwner().toString());
            home_tv.setText(asset.getHome() == null ? "" : asset.getHome().toString());
            ip_tv.setText(asset.getIp());
            comments_tv.setText(asset.getComments());

            item_spinner.setSelection(dm.getItems().indexOf(asset.getItem()));
            status_spinner.setSelection(Asset.Status.all.indexOf(asset.getStatus().toString()));
            owner_spinner.setSelection(dm.getUsers().indexOf(asset.getOwner()));
            home_spinner.setSelection(dm.getLocations().indexOf(asset.getHome()));

            ece_et.setText(asset.getTag_ece());
            ece_et.setEnabled(false);
            vu_et.setText(asset.getTag_vu());
            unit_et.setText(asset.getTag_unit());
            svc_et.setText(asset.getTag_svc());
            serial_et.setText(asset.getSerial());
            price_et.setText(""+asset.getPrice());
            purchase_et.setText(asset.getPurchased() == null ? "" : dfmt2.format(asset.getPurchased()));
            ip_et.setText(asset.getIp());
            comments_et.setText(asset.getComments());

        } else {
            if (ece_tag != null) ece_et.setText(ece_tag);
            findViewById(R.id.doinv_wrapper).setVisibility(View.VISIBLE);
            findViewById(R.id.lastinv_label).setVisibility(View.INVISIBLE);
            findViewById(R.id.holder_label).setVisibility(View.INVISIBLE);
            findViewById(R.id.current_label).setVisibility(View.INVISIBLE);
        }
    }

    public void showEditPrompt() {
        Toast t = Toast.makeText(this,"Click the top-right button to edit this item",Toast.LENGTH_SHORT);
        t.show();
    }

    private void save() {
        if (this.checkFields()) {
            // get ui fields
            String ece_tag = ece_et.getText().toString();
            Item item = (Item)item_spinner.getSelectedItem();
            Asset.Status status = Asset.Status.valueOf(status_spinner.getSelectedItem().toString());
            String vu_tag = vu_et.getText().toString();
            String unit_tag = unit_et.getText().toString();
            String svc_tag = svc_et.getText().toString();
            String serial = serial_et.getText().toString();
            User owner = (User)owner_spinner.getSelectedItem();
            Location home = (Location)home_spinner.getSelectedItem();
            float price = Float.parseFloat(price_et.getText().toString().length() == 0 ? "0.0" : price_et.getText().toString());
            Date purchase = null;
            try {
                String date_s = purchase_et.getText().toString();
                purchase = dfmt2.parse(date_s.length() == 0 ? "08/01/2015" : date_s);
            }
            catch (ParseException e) {
                e.printStackTrace();
                return;
            }
            String ip = ip_et.getText().toString();
            String comments = comments_et.getText().toString();

            // set the item
            Asset y = this.asset != null ? this.asset : new Asset();
            y.setTag_ece(ece_et.getText().toString());
            y.setItem(item.getId());
            y.setStatus(status);
            y.setTag_vu(vu_tag);
            y.setTag_unit(unit_tag);
            y.setTag_svc(svc_tag);
            y.setSerial(serial);
            y.setOwner(owner.getUid());
            y.setHome(home.getId());
            y.setPrice(price);
            y.setPurchased(purchase);
            y.setIp(ip);
            y.setComments(comments);

            CheckBox doinv = (CheckBox)findViewById(R.id.doinv_cb);
            if (doinv.isChecked()) y.doinv = true;

            // post it to the datamanager
            DataManager.sharedManager().setModDelegate(this);
            DataManager.sharedManager().saveAsset(y);
            this.tr.setEnabled(false);
        }
    }

    @Override
    public void saveSuccess(Object i) {
        this.asset = (Asset)i;
        this.tr.setEnabled(true);
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
