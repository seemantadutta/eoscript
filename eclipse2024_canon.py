from eoscript import Exposure, Script


DEFAULT_ISO = 800
DEFAULT_FSTOP = 8
DEFAULT_SHUTTER_SPEED = 1/1000

class expinfo:
    iso = DEFAULT_ISO
    fstop = DEFAULT_FSTOP
    shutter = DEFAULT_SHUTTER_SPEED



MIN_STEP_FAST = 0.333 # Verify your setup to see how fast you can go! Gap between consecutive shots
MIN_STEP_SLOW = 1.000 # Verify your setup with USB updates. Gap between USB updates

_1 = Exposure(1)

def _setup_for_partials(phase0, phase1):
    script.banner(f"{phase0} -> {phase1}: partials")
    script.phase = phase0
    script.comment = f"{phase0} -> {phase1} partials"
    script.iso = 100
    script.exposure = _1 / 25
    script.min_time_step = MIN_STEP_SLOW
    script.incremental = "N"

def _diamond_ring(phase, offset, exposure):
    script.banner(f"{phase} fast exposures for diamond ring & baily's beads.")
    script.phase = phase
    script.offset = offset
    script.iso = 100
    script.exposure = exposure
    script.min_time_step = 0.66
    script.comment = "fast burst"
    script.send_exposure()
    script.offset += MIN_STEP_SLOW
    script.release_command = "TAKEPIC"
    for _ in range(4):
        script.capture()
        exposure *= 2
        script.exposure = exposure


def _earthshine(label):
    script.banner(f"{label} long exposures for Earthshine")
    script.comment = "long exposures for Earthshine"
    script.min_time_step = MIN_STEP_SLOW
    script.incremental = "N"
    script.iso = 100
    exposure = 0.5
    for _ in range(4):
        exposure *= 2
        script.capture(exposure=exposure)




def _main_sequence(label, phase, initial_offset = 0, ev_stops = 1, initial_exposure = .001, final_exposure = 0.001, direction = "increasing"):
    assert direction in {"increasing", "decreasing"}

    script.banner(f"{label}: fast bursts for stacking")
    script.comment = "Fast, manual stacks"
    script.min_time_step = MIN_STEP_FAST
    script.phase = phase
    script.iso = 100
    NUM_PHOTOS_PER_STACK = 8
    exposure = initial_exposure

    script.offset = initial_offset

    # TODO: Find a better way to combine these loops
    if (direction == "increasing"):
        # 8 gives us exposures until 4s
        while exposure <= final_exposure:
            script.exposure = exposure
            if (exposure == initial_exposure):
                script.offset += MIN_STEP_SLOW
            else:
                script.offset += MIN_STEP_SLOW

            script.send_exposure()


            # This is a hack for Canon, where for longer exposures, we need to give the USB more time to settle
            # before sending the RELEASE command. So we use MIN_STEP_SLOW, except for exposures larger than 1s
            # where we use (MIN_STEP_SLOW + 1.0) between SETEXP and RELEASE commands

            # Use 1.024 here because the called code will automatically convert this to usual camera stops of shutter speed
            if (exposure > 1.024):
                script.offset += MIN_STEP_SLOW + 1.0
                release_time = 0.40
            else:
                script.offset += MIN_STEP_SLOW
                release_time = 0.20

            for _ in range(NUM_PHOTOS_PER_STACK):
                script.release_command = "RELEASE"
                script.release(release_time, exposure=exposure)

            exposure *= 2 ** ev_stops
    else:
        while exposure >= final_exposure:
            script.exposure = exposure
            if (exposure == initial_exposure):
                script.offset += MIN_STEP_SLOW
            else:
                script.offset += MIN_STEP_SLOW

            script.send_exposure()


            # This is a hack for Canon, where for longer exposures, we need to give the USB more time to settle
            # before sending the RELEASE command. So we use MIN_STEP_SLOW, except for exposures larger than 1s
            # where we use (MIN_STEP_SLOW + 1.0) between SETEXP and RELEASE commands

            # Use 1.024 here because the called code will automatically convert this to usual camera stops of shutter speed
            if (exposure > 1.024):
                script.offset += MIN_STEP_SLOW + 1.0
                release_time = 0.40
                script.min_time_step = 0.5
            else:
                script.offset += MIN_STEP_SLOW
                release_time = 0.20

            for _ in range(NUM_PHOTOS_PER_STACK):
                script.release_command = "RELEASE"
                script.release(release_time, exposure=exposure)

            exposure /= 2 ** ev_stops




