# Where the method comes from

None of the four steps is new on its own. Other fields compare two copies of the same thing all the time,
and each step here copies one of their tricks. What had not been done was to put them together for
engraved maps, where the paper has shrunk and every copy is coloured differently.

## Stamp collecting

Engraved postage stamps come off plates too, and collectors want to know exactly which plate a stamp came
from and whether it was re-engraved. Robert Mustacich scanned stamps at 1200 dpi, lined two of them up,
cut the pair into a grid of 96 cells, and let each cell shift a little on its own to allow for the paper
shrinking (he measured about one percent when wet). Then he matched the brightness and subtracted one scan
from the other. Re-engraved lines and plate cracks were what was left. Our step 2 is his grid made smooth,
and our step 4 is his subtraction.

- R. V. Mustacich, "Digital Image Differencing of High Resolution Stamp Images", *Proceedings of the 2nd
  International Symposium on Analytical Methods in Philately* (2015), pp. 57-72.
  https://www.battleship-revenues.com/articles/imgsub.html

## Astronomy

To find a new star, astronomers subtract last month's picture of the sky from tonight's. The two pictures
never match in sharpness or brightness, so before subtracting they fit a small correction that makes one
look like the other. Our step 3 does the simplest version of that: a brightness correction, fitted tile by
tile, using only the lines both copies share.

- C. Alard and R. H. Lupton, "A Method for Optimal Image Subtraction", *The Astrophysical Journal* 503
  (1998). doi:10.1086/305984
- D. M. Bramich, "A new algorithm for difference image analysis", *MNRAS Letters* (2008).
  doi:10.1111/j.1745-3933.2008.00464.x

## Pathology

Tissue slides are enormous images, the tissue stretches when it is cut, and each slide is stained in
different colours. Pathologists separate one stain from another by the way each absorbs light. Engraving
ink and watercolour are the same kind of problem. Our step 1 is a much simpler cousin: ink darkens all
three colour channels and a wash does not, and a painted area is much wider than an engraved line, so both
can be removed without a colour model.

- A. C. Ruifrok and D. A. Johnston, "Quantification of histochemical staining by color deconvolution",
  *Analytical and Quantitative Cytology and Histology* 23 (2001), 291-299.
- M. Macenko and others, "A method for normalizing histology slides for quantitative analysis", *ISBI*
  (2009). doi:10.1109/ISBI.2009.5193250

## Print inspection

Factories check printed circuit boards and packaging by comparing each one with a perfect reference. A
line that is a pixel off is not a defect, so the check allows a small tolerance near every edge. Step 4
uses the same idea: ink only counts as missing if there is none within about eight pixels in the other copy.

- MVTec HALCON operator reference, `compare_variation_model`.
  https://www.mvtec.com/doc/halcon/13/en/prepare_direct_variation_model.html

## The optical flow

The smooth warp in step 2 starts from DIS optical flow, a fast way to estimate how every point in one image
has moved in the other. We then smooth it heavily so it can follow the paper but not an engraver's changes.

- T. Kroeger, R. Timofte, D. Dai and L. Van Gool, "Fast Optical Flow Using Dense Inverse Search", *ECCV*
  (2016). doi:10.1007/978-3-319-46493-0_29

## People who have asked for this

- M. F. Pavo-López and J.-L. Amaro-Mellado compared the plates of the Rome editions of Ptolemy's
  *Geography* by eye, found seven states nobody had recorded, and ended by asking for automatic
  image-change detection. *ISPRS International Journal of Geo-Information* 13 (2024), 195.
  doi:10.3390/ijgi13060195
- S. B. Hedges measured how copper plates wear, about one to two thousandths of a millimetre a year, and
  named aligning the two images as the obstacle to comparing prints directly. *Proceedings of the Royal
  Society A* 462 (2006). doi:10.1098/rspa.2006.1736
- P. Labedan and others do this comparison for coins struck from the same die. Coins are rigid, so one
  global fit is enough; paper is not, which is why step 2 exists. arXiv:2502.01186 (2025).
