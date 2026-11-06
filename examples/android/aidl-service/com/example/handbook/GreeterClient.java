package com.example.handbook;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.IBinder;
import android.os.RemoteException;

/**
 * Client side. Status: syntax and structure sketch, NOT built here (no JDK / Android SDK).
 * Ordinary apps bind with bindService(); platform code that uses ServiceManager is a
 * different, non-public path.
 */
public final class GreeterClient implements ServiceConnection, IBinder.DeathRecipient {
    private volatile IGreeter service;

    public void connect(Context context) {
        context.bindService(new Intent(context, GreeterService.class), this, Context.BIND_AUTO_CREATE);
    }

    public void disconnect(Context context) {
        context.unbindService(this);
        service = null;
    }

    @Override
    public void onServiceConnected(ComponentName name, IBinder binder) {
        service = IGreeter.Stub.asInterface(binder);
        try {
            binder.linkToDeath(this, 0);
        } catch (RemoteException e) {
            service = null; // the process died before we could watch it
        }
    }

    @Override
    public void onServiceDisconnected(ComponentName name) {
        service = null; // the binding survives; Android reconnects when the service restarts
    }

    @Override
    public void binderDied() {
        service = null;
    }

    /** Call from a worker thread: greet() blocks for the whole round trip. */
    public String greetBlocking(String name) throws RemoteException {
        IGreeter current = service;
        if (current == null) {
            throw new IllegalStateException("not connected");
        }
        return current.greet(name).text;
    }
}
