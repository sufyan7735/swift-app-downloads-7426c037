import sys; sys.path.insert(0, "/tmp/cat")
from rtl import recompose, cols_rev
from engine import render

E = 580  # right content edge
p1 = []
# --- mechanical section ---
p1 += [((80, 92, 200, 111), E - 120)]                      # title -> right
p1 += [((375, 116, 590, 372), 30)]                         # drawing -> left
p1 += [((37, 116, 162, 352), E - 125)]                     # labels -> right
p1 += [((162, 116, 370, 352), E - 125 - 208)]              # values -> middle
p1 += [((60, 352, 360, 364), E - 300)]                     # footnote -> right
# --- electrical ---
p1 += [((75, 370, 185, 393), E - 110)]
p1 += [((37, 393, 162, 510), E - 125)]
p1 += cols_rev(162, 580, 5, 393, 510, 37)
# --- bottom: bifacial + thermal (left) <-> curves (right) ---
p1 += [((375, 525, 595, 725), 22)]                         # curves -> left
p1 += [((37, 525, 200, 552), E - 163)]                     # bifacial title
p1 += [((210, 538, 290, 552), E - 163 - 85)]               # 710W note
p1 += [((37, 552, 162, 660), E - 125)]
p1 += cols_rev(162, 369, 3, 552, 660, E - 125 - 207)
p1 += [((100, 660, 205, 683), E - 105)]                    # thermal title
p1 += [((37, 683, 162, 740), E - 125)]
p1 += [((162, 683, 366, 740), E - 125 - 204)]

p0 = []
p0 += [((278, 625, 296, 652), 4)]
p0 += [((296, 625, 595, 652), 22), ((300, 652, 595, 740), 26)]
p0 += [((60, 652, 300, 720), E - 240)]
p0 += [((280, 520, 595, 605), 26)]                          # certifications -> left
p0 += [((50, 515, 245, 605), E - 195)]                      # award logos -> right

recompose("/tmp/cat/s720.pdf", "/tmp/cat/s720r.pdf", {0: p0, 1: p1})
render("/tmp/cat/s720r.pdf", "/tmp/cat/r720", dpi=130)
