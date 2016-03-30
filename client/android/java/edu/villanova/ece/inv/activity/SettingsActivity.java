package edu.villanova.ece.inv2.activity;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import com.breadtech.breadinterface.BIActivity;

import org.apache.http.auth.AUTH;

import java.util.Date;
import java.util.Set;

import edu.villanova.ece.inv2.R;
import edu.villanova.ece.inv2.manager.ApiManager;
import edu.villanova.ece.inv2.manager.AuthManager;
import edu.villanova.ece.inv2.model.User;


public class SettingsActivity extends BIActivity {

    private SharedPreferences pref;
    private Spinner defaultListSpinner;
    private EditText keepAliveEditText;
    private TextView uidTextView, timeRemainingTextView;

    //
    // ui
    //
    @Override
    public int tl_icon() {
        return R.drawable.ic_close_white_36dp;
    }

    @Override
    public String tm_label() {
        return "Settings";
    }

    @Override
    public int tr_icon() {
        return R.drawable.ic_done_white_36dp;
    }

    //
    // functionality
    @Override
    public void tl_clicked() {
        finish();
    }

    @Override
    public void tr_clicked() {
        save();
    }

    //
    // lifecycle
    //

    @Override
    public void init() {
        super.init();

        this.setContentView(R.layout.activity_settings);
        this.pref = getSharedPreferences("inv",0);

        defaultListSpinner = (Spinner)findViewById(R.id.defaultlist_spinner);
        keepAliveEditText = (EditText)findViewById(R.id.keepalive_et);
        uidTextView = (TextView)findViewById(R.id.logininfo_tv);
        timeRemainingTextView = (TextView)findViewById(R.id.logintime_tv);

        ArrayAdapter<String> modeAdapter = new ArrayAdapter<String>(this,
                android.R.layout.simple_spinner_item,
                MainActivity.Mode.modes);
        defaultListSpinner.setAdapter(modeAdapter);

        //
        // refresh login
        findViewById(R.id.login_b).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                int expire = pref.getInt("Expire", 3600);
                ApiManager.getToken(AuthManager.getToken(), "", expire, new ApiManager.TokenDelegate() {
                    @Override
                    public void gotToken(String t) {
                        (Toast.makeText(SettingsActivity.this,
                                "Login Successfully Refreshed", Toast.LENGTH_LONG)).show();
                        SharedPreferences.Editor editor = pref.edit();
                        editor.putLong("Login", (new Date()).getTime());
                        editor.putString("Token", t);
                        editor.commit();
                        update();
                    }

                    @Override
                    public void getTokenFailed(int code, String reason) {
                        (Toast.makeText(SettingsActivity.this,
                                "Login Refresh Failed (" + code + ": " + reason + ")", Toast.LENGTH_LONG)).show();
                    }
                });
            }
        });

        //
        // view profile
        findViewById(R.id.profile_b).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(SettingsActivity.this,UserInfoActivity.class);
                i.putExtra("User", AuthManager.getUser().getUid());
                startActivity(i);
            }
        });

        //
        // logout
        findViewById(R.id.logout_b).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                new AlertDialog.Builder(SettingsActivity.this)
                        .setIcon(android.R.drawable.ic_dialog_alert)
                        .setTitle("Logout")
                        .setMessage("Are you sure that you want to log out?")
                        .setPositiveButton("Yes", new DialogInterface.OnClickListener() {
                            @Override
                            public void onClick(DialogInterface dialog, int which) {
                                // clear the static token
                                AuthManager.logout();
                                // clear the token in shared prefrences
                                SharedPreferences.Editor editor = pref.edit();
                                editor.putString("Token", "");
                                editor.commit();
                                (Toast.makeText(SettingsActivity.this,
                                        "Logged out", Toast.LENGTH_LONG)).show();
                                // pop out to the root activity
                                Intent i = new Intent(SettingsActivity.this, AuthManager.AuthActivity.class);
                                i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
                                startActivity(i);
                            }
                        })
                        .setNegativeButton("No", null)
                        .show();
            }
        });

        //
        // item category
        findViewById(R.id.ic_b).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(SettingsActivity.this,ListActivity.class);
                i.putExtra("Mode", ListActivity.Mode.ItemCategory);
                startActivity(i);
            }
        });

        //
        // item manufacturer
        findViewById(R.id.im_b).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(SettingsActivity.this,ListActivity.class);
                i.putExtra("Mode", ListActivity.Mode.ItemManufacturer);
                startActivity(i);
            }
        });

        //
        // location building
        findViewById(R.id.lb_b).setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(SettingsActivity.this,ListActivity.class);
                i.putExtra("Mode", ListActivity.Mode.LocationBuilding);
                startActivity(i);
            }
        });


    }

    @Override
    public void update() {
        super.update();

        int mode = this.pref.getInt("List", MainActivity.Mode.Assets);
        defaultListSpinner.setSelection(mode);

        int expire = this.pref.getInt("Expire", 3600);
        keepAliveEditText.setText(""+expire/60);

        User u = AuthManager.getUser();
        uidTextView.setText(u.toString());

        long logintime = this.pref.getLong("Login",0);
        long timeRemaining= logintime + expire*1000 - (new Date()).getTime();
        timeRemainingTextView.setText(""+timeRemaining/60000+" minutes");
    }

    //
    // utility methods
    //
    private void save() {
        String mode_s = (String)defaultListSpinner.getSelectedItem();
        int mode = MainActivity.Mode.modes.indexOf(mode_s);
        int expire = Integer.parseInt(keepAliveEditText.getText().toString());
        expire = expire < 1 ? 60 : expire*60;

        SharedPreferences.Editor editor = pref.edit();
        editor.putInt("List",mode);
        editor.putInt("Expire",expire);
        editor.commit();

        (Toast.makeText(SettingsActivity.this,
                "Settings saved", Toast.LENGTH_LONG)).show();
        finish();
    }
}