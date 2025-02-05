import unittest
import textwrap

from eoscript import Script, Exposure

def compare(actual, expected, debug=False):
    passes = actual == expected
    if debug and not passes:
        with open("actual.txt", "w") as fout:
            fout.write(actual)
        with open("expected.txt", "w") as fout:
            fout.write(expected)
        print("Wrote actual.txt and expected.txt")
    return passes

class TestExposure(unittest.TestCase):

    def test_basics(self):
        script = Script()
        script.comment = "test basics"
        script.camera = "Nikon Z7"
        script.fstop = 8
        script.iso = 800
        script.exposure = Exposure(1) / 400
        script.phase = "C1"
        script.capture()
        script.capture()
        script.capture()
        script.file_comment = "# testing a file comment"
        script.capture()
        script.capture()
        script.capture()

        expected = textwrap.dedent("""\
            # Action, Date/Ref, Offset sign, Time (offset), Camera, Exposure, Aperture, ISO, MLU, Quality, Size, Incremental, Comment
            TAKEPIC,C1,+,00:00:00.000,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            TAKEPIC,C1,+,00:00:03.002,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            TAKEPIC,C1,+,00:00:06.005,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            # testing a file comment
            TAKEPIC,C1,+,00:00:09.008,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            TAKEPIC,C1,+,00:00:12.010,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            TAKEPIC,C1,+,00:00:15.012,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,test basics
            """)
        assert compare(str(script), expected)

    def test_bracket(self):
        """
        Verifies we can capture brackets and comment annotations.
        """
        script = Script()
        script.camera = "Nikon Z7"
        script.fstop = 8
        script.iso = 800
        script.exposure = Exposure(1) / 400
        script.phase = "C2"
        script.offset = -15.0
        script.banner("3x bracket in 1 EV Stops")
        script.capture_bracket(3)
        script.banner("5x bracket in 1 EV Stops")
        script.capture_bracket(5)
        script.banner("7x bracket in 2/3 EV Stops")
        script.capture_bracket(7, 2.0/3.0)

        expected = textwrap.dedent("""\
            # Action, Date/Ref, Offset sign, Time (offset), Camera, Exposure, Aperture, ISO, MLU, Quality, Size, Incremental, Comment
            #------------------------------------------------------------------------------------------------------------------------
            # 3x bracket in 1 EV Stops
            #------------------------------------------------------------------------------------------------------------------------
            TAKEPIC,C2,-,00:00:15.000,Nikon Z7,1/800 , 8.0, 800,0.0,RAW+F-JPG,None,N,  -1.000 EV Stops
            TAKEPIC,C2,-,00:00:11.999,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,Y,  +0.000 EV Stops
            TAKEPIC,C2,-,00:00:08.996,Nikon Z7,1/200 , 8.0, 800,0.0,RAW+F-JPG,None,Y,  +1.000 EV Stops
            #------------------------------------------------------------------------------------------------------------------------
            # 5x bracket in 1 EV Stops
            #------------------------------------------------------------------------------------------------------------------------
            TAKEPIC,C2,-,00:00:05.991,Nikon Z7,1/1600, 8.0, 800,0.0,RAW+F-JPG,None,N,  -2.000 EV Stops
            TAKEPIC,C2,-,00:00:02.991,Nikon Z7,1/800 , 8.0, 800,0.0,RAW+F-JPG,None,Y,  -1.000 EV Stops
            TAKEPIC,C2,+,00:00:00.011,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,Y,  +0.000 EV Stops
            TAKEPIC,C2,+,00:00:03.013,Nikon Z7,1/200 , 8.0, 800,0.0,RAW+F-JPG,None,Y,  +1.000 EV Stops
            TAKEPIC,C2,+,00:00:06.018,Nikon Z7,1/100 , 8.0, 800,0.0,RAW+F-JPG,None,Y,  +2.000 EV Stops
            #------------------------------------------------------------------------------------------------------------------------
            # 7x bracket in 2/3 EV Stops
            #------------------------------------------------------------------------------------------------------------------------
            TAKEPIC,C2,+,00:00:09.028,Nikon Z7,1/1600, 8.0, 800,0.0,RAW+F-JPG,None,N,  -2.000 EV Stops
            TAKEPIC,C2,+,00:00:12.029,Nikon Z7,1/1000, 8.0, 800,0.0,RAW+F-JPG,None,Y,  -1.333 EV Stops
            TAKEPIC,C2,+,00:00:15.030,Nikon Z7,1/640 , 8.0, 800,0.0,RAW+F-JPG,None,Y,  -0.667 EV Stops
            TAKEPIC,C2,+,00:00:18.031,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,Y,  +0.000 EV Stops
            TAKEPIC,C2,+,00:00:21.034,Nikon Z7,1/250 , 8.0, 800,0.0,RAW+F-JPG,None,Y,  +0.667 EV Stops
            TAKEPIC,C2,+,00:00:24.038,Nikon Z7,1/160 , 8.0, 800,0.0,RAW+F-JPG,None,Y,  +1.333 EV Stops
            TAKEPIC,C2,+,00:00:27.044,Nikon Z7,1/100 , 8.0, 800,0.0,RAW+F-JPG,None,Y,  +2.000 EV Stops
            """)
        assert compare(str(script), expected)

    def test_long_exposure(self):
        """
        Take some long exposures.
        """
        script = Script()
        script.camera = "Nikon Z7"
        script.fstop = 8
        script.iso = 64
        script.exposure = Exposure(8)
        script.phase = "MAX"
        script.comment = "long exposure"
        script.capture()
        script.capture()
        script.capture()
        expected = textwrap.dedent("""\
            # Action, Date/Ref, Offset sign, Time (offset), Camera, Exposure, Aperture, ISO, MLU, Quality, Size, Incremental, Comment
            TAKEPIC,MAX,+,00:00:00.000,Nikon Z7,8     , 8.0,  64,0.0,RAW+F-JPG,None,N,long exposure
            TAKEPIC,MAX,+,00:00:11.000,Nikon Z7,8     , 8.0,  64,0.0,RAW+F-JPG,None,N,long exposure
            TAKEPIC,MAX,+,00:00:22.000,Nikon Z7,8     , 8.0,  64,0.0,RAW+F-JPG,None,N,long exposure
            """)
        assert compare(str(script), expected)

    def test_contact_times(self):
        """
        Setting the contact times and capturing exposrues using HH:MM:SS.
        """
        script = Script(
            #                 UTC                LOCAL TEXAS
            c1  = "2024/04/08 17:21:27.5",     # 12:21:27.5 PM
            c2  = "2024/04/08 18:38:46.6",     #  1:38:46.6 PM
            max = "2024/04/08 18:40:58.0",     #  1:40:58.0 PM
            c3  = "2024/04/08 18:43:09.4",     #  1:43:09.4 PM
            c4  = "2024/04/08 20:01:20.9",     #  3:01:20.9 PM
        )

        script.camera = "Nikon Z7"
        script.fstop = 8
        script.banner("C1 -> C2: partials")
        script.iso = 800
        script.phase = "C1"
        script.exposure = Exposure(1) / 400
        script.comment = "C1 -> C2 partials"

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

        script.banner("C3 -> C4: partials")
        script.iso = 800
        script.phase = "C3"
        script.exposure = Exposure(1) / 400
        script.comment = "C3 -> C4 partials"

        # All times are UTC!!!
        script.capture("18:45:09")
        script.capture("18:53:23")
        script.capture("19:01:37")
        script.capture("19:09:51")
        script.capture("19:18:05")
        script.capture("19:26:19")
        script.capture("19:34:33")
        script.capture("19:42:47")
        script.capture("19:51:01")
        script.capture("19:59:20")

        expected = textwrap.dedent("""\
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
            # Action, Date/Ref, Offset sign, Time (offset), Camera, Exposure, Aperture, ISO, MLU, Quality, Size, Incremental, Comment
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
            #------------------------------------------------------------------------------------------------------------------------
            # C3 -> C4: partials
            #------------------------------------------------------------------------------------------------------------------------
            TAKEPIC,C3,+,00:01:59.600,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C3 -> C4 partials
            TAKEPIC,C3,+,00:10:13.600,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C3 -> C4 partials
            TAKEPIC,C3,+,00:18:27.600,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C3 -> C4 partials
            TAKEPIC,C3,+,00:26:41.600,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C3 -> C4 partials
            TAKEPIC,C3,+,00:34:55.600,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C3 -> C4 partials
            TAKEPIC,C3,+,00:43:09.600,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C3 -> C4 partials
            TAKEPIC,C3,+,00:51:23.600,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C3 -> C4 partials
            TAKEPIC,C3,+,00:59:37.600,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C3 -> C4 partials
            TAKEPIC,C3,+,01:07:51.600,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C3 -> C4 partials
            TAKEPIC,C3,+,01:16:10.600,Nikon Z7,1/400 , 8.0, 800,0.0,RAW+F-JPG,None,N,C3 -> C4 partials
            """)
        assert compare(str(script), expected)


    def test_typical_c2_to_c3(self):
        """
        Setting up for fast exposures just before C2 and after C3.
        Plus slower brackets during totality.

        There is still plenty of time during the 2024 eclipse in totality to
        capture more shots, but this is a unit test and demonstates the
        functionality.
        """
        script = Script()
        script.camera = "Nikon Z7"
        script.fstop = 8

        def _diamond_ring(phase, offset):
            script.iso = 64
            script.banner(f"{phase} fast exposures for diamond ring & baily's beads.")
            script.exposure = Exposure(1) / 500
            script.phase = phase
            script.offset = offset
            min_time_step = 0.300
            script.min_time_step = min_time_step
            script.comment = "fast burst"
            script.send_exposure()
            script.offset += 3.0
            for _ in range(int(10/min_time_step + 0.5)):
                script.capture()

        _diamond_ring("C2", -13.0)

        script.banner("Totality bracketed shots")
        script.comment = "brackets"
        script.min_time_step = 1.0
        for _ in range(3):
            script.capture_bracket(3, ev_step=2)
        script.exposure = Exposure(1) / 125
        script.capture_bracket(11, ev_step=1)

        script.comment = "some long exposures for Earthshine"
        duration = 0.5
        for _ in range(4):
            duration *= 2
            script.capture(exposure=duration)

        script.banner("Brackets around maximum totality.")
        script.phase = "MAX"
        script.offset = -5.0
        script.exposure = Exposure(1) / 60
        script.comment = "max totality"
        script.capture_bracket(11, ev_step=1)

        _diamond_ring("C3", -5.0)

        expected = textwrap.dedent("""\
            # Action, Date/Ref, Offset sign, Time (offset), Camera, Exposure, Aperture, ISO, MLU, Quality, Size, Incremental, Comment
            #------------------------------------------------------------------------------------------------------------------------
            # C2 fast exposures for diamond ring & baily's beads.
            #------------------------------------------------------------------------------------------------------------------------
            SETEXP,C2,-,00:00:13.000,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,N,sending all camera exposure settings via USB
            TAKEPIC,C2,-,00:00:10.000,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:09.698,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:09.396,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:09.094,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:08.792,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:08.490,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:08.188,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:07.886,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:07.584,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:07.282,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:06.980,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:06.678,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:06.376,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:06.074,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:05.772,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:05.470,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:05.168,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:04.866,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:04.564,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:04.262,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:03.960,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:03.658,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:03.356,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:03.054,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:02.752,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:02.450,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:02.148,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:01.846,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:01.544,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:01.242,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:00.940,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:00.638,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C2,-,00:00:00.336,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            #------------------------------------------------------------------------------------------------------------------------
            # Totality bracketed shots
            #------------------------------------------------------------------------------------------------------------------------
            TAKEPIC,C2,-,00:00:00.034,Nikon Z7,1/2000, 8.0,  64,0.0,RAW+F-JPG,None,N,brackets  -2.000 EV Stops
            TAKEPIC,C2,+,00:00:00.966,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +0.000 EV Stops
            TAKEPIC,C2,+,00:00:01.968,Nikon Z7,1/125 , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +2.000 EV Stops
            TAKEPIC,C2,+,00:00:02.976,Nikon Z7,1/2000, 8.0,  64,0.0,RAW+F-JPG,None,N,brackets  -2.000 EV Stops
            TAKEPIC,C2,+,00:00:03.977,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +0.000 EV Stops
            TAKEPIC,C2,+,00:00:04.979,Nikon Z7,1/125 , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +2.000 EV Stops
            TAKEPIC,C2,+,00:00:05.987,Nikon Z7,1/2000, 8.0,  64,0.0,RAW+F-JPG,None,N,brackets  -2.000 EV Stops
            TAKEPIC,C2,+,00:00:06.987,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +0.000 EV Stops
            TAKEPIC,C2,+,00:00:07.989,Nikon Z7,1/125 , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +2.000 EV Stops
            TAKEPIC,C2,+,00:00:08.997,Nikon Z7,1/4000, 8.0,  64,0.0,RAW+F-JPG,None,N,brackets  -5.000 EV Stops
            TAKEPIC,C2,+,00:00:09.998,Nikon Z7,1/2000, 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  -4.000 EV Stops
            TAKEPIC,C2,+,00:00:10.998,Nikon Z7,1/1000, 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  -3.000 EV Stops
            TAKEPIC,C2,+,00:00:11.999,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  -2.000 EV Stops
            TAKEPIC,C2,+,00:00:13.001,Nikon Z7,1/250 , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  -1.000 EV Stops
            TAKEPIC,C2,+,00:00:14.005,Nikon Z7,1/125 , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +0.000 EV Stops
            TAKEPIC,C2,+,00:00:15.013,Nikon Z7,1/60  , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +1.000 EV Stops
            TAKEPIC,C2,+,00:00:16.029,Nikon Z7,1/30  , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +2.000 EV Stops
            TAKEPIC,C2,+,00:00:17.061,Nikon Z7,1/15  , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +3.000 EV Stops
            TAKEPIC,C2,+,00:00:18.125,Nikon Z7,1/8   , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +4.000 EV Stops
            TAKEPIC,C2,+,00:00:19.253,Nikon Z7,1/4   , 8.0,  64,0.0,RAW+F-JPG,None,Y,brackets  +5.000 EV Stops
            TAKEPIC,C2,+,00:00:20.509,Nikon Z7,1     , 8.0,  64,0.0,RAW+F-JPG,None,Y,some long exposures for Earthshine
            TAKEPIC,C2,+,00:00:22.509,Nikon Z7,2     , 8.0,  64,0.0,RAW+F-JPG,None,Y,some long exposures for Earthshine
            TAKEPIC,C2,+,00:00:25.509,Nikon Z7,4     , 8.0,  64,0.0,RAW+F-JPG,None,Y,some long exposures for Earthshine
            TAKEPIC,C2,+,00:00:30.509,Nikon Z7,8     , 8.0,  64,0.0,RAW+F-JPG,None,Y,some long exposures for Earthshine
            #------------------------------------------------------------------------------------------------------------------------
            # Brackets around maximum totality.
            #------------------------------------------------------------------------------------------------------------------------
            TAKEPIC,MAX,-,00:00:05.000,Nikon Z7,1/2000, 8.0,  64,0.0,RAW+F-JPG,None,N,max totality  -5.000 EV Stops
            TAKEPIC,MAX,-,00:00:03.999,Nikon Z7,1/1000, 8.0,  64,0.0,RAW+F-JPG,None,Y,max totality  -4.000 EV Stops
            TAKEPIC,MAX,-,00:00:02.998,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,max totality  -3.000 EV Stops
            TAKEPIC,MAX,-,00:00:01.996,Nikon Z7,1/250 , 8.0,  64,0.0,RAW+F-JPG,None,Y,max totality  -2.000 EV Stops
            TAKEPIC,MAX,-,00:00:00.992,Nikon Z7,1/125 , 8.0,  64,0.0,RAW+F-JPG,None,Y,max totality  -1.000 EV Stops
            TAKEPIC,MAX,+,00:00:00.016,Nikon Z7,1/60  , 8.0,  64,0.0,RAW+F-JPG,None,Y,max totality  +0.000 EV Stops
            TAKEPIC,MAX,+,00:00:01.033,Nikon Z7,1/30  , 8.0,  64,0.0,RAW+F-JPG,None,Y,max totality  +1.000 EV Stops
            TAKEPIC,MAX,+,00:00:02.066,Nikon Z7,1/15  , 8.0,  64,0.0,RAW+F-JPG,None,Y,max totality  +2.000 EV Stops
            TAKEPIC,MAX,+,00:00:03.133,Nikon Z7,1/8   , 8.0,  64,0.0,RAW+F-JPG,None,Y,max totality  +3.000 EV Stops
            TAKEPIC,MAX,+,00:00:04.266,Nikon Z7,1/4   , 8.0,  64,0.0,RAW+F-JPG,None,Y,max totality  +4.000 EV Stops
            TAKEPIC,MAX,+,00:00:05.533,Nikon Z7,1/2   , 8.0,  64,0.0,RAW+F-JPG,None,Y,max totality  +5.000 EV Stops
            #------------------------------------------------------------------------------------------------------------------------
            # C3 fast exposures for diamond ring & baily's beads.
            #------------------------------------------------------------------------------------------------------------------------
            SETEXP,C3,-,00:00:05.000,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,N,sending all camera exposure settings via USB
            TAKEPIC,C3,-,00:00:02.000,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,-,00:00:01.698,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,-,00:00:01.396,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,-,00:00:01.094,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,-,00:00:00.792,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,-,00:00:00.490,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,-,00:00:00.188,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:00.114,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:00.416,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:00.718,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:01.020,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:01.322,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:01.624,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:01.926,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:02.228,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:02.530,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:02.832,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:03.134,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:03.436,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:03.738,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:04.040,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:04.342,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:04.644,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:04.946,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:05.248,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:05.550,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:05.852,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:06.154,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:06.456,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:06.758,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:07.060,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:07.362,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            TAKEPIC,C3,+,00:00:07.664,Nikon Z7,1/500 , 8.0,  64,0.0,RAW+F-JPG,None,Y,fast burst
            """)
        assert compare(str(script), expected)

