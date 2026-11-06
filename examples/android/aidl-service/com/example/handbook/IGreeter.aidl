package com.example.handbook;

import com.example.handbook.Greeting;
import com.example.handbook.IGreeterListener;

interface IGreeter {
    // Synchronous: the calling thread blocks until the service replies.
    Greeting greet(in String name);

    void register(in IGreeterListener listener);
    void unregister(in IGreeterListener listener);

    oneway void ping();
}
