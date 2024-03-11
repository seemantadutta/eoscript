from eoscript import Exposure, Script

MIN_STEP_FAST = 0.5 # Verify your setup to see how fast you can go! Gap between consecutive shots
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

def _diamond_ring(phase, offset):
    script.banner(f"{phase} fast exposures for diamond ring & baily's beads.")
    script.phase = phase
    script.offset = offset
    script.iso = 100
    script.exposure = _1 / 500
    script.min_time_step = MIN_STEP_FAST
    script.comment = "fast burst"
    script.send_exposure()
    script.offset += MIN_STEP_SLOW
    for _ in range(40):
        script.capture()


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


def _fast_manual_stacks(label, phase):
    script.banner(f"{label}: fast bursts for stacking")
    script.comment = "Fast, manual stacks"
    script.min_time_step = MIN_STEP_FAST
    script.phase = phase
    script.iso = 100
    NUM_PHOTOS_PER_STACK = 8
    exposure = 1.0 / 15
    while exposure < 4.0:
        script.exposure = exposure
        script.offset += MIN_STEP_SLOW - MIN_STEP_FAST
        script.send_exposure()
        # This is a hack for Canon, where for longer exposures, we need to give the USB more time to settle
        # before sending the RELEASE command. So we use MIN_STEP_SLOW, except for exposures larger than 1s
        # where we use (MIN_STEP_SLOW + 1.0) between SETEXP and RELEASE commands

        if (exposure > 1.0):
            script.offset += MIN_STEP_SLOW + 1.0
        else:
            script.offset += MIN_STEP_SLOW

        for _ in range(NUM_PHOTOS_PER_STACK):
            script.release_command = "RELEASE"
            script.release(0.20, exposure=exposure)
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


if __name__ == '__main__':
    # Ultimate Eclipse capture for 4m20s of totality.


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
    script.fstop = 8

    _setup_for_partials("C1", "C2")

    # script.banner("C2 -> MAX: cronoa Mr. Eclispe brackets.")
    # script.comment = "Mr. Eclipse bracket chart."
    # script.iso = 100
    # script.exposure = _1 / 60
    # script.min_time_step = MIN_STEP_SLOW
    # script.capture_bracket(11)

    #------------------------------------------------------------------------------
    # Fast, manual stacks for ultimate post processing.
    _fast_manual_stacks("C2 -> MAX", "C2")

   

    script.save("eclipse2024_canon_1.csv")