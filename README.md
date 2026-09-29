# Copperplate states

Before about 1800 a printed map started life as a copper plate. An engraver cut the whole map into it, backwards,
by hand, and it took months. Then the plate was inked and pressed onto paper, again and again, sometimes for a
hundred years.

Plates were valuable, so they changed hands. A publisher died and his son kept printing. A rival bought the plate,
scratched out the old name and cut in his own. Along the way people altered the copper: they added a ship, re-cut a
coat of arms, engraved a grid for a place-name index. Map historians call each altered version a *state*, and
telling states apart is one of the basic jobs of the field. For Dutch atlases the standard reference is *Koeman's
Atlantes Neerlandici*, edited by Peter van der Krogt, and it was built by comparing copies by eye.

Can a computer make that comparison? This repository tries it on maps from the
[Allard Pierson](https://www.allardpierson.nl/) in Amsterdam, and checks every answer against van der Krogt.

![A ship present in one impression and absent from the other](results/gallery/ship.jpg)

Gerard Mercator, *Anglia regnum*, 1595. Left is HB-KZL 31.17.20. In the middle is HB-KZL 31.17.19, turned and
stretched so it lies exactly on the left one. On the right the two are laid on top of each other: dark where both
have ink, red where only the left copy has it, cyan where only the middle one does. Van der Krogt describes a proof
state of this plate in which the ship is missing. The program marks the ship without being told where to look.

## The test

The Allard Pierson catalogue copies van der Krogt's state descriptions into the records of 24 of its digitised
maps, and the collection owns at least one other copy of each. That makes 8 plates and 30 pairs of copies where an
expert has already written down what changed. They are all in [`data/pairs.json`](data/pairs.json).

One catch. A catalogue note says which states exist, not which state a given copy is. So I also looked at every
result myself.

| Plate | What van der Krogt records | What the program found |
|---|---|---|
| Mercator, *Anglia*, 1595 | a proof state without the ship and without the ornament under *Germanicvs* | both |
| Blaeu, *Hibernia*, 1634 | four ships added around Ireland in a later state | no change, which is right: both copies here are the first state |
| Blaeu, *Suevia*, 1630 | the longitude figures in the border re-engraved | the changed figures |
| N. Visscher, *Lotharingia*, 1690 | with and without a coordinate grid | the grid, and also a re-engraved north-east corner that the note does not mention |
| Blaeu, *Champagne*, 1634 | the bars in the coat of arms run the other way | the bars |
| N. Visscher, *Belgii*, 1680 | a place-name list printed on the back | no change, which is right: the scans only show the front |
| N. Visscher, *Helvetia*, 1677 | with and without coordinates | the five copies fall into two groups, 32.20.26, .25 and .22 against .24 and .23, and the border letters are in one group only |
| *Danubii fluvii pars superior*, 1690 | a second state adds coordinates | one copy, HB-KZL 34.20.15, differs from the other four; I have not checked it by eye yet |

Every change that van der Krogt describes on the front of a sheet was found, six out of six, and the two pairs that
really are identical came out identical. Every pair was recognised as the same plate.

The Helvetia row surprised me. Nobody told the program which copies belong together, but when it compares all
five with each other the differences sort them into two states. That is the same job a bibliographer does with a
pile of copies on a table.

The output for every pair is in [`results/`](results/).

## Three more

![Coat of arms re-cut](results/gallery/coat_of_arms.jpg)

Blaeu, *Champagne*, 1634, HB-KZL 32.12.03 and 32.12.02. The crown, the cherubs and the frame lie exactly on top
of each other. The bars inside the shield cross in an X. It is one plate, and somebody re-cut the shield.

![Longitude figures re-engraved](results/gallery/longitude_figures.jpg)

Blaeu, *Sueviae nova tabula*, 1630, HB-KZL 32.01.42 and 32.01.41. The map itself is identical. Look at the numbers
in the border: 40 and 27 on the left, 20 and 40 in the middle.

![Coordinate grid added](results/gallery/coordinate_grid.jpg)

N. Visscher, *Lotharingia*, 1690, HB-KZL 31.33.21 and 31.33.18. The letters B and C in the border, and the thin
ruled lines across the map, are only in the left copy. They are the grid for a place-name index.

## How it works

Two prints from one plate never lie exactly on top of each other. The paper was printed damp and shrank as it
dried, and not by the same amount everywhere. Each copy was hand-coloured by a different person. One copy was
printed with more ink than another. Simply subtracting one scan from the other gives a picture full of differences,
almost none of them real.

So the program works in four steps. Each is borrowed from a field that already compares two copies of one thing;
[`docs/sources.md`](docs/sources.md) has the details.

1. Keep only the ink. Engraved lines are thin and dark in every colour channel. Watercolour is not dark in every
   channel, and a painted area is much wider than a line, so both can be thrown away.
2. Line the copies up, then let one bend a little. First a single rotation, scale and shift for the whole sheet.
   Then a gentle warp that follows the shrinking of the paper. It is kept stiff on purpose, so it cannot bend
   around a changed number and hide it. Stamp collectors do the same thing to compare engraved stamps.
3. Match the darkness. A pale copy is brightened to match a dark one, using only the lines both copies have.
   Astronomers do this before they subtract two pictures of the sky.
4. Look for ink in one copy that is missing from the other. A worn line fades to about half its strength. A line
   that was never engraved, or was burnished out, is gone. Only the second kind is marked.

The code is in [`copperplate/compare.py`](copperplate/compare.py).

## What it cannot do yet

I tuned the settings on eight of these thirty pairs. That makes this a pilot, not a measurement. The honest next
step is to plant fake changes into pairs I know are identical and find out how small a change it still catches.

Small numbers along the border sometimes get marked when nothing changed, and so do coloured bands painted along
the frame.

The backs of the sheets were not scanned. In one copy you can see the place-name register on the back faintly
through the paper, so some of those states may be detectable after all.

The ground truth here is the catalogue's copy of van der Krogt's notes, not the printed volumes. Checking the
results against the volumes, and against his own eye, is the work I am proposing to do next.

## Running it

You need Docker and `make`. Nothing else is installed on your machine.

```sh
make image      # build the container
make fetch      # download the 24 scans from the Allard Pierson image server (about 860 MB)
make compare    # compare all 30 pairs, results go to results/
make figures    # the pictures on this page, in results/gallery/
make lint       # ruff
```

## Credits

The scans are open access from the Allard Pierson, University of Amsterdam. They are fetched from its IIIF image
server and are not stored in this repository. The state descriptions are from *Koeman's Atlantes Neerlandici*,
edited by P. van der Krogt, as quoted in the Allard Pierson catalogue. The code is under the MIT licence.
