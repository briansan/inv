package edu.villanova.ece.inv2.manager;

import android.os.Handler;
import android.os.Looper;
import android.util.Base64;
import android.util.Log;

import com.breadtech.util.HttpTask;
import com.breadtech.util.HttpTask.HttpResponder;
import com.google.gson.Gson;

import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.ProtocolException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;


import org.apache.http.conn.ssl.AllowAllHostnameVerifier;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import javax.net.ssl.HttpsURLConnection;

import edu.villanova.ece.inv2.model.Asset;
import edu.villanova.ece.inv2.model.Inventory;
import edu.villanova.ece.inv2.model.Item;
import edu.villanova.ece.inv2.model.Label;
import edu.villanova.ece.inv2.model.Location;
import edu.villanova.ece.inv2.model.Token;
import edu.villanova.ece.inv2.model.User;

/**
 * Created by bk on 7/27/15.
 */
public class ApiManager {

    // constants
    private static final String API_URL = "https://inv.breadtech.com/api/v1/";
    private static final String USER_URL = API_URL + "user";
    private static final String SELF_URL = USER_URL + "/me";
    private static final String ITEM_URL = API_URL + "item";
    private static final String CATEGORY_URL = ITEM_URL + "/category";
    private static final String MANUFACTURER_URL = ITEM_URL + "/manufacturer";
    private static final String LOCATION_URL = API_URL + "location";
    private static final String BUILDING_URL = LOCATION_URL + "/building";
    private static final String ASSET_URL = API_URL + "asset";
    private static final String INV_URL = API_URL + "inv";
    private static final String TAG = "ApiManager";

    // api convenience methods
    private static String user_url( String id ) { return USER_URL+'/'+id; }
    private static String item_url( int id ) { return ITEM_URL+'/'+id; }
    private static String location_url( int id ) { return LOCATION_URL+'/'+id; }
    private static String asset_url( String id ) { return ASSET_URL+'/'+id; }
    private static String inv_url( int id ) { return INV_URL+'/'+id; }

    // convenience method to return the right url for the given class
    public static String mkurl( Class type ) {
        return mkurl(type, 0);
    }

    public static String mkurl( Class type, int id ) {
        String url = API_URL;
        if      (type == User.class)      url = id>0 ? user_url("")     : USER_URL;
        else if (type == Item.class)      url = id>0 ? item_url(id)     : ITEM_URL;
        else if (type == Location.class)  url = id>0 ? location_url(id) : LOCATION_URL;
        else if (type == Asset.class)     url = id>0 ? asset_url("")    : ASSET_URL;
        else if (type == Inventory.class) url = id>0 ? inv_url(id)      : INV_URL;
        else if (type == Label.ItemCategory.class) url = CATEGORY_URL;
        else if (type == Label.ItemManufacturer.class) url = MANUFACTURER_URL;
        else if (type == Label.LocationBuilding.class) url = BUILDING_URL;
        return url;
    }
    public static String mkurl( Class type, String id ) {
        String url = API_URL;
        if      (type == User.class)      url = id.equals("") ? USER_URL : user_url(id);
        else if (type == Asset.class)     url = id.equals("") ? ASSET_URL : asset_url(id);
        return url;
    }

    // convenience method to construct an api request
    private static HttpURLConnection makeUrlConnection( String url_s, String uname, String passwd ) {
        HttpURLConnection conn = null;
        try {
            URL url = new URL(url_s);
            conn = (HttpURLConnection) url.openConnection();
            if (conn.getClass() == HttpsURLConnection.class) {
                HttpsURLConnection sconn = (HttpsURLConnection)conn;
            }
            String authInfo = new String(Base64.encode((uname + ':' + passwd).getBytes(), Base64.NO_WRAP));
            String basicAuth = "Basic "+authInfo;
            conn.setRequestProperty("Authorization", basicAuth);
        }
        catch (Exception e) {
            e.printStackTrace();
        }
        return conn;
    }

    private static HttpURLConnection makeUrlConnection( String url_s, String token ) {
        return makeUrlConnection(url_s, token, "");
    }

    // convenience method to convert object to json


