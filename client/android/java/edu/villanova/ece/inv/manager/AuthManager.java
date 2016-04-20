package edu.villanova.ece.inv.manager;

import android.app.Activity;
import android.app.Dialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import org.apache.http.auth.AUTH;

import java.util.Date;
import java.util.Timer;
import java.util.TimerTask;

import edu.villanova.ece.inv.R;
import edu.villanova.ece.inv.activity.MainActivity;
import edu.villanova.ece.inv.model.User;

/**
 * Created by bk on 8/11/15.
 */
public class AuthManager
{

    public static final int AUTH_OK = 1024;
    public static final String TAG = "AuthManager";

    public static String getToken() {return _token;}
    public static User getUser() {return _user;}
    public static void logout() {
        _token = "";
    }

    private static String _token;
    private static User _user;


    public static class AuthActivity extends Activity implements ApiManager.GetMethodDelegate, ApiManager.TokenDelegate {
        // constants
        public static final String PREFS_NAME = "inv";

        // instance variables
        private Dialog loginDialog;
        private DataManager dm;

        //
        // login
        //

        public void refreshToken() {
            login(_token, "");
        }

        public void login(String uname, String passwd) {
            SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
            int expire = settings.getInt("Expire",3600);
            ApiManager.getToken(uname, passwd, expire, this);
        }


        private String retreiveToken() {
            SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
            _token = settings.getString("Token", "");
            return _token;
        }

        private void storeToken(String token) {
            _token = token;
            // store the token in shared prefrences
            SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
            SharedPreferences.Editor editor = settings.edit();
            editor.putString("Token", _token);
            editor.commit();
        }

        @Override
        public void onResume() {
            super.onResume();
            checkAuth();
        }

        private void checkAuth() {
            // get the token
            retreiveToken();

            // see if there is a token in the shared prefs
            // no token, require auth
            if (_token.length() == 0) {
                displayLogin();
            } else {
                checkToken();
            }
        }

        public void checkToken() {refreshToken();}

        @Override
        public void getTokenFailed(int code, String reason) {
            Log.d(TAG, "token failed " + code + reason);
            if (code == 401)
                tokenStale();
            else
                failure(code, reason);
        }

        public void tokenStale() {
            if (this.loginDialog != null && this.loginDialog.isShowing()) {
                this.loginDialog.setTitle("Bad Credentials");
                this.loginDialog.findViewById(R.id.login).setEnabled(true);
            } else {
                displayLogin();
            }
        }

        private void displayLogin() {
            if (loginDialog == null) loginDialog = initLoginDialog();
            loginDialog.show();
        }

        public Dialog initLoginDialog() {
            // create the dialog
            loginDialog = new Dialog(this);

            // initialize the necessities
            loginDialog.setCancelable(false);
            loginDialog.setCanceledOnTouchOutside(false);
            loginDialog.setContentView(R.layout.dialog_login);
            loginDialog.setTitle("Authentication Required");

            // set the ivars
            final EditText usernameET = (EditText)loginDialog.findViewById(R.id.uname);
            final EditText passwordET = (EditText)loginDialog.findViewById(R.id.passwd);

            // set the button click
            final Button login = (Button)loginDialog.findViewById(R.id.login);
            login.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    // get credentials
                    String uname = usernameET.getText().toString();
                    String passwd = passwordET.getText().toString();

                    // perform login async
                    login.setEnabled(false);
                    login(uname, passwd);
                    loginDialog.setTitle("Logging in...");
                }
            });

            return loginDialog;
        }

        @Override
        public void gotToken(String token) {
            storeToken(token);

            SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
            SharedPreferences.Editor editor = settings.edit();
            editor.putLong("Login", (new Date()).getTime());
            editor.commit();

            if (this.loginDialog != null && this.loginDialog.isShowing()) {
                this.loginDialog.setTitle("Success!");
                (new Timer()).schedule(new TimerTask() {
                    @Override
                    public void run() {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                loginDialog.dismiss();
                                loginDialog = null;
                            }
                        });
                    }
                }, 1000);
            }

            ApiManager.getUser(_token, AuthActivity.this);
        }

        @Override
        public void gotEntity(Object obj) {
            if (obj.getClass() == User.class) {
                _user = (User)obj;
                Intent i = new Intent(this, MainActivity.class);
                i.putExtra("Token",_token);
                startActivity(i);
            }
        }

        @Override
        public void getEntityFailed(int code, String info) {

        }

        public void failure(int code, String reason){
            Log.d(TAG, "DataManager failure: " + code + " " + reason);
        }
    }

    //
    // authorization module
    //
    public static int LabelView       = 1;
    public static int SubentityView   = 1 << 1;
    public static int EntityView      = 1 << 2;
    public static int EntityModify    = 1 << 3;
    public static int EntityModifyWorld = 1 << 4;
    public static int SubentityModify = 1 << 5;
    public static int LabelModify     = 1 << 6;
    public static int UserModifyWorld = 1 << 7;

    public static boolean checkAuth(int perm) {
        return !((_user.getPerm() & perm) == 0);
    }

    public static boolean userCanModifyEntity() {return checkAuth(EntityModify);}
    public static boolean userCanModifyEntityWorld() {return checkAuth(EntityModify);}
    public static boolean userCanModifySubentity() {return checkAuth(EntityModify);}
    public static boolean userCanModifySubentityWorld() {return checkAuth(EntityModify);}
    public static boolean userCanModifyLabel() {return checkAuth(EntityModify);}
    public static boolean userCanModifyUserWorld() {return checkAuth(EntityModify);}
}
