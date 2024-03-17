from eoscript import Exposure, Script

# Ultimate Eclipse capture for 4m20s of totality.

MIN_STEP_FAST = 0.333 # Verify your setup to see how fast you can go!
MIN_STEP_SLOW = 1.000 # Verify your setup with USB updates.

_1 = Exposure(1)

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

script.camera = "Nikon Z7"
script.fstop = 8

def _setup_for_partials(phase0, phase1):
    script.banner(f"{phase0} -> {phase1}: partials")
    script.phase = phase0
    script.comment = f"{phase0} -> {phase1} partials"
    script.iso = 64
    script.exposure = _1 / 25
    script.min_time_step = MIN_STEP_SLOW
    script.incremental = "N"

#------------------------------------------------------------------------------
# C1 partials

_setup_for_partials("C1", "C2")

# All times are UTC!!!
# All times are UTC!!!
# All times are UTC!!!
script.capture("17:23:27")
script.capture()
script.capture()
script.capture("17:31:35")
script.capture()
script.capture()
script.capture("17:39:43")
script.capture()
script.capture()
script.capture("17:47:51")
script.capture()
script.capture()
script.capture("17:55:59")
script.capture()
script.capture()
script.capture("18:04:07")
script.capture()
script.capture()
script.capture("18:12:15")
script.capture()
script.capture()
script.capture("18:20:23")
script.capture()
script.capture()
script.capture("18:28:31")
script.capture()
script.capture()
script.capture("18:36:46")
script.capture()
script.capture()

#------------------------------------------------------------------------------
# C2 diamond ring

def _diamond_ring(phase, offset):
    script.banner(f"{phase} fast exposures for diamond ring & baily's beads.")
    script.phase = phase
    script.offset = offset
    script.iso = 64
    script.exposure = _1 / 500
    script.min_time_step = MIN_STEP_FAST
    script.comment = "fast burst"
    script.send_exposure()
    script.offset += MIN_STEP_SLOW
    for _ in range(40):
        script.capture()

_diamond_ring("C2", -10.0 - MIN_STEP_SLOW)

#------------------------------------------------------------------------------
# C2 long exposures

def _earthshine(label):
    script.banner(f"{label} long exposures for Earthshine")
    script.comment = "long exposures for Earthshine"
    script.min_time_step = MIN_STEP_SLOW
    script.incremental = "N"
    script.iso = 64
    exposure = 0.5
    for _ in range(4):
        exposure *= 2
        script.capture(exposure=exposure)

_earthshine("C2")

#------------------------------------------------------------------------------
# C2 Mr. Eclipse bracket sets.

script.banner("C2 -> MAX: cronoa Mr. Eclispe brackets.")
script.comment = "Mr. Eclipse bracket chart."
script.iso = 64
script.exposure = _1 / 60
script.min_time_step = MIN_STEP_SLOW
script.capture_bracket(11)

#------------------------------------------------------------------------------
# Fast, manual stacks for ultimate post processing.

def _fast_manual_stacks(label):
    script.banner(f"{label}: fast bursts for stacking")
    script.comment = "Fast, manual stacks"
    script.min_time_step = MIN_STEP_FAST
    script.iso = 64
    NUM_PHOTOS_PER_STACK = 8
    exposure = 1.0 / 1000
    while exposure < 4.0:
        script.exposure = exposure
        script.send_exposure()
        script.offset += MIN_STEP_SLOW
        for _ in range(NUM_PHOTOS_PER_STACK):
            script.capture(exposure=exposure)
        exposure *= 2.0

_fast_manual_stacks("C2 -> MAX")

# Take some bracketed shots around totality.

#------------------------------------------------------------------------------
# MAX Mr. Eclipse bracket sets.

script.banner("Approaching MAX Totality at C2,+,00:02:11")
script.comment = "Mr. Eclipse bracket chart."
script.iso = 64
script.exposure = _1 / 60
script.min_time_step = MIN_STEP_SLOW
script.capture_bracket(13)
script.file_comment = "C2,+,00:02:11  is Max Totality !!!"
#script.offset += 4.0 # To align center stack at max totality.
script.capture_bracket(13)
script.capture_bracket(13)

#------------------------------------------------------------------------------
# Fast an manual stacks for ultimate post processing.

_fast_manual_stacks("MAX -> C3")

#------------------------------------------------------------------------------
# C3 long exposures for earthshine
_earthshine("C3")

script.file_comment = "C2,+,00:04:22 is end of totality"

#------------------------------------------------------------------------------
# C3 diamond ring

_diamond_ring("C3", -2.0 - MIN_STEP_SLOW)

#------------------------------------------------------------------------------
# C3 partials

_setup_for_partials("C3", "C4")

# All times are UTC!!!
# All times are UTC!!!
# All times are UTC!!!
script.capture("18:45:09")
script.capture()
script.capture()
script.capture("18:53:23")
script.capture()
script.capture()
script.capture("19:01:37")
script.capture()
script.capture()
script.capture("19:09:51")
script.capture()
script.capture()
script.capture("19:18:05")
script.capture()
script.capture()
script.capture("19:26:19")
script.capture()
script.capture()
script.capture("19:34:33")
script.capture()
script.capture()
script.capture("19:42:47")
script.capture()
script.capture()
script.capture("19:51:01")
script.capture()
script.capture()
script.capture("19:59:20")
script.capture()
script.capture()

script.save("eclipse2024.csv")