Eclipse Orchestrator Scripting
===============================

This is a simple python script that makes generating a CSV file to be loaded
into Eclipse Orchestrator (EO) program by
[Moonglow Technologies](http://www.moonglowtechnologies.com/products/EclipseOrchestrator/index.shtml).

Basic features
^^^^^^^^^^^^^^

Once instanciates a `Script` object and assigns settings, each time an capture is commaned the current settings are
used.  Settings are only changed when one assigns a new value and captures an image.  Here's a basic example:

```python
    from eoscript import Exposure, Script

    min_time_step = 0.300

    script = Script()

    script.camera = "Nikon Z7"
    script.fstop = 8
    script.iso = 64
    script.exposure = Exposure(1) / 500

    script.banner("Capture a bunch of photos just before C2.")
    script.comment = "diamond ring & baily's beads"
    script.phase = "C2"
    script.offset = -13.0
    script.min_time_step = min_time_step
    script.send_exposure()
    script.offset += 3
    for _ in range(36):
        script.capture()

    script.save("eclipse2024.csv")
```

If you saved the above in `eclipse2024.py`, then you can "render" the script by running it:

    python eclipse2024.py
    Wrote eclipse2024.csv

You can now examine the results:

    #Action,Date/Ref,Offset sign,Time (offset),Camera,Exposure,Aperture,ISO,MLU,Quality,Size,Incremental,Comment
    #------------------------------------------------------------------------------------------------------------------------
    # Capture a bunch of photos just before C2.
    #------------------------------------------------------------------------------------------------------------------------
    SETEXP,C2,-,00:00:13.000,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,N,sending all camera exposure settings via USB
    TAKEPIC,C2,-,00:00:10.000,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,diamond ring & baily's beads
    TAKEPIC,C2,-,00:00:09.698,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,diamond ring & baily's beads
    TAKEPIC,C2,-,00:00:09.396,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,diamond ring & baily's beads
    ...
    TAKEPIC,C2,-,00:00:00.034,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,diamond ring & baily's beads
    TAKEPIC,C2,+,00:00:00.268,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,diamond ring & baily's beads
    TAKEPIC,C2,+,00:00:00.570,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,diamond ring & baily's beads

So 13 seconds before C2, we send our camera settings over USB, then at -10 seconds to C2, we start taking photos as fast
as possible  using `incremental` set to `Y`.  This will avoid updating the camera exposure settings over USB since
nothing has changed.  This is the fastest way to capture images with Eclipse Orchestrator that I've found.  See
`How to capture fast` below for more information about how to determine your fastest settings.

Taking brackets
^^^^^^^^^^^^^^^

During totality, we'll want to take a bunch of bracketed shots so we can later post process the images to produce a
final, detailed image of totality.  It's also less time critical, so we should update `min_time_step` such that updating
settings via USB before each exposure is reliable for you setup. In our script, update the camera settigs, the phase and
offset, then capture brackets:

```python
    script.banner("Totality")
    script.comment = "totality"
    script.phase = "MAX"
    script.offset = -14.0
    script.min_time_step = 1.0
    script.exposure = Exposure(1) / 15
    script.capture_bracket(19, ev_step=2/3.0)
```

which will produce this output in the rendered file, 28 seconds to capture 12 stops of dynamic range:

    #------------------------------------------------------------------------------------------------------------------------
    # Totality
    #------------------------------------------------------------------------------------------------------------------------
    TAKEPIC,MAX,-,00:00:14.000,Nikon Z7,1/1000, 8.0,  64,0.0,RAW+F-JPG,None,N,totality  -6.000 EV Stops
    TAKEPIC,MAX,-,00:00:12.999,Nikon Z7,1/640 , 8.0,  64,0.0,RAW+F-JPG,None,Y,totality  -5.333 EV Stops
    ...
    TAKEPIC,MAX,-,00:00:04.888,Nikon Z7,1/15  , 8.0,  64,0.0,RAW+F-JPG,None,Y,totality  +0.000 EV Stops
    ...
    TAKEPIC,MAX,+,00:00:07.574,Nikon Z7,2.5   , 8.0,  64,0.0,RAW+F-JPG,None,Y,totality  +5.333 EV Stops
    TAKEPIC,MAX,+,00:00:11.262,Nikon Z7,4     , 8.0,  64,0.0,RAW+F-JPG,None,Y,totality  +6.000 EV Stops

Brackets are always centered in expouse around the current camera settings when calling `capture_bracket()`.  Note
that the `Exposure` class rounds to the nearest 1/3 stop, and will not shoot faster than `1/8000` or longer than `30` as
is typical for digital cameras.

Capturing partials
^^^^^^^^^^^^^^^^^^

It's up to you have you want to catpure partials, I'm planning on only taking 10, single exposures at times computed by
Dr. Gordon Telepun's execellent Solar Eclipse Timer app.  To do this, we specifiy the conact times, then capture images
by specifing `HH:MM:SS`:

```python
    from eoscript import Exposure, Script

    # All times are UTC!!!
    # All times are UTC!!!
    # All times are UTC!!!
    script = Script(
        #                 UTC                Texas Local
        c1  = "2024/04/08 17:21:27.5",     # 12:21:27.5 PM
        c2  = "2024/04/08 18:38:46.6",     #  1:38:46.6 PM
        max = "2024/04/08 18:40:58.0",     #  1:40:58.0 PM
        c3  = "2024/04/08 18:43:09.4",     #  1:43:09.4 PM
        c4  = "2024/04/08 20:01:20.9",     #  3:01:20.9 PM
    )

    script.banner("C1 -> C2: partials")
    script.phase = "C1"
    script.camera = "Nikon Z7"
    script.fstop = 8
    script.iso = 800
    script.exposure = Exposure(1) / 400
    script.comment = "C1 -> C2 partials"

    # All times are UTC!!!
    # All times are UTC!!!
    # All times are UTC!!!
    script.capture("17:23:27")
    script.capture("17:31:35")
    script.capture("17:39:43")
    script.capture("17:47:51")
    script.capture("17:55:59")
    script.capture("18:04:07")
    script.capture("18:12:15")
    script.capture("18:20:23")
    script.capture("18:28:31")
    script.capture("18:36:46")

    script.save("eclipse2024.csv")
```

The above produces this output file:

    # Keep these commented out to use the computed contact times of the computer.
    # Add a GPS receiver to get < 1s accurate computed contact times.
    # Event, Date, Time
    # C1,  2024/04/08,17:21:27.500000
    # C2,  2024/04/08,18:38:46.600000
    # MAX, 2024/04/08,18:40:58.000000
    # C3,  2024/04/08,18:43:09.400000
    # C4,  2024/04/08,20:01:20.900000
    #
    # C1:C2  duration: 01:17:19.100
    # C2:MAX duration: 00:02:11.400
    # MAX:C3 duration: 00:02:11.400
    # C3:4   duration: 01:18:11.500
    #
    #Action,Date/Ref,Offset sign,Time (offset),Camera,Exposure,Aperture,ISO,MLU,Quality,Size,Incremental,Comment
    #------------------------------------------------------------------------------------------------------------------------
    # C1 -> C2: partials
    #------------------------------------------------------------------------------------------------------------------------
    TAKEPIC,C1,+,00:01:59.500,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C1 -> C2 partials
    TAKEPIC,C1,+,00:10:07.500,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C1 -> C2 partials
    TAKEPIC,C1,+,00:18:15.500,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C1 -> C2 partials
    TAKEPIC,C1,+,00:26:23.500,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C1 -> C2 partials
    TAKEPIC,C1,+,00:34:31.500,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C1 -> C2 partials
    TAKEPIC,C1,+,00:42:39.500,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C1 -> C2 partials
    TAKEPIC,C1,+,00:50:47.500,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C1 -> C2 partials
    TAKEPIC,C1,+,00:58:55.500,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C1 -> C2 partials
    TAKEPIC,C1,+,01:07:03.500,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C1 -> C2 partials
    TAKEPIC,C1,+,01:15:18.500,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C1 -> C2 partials

Note the contact times are now included in comments, and also note the durations between the contact times:

    # C1:C2  duration: 01:17:19.100
    # C2:MAX duration: 00:02:11.400
    # MAX:C3 duration: 00:02:11.400
    # C3:4   duration: 01:18:11.500

This will help you iterate on the script to know if your offsets may be overlapping.  Currently this tool does not
detect if you have overlapping exposures, as you can use Eclipse Orchestrator itself to visualize your exposures.  If
you have a multiple camera setup, it will be harder to add such error checking.

How to caputre fast
===================

Sending camera settings via USB is actually slow, as most manufacturors have not optimized this.  Using only USB I was
only able to trigger my Nikon Z7 every 0.80 seconds to reliably capture images.  Adding a serial cable to the setup, I'm
now reilably able to trigger my Nikon Z7 ever0.30 seconds.

You will need to acquire or build a serial cable to trigger your camera. Typically this includes:

1. A USB to DB9 male serial cable using the FTDI chipset
2. A DB9 femail to custom camera shutter release adapter (lots of online astro folks build and sell these online).
3. Camera shutter release cable

Once you have your USB and Serial cable on hand, you can start to tweak the settings in Eclipse Orchestrator.  Under the
hardware settings, you can identify which COM port you've connected the serial cable, and then adjust settings.  The
biggest setting is how long to hold the shutter singal for.  Modern fast cameras can probably get away with 50ms. Note
the default in Eclipse Orchestrator is 150ms.

Next, we tune settings, capture 60 frames as fast as possible for C2, then verify the camera actually captured the
expected photos.

Eclipse Orchestrator can simulate a C2 contact, which starts about -40 seconds, so this is my script for finding the
fastest settings:

```python

    from eoscript import Exposure, Script
    script = Script(
        #                 UTC                Texas Local
        c1  = "2024/04/08 17:21:27.5",     # 12:21:27.5 PM
        c2  = "2024/04/08 18:38:46.6",     #  1:38:46.6 PM
        max = "2024/04/08 18:40:58.0",     #  1:40:58.0 PM
        c3  = "2024/04/08 18:43:09.4",     #  1:43:09.4 PM
        c4  = "2024/04/08 20:01:20.9",     #  3:01:20.9 PM
    )

    script.banner("C2: Diamond Ring & Baily's Beads")
    script.comment = "diamond ring, fast burst"
    script.phase = "C2"
    script.iso = 500 # 64
    script.exposure = _1 / 500
    script.min_time_step = 0.300

    script.offset = -37.0
    script.send_exposure()
    script.offset += 3.0

    for _ in range(60):
        script.capture()
```

The procedure is to:

1. Exit Eclipse Orchestrator
2. Format your memory card with your camera
3. Plug in your camera via USB, wait for serical cable to stop triggering (every time the USB is connected, the trigger is fired 5-6 shots)
4. Plug in your serial cable
5. Open Eclipse Orchestrator
6. Execute a simulated C2 Contact
7. Obeserver the images being captured
8. On completion, exit Eclipse Orchestrator
9. Turn off your camera and pop the memory card out
10. Insert yoru memory card into a card reader
11. Scan the photos with `scan_photos.py`

Verify:
* The number of image captured.
* The captured images have the corret ISO and shutter speeds.

For example, when I run `scan_photos.py`:

    python scan_photos.py d:\DCIM\102NZ7__\
    Filename                        , Offset       , Campera, Exposure, Fstop, ISO, Quality
    d:\DCIM\102NZ7__\_NIK5179.NEF   , +,00:00:00.000, NIKON Z 7, 1/500 , 8   ,  64 , RAW
    d:\DCIM\102NZ7__\_NIK5180.NEF   , +,00:00:00.930, NIKON Z 7, 1/500 , 8   ,  64 , RAW
    d:\DCIM\102NZ7__\_NIK5181.NEF   , +,00:00:00.030, NIKON Z 7, 1/500 , 8   ,  64 , RAW
    ...
    d:\DCIM\102NZ7__\_NIK5236.NEF   , +,00:00:00.930, NIKON Z 7, 1/500 , 8   ,  64 , RAW
    d:\DCIM\102NZ7__\_NIK5237.NEF   , +,00:00:00.030, NIKON Z 7, 1/500 , 8   ,  64 , RAW
    d:\DCIM\102NZ7__\_NIK5238.NEF   , +,00:00:00.031, NIKON Z 7, 1/500 , 8   ,  64 , RAW
    60 files

If you're missing photos, you'll have to increase `min_time_stop` so the camera has more time between exposures.

GPS
====
Any standard Serial or USB based GPS dongle should work. If using a serial port GPS, FTDI based devices have a better
track record with EO than prolific ones.

The dongle that was found to work with EO can be purchased from Amazon here: https://a.co/d/25HXdal

It is recommended that the ublox u-center app is installed on windows and the GPS dongle is set to emit
only GP* NMEA strings. EO only understands GPS satellite strings and can't parse GLONASS or BeiDou satellite NMEA strings.
Check this CN thread on how to do that: https://www.cloudynights.com/topic/910898-eclipse-orchestrator-and-gps-module-help/

When using a GPS device, ensure that ther ClkErr in EO is less than .1s. This can be seen at the top of the EO interface.

Multiple cameras
================

I have not tested the use of multiple cameras.  If Eclipse Orchestrator doesn't mind if the input csv files is not in
any kind of time order, then this tool should work as is, but this isn't tested.