    public static String obj2urlencode( Object obj ) {
        String y = "";
        String json_str = new Gson().toJson(obj);
        try {
            JSONObject jsonobj = new JSONObject(json_str);
            Iterator<String> it = jsonobj.keys();
            do {
                String key = it.next();
                y += key+'='+jsonobj.getString(key);
                if (it.hasNext()) y += '&';
            } while(it.hasNext());
        } catch (JSONException e) {
            e.printStackTrace();
        }
        return y;
    }

    // handling token based authentication
    public static void getToken( String uname, String passwd, int expire, final TokenDelegate delegate) {
        // construct the http connection
        String query = "expire="+expire;
        HttpURLConnection conn = makeUrlConnection(API_URL, uname, passwd);
        HttpResponder responder = new HttpResponder() {
            @Override
            public void success() {
                // convert the json to token
                Log.d(TAG,body);
                Token t = new Gson().fromJson(body, Token.class);
                // tell the delegate that we got the token
                delegate.gotToken(t.getToken());
            }

            @Override
            public void failure()
            {
                delegate.getTokenFailed(code,body);
            }
        };

        // execute the http connection
        new HttpTask(conn,responder,query).execute((Void) null);
    }

    public static void getToken( String token, int expire, final TokenDelegate delegate) {
        getToken(token, "", expire, delegate);
    }

    // user information
    public static void getUser( String token, final GetMethodDelegate delegate ) {
        // construct the http connection
        HttpURLConnection conn = makeUrlConnection(SELF_URL, token);
        HttpResponder responder = new HttpResponder() {
            @Override
            public void success() {
                final User user = new Gson().fromJson(body, User.class);
                // alert the delegate that login is successful
                delegate.gotEntity(user);
            }

            @Override
            public void failure() {
                delegate.getEntityFailed(code,body);
            }
        };
        // execute the http connection
        new HttpTask(conn,responder).execute((Void) null);
    }


    // generic method to make api requests
    public static void getEntity( final Class type, int id, String token, final GetMethodDelegate delegate ) {
        // determine the correct url to use
        String url = mkurl(type, id);
        HttpURLConnection conn = makeUrlConnection( url, token );

        // construct the http connection
        HttpResponder responder = new HttpResponder() {
            @Override
            public void success() {
                Object obj = new Gson().fromJson(body, type);
                // alert the delegate that login is successful
                delegate.gotEntity(obj);
            }

            @Override
            public void failure() {
                delegate.getEntityFailed(code,body);
            }
        };

        // execute the http connection
        new HttpTask(conn,responder).execute((Void) null);
    }

    public static void getEntityAll( final Class type, String token, final GetAllMethodDelegate delegate ) {
        // determine the correct url to use
        String url = mkurl(type);
        HttpURLConnection conn = makeUrlConnection( url, token );

        // construct the http connection
        HttpResponder responder = new HttpResponder() {
            @Override
            public void success() {
                ArrayList list = new ArrayList();
                try {
                    // convert the body into the json array
                    JSONArray array = new JSONArray(body);
                    int n = array.length();
                    if (n==0) {
                        delegate.gotEntityAll(type,new ArrayList());
                        return;
                    }
                    // break down the json array and convert to a list of java objects
                    for (int i = 0; i < n; i++) {
                        JSONObject obj = array.getJSONObject(i);
                        list.add( new Gson().fromJson(obj.toString(),type));
                    }
                    // alert the delegate that the entities have been fetched
                    delegate.gotEntityAll(type,list);
                }
                catch (Exception e) {
                    e.printStackTrace();
                    delegate.getEntityFailed(code,"Bad JSON");
                }
            }

            @Override
            public void failure() {
                delegate.getEntityFailed(code,body);
            }
        };

        // execute the http connection
        new HttpTask(conn,responder).execute((Void) null);
    }

    // generic method to make api requests (for items, locations, and invs)
    public static void setEntity( final Class type, int id, Object obj, String token, final SetMethodDelegate delegate ) {
        // determine the correct url to use
        String url = mkurl(type, id);
        HttpURLConnection conn = makeUrlConnection( url, token );
        try {
            // customize the url for doing an update
            conn.setRequestMethod("PUT");
        }
        catch (ProtocolException e) {
            e.printStackTrace();

        }

        // construct the http connection
        HttpResponder responder = new HttpResponder() {
            @Override
            public void success() {
                Object obj = new Gson().fromJson(body, type);
                // alert the delegate that login is successful
                delegate.setEntitySuccess(obj);
            }

            @Override
            public void failure() {
                delegate.setEntityFailure(code,body);
            }
        };

        String query = obj2urlencode(obj);
        // execute the http connection
        new HttpTask(conn,responder,query).execute((Void) null);
    }

