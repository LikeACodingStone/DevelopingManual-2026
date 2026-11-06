package com.example.handbook;

import android.app.Service;
import android.content.Intent;
import android.os.IBinder;
import android.os.RemoteCallbackList;
import android.os.RemoteException;

/**
 * Bound service exposing IGreeter. Status: syntax and structure sketch, NOT built here
 * (no JDK / Android SDK). Binder calls arrive on Binder threads, not the main thread.
 */
public class GreeterService extends Service {
    // Removes listeners whose process died; plain List<IGreeterListener> would keep dead proxies.
    private final RemoteCallbackList<IGreeterListener> listeners = new RemoteCallbackList<>();

    private final IGreeter.Stub binder = new IGreeter.Stub() {
        @Override
        public Greeting greet(String name) {
            Greeting greeting = new Greeting();
            greeting.text = "Hello, " + (name == null ? "" : name);
            greeting.count = 1;
            broadcast(greeting);
            return greeting;
        }

        @Override
        public void register(IGreeterListener listener) {
            listeners.register(listener);
        }

        @Override
        public void unregister(IGreeterListener listener) {
            listeners.unregister(listener);
        }

        @Override
        public void ping() {
            // oneway: nothing is returned to the caller
        }
    };

    private void broadcast(Greeting greeting) {
        int count = listeners.beginBroadcast();
        try {
            for (int i = 0; i < count; i++) {
                try {
                    listeners.getBroadcastItem(i).onGreeting(greeting);
                } catch (RemoteException ignored) {
                    // the listener's process is gone; RemoteCallbackList removes it
                }
            }
        } finally {
            listeners.finishBroadcast();
        }
    }

    @Override
    public IBinder onBind(Intent intent) {
        return binder;
    }

    @Override
    public void onDestroy() {
        listeners.kill();
        super.onDestroy();
    }
}
