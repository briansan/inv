package com.breadtech.util;

import android.os.AsyncTask;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.util.Map;

/**
 * Created by bk on 7/27/15.
 */

// inner class definition of async http task
public class HttpTask extends AsyncTask<Void, Void, Boolean> {

    public static abstract class HttpResponder {
        public int code;
        public Map headers;
        public String body;
        public abstract void success();
        public abstract void failure();
        public void response(final int code, Map headers, String body) {
            this.code = code;
            this.headers = headers;
            this.body = body;
            // post the http response onto the main thread
            new Handler(Looper.getMainLooper()).post(new Runnable() {
                @Override
                public void run() {
                    if (code >= 200 && code < 300) {
                        success();
                    } else {
                        failure();
                    }
                }
            });
        }
    }

    private HttpURLConnection conn;
    private HttpResponder responder;
    private String postdata;
    private static final String TAG = "HttpTask";

    public HttpTask(HttpURLConnection conn, HttpResponder responder) {
        this.conn = conn;
        this.responder = responder;
    }

    public HttpTask(HttpURLConnection conn, HttpResponder responder, String postdata) {
        this.conn = conn;
        this.responder = responder;
        this.postdata = postdata;
    }

    @Override
    protected Boolean doInBackground(Void... params) {

        Log.d(TAG, conn.getURL().toString() );
        if (postdata != null) {
            try {
                conn.setDoOutput(true);
                conn.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
                // set the form data
                OutputStream output = conn.getOutputStream();
                output.write(postdata.getBytes());
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        // get response data input stream
        BufferedReader br;
        try {
            // set up the objs to construct the response body
            br = new BufferedReader(new InputStreamReader(this.conn.getInputStream()));
        }
        catch (FileNotFoundException e) {
            br = new BufferedReader(new InputStreamReader(this.conn.getErrorStream()));
        }
        catch (Exception e) {
            e.printStackTrace();
            return false;
        }

        // read in input stream
        try {
            StringBuilder sb = new StringBuilder();
            String line;
            while((line = br.readLine()) != null) {
                sb.append(line+"\n");
            }
            br.close();
            String resp = sb.toString();

            // call the response listener to send the response data
            this.responder.response( this.conn.getResponseCode(), this.conn.getHeaderFields(), resp);
            this.conn.disconnect();
        }
        catch (Exception e) {
            e.printStackTrace();
            return false;
        }

        return true;
    }
}