# This functin works for 150ms/600 baud serial cable settings
def _fast_manual_stacks(label, phase):
    script.banner(f"{label}: fast bursts for stacking")
    script.comment = "Fast, manual stacks"
    script.min_time_step = MIN_STEP_FAST
    script.phase = phase
    script.iso = 100
    NUM_PHOTOS_PER_STACK = 8
    initial_exposure = 1.0 / 1000
    exposure = initial_exposure
    
    # while exposure < 4.0:
    #     script.exposure = exposure
    #     script.offset += MIN_STEP_SLOW
    #     script.send_exposure()
    #     exposure *= 2.0

    # 8 gives us exposures until 4s
    while exposure < 8.0:
        script.exposure = exposure
        if (exposure == initial_exposure):
            script.offset += MIN_STEP_SLOW
        else:
            script.offset += MIN_STEP_SLOW

        script.send_exposure()


        # This is a hack for Canon, where for longer exposures, we need to give the USB more time to settle
        # before sending the RELEASE command. So we use MIN_STEP_SLOW, except for exposures larger than 1s
        # where we use (MIN_STEP_SLOW + 1.0) between SETEXP and RELEASE commands

        # Use 1.024 here because the called code will automatically convert this to usual camera stops of shutter speed
        if (exposure > 1.024):
            script.offset += MIN_STEP_SLOW + 1.0
            release_time = 0.40
        else:
            script.offset += MIN_STEP_SLOW
            release_time = 0.20

        for _ in range(NUM_PHOTOS_PER_STACK):
            script.release_command = "RELEASE"
            script.release(release_time, exposure=exposure)
        exposure *= 2.0



def _get_release_time(exposure):
    # Use 1.024 here because the called code will automatically convert this to usual camera stops of shutter speed
    offset_delta = 0
    release_time = 0
    if (exposure > 1.024):
        offset_delta = 1.0
        release_time = 0.40
    else:
        offset_delta += MIN_STEP_SLOW
        release_time = 0.20

    return offset_delta, release_time


def _generate_main_totality_sequence(label):
    """
    The "Main Totality Sequence" consists of shots that are centered around MAX eclipse.
    This is done such that the shortest exposures are synchronized with MAX eclipse. And then
    shorter exposures are progressively added on either side of MAX eclipse leading up to C2 on
    one side and C3 on the other side.

    This allows us to take the shortest exposures when the moon is most centered on the sun to capture the
    faintest corona details, while the longer exposures are closer to C2 and C3 where we are trying to
    capture the fainter details of the corona and the centered moon doesn't matter as much.

    So, this main sequence will look something like this:

    C2----------------------------------------> MAX ------------------------------------------>C3
          4,  1,  1/4,  1/15,  1/60,  1/250,  1/1000,  1/500,  1/125,  1/30,  1/8,  1/2,  2

          
    Note: we are leaving some leading time off after C2 and some trailing time before C3. This allows
    time for SETEXP to settle
    """

    script.banner(f"{label}: Main Totality Sequence")
    script.comment = "Main Totality Sequence"
    script.min_time_step = MIN_STEP_FAST
    script.phase = "MAX"
    script.iso = 100


    exposure = 1.0 / 1000
    # Add the first SETEXP at (MAX-1)
    script.exposure = exposure
    script.offset = -1
    script.send_exposure()
    script.offset += 1  # Allow it to settle, this also lines us up at exactly MAX before we start releasing the shutter

    # Add the 8 exposures centered around MAX, separated by .333s
    for _ in range(8):
        release_time = 0.20
        script.release_command = "RELEASE"
        script.release(release_time, exposure=exposure)

    script.offset += MIN_STEP_SLOW - MIN_STEP_FAST


    # Add exposures *AFTER MAX*, these start at 1/500 and differ by 2 stops
    exposure =  1/500
    for __ in range (6):
        script.exposure = exposure
        script.send_exposure()
        if (exposure > 1.024):
            script.offset += 2 # Allow it to settle
        else:
            script.offset += 1 # Allow it to settle

        for _ in range(8):
            o, r = _get_release_time(exposure)
            release_time = r
            script.release_command = "RELEASE"
            script.release(release_time, exposure=exposure)

        script.offset += MIN_STEP_SLOW - MIN_STEP_FAST
        exposure = exposure * 4


    # Add exposures BEFORE MAX, these start right after C2, and also differ by 2 stops
    exposure =  4
    script.phase = "C2"
    script.offset = 10
    for __ in range (6):
        script.exposure = exposure
        script.send_exposure()
        if (exposure >= 1):
            script.offset += 2 # Allow it to settle
        else:
            script.offset += 1 # Allow it to settle
            
        for _ in range(8):
            o, r = _get_release_time(exposure)
            release_time = r
            script.release_command = "RELEASE"
            script.release(release_time, exposure=exposure)

            # Special case for longer exposures which need more gap between shots
            if (exposure > 1.024):
                script.offset += .100

        script.offset += MIN_STEP_SLOW - MIN_STEP_FAST
        exposure = exposure / 4
        



    while exposure < 8.0:
        script.exposure = exposure
        if (exposure == initial_exposure):
            script.offset += MIN_STEP_SLOW
        else:
            script.offset += MIN_STEP_SLOW

        script.send_exposure()


        # This is a hack for Canon, where for longer exposures, we need to give the USB more time to settle
        # before sending the RELEASE command. So we use MIN_STEP_SLOW, except for exposures larger than 1s
        # where we use (MIN_STEP_SLOW + 1.0) between SETEXP and RELEASE commands

        # Use 1.024 here because the called code will automatically convert this to usual camera stops of shutter speed
        if (exposure > 1.024):
            script.offset += MIN_STEP_SLOW + 1.0
            release_time = 0.40
        else:
            script.offset += MIN_STEP_SLOW
            release_time = 0.20

        for _ in range(NUM_PHOTOS_PER_STACK):
            script.release_command = "RELEASE"
            script.release(release_time, exposure=exposure)
        exposure *= 2.0


