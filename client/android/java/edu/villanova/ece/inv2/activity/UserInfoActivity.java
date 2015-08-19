package edu.villanova.ece.inv2.activity;

import android.app.FragmentManager;
import android.app.FragmentTransaction;
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

import edu.villanova.ece.inv2.R;
import edu.villanova.ece.inv2.fragment.AssetListFragment;
import edu.villanova.ece.inv2.manager.AuthManager;
import edu.villanova.ece.inv2.model.Asset;
import edu.villanova.ece.inv2.manager.DataManager;
import edu.villanova.ece.inv2.model.Location;
import edu.villanova.ece.inv2.model.User;

/**
 * Created by bk on 8/6/15.
 */
public class UserInfoActivity extends BIActivity implements DataManager.ModificationDelegate,
        AdapterView.OnItemSelectedListener, AssetListFragment.Delegate {

    //
    // constants
    private static final String TAG = "UserInfoActivity";
    private static final String DEFAULT_BUTTON_TEXT = "Select from list";

    //
    // state
    private boolean editing;
    private boolean showingAssets;
    //
    // ui
    private ViewSwitcher fname_switcher;
    private ViewSwitcher lname_switcher;
    private ViewSwitcher phone_switcher;
    private ViewSwitcher email_switcher;

    private TextView uid_tv;
    private TextView fname_tv;
    private TextView lname_tv;
    private TextView phone_tv;
    private TextView email_tv;

    private EditText fname_et;
    private EditText lname_et;
    private EditText phone_et;
    private EditText email_et;

    private AssetListFragment frag;

    //
    // model
    User user;

    //
    // interface
    @Override
    public int tl_icon() {
        return this.editing ? R.drawable.ic_close_white_36dp : R.drawable.ic_keyboard_backspace_white_36dp;
    }

    @Override
    public String tm_label() {
        return this.editing ? "Edit User" : "User Info";
    }

    @Override
    public int tr_icon() {
        return AuthManager.getUser().equals(this.user)
                ? this.editing ? R.drawable.ic_done_white_36dp : R.drawable.ic_edit_white_36dp
                : 0;
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
        if (this.editing && this.user != null) {
            this.setEditing(false);
        } else
            finish();
    }

    @Override
    public void tr_clicked() {
        if (AuthManager.getUser().equals(this.user)) {
            if (this.editing)
                this.save();
            else
                this.setEditing(true);
        }
    }

    @Override
    public void bm_clicked() {
        if (!this.showingAssets && !this.editing) showAssets();
    }

    private void showAssets() {
        FragmentManager fm = getFragmentManager();
        FragmentTransaction ft = fm.beginTransaction();
        if (frag == null) frag = AssetListFragment.newInstance(this.user);
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
        fname_switcher.showNext();
        lname_switcher.showNext();
        phone_switcher.showNext();
        email_switcher.showNext();
        this.update();
    }

    @Override
    public void init() {
        super.init();
        this.setContentView(R.layout.activity_user_info);

        // initialize ui references
        fname_et = (EditText) findViewById(R.id.fname_et);
        lname_et = (EditText) findViewById(R.id.lname_et);
        phone_et = (EditText) findViewById(R.id.phone_et);
        email_et = (EditText) findViewById(R.id.email_et);

        uid_tv = (TextView) findViewById(R.id.uid_tv);
        fname_tv = (TextView) findViewById(R.id.fname_tv);
        lname_tv = (TextView) findViewById(R.id.lname_tv);
        phone_tv = (TextView) findViewById(R.id.phone_tv);
        email_tv = (TextView) findViewById(R.id.email_tv);

        fname_switcher = (ViewSwitcher) findViewById(R.id.fname_switcher);
        lname_switcher = (ViewSwitcher) findViewById(R.id.lname_switcher);
        phone_switcher = (ViewSwitcher) findViewById(R.id.phone_switcher);
        email_switcher = (ViewSwitcher) findViewById(R.id.email_switcher);

    }

    @Override
    public void start() {
        super.start();

        // check if an item was specified
        Intent i = getIntent();
        String id = i.getStringExtra("User");

        // initialize ui fields if item exists
        if (id != null) {
            this.user = DataManager.sharedManager().getUser(id);
        } else {
            this.setEditing(true);
        }
    }

    public boolean checkFields() {
        // check user input
        String fname, lname, email, phone;
        fname = fname_et.getText().toString();
        lname = lname_et.getText().toString();
        email = email_et.getText().toString();
        phone = phone_et.getText().toString();

        boolean fname_empty = fname.length() == 0;
        boolean lname_empty = lname.length() == 0;
        boolean email_empty = email.length() == 0;
        boolean phone_empty = phone.length() == 0;

        if (fname_empty || lname_empty || email_empty || phone_empty) {
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

        if (this.user != null) {
            DataManager dm = DataManager.sharedManager();

            uid_tv.setText(this.user.getUid());
            fname_tv.setText(this.user.getFname());
            lname_tv.setText(this.user.getLname());
            phone_tv.setText(this.user.getPhone());
            email_tv.setText(this.user.getEmail());

            fname_et.setText(this.user.getFname());
            lname_et.setText(this.user.getLname());
            phone_et.setText(this.user.getPhone());
            email_et.setText(this.user.getEmail());
        }
    }

    public void showEditPrompt() {
        Toast t = Toast.makeText(this,"Click the top-right button to edit this User",Toast.LENGTH_SHORT);
        t.show();
    }

    private void save() {
        if (this.checkFields()) {
            // get ui fields
            String fname, lname, email, phone;
            fname = fname_et.getText().toString();
            lname = lname_et.getText().toString();
            email = email_et.getText().toString();
            phone = phone_et.getText().toString();

            // set the item
            User y = this.user != null ? this.user : new User();
            y.setFname(fname);
            y.setLname(lname);
            y.setEmail(email);
            y.setPhone(phone);

            // post it to the datamanager
            DataManager.sharedManager().setModDelegate(this);
            DataManager.sharedManager().saveUser(y);
        }
    }

    @Override
    public void saveSuccess(Object i) {
        this.user = (User)i;
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
