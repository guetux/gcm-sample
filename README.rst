Google Cloud Message Sample
===========================

This is a simple port of the GCM example project from ant to gradle building.

Thanks to gradle, running the example is about 200 times more fun at least!

`Check out more about GCM and the sample project here
<http://developer.android.com/google/gcm/demo.html>`_

Usage
-----

**IMPORTANT**: You need to use gradle 1.2 and android sdk r21 in order for this
project to work!

To start the server, put your simple api key into
``gcm-demo-server/src/main/resources/api.key`` and do:

::

    $ gradle jettyRun


To run the client, put your key and sender into
``gcm-demo-client/src/.../CommonUtilities.java`` and hit:

::

    $ grade installDebug
    $ adb logcat

Open the app and start experimenting!
