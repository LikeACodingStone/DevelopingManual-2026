package com.example.handbook;

import com.example.handbook.Greeting;

// oneway: the caller does not wait. Delivery order is preserved per binder, but a slow
// receiver can still back up the service's outgoing transactions.
oneway interface IGreeterListener {
    void onGreeting(in Greeting greeting);
}
