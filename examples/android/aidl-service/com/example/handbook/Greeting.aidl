package com.example.handbook;

// Structured parcelable: the AIDL compiler generates the Java class (public fields).
parcelable Greeting {
    String text;
    int count;
}
