from eoscript import Exposure, Script

#------------------------------------------------------------------------------
# Write you scirpt!

_1 = Exposure(1)

# All times are UTC!!!
# All times are UTC!!!
# All times are UTC!!!
script = Script(
    c1  = "2024/04/08 17:21:27.5",     # 12:21:27.5 PM
    c2  = "2024/04/08 18:38:46.6",     #  1:38:46.6 PM
    max = "2024/04/08 18:40:58.0",     #  1:40:58.0 PM
    c3  = "2024/04/08 18:43:09.4",     #  1:43:09.4 PM
    c4  = "2024/04/08 20:01:20.9",     #  3:01:20.9 PM
    min_time_step = 0.30,
)

script.camera = "Nikon Z7"
script.fstop = 8

script.banner("C1 -> C2: partials")
script.iso = 800
script.phase = "C1"
script.exposure = _1 / 400
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

script.banner("C2: Diamond Ring & Baily's Beads")
script.comment = "diamond ring, fast burst"
script.phase = "C2"
script.iso = 500 # 64
script.exposure = _1 / 500
script.min_time_step = 0.300

script.offset = -37.0
script.send_exposure()
script.offset += 3

for _ in range(60):
    script.capture()
#
# script.banner("C2 -> MAX: cronoa")
# script.comment = "Mr. Eclipse bracket chart."
# script.iso = 500 # 64
# script.exposure = _1 / 15
# script.min_time_step = 0.50
#
# for _ in range(3):
    # script.capture_bracket(13)
#
#
# script.banner("MAX: totality")
# script.phase = "MAX"
# script.send_exposure()
#
# script.banner("C3: Diamond Ring & Baily's Beads")
#
# script.phase = "C3"
# script.send_exposure()
#
#
# script.banner("C3 -> C4: partials")
# script.phase = "C3"
# script.iso = 800
# script.exposure = _1 / 400
# script.comment = "C3 -> C4 partials"
#
# # All times are UTC!!!
# # All times are UTC!!!
# # All times are UTC!!!
# script.capture("18:45:09")
# script.capture("18:53:23")
# script.capture("19:01:37")
# script.capture("19:09:51")
# script.capture("19:18:05")
# script.capture("19:26:19")
# script.capture("19:34:33")
# script.capture("19:42:47")
# script.capture("19:51:01")
# script.capture("19:59:20")

script.save("nick.csv")