package edu.villanova.ece.inv.activity;

import android.app.AlertDialog;
import android.app.FragmentManager;
import android.app.FragmentTransaction;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.ActivityInfo;
import android.util.Log;
import android.widget.Toast;

import com.breadtech.breadinterface.BIActivity;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Timer;
import java.util.TimerTask;

import edu.villanova.ece.inv.R;
import edu.villanova.ece.inv.fragment.AssetListFragment;
import edu.villanova.ece.inv.fragment.InvListFragment;
import edu.villanova.ece.inv.fragment.ItemListFragment;
import edu.villanova.ece.inv.fragment.LocationListFragment;
import edu.villanova.ece.inv.fragment.UserListFragment;
import edu.villanova.ece.inv.manager.AuthManager;
import edu.villanova.ece.inv.model.Asset;
import edu.villanova.ece.inv.manager.DataManager;
import edu.villanova.ece.inv.model.Inventory;
import edu.villanova.ece.inv.model.Item;
import edu.villanova.ece.inv.model.Location;
import edu.villanova.ece.inv.model.User;


public class MainActivity extends BIActivity implements DataManager.DataDelegate,
        ItemListFragment.Delegate, LocationListFragment.Delegate,
        AssetListFragment.Delegate, InvListFragment.Delegate, UserListFragment.Delegate
{

    //
    // constants
    public static final String TAG = "MainActivity";

    //
    // mode enum definition
    public static class Mode {
        public static final int Items = 0;
        public static final int Locations = 1;
        public static final int Users = 2;
        public static final int Assets = 3;
        public static final int Invs = 4;

        public static final HashMap<Integer,Integer> modeNextIconMap;
        static
        {
            modeNextIconMap = new HashMap<Integer, Integer>();
            modeNextIconMap.put(Items, R.drawable.ic_my_location_white_36dp);
            modeNextIconMap.put(Locations, R.drawable.ic_perm_contact_calendar_white_36dp);
            modeNextIconMap.put(Users, R.drawable.ic_shopping_cart_white_36dp);
            modeNextIconMap.put(Assets, R.drawable.ic_assignment_white_36dp);
            modeNextIconMap.put(Invs, R.drawable.ic_computer_white_36dp);
        }
        public static final HashMap<Integer,String> modeStringMap;
        static
        {
            modeStringMap = new HashMap<Integer, String>();
            modeStringMap.put(Items, "Items");
            modeStringMap.put(Locations, "Locations");
            modeStringMap.put(Users, "Users");
            modeStringMap.put(Assets, "Assets");
            modeStringMap.put(Invs, "Inventory Log");
        }
        public static final ArrayList<String> modes;
        static
        {
            modes = new ArrayList<String>();
            modes.add("Items");
            modes.add("Locations");
            modes.add("Users");
            modes.add("Assets");
            modes.add("Inventory Log");
        }
    }

    //
    // instance variables
    protected ProgressDialog downloadingProgress, processingProgress;

    protected DataManager dm;
    protected int mode;
    protected static boolean downloadFlag;

    //
    // ui
    //
    @Override
    public int tl_icon() {
        return R.drawable.ic_refresh_white_36dp;
    }

    @Override
    public String tm_label() {
        return "inv";
    }

    @Override
    public int tr_icon() {
        return R.drawable.ic_settings_white_36dp;
    }

    @Override
    public int bl_icon() {
        return R.drawable.ic_barcode_white_36dp;
    }


    @Override
    public String bm_label() {
        return Mode.modeStringMap.get(this.mode);
    }

    @Override
    public int br_icon() {
        return (this.mode == Mode.Locations && AuthManager.checkAuth(AuthManager.SubentityModify)) ||
                (this.mode == Mode.Items && AuthManager.checkAuth(AuthManager.SubentityModify)) ||
                (this.mode == Mode.Users && AuthManager.checkAuth(AuthManager.UserModifyWorld)) ||
                (this.mode == Mode.Assets && AuthManager.checkAuth(AuthManager.EntityModify)) ||
                (this.mode == Mode.Invs && AuthManager.checkAuth(AuthManager.EntityModify))
                ? R.drawable.ic_add_white_36dp: 0 ;
    }

    //
    // functionality

    @Override
    public void tl_clicked() {
        new AlertDialog.Builder(this)
                .setIcon(R.drawable.ic_refresh_white_36dp)
                .setTitle("Refresh")
                .setMessage("Are you sure that you really want refresh all the data?")
                .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        downloadData();
                    }
                })
                .setNegativeButton("No", null)
                .show();
    }

    @Override
    public void tr_clicked() {
        startActivity( new Intent(this, SettingsActivity.class));
    }

    @Override
    public void bl_clicked() {
        IntentIntegrator scanner = new IntentIntegrator(this);
        scanner.initiateScan();
    }

    @Override
    public void bm_clicked() {
        if (this.mode == 4) this.mode = 0; else mode++;
        this.update();
    }

    @Override
    public void br_clicked() {
        if (this.mode == Mode.Locations && AuthManager.checkAuth(AuthManager.SubentityModify)) {
            Intent i = new Intent(this, LocationInfoActivity.class);
            startActivity(i);
        } else if (this.mode == Mode.Items && AuthManager.checkAuth(AuthManager.SubentityModify)) {
            Intent i = new Intent(this, ItemInfoActivity.class);
            startActivity(i);
        } else if (this.mode == Mode.Users && AuthManager.checkAuth(AuthManager.UserModifyWorld)) {
            new AlertDialog.Builder(this)
                    .setIcon(R.drawable.abc_ic_clear_mtrl_alpha)
                    .setTitle("Not Available")
                    .setMessage("This feature is currently locked. Sorry.")
                    .setNegativeButton("Deal with it", null)
                    .show();
        } else if (this.mode == Mode.Assets && AuthManager.checkAuth(AuthManager.EntityModify)) {
            Intent i = new Intent(this, AssetInfoActivity.class);
            startActivity(i);
        } else if (this.mode == Mode.Invs && AuthManager.checkAuth(AuthManager.EntityModify)) {
            Intent i = new Intent(this, InvInfoActivity.class);
            startActivity(i);
        }
    }

    //
    // lifecycle
    //

    @Override
    public void init() {
        super.init();
        this.setContentView(R.layout.activity_main);

        this.dm = DataManager.sharedManager();

        SharedPreferences pref = getSharedPreferences("inv", 0);
        this.mode = pref.getInt("List", Mode.Assets);

        User u = AuthManager.getUser();
        if (u != null)
            Toast.makeText(this, "Welcome " +u.getFname()+" "+u.getLname(),Toast.LENGTH_LONG).show();

        if (!downloadFlag) {
            downloadData();
            downloadFlag = true;
        }
    }

    public void onActivityResult(int requestCode, int resultCode, Intent intent) {

        //
        // returning from the barcode scanner
        IntentResult scanner = IntentIntegrator.parseActivityResult(requestCode,resultCode,intent);
        if (scanner != null) {
            String ece_tag = scanner.getContents();
            if (ece_tag == null || ece_tag.length() == 0) return;
            Intent i = new Intent(this,AssetInfoActivity.class);
            i.putExtra("Asset", ece_tag);
            startActivity(i);
        }
    }


    //
    // data loading
    //


    public ProgressDialog initLoadingDialog() {
        // create the dialog
        ProgressDialog y = new ProgressDialog(MainActivity.this);

        y.setCancelable(false);
        y.setCanceledOnTouchOutside(false);

        y.setIndeterminate(false);
        y.setMax(8);
        y.setProgressStyle(ProgressDialog.STYLE_HORIZONTAL);

        y.setTitle("Loading data...");

        return y;
    }

    public void downloadData() {
        setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
        downloadingProgress = initLoadingDialog();
        downloadingProgress.setTitle("Downloading data...");
        downloadingProgress.show();
        this.dm.setDelegate(this);
        this.dm.init();
    }


    @Override
    public void downloadingDidProgress(String msg) {
        downloadingProgress.incrementProgressBy(1);
        downloadingProgress.setTitle(msg);
    }

    @Override
    public void downloadingDidComplete() {


        downloadingProgress.setTitle("Done!");
        (new Timer()).schedule(new TimerTask() {
            @Override
            public void run() {

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        if (downloadingProgress != null && downloadingProgress.isShowing()) {
                            downloadingProgress.dismiss();
                        }

                        processingProgress = initLoadingDialog();
                        processingProgress.setProgress(0);
                        processingProgress.setMax(dm.processData());
                        processingProgress.show();
                    }
                });
            }
        }, 1000);
    }

    @Override
    public void processingDidProgress( final String msg ) {
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                processingProgress.incrementProgressBy(1);
                processingProgress.setTitle(msg);
            }
        });
    }

    @Override
    public void processingDidComplete() {

        runOnUiThread(new Runnable() {
            @Override
            public void run() {

                processingProgress.setTitle("Done!");
                (new Timer()).schedule(new TimerTask() {
                    @Override
                    public void run() {

                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                processingProgress.dismiss();
                                DataManager.sharedManager().sortItemsByManufacturer();
                                update();
                            }
                        });
                    }
                }, 1000);
            }
        });
    }

    @Override
    public void failure(int code, String reason){
        Log.d(TAG, "DataManager failure: " + code + " " + reason);
    }

    //
    // after login, show data
    //

    @Override
    public void pause() {
        super.pause();

        if (downloadingProgress != null && downloadingProgress.isShowing()) {
            downloadingProgress.dismiss();
        }
        downloadingProgress = null;
    }
    @Override
    public void update() {
        super.update();

        if (this.dm.downloadComplete()) {
            FragmentManager fm = getFragmentManager();
            FragmentTransaction ft = fm.beginTransaction();
            if (this.mode == Mode.Locations) {
                LocationListFragment frag = LocationListFragment.newInstance();
                ft.replace(R.id.fragment, frag);
            } else if (this.mode == Mode.Items) {
                ItemListFragment frag = ItemListFragment.newInstance();
                ft.replace(R.id.fragment, frag);
            } else if (this.mode == Mode.Users) {
                UserListFragment frag = UserListFragment.newInstance();
                ft.replace(R.id.fragment, frag);
            } else if (this.mode == Mode.Assets) {
                AssetListFragment frag = AssetListFragment.newInstance();
                ft.replace(R.id.fragment, frag);
            } else if (this.mode == Mode.Invs) {
                InvListFragment frag = InvListFragment.newInstance();
                ft.replace(R.id.fragment, frag);
            }
            ft.commit();
        }
    }

    @Override
    public void didSelectItem(Item item) {
        // display item info
        Intent i = new Intent(this,ItemInfoActivity.class);
        i.putExtra("Item", item.getId());
        this.startActivity(i);
    }

    @Override
    public void didSelectLocation(Location loc) {
        Intent i = new Intent(MainActivity.this, LocationInfoActivity.class);
        i.putExtra("Location",loc.getId());
        this.startActivity(i);
    }

    @Override
    public void didSelectUser(User u) {
        Intent i = new Intent(MainActivity.this, UserInfoActivity.class);
        i.putExtra("User", u.getUid());
        this.startActivity(i);
    }

    @Override
    public void didSelectAsset(Asset item) {
        Intent i = new Intent(MainActivity.this, AssetInfoActivity.class);
        i.putExtra("Asset",item.tag_ece);
        this.startActivity(i);
    }


    @Override
    public void didSelectInv(Inventory inv) {
        Intent i = new Intent(MainActivity.this, InvInfoActivity.class);
        i.putExtra("Inv", inv.getId());
        this.startActivity(i);
    }
}