def _fast_manual_stacks2(label, phase):
    script.banner(f"{label}: fast bursts for stacking")
    script.comment = "Fast, manual stacks"
    script.min_time_step = MIN_STEP_FAST
    script.phase = phase
    script.iso = 100
    NUM_PHOTOS_PER_STACK = 8
    exposure = 2.0

    script.exposure = exposure
    script.offset += MIN_STEP_SLOW - MIN_STEP_FAST
    script.send_exposure()
    script.offset += MIN_STEP_SLOW
    for _ in range(NUM_PHOTOS_PER_STACK):
        script.release_command = "RELEASE"
        script.release(0.20, exposure=exposure)



def _uneclisped_sun_photos(phase, offset, count, delta, banner, expinfo):
    script.banner(f"{phase} {banner}")
    script.phase = phase
    script.offset = offset
    script.iso = expinfo.iso
    script.exposure = expinfo.shutter
    script.fstop = expinfo.fstop
    script.min_time_step = 300
    script.comment = "fast burst"
    script.release_command = "TAKEPIC"
    for _ in range(count):
        script.capture()
        


if __name__ == '__main__':
    # Ultimate Eclipse capture for 4m20s of totality.

    '''
    The EO script will have the following flow:

    1. Take 3 uneclipsed sun photos, to make sure focus and exposure are good. 
    These should be done about 30mins before C1, spaced 5 mins apart

    2. Voice prompt for C1
    
    2. Start partials, at every 1% progress starting at C1, through C2.

    3. Battery change at around 90% progress in partials

    4. Voice prompt for filter removal

    5. Take Bailey's beads and diamond ring shot close to C2


    5. At C2-2 seconds, SETEXP up the C2 exposure. At C2+3, start the long exposure sequence from 4s, 1s, .5s.
       This will take 48 photos, bracketed exposure wise and will use RELEASE

    6. There is a TIME GAP from here until MAX (earthshine shots)

    7. At MAX eclipse, the second half of bracket shots starting at 1/1000 are taken. This will be 56 shots, bracketed
       exposure wise

    8. There is a TIME GAP from here until C3 (Insurance shots)

    9. Take Bailey's beads and diamond ring close to C3

    10. Continue with partials every 1% progress

    11. Battery change once more

    12. Uneclipsed Sun?

    '''


    # All times are UTC!!!
    # All times are UTC!!!
    # All times are UTC!!!
    script = Script(
        #                 UTC                LOCAL TEXAS
        c1  = "2024/04/08 17:21:27.5",     # 12:21:27.5 PM
        c2  = "2024/04/08 18:38:46.6",     #  1:38:46.6 PM
        max = "2024/04/08 18:40:58.0",     #  1:40:58.0 PM
        c3  = "2024/04/08 18:43:09.4",     #  1:43:09.4 PM
        c4  = "2024/04/08 20:01:20.9",     #  3:01:20.9 PM
    )

    script.camera = "C5d4"

    # phase, offset to start taking photos, count of shots, difference between each shot, text banner, exposure info
    expinfo.fstop = 8
    expinfo.iso = 100
    expinfo.shutter = 1/1000
    _uneclisped_sun_photos("C1", -1200, 3, 300, "UNECLIPSED SUN - test exposures in the field", expinfo)




    #_setup_for_partials("C1", "C2")

    # C2->MAX cycle
    _main_sequence("C2 sequence (C2->MAX)", "C2", 2, 2, 4, 1/500, "decreasing")

    # Single exposure of 1/1000 centered at MAX
    _main_sequence("MAX Single Shot", "MAX", -2, 2, 0.001, 0.001)

    offset = script.offset
    _main_sequence("MAX sequence (MAX->C3)", "MAX", offset, 2, 0.002, 4)





    #_diamond_ring("C2", -10, 1/4000)
    


    ''' Solar filter Test '''
    '''
    _diamond_ring("C2", -2, 1/1000)

    _diamond_ring("C2", +5, 1/8000)

    script.fstop = 16
    _diamond_ring("C2", +10, 1/500)

    script.iso = 800
    script.fstop = 8
    _diamond_ring("C2", +15, 1/1600)
    '''
    script.save("eclipse2024_canon_main2024__.csv")
    #script.save("SolarFilterTest.csv")