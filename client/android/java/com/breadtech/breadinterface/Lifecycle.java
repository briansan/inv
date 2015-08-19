package com.breadtech.breadinterface;

/**
 * Created by bk on 12/12/14.
 */
public interface Lifecycle {
    public void init();
    public void start();
    public void resume();
    public void update();
    public void clear();
    public void pause();
    public void stop();
    public void cleanup();
}