    // generic method to make api requests (for users and assets)
    public static void setEntity( final Class type, String id, Object obj, String token, final SetMethodDelegate delegate ) {
        // determine the correct url to use
        String url = mkurl(type, id);
        HttpURLConnection conn = makeUrlConnection( url, token );
        try {
            // customize the url for doing an update
            conn.setRequestMethod("PUT");
        }
        catch (ProtocolException e) {
            e.printStackTrace();

        }

        // construct the http connection
        HttpResponder responder = new HttpResponder() {
            @Override
            public void success() {
                Object obj = new Gson().fromJson(body, type);
                // alert the delegate that login is successful
                delegate.setEntitySuccess(obj);
            }

            @Override
            public void failure() {
                delegate.setEntityFailure(code,body);
            }
        };

        String query = obj2urlencode(obj);
        // execute the http connection
        new HttpTask(conn,responder,query).execute((Void) null);
    }

    // generic method to make api requests
    public static void addEntity( final Class type, Object obj, String token, final AddMethodDelegate delegate ) {
        // determine the correct url to use
        String url = mkurl(type);
        HttpURLConnection conn = makeUrlConnection( url, token );

        // construct the http connection
        HttpResponder responder = new HttpResponder() {
            @Override
            public void success() {
                Object obj = new Gson().fromJson(body, type);
                // alert the delegate that login is successful
                delegate.addEntitySuccess(obj);
            }

            @Override
            public void failure() {
                delegate.addEntityFailure(code, body);
            }
        };

        String query = obj2urlencode(obj);
        // execute the http connection
        new HttpTask(conn,responder,query).execute((Void) null);
    }

    // generic method to make api requests
    public static void deleteEntity( final Class type, int id, String token, final RemoveMethodDelegate delegate ) {
        // determine the correct url to use
        String url = mkurl(type, id);
        HttpURLConnection conn = makeUrlConnection( url, token );
        try {
            // customize the url for doing an update
            conn.setRequestMethod("DELETE");
        }
        catch (ProtocolException e) {
            e.printStackTrace();
        }

        // construct the http connection
        HttpResponder responder = new HttpResponder() {
            @Override
            public void success() {
                // alert the delegate that login is successful
                delegate.removeEntitySuccess(body);
            }

            @Override
            public void failure() {
                delegate.removeEntityFailure(code,body);
            }
        };

        // execute the http connection
        new HttpTask(conn,responder).execute((Void) null);
    }

    // generic method to make api requests
    public static void deleteEntity( final Class type, String id, String token, final RemoveMethodDelegate delegate ) {
        // determine the correct url to use
        String url = mkurl(type, id);
        HttpURLConnection conn = makeUrlConnection( url, token );
        try {
            // customize the url for doing an update
            conn.setRequestMethod("DELETE");
        }
        catch (ProtocolException e) {
            e.printStackTrace();
        }

        // construct the http connection
        HttpResponder responder = new HttpResponder() {
            @Override
            public void success() {
                // alert the delegate that login is successful
                delegate.removeEntitySuccess(body);
            }

            @Override
            public void failure() {
                delegate.removeEntityFailure(code,body);
            }
        };

        // execute the http connection
        new HttpTask(conn,responder).execute((Void) null);
    }

    // inner class definition of delegate response to method calls
    public interface TokenDelegate {
        public void gotToken(String t);
        public void getTokenFailed(int code, String reason);
    }

    public interface GetMethodDelegate {
        public void gotEntity(Object obj);
        public void getEntityFailed(int code, String info);
    }

    public interface GetAllMethodDelegate {
        public void gotEntityAll(Class type, ArrayList obj);
        public void getEntityFailed(int code, String info);
    }
    public interface SetMethodDelegate {
        public void setEntitySuccess(Object item);

        public void setEntityFailure(int code, String reason);
    }
    public interface AddMethodDelegate {
        public void addEntitySuccess(Object item);

        public void addEntityFailure(int code, String reason);
    }
    public interface RemoveMethodDelegate {
        public void removeEntitySuccess(String msg);
        public void removeEntityFailure(int code, String reason);
    }
}
