# Comparing two impressions of the same plate: methods from other fields

> **Question this file answers.** Other fields also compare two images of "the same thing" and find
> where they differ, despite distortion and appearance change. Has any of them already solved our
> problem, which is deciding same plate or re-engraved copy, same state or altered, and locating
> the alteration? What should we copy from them?
>
> **Research date:** 2026-09-24. **[VERIFIED]** means I read the source myself: the page, the paper,
> or at least its abstract. Where only the abstract was read, the tag says **[VERIFIED: abstract]**.
> **[UNVERIFIED]** means the claim comes only from a search snippet or from secondary reporting.
> Bibliographic metadata (authors, year, venue, DOI) for every numbered reference was checked
> against Semantic Scholar, Crossref, PubMed or arXiv. Nothing is cited from memory alone.
>
> **Already known and not re-surveyed** (see `plate-states.md` and the project notes): Hedges' print
> clock; Labedan et al. (arXiv:2502.01186) and ACCADIL; Cornet et al. (arXiv:2407.20876); Heinecke et
> al. (arXiv:2112.00290); Dutta/Bergel/Zisserman VISE chapbooks; Wang et al. DHQ 2025; Wilkinson et
> al. DHQ 2021; Johnson/Sethares chain lines; Shen/Aubry watermarks and ArtMiner; Davari et al.
> (arXiv:1712.04482); Sindel/Maier/Christlein registration; Pavo-López & Amaro-Mellado 2024.

---

## 0. Plain-language summary

**Yes, the core of the problem has been solved elsewhere, most closely by a stamp collector.** In
2015 the chemist and philatelist Robert Mustacich published a method for comparing two
high-resolution scans of postage stamps printed from engraved plates. He aligned them with a coarse
fit and then about 100 small local corrections for uneven paper shrinkage, matched their colours,
and subtracted one from the other. What was left showed re-entries, plate cracks and forgeries at the
scale of single lines [1]. His problem is ours on a smaller sheet: engraved plate, damp-printed paper
that shrank unevenly, and differences in inking. **Astronomy** supplies the second half. For thirty
years astronomers have subtracted two images of the same sky taken under different conditions. They
fit a "blur-and-brightness" correction between the two images first, so that only real changes
survive [2–5]. That is our problem of different ink density and wear. **Medical and pathology image
registration** supplies the tool for bending one gigapixel image smoothly onto another [16–19].
**Industrial print inspection** shows how to allow a small tolerance along every line edge so that
tiny misalignments are not reported as changes [23]. Deep-learning change detectors from satellite
imaging and foundation models (DINO, SAM) are **less useful** here. They are built to find
"a building appeared", work on 14–16-pixel patches, and need training labels we do not have. **What
is missing everywhere** is the combination: nobody has published it for copperplate maps, and
nobody has handled hand colouring and atlas folds together. The recipe exists; it has not been
assembled for our material.

---

## 1. Philately: the closest analogue

Stamps were printed from engraved (line-engraved, intaglio) plates. Collectors "plate" a stamp
(identify its position on the sheet and which plate printed it) and look for re-entries, retouches,
cracks and forgeries. This is the same question as ours, asked about 20 × 25 mm images.

### 1.1 Mustacich, "Digital Image Differencing of High Resolution Stamp Images" (2015) [1]: the key find

- **What it does** [VERIFIED, read the article as republished by the author]: it subtracts one
  1200 dpi stamp scan from another pixel by pixel, so that small differences across the whole stamp
  become visible.
- **Registration**: (1) a first-order translation and rotation, optimised with Nelder–Mead from
  "virtual corners" fitted to edge lines; (2) **second-order corrections**, where the image is
  divided into a grid of **typically 96 sections (12 × 8)** and each section gets its own x,y
  adjustment at a precision of hundredths of a pixel (about 21 µm per pixel). All corrections are
  accumulated and applied once to the raw image, with no repeated interpolation.
- **Paper shrinkage**: he measured that stamps expand by about **1 % when wetted** (200–300 µm).
  Stamps from the same sheet shrink almost uniformly. Comparing stamps from *different* sheets
  shows "large gradients attributable to differential post-printing shrinkage". His local
  second-order grid is what absorbs this.
- **Appearance**: colour is normalised with a quadratic Bézier tone curve that maps one image's
  values onto the other's. Uneven inking adds "substantial noise", but the design still aligned.
- **Findings**: re-entries and plate cracks invisible in the originals become apparent after
  subtraction. A forgery shows "large differences throughout", because a copy is displaced in small
  amounts everywhere. Across ten plate blocks, the distortion pattern for a given plate position was
  "extraordinary" in its consistency. That means the residual *displacement field* is itself a
  fingerprint of the plate.
- **Transfer to us**: almost complete. His grid of 96 local offsets is our grid of about 100
  blocks, but he uses the offsets **to warp and then subtract**, not as the change statistic. That
  is the step we are missing. His forgery observation (copy = small shifts everywhere; same plate =
  smooth field plus a clean difference) is a principled basis for our SAME PLATE verdict.
- **Does not fit / limits**: no hand colouring or folds; the colour correction is global, not local.
  It also relies on 1200 dpi scans with a controlled scanner mask. Scanner distortion was reduced to
  under 0.03 px, which our IIIF scans from unknown equipment will not match. It is a symposium paper,
  not peer-reviewed CV. Follow-up: Mustacich, "A Versatile Comparison of Stamps by High Resolution
  Image Differencing", Third International Symposium on Analytical Methods in Philately
  [UNVERIFIED, search snippet only; the symposium page returned 404].

### 1.2 Mustacich, "Seeing Only the Cancel" (2016) [6]

- [VERIFIED, read] He removes the stamp design so that only the overprinted postmark remains. The
  method reduces RGB to 12-bit colour and deletes every colour found in a reference area with no
  cancel on it. It fails when the inks are close in colour, and transparent black over red prints
  as "blackish-red".
- **Transfer**: this is the mirror image of our hand-colour problem, where we want to keep the black
  ink and drop the wash. The naive colour-palette approach is fragile, which argues for a proper
  optical-density separation (§9.2) over palette tricks.

### 1.3 Computer plating tools

- **GBPS "E-Gauge" / Penny Red Die I plating tool** [UNVERIFIED; the page returned 403, so this is
  a search snippet]: a computerised version of the classic Fisher-Brown measurement. You overlay a
  gauge on an 800 dpi scan and measure the positions of the hand-punched corner check letters. The
  letters were punched by hand, so their positions differ from plate to plate.
  **Transfer**: the philatelic principle matches our border numerals and lettering. The
  *hand-punched or hand-cut* elements are the discriminating evidence between plates, because the
  transferred or engraved design is repeated. Our "different plate" verdict should give weight to
  lettering and numerals, not only to line work.
- **RIT Penny Red plate identification** (Larry Rausch, presentation, c. 2017) [7] [VERIFIED, read
  the slides via reader]: a CNN classifier on three 224 × 224 corner/letter crops, 151 plates,
  **88.9 % accuracy (8,001 of 9,000 test scans)**. **Does not fit**: it is classification into known
  plates with thousands of labelled examples, not pairwise comparison, and we have tens of pairs.
- **PlateAI (David Fussichen)**: a multi-branch CNN trained on about 9,000 reference-plating scans
  plus about 10,000 collector scans [UNVERIFIED; the claim appears in a search snippet and could not
  be confirmed on stampplating.com or stampsmarter.org]. Same objection: supervised classification.

**Philately verdict:** the most useful philatelic work is Mustacich's registration-plus-subtraction,
not the ML plating tools.

---

## 2. Banknotes, security print, questioned documents

- **Berenguel Centeno et al., "Identity document and banknote security forensics: a survey"**
  (arXiv:1910.08993, 2019) [8] [VERIFIED: abstract]: it classifies security features into substrate,
  inks and printing. The abstract does not say whether registration-and-difference against a
  genuine reference is covered.
- The reference-comparison method in this field is "binarise the document and find discrepancies
  relative to a reference genuine document", measuring positions, sizes and shapes of elements
  [UNVERIFIED; search snippets from a patent and survey pages]. Counterfeits are caught mainly
  because non-intaglio processes (offset, inkjet) cannot reproduce intaglio line precision. **Does
  not fit**: our question is copper against copper (a re-engraved plate), not intaglio against
  offset, so process-signature features do not apply.
- **Printer forensics**, e.g. Mikkilineni et al., "Printer identification based on graylevel
  co-occurrence features" (SPIE 2005) [9] [VERIFIED: metadata only]: texture statistics identify
  the device, for example laser-printer banding. **Does not fit**: it identifies the machine, not a
  location-specific plate alteration.
- **Questioned-document examination** uses overlay and superimposition in general tools such as
  Photoshop and the Video Spectral Comparator [UNVERIFIED; snippets]. It offers no method beyond
  "align and overlay", which we already do.

**Verdict:** weakest of the surveyed fields for us. The operational practice is overlay with an
expert eye.

---

## 3. Analytical bibliography: type damage and collation

### 3.1 Print & Probability (Warren, G'Sell, Berg-Kirkpatrick et al.)

- Goal: attribute anonymous early modern English books to printers by finding the **same damaged
  type sort** in two books.
  - Warren, Williams, Rijhwani & G'Sell, "Damaged Type and *Areopagitica*'s Clandestine Printers",
    *Milton Studies* 62(1):1–47, 2020 [10] [VERIFIED: publisher abstract]: attributes the printing
    to Matthew Simmons and Thomas Paine.
  - Goyal et al., "A Probabilistic Generative Model for Typographical Analysis of Early Modern
    Printing", ACL 2020 [11] [VERIFIED: abstract]: a template model with **interpretable spatial
    perturbation latents** plus a separate latent for inking variation and noise. The inference
    network sees only the **residual** between the observation and the warped template.
  - Vogler et al., "Contrastive Attention Networks for Attribution of Early Modern Print", AAAI 2023
    [12] [VERIFIED: abstract]: contrastive metric learning that is sensitive to subtle glyph damage
    but robust to digitisation noise. The **scarce supervision problem is solved by synthesising
    bends, fractures and inking variation**.
- **Transfer**: (a) the idea of modelling geometry explicitly and letting *only the residual* carry
  the evidence is exactly warp-then-difference. (b) **Synthetic alteration injection**: to measure
  our detector's sensitivity to small alterations, paste synthetic numerals and ships and erase
  lines in one impression. That turns tens of labelled pairs into thousands of test cases.
- **Does not fit**: their unit is a segmented glyph a few dozen pixels in size, taken from thousands
  of repetitions. We have one large, non-repeating image per impression. Learned metric
  embeddings would need training data we do not have.

### 3.2 Optical and digital collation

- Mechanical and optical collators: Hinman, McLeod Portable, Hailey's Comet, Lindstrand Comparator.
  All use mirrors or superimposition so that the human eye fuses two pages [UNVERIFIED; search
  snippets. The Project MUSE census "Armadillos of Invention" exists but was not read].
- **Traherne Digital Collator** (Oxford Traherne with VGG; Dutta, Chung, Sridhar, Zisserman; v3.0,
  2026) [13] [VERIFIED, read project page and v2.0.5 user instructions]: it automatically aligns and
  overlays two page images, with toggle, transparent-overlay and two-colour visualisations. The
  manual documents a "Curved book" compare mode that **corrects for page curvature**. No paper
  describes its alignment model.
- **VGG Image Compare** (Sridhar, Dutta, Zisserman) [14] [VERIFIED, read]: a browser tool offering
  **similarity, affine and thin-plate-spline** transforms and difference visualisations.
- **Transfer**: this is the humanities-accepted form of our overlay view (cyan/red). A TPS option
  already exists in a tool bibliographers use, which is a useful argument for adoption. **Does not
  fit**: these are visualisers with no change statistic and no localisation output. The human is
  the detector, which is exactly the step we want to automate.

---

## 4. Astronomy: difference imaging with kernel matching

This is the most mature theory of "subtract two images of the same thing taken under different
conditions".

- **Alard & Lupton (1998), "A Method for Optimal Image Subtraction"**, ApJ 503:325 [2] [VERIFIED:
  abstract]. It fits a **convolution kernel** that makes the sharper image look like the blurrier
  one by linear least squares over *all pixels*, and **fits the differential background at the
  same time**. Residuals come out close to photon noise.
- **Alard (1999/2000), "Image subtraction with non-constant kernel solutions"** [3] [VERIFIED:
  abstract]: a **spatially varying kernel** at almost no extra cost, which also absorbs
  "differential rotation between the images".
- **Bramich (2008), "A new algorithm for difference image analysis"**, MNRAS Letters [4] [VERIFIED:
  abstract]: the kernel is a **free pixel array**, so it also **absorbs small residual
  misalignments** (translations need no resampling). It extends to spatially varying kernels by
  solving on a grid of subregions and interpolating, which is our block grid used for photometry.
- **Zackay, Ofek & Gal-Yam (2016), "Proper image subtraction" (ZOGY)**, ApJ 830:27 [5] [VERIFIED:
  abstract]: a closed-form optimal difference statistic with **white, uncorrelated noise**. It gives
  a **significance image** with credible detection thresholds, is symmetric in new versus reference,
  and has extensions "resilient to registration errors".
- **Hu et al., SFFT (2022), ApJ** [15] [VERIFIED: abstract]: kernel fitting in Fourier space, about
  10× faster, with spatially varying PSF, **photometric scaling and background**, fitted by splines.
  The authors warn that the flexible δ-basis "may also make it more prone to overfitting".
- **Transfer**:
  1. The *kernel* models ink spread, paper absorbency, pressure and scan blur. The *photometric
     scale* models ink density. The *background* models paper tone, foxing and wash. All three
     are fitted per tile and smoothly interpolated, and this is the formal version of "normalise
     ink density". It applies after geometric registration.
  2. A **significance (Scorr) map** instead of a raw difference gives a principled threshold, which
     is what our block statistic lacks for small alterations.
  3. The Bramich/SFFT overfitting warning carries over: a kernel that is too flexible can "explain
     away" a real alteration. Keep the kernel small (a few px) compared with the smallest alteration
     (a border numeral).
- **Does not fit**: astronomy assumes the sky is mostly empty with sparse point sources, so the
  "background-dominated noise" optimality of ZOGY does not hold for dense line work. Plate *wear*
  thins lines. That is not a convolution, so kernel matching will leave residuals along every worn
  line. Lower expectations: it cancels density and blur differences, not wear.

---

## 5. Remote-sensing change detection

### 5.1 Classical

- Singh (1989), "Digital change detection techniques using remotely-sensed data", *IJRS* [20]
  [VERIFIED: metadata]: the standard review of image differencing, ratioing and related methods.
- **MAD / IR-MAD**: Nielsen, Conradsen & Simpson (1998), *RSE* [21]; Nielsen (2007), "The
  Regularized Iteratively Reweighted MAD Method", *IEEE TIP* [22] [VERIFIED: metadata; content from
  domain knowledge, so treat the following as UNVERIFIED]: canonical-correlation differences between
  two multiband images are invariant to linear radiometric transforms of each band. The iterative
  reweighting fits the no-change relation on likely no-change pixels.
  **Transfer**: an interesting model for hand colour. Colour wash is roughly a per-region linear
  transform of the RGB bands, so IR-MAD-style *local* invariance could cancel it. In practice,
  separating the ink first (§9.2) is simpler.
- **Dai & Khorram (1998), "The effects of image misregistration on the accuracy of remotely sensed
  change detection"**, *IEEE TGRS* 36(5) [24] [VERIFIED: metadata; the finding comes from the search
  summary, UNVERIFIED]: registration better than **about 1/5 pixel** is needed for change-detection
  error under 10 %. **Transfer**: this explains why our block statistic is noisy near line edges.
  Pixel-level differencing of line art needs sub-pixel registration *or* an edge-tolerant
  comparison (§6).

### 5.2 Deep

- **FC-Siamese** (Daudt, Le Saux & Boulch, ICIP 2018) [25]; **BIT** (Chen, Qi & Shi, *IEEE TGRS*
  2021) [26]; **ChangeFormer** (Bandara & Patel, IGARSS 2022) [27] [VERIFIED: abstracts/metadata]:
  supervised Siamese networks on **co-registered** image pairs, trained on thousands of labelled
  building and land-cover changes.
- **ChangeDINO** (Cheng & Hsu, 2025, ISPRS Annals) [28] [VERIFIED: abstract]: fuses frozen DINOv3
  features to gain robustness "under illumination variation, off-nadir views, and scarce labels".
  It is still supervised.
- **AnyChange / Segment Any Change** (Zheng, Zhong, Zhang & Ermon, NeurIPS 2024) [29] [VERIFIED:
  abstract]: zero-shot change detection by "bitemporal latent matching" in SAM's latent space,
  object-centric.
- **Transfer**: the idea that pretrained semantic features ignore illumination and season carries
  over, since hand colour is our "season". **Does not fit**: (1) all of these networks need labels
  or detect *objects* (buildings), while our changes are a few strokes. (2) They assume
  co-registration is done. (3) Backbone patch size (14–16 px) is coarser than a hairline, and SAM
  segments regions, not line strokes. Useful at most as a **coarse detector of large re-engraved
  regions**, not for numerals.

---

## 6. Industrial and print inspection

- **Golden-template / variation model** (MVTec HALCON) [23] [VERIFIED, read operator reference v13]:
  from an ideal image and a **variation image** it computes two threshold images using an
  `AbsThreshold` (minimum grey-level difference) and a `VarThreshold` (a factor times the local
  variation). In the single-reference "direct" mode the documented example builds the variation
  image with **`sobel_amp` of the reference**. The tolerance is therefore proportional to edge
  strength, so misalignment along edges is not flagged. The exact comparison formula did not render
  on the page.
  **Transfer, cheap and direct**: build our variation image from the gradient magnitude of the
  registered reference impression and flag only pixels where |A − B| > max(abs, k·|∇A|). This removes
  edge-misregistration residuals without losing interior changes. MVTec also describes
  **anisotropic shape-based matching** with local models of variable scaling for distorted print
  [UNVERIFIED; snippet].
- **Liu et al. (2023), "Printing Defect Detection Based on Scale-Adaptive Template Matching and
  Image Alignment"**, *Sensors* 23:4414 [30] [VERIFIED: abstract]: CNN-feature template matching,
  then alignment and difference. Nothing beyond our pipeline.
- **Anomaly detection**: PatchCore (Roth et al., CVPR 2022) [31], PaDiM (Defard et al., ICPR-W 2021)
  [32], EfficientAD (Batzner et al., WACV 2024) [33] [VERIFIED: abstracts]. These learn "normal"
  from many defect-free samples of a product. PaDiM explicitly evaluates on **non-aligned** data.
  - **RegAD** (Huang et al., ECCV 2022) [34] [VERIFIED: abstract]: few-shot anomaly detection that
    uses **registration** as a proxy task and compares registered features of the test image and
    its support images.
  - **AnomalyDINO** (Damm et al., WACV 2025) [35] [VERIFIED: abstract]: training-free, **one-shot**
    anomaly detection by patch-level nearest neighbours in DINOv2 space.
  - **Transfer**: AnomalyDINO or RegAD is the only learned approach that fits our data regime (one
    reference, no training). **Does not fit well**: the MVTec benchmarks have defects that are
    semantic (scratches, missing parts) on textureless objects. Our "normal" is dense, self-similar
    hatching, where a shifted numeral may look perfectly normal at patch level. Patch
    nearest-neighbour search has no idea of *position*, so an alteration that reuses common line
    patterns (a re-cut cartouche) may be invisible. Treat it as an experiment, not a replacement.

---

## 7. Registration: matchers, flows, deformable models

### 7.1 Learned sparse and dense matchers (all [VERIFIED: abstract/metadata])

| Method | Year / venue | What matters for us |
|---|---|---|
| SuperPoint [36] + LightGlue [37] | CVPRW 2018 / ICCV 2023 | fast sparse matching; adaptive depth |
| DISK [38] | NeurIPS 2020 | learned keypoints |
| LoFTR [39] | CVPR 2021 | detector-free; dense matches "in low-texture areas" |
| DKM [40] | CVPR 2023 | dense kernelised matching |
| RoMa [41] | CVPR 2024 | frozen DINOv2 coarse features + ConvNet fine features; the authors state DINOv2 features are "inherently coarse" |
| MASt3R [42] | ECCV 2024 | matching grounded in 3D pointmaps |
| MatchAnything [43] | arXiv 2025 | cross-modality pre-training |
| UFM [44] | NeurIPS 2025 | unified flow + wide-baseline; "62 % less error and 6.7× faster" than RoMa |
| RoMa v2 [45] | arXiv 2025 | DINOv3, two-stage match-then-refine, custom CUDA refinement kernel |

**Honest assessment:** these methods solve *wide-baseline 3D* matching: viewpoint, illumination,
occlusion. Our geometry is 2D, nearly identical, and smooth. SIFT + RANSAC already finds the global
model at about 0.05 % residual. What we lack is **dense, sub-pixel, smooth** correspondence at
full resolution, and these networks run at reduced resolution on coarse features. The one useful
by-product is the **per-pixel certainty map** (RoMa, UFM "co-visible" pixels): regions that cannot
be matched are candidate alterations. Using them is optional, not a priority.

### 7.2 Optical flow

- **DIS** (Kroeger et al., ECCV 2016) [46] [VERIFIED: abstract]: inverse-compositional patch search
  plus multi-scale aggregation plus variational refinement, running at hundreds of Hz on one CPU
  core at 1024 × 436. It is in OpenCV (`cv2.DISOpticalFlow`). **Good fit** for a residual dense
  field after the global warp: the residual displacements are a few pixels, with texture everywhere.
- **RAFT** (Teed & Deng, ECCV 2020) [47] [VERIFIED: metadata]: higher accuracy, GPU and memory
  heavy; it would have to run tiled.
- Caveat for both: flow is **too flexible**. It will warp a moved numeral onto its old position and
  hide the change. Use flow only to *estimate* the field, then **project it onto a smooth model**
  (B-spline or TPS) and difference with the smooth warp. The residual between the raw and smooth
  flow is itself a change signal.

### 7.3 Parametric deformable registration (medical and pathology)

- **Thin-plate splines**: Bookstein (1989), *IEEE PAMI* [16] [VERIFIED: metadata]. Fit to our
  existing ZNCC block offsets; this is exactly what VGG Image Compare offers [14].
- **B-spline free-form deformation**: Rueckert et al. (1999), *IEEE TMI* [17]; **elastix**: Klein et
  al. (2010), *IEEE TMI* [18] [VERIFIED: metadata]. It has a control-point spacing parameter that
  **directly encodes our physical prior**: paper shrinkage is smooth over centimetres, so control
  points every few hundred pixels cannot bend a single numeral.
- **VoxelMorph** (Balakrishnan et al., *IEEE TMI* 2019) [19] [VERIFIED: abstract]: a learned
  deformation field trained on many pairs. **Does not fit**: its benefit is speed across large
  datasets, and we have tens of pairs.
- **Whole-slide pathology registration** is the closest registration analogue: gigapixel images,
  non-rigid tissue deformation, and different stains giving a different appearance of the same
  structure.
  - **VALIS** (Gatenbee et al., *Nat. Commun.* 2023) [48] [VERIFIED: abstract]: a Python pipeline
    for rigid-then-non-rigid registration of multi-gigapixel WSIs and warping at full resolution.
  - **ANHIR challenge** (Borovec et al., *IEEE TMI* 2020) [49] [VERIFIED: metadata]: a benchmark
    for non-rigid histology registration.
  - **Transfer**: VALIS already solves the *engineering* problem of "fit at low resolution, apply
    the deformation to a 40 MP+ image".

---

## 8. Art history and conservation: impressions and states

- The known Sindel/Christlein work (not re-surveyed) remains the art-history state of the art for
  registration.
- **Ukiyo-e**: Khan & van Noord (BMVC 2024) [50] [VERIFIED, read the passage]: in a 175k-print
  dataset, "reprints, later editions using re-carved blocks, or (colour-faded) copies from the same
  woodblock" are grouped as duplicates at **cosine similarity > 0.94**, with no attempt to tell a
  re-carved block from the same block. **Relevance**: it confirms the problem is recognised in
  another print tradition and **not solved there**. Global embeddings cannot separate "same block"
  from "re-carved copy".
- **Rembrandt**: the WIRE project (Cornell) used watermarks, not plate comparison, to sequence
  impressions [UNVERIFIED; snippet]. It belongs to the Johnson/Sethares line, which is already
  known.
- No computational study of Dürer impression sequences or engraving plate wear was found (§11).

---

## 9. Foundation models (DINOv2/v3, SAM): help or hurt?

- DINOv2 (Oquab et al., TMLR 2024) [51] and DINOv3 (Siméoni et al., 2025) [52] [VERIFIED:
  abstracts]. DINOv3's "Gram anchoring" targets dense-feature degradation, so its dense features are
  better than DINOv2's.
- **Help**: robust to appearance (colour, paper tone). Useful for (a) coarse initial matching when
  sheets are cropped differently; (b) detecting large re-engraved regions (ChangeDINO-style, [28]);
  (c) one-shot anomaly scoring (AnomalyDINO [35]).
- **Hurt**: the RoMa authors, who build on DINOv2, call its features "inherently coarse" [41] and
  need a separate ConvNet for fine localisation. A 14–16 px patch at our scale is several
  hatching lines. A re-engraved numeral changes a fraction of a patch, and semantic invariance is
  designed to *ignore* exactly that kind of low-level stroke change. Expect them to miss small
  alterations and to see copies and originals as identical, which is the ukiyo-e experience [50].
- **Verdict**: use them only as auxiliary coarse signals. Do not use them for the SAME PLATE verdict
  or for fine localisation.

### 9.2 Colour separation (from histopathology)

- **Colour deconvolution**: Ruifrok & Johnston (2001), *Anal. Quant. Cytol. Histol.* 23(4):291–299
  [53]; **stain normalisation**: Macenko et al. (ISBI 2009) [54] [VERIFIED: metadata]. Convert RGB to
  optical density, OD = −log(I/I₀). In OD space transparent layers **add linearly**, so the image can
  be separated into per-stain concentration channels.
- **Transfer**: watercolour wash over printed ink is the same physics as two stains on a slide. It is
  transparent and subtractive, and it adds in OD. Estimate a black-ink vector (near-neutral, high OD
  in all channels) and one or two wash vectors per sheet, as Macenko does from the OD histogram.
  Then compare only the **ink concentration channel**. Background paper tone becomes I₀, estimated
  locally. This is better grounded than Mustacich's palette trick [6] and would remove most colour
  false positives. Simple fallback: max-OD channel, or Sauvola binarisation (Sauvola & Pietikäinen,
  *Pattern Recognition* 2000) [55] on the ink channel.
- **Does not fit fully**: opaque bodycolour, gold heightening, or wash dense enough to saturate the
  ink will still leave residuals, so mask pixels where the wash OD exceeds a threshold.

---

## 10. Recommendation for our pipeline (ranked)

Failure key: **C** = colour/fold false positives, **S** = missed small alterations,
**L** = coarse localisation.

| # | Change | Source | C | S | L |
|---|---|---|---|---|---|
| 1 | **Warp with a smooth dense field, then difference pixels, instead of voting blocks.** Fit a TPS or B-spline field (control spacing ≫ numeral size, e.g. a few hundred px at full resolution) to the existing ZNCC block offsets, made denser (e.g. 20×20 → 50×50 blocks) or refined by DIS flow projected onto the spline. Warp B at full resolution once; compute a per-pixel difference. | Mustacich [1]; Rueckert/elastix [17,18]; Bookstein [16]; DIS [46]; VALIS [48] | ~ | **++** | **++** |
| 2 | **Compare ink, not RGB.** Per sheet: OD transform, estimate ink and wash vectors (Macenko), keep the ink channel; mask saturated-wash pixels. | Ruifrok & Johnston [53]; Macenko [54]; cf. Mustacich [6] | **++** | + | ~ |
| 3 | **Photometric/kernel matching before subtraction.** Per tile: fit a small convolution kernel + gain + background (Alard–Lupton/Bramich) on the ink channel, interpolate smoothly, and difference. Report a noise-normalised significance map (ZOGY-style). | [2–5, 15] | + | **+** | + |
| 4 | **Edge-tolerant threshold.** Flag a pixel only if \|A−B\| > max(t_abs, k·\|∇A\|), or, for binarised ink, flag B-ink with no A-ink within r px (and vice versa). Output connected components as boxes: "ink only in A" = removed line, "only in B" = added line. | HALCON variation model [23]; Dai & Khorram [24] | + | + | **++** |
| 5 | **Fold and edges: mask or split.** A crease is a discontinuity a smooth spline cannot model. Either mask a band along the fold, or register the left and right halves with independent smooth fields. | pathology/medical practice (no single source; our inference) | **++** (fold) | ~ | ~ |
| 6 | **Re-base the SAME PLATE verdict on the residual displacement field.** Same plate gives a field that a smooth spline explains, with small, spatially clustered difference components. A re-engraved copy gives "small shifts everywhere" (non-smooth residual flow and ubiquitous difference). Use the RMS of flow minus the spline fit as the statistic. | Mustacich forgery finding [1] | ~ | ~ | ~ |
| 7 | **Measure sensitivity with synthetic alterations.** Inject synthetic numerals, erase lines, paste a ship into one impression of real same-state pairs, and plot detection rate against alteration size. This turns tens of pairs into a calibration curve. | Vogler et al. synthesis [12] | – | (evaluation) | – |
| 8 | *Optional*: RoMa v2 / UFM certainty maps or AnomalyDINO on registered tiles as a second opinion for large re-engraved regions. Not a replacement: too coarse for numerals. | [44, 45, 35] | + | – | – |

**Expected net effect:** #2 + #5 address the measured colour/fold false positives. #1 + #3 + #4
turn the overlay, which already *shows* the numerals, into a statistic that *detects* them, and
localise at stroke resolution rather than block resolution. #6 makes the verdict principled. #7
makes all of it measurable. Items 1–5 need no deep learning and no training data. Everything is
available in OpenCV, SciPy, elastix or SimpleITK.

**Main risk:** over-flexible warps (flow, fine B-spline, large kernels) absorb real alterations.
Every flexible step must have a flexibility budget set by physics: paper shrinkage is smooth over
centimetres, ink spread is a few pixels. Validate the budget with #7.

---

## 11. Searched, not found

- **A peer-reviewed CV paper on computer-assisted stamp plating or re-entry detection.** Beyond
  Mustacich (symposium proceedings) and hobbyist or society tools, none was found. PlateAI's primary
  documentation could not be reached.
- **Traherne Digital Collator alignment algorithm.** No paper; only the user docs, which confirm
  curvature correction.
- **Computational comparison of impressions of Rembrandt/Dürer engravings for state or wear** (other
  than the known Johnson/Sethares and Sindel work). Searches returned only watermark projects and
  general printmaking pages.
- **Ukiyo-e same-block against re-carved-block discrimination.** Only the cosine-similarity duplicate
  grouping in [50].
- **Banknote intaglio registration-and-difference papers.** Only patents and the survey [8]; the
  survey's full text was not read.
- **A citable primary source for Change Vector Analysis (Malila 1980).** The Crossref query failed,
  so CVA is mentioned only through the Singh review [20].
- **HALCON variation-model exact formula** (did not render) and **HOTPANTS** (Becker) primary
  reference, both not verified. HOTPANTS is omitted.
- **GBPS E-Gauge page** (403) and **Analytical Philately 2017 symposium page** (404).

---

## 12. Bibliography

1. Mustacich, R. V. (2015). "Digital Image Differencing of High Resolution Stamp Images." *Proc. 2nd Int. Symposium on Analytical Methods in Philately*, Itasca IL, pp. 57–72. Online: https://www.battleship-revenues.com/articles/imgsub.html
2. Alard, C. & Lupton, R. H. (1998). "A Method for Optimal Image Subtraction." *ApJ* 503. doi:10.1086/305984. arXiv:astro-ph/9712287
3. Alard, C. (1999/2000). "Image subtraction with non-constant kernel solutions." arXiv:astro-ph/9903111
4. Bramich, D. M. (2008). "A new algorithm for difference image analysis." *MNRAS Letters*. doi:10.1111/j.1745-3933.2008.00464.x. arXiv:0802.1273
5. Zackay, B., Ofek, E. O. & Gal-Yam, A. (2016). "Proper image subtraction — optimal transient detection, photometry, and hypothesis testing." *ApJ* 830:27. doi:10.3847/0004-637X/830/1/27. arXiv:1601.02655
6. Mustacich, R. V. (2016). "Seeing Only the Cancel." *The American Revenuer* 69(3):79–82. http://www.battleship-revenues.com/articles/seecxl.html
7. Rausch, L. (c. 2017). "Plate Identification of Great Britain Penny Red by Deep Computer Scanning" (RIT; slides). http://rpastamps.org/presentations/pennyredproject.pdf
8. Berenguel Centeno, A., Ramos Terrades, O., Lladós Canet, J. & Cañero Morales, C. (2019). "Identity document and banknote security forensics: a survey." arXiv:1910.08993
9. Mikkilineni, A. K., Chiang, P.-J., Ali, G. N., Chiu, G. T.-C. et al. (2005). "Printer identification based on graylevel co-occurrence features for security and forensic applications." *Proc. SPIE*. doi:10.1117/12.593796
10. Warren, C. N., Williams, P., Rijhwani, S. & G'Sell, M. (2020). "Damaged Type and *Areopagitica*'s Clandestine Printers." *Milton Studies* 62(1):1–47. https://muse.jhu.edu/article/748968
11. Goyal, K., Dyer, C., Warren, C. N., G'Sell, M. & Berg-Kirkpatrick, T. (2020). "A Probabilistic Generative Model for Typographical Analysis of Early Modern Printing." *ACL 2020*. doi:10.18653/v1/2020.acl-main.266. arXiv:2005.01646
12. Vogler, N., Goyal, K., Reddy, K. PV, Pertseva, E., Lemley, S. V., Warren, C. N., G'Sell, M. & Berg-Kirkpatrick, T. (2023). "Contrastive Attention Networks for Attribution of Early Modern Print." *AAAI 2023*. arXiv:2306.07998. Project: http://printprobability.org/
13. Dutta, A., Chung, J. S., Sridhar, P. & Zisserman, A. (2026). *Traherne Digital Collator* v3.0 (software). https://www.robots.ox.ac.uk/~vgg/software/traherne/ ; user instructions v2.0.5: https://oxfordtraherne.web.ox.ac.uk/sitefiles/traherne-digital-collator-user-instructions-v2.0.5.pdf
14. Sridhar, P., Dutta, A. & Zisserman, A. *Image Compare* (software, VGG Oxford). https://vgg.gitlab.io/image-compare/
15. Hu, L., Wang, L., Chen, X. & Yang, J. (2022). "Image Subtraction in Fourier Space." *ApJ*. doi:10.3847/1538-4357/ac7394. arXiv:2109.09334
16. Bookstein, F. L. (1989). "Principal warps: thin-plate splines and the decomposition of deformations." *IEEE TPAMI*. doi:10.1109/34.24792
17. Rueckert, D., Sonoda, L. I., Hayes, C., Hill, D. L. G. et al. (1999). "Nonrigid registration using free-form deformations: application to breast MR images." *IEEE TMI*. doi:10.1109/42.796284
18. Klein, S., Staring, M., Murphy, K., Viergever, M. A. & Pluim, J. P. W. (2010). "elastix: A Toolbox for Intensity-Based Medical Image Registration." *IEEE TMI*. doi:10.1109/TMI.2009.2035616
19. Balakrishnan, G., Zhao, A., Sabuncu, M. R., Guttag, J. & Dalca, A. V. (2019). "VoxelMorph: A Learning Framework for Deformable Medical Image Registration." *IEEE TMI*. doi:10.1109/TMI.2019.2897538. arXiv:1809.05231
20. Singh, A. (1989). "Digital change detection techniques using remotely-sensed data." *Int. J. Remote Sensing*. doi:10.1080/01431168908903939
21. Nielsen, A. A., Conradsen, K. & Simpson, J. J. (1998). "Multivariate Alteration Detection (MAD) and MAF Postprocessing in Multispectral, Bitemporal Image Data." *Remote Sensing of Environment*. doi:10.1016/S0034-4257(97)00162-4
22. Nielsen, A. A. (2007). "The Regularized Iteratively Reweighted MAD Method for Change Detection in Multi- and Hyperspectral Data." *IEEE TIP*. doi:10.1109/TIP.2006.888195
23. MVTec. HALCON Operator Reference v13: `prepare_variation_model`, `prepare_direct_variation_model`, `compare_variation_model`. https://www.mvtec.com/doc/halcon/13/en/prepare_direct_variation_model.html
24. Dai, X. & Khorram, S. (1998). "The effects of image misregistration on the accuracy of remotely sensed change detection." *IEEE TGRS* 36(5):1566–1577. doi:10.1109/36.718860
25. Daudt, R. C., Le Saux, B. & Boulch, A. (2018). "Fully Convolutional Siamese Networks for Change Detection." *ICIP 2018*. doi:10.1109/ICIP.2018.8451652. arXiv:1810.08462
26. Chen, H., Qi, Z. & Shi, Z. (2021). "Remote Sensing Image Change Detection With Transformers." *IEEE TGRS*. doi:10.1109/TGRS.2021.3095166. arXiv:2103.00208
27. Bandara, W. G. C. & Patel, V. M. (2022). "A Transformer-Based Siamese Network for Change Detection." *IGARSS 2022*. doi:10.1109/IGARSS46834.2022.9883686. arXiv:2201.01293
28. Cheng, C.-H. & Hsu, C.-C. (2025). "ChangeDINO: DINOv3-Driven Building Change Detection in Optical Remote Sensing Imagery." *ISPRS Annals*. arXiv:2511.16322
29. Zheng, Z., Zhong, Y., Zhang, L. & Ermon, S. (2024). "Segment Any Change." *NeurIPS 2024*. arXiv:2402.01188
30. Liu, X., Li, Y., Guo, Y. & Zhou, L. (2023). "Printing Defect Detection Based on Scale-Adaptive Template Matching and Image Alignment." *Sensors* 23:4414. doi:10.3390/s23094414
31. Roth, K., Pemula, L., Zepeda, J., Schölkopf, B., Brox, T. & Gehler, P. (2022). "Towards Total Recall in Industrial Anomaly Detection" (PatchCore). *CVPR 2022*. doi:10.1109/CVPR52688.2022.01392. arXiv:2106.08265
32. Defard, T., Setkov, A., Loesch, A. & Audigier, R. (2021). "PaDiM: a Patch Distribution Modeling Framework for Anomaly Detection and Localization." *ICPR Workshops*. doi:10.1007/978-3-030-68799-1_35. arXiv:2011.08785
33. Batzner, K., Heckler, L. & König, R. (2024). "EfficientAD: Accurate Visual Anomaly Detection at Millisecond-Level Latencies." *WACV 2024*. doi:10.1109/WACV57701.2024.00020. arXiv:2303.14535
34. Huang, C., Guan, H., Jiang, A., Zhang, Y. et al. (2022). "Registration based Few-Shot Anomaly Detection." *ECCV 2022*. arXiv:2207.07361
35. Damm, S., Laszkiewicz, M., Lederer, J. & Fischer, A. (2025). "AnomalyDINO: Boosting Patch-based Few-Shot Anomaly Detection with DINOv2." *WACV 2025*. doi:10.1109/WACV61041.2025.00136. arXiv:2405.14529
36. DeTone, D., Malisiewicz, T. & Rabinovich, A. (2018). "SuperPoint: Self-Supervised Interest Point Detection and Description." *CVPRW 2018*. doi:10.1109/CVPRW.2018.00060. arXiv:1712.07629
37. Lindenberger, P., Sarlin, P.-E. & Pollefeys, M. (2023). "LightGlue: Local Feature Matching at Light Speed." *ICCV 2023*. doi:10.1109/ICCV51070.2023.01616. arXiv:2306.13643
38. Tyszkiewicz, M., Fua, P. & Trulls, E. (2020). "DISK: Learning local features with policy gradient." *NeurIPS 2020*. arXiv:2006.13566
39. Sun, J., Shen, Z., Wang, Y., Bao, H. & Zhou, X. (2021). "LoFTR: Detector-Free Local Feature Matching with Transformers." *CVPR 2021*. doi:10.1109/CVPR46437.2021.00881. arXiv:2104.00680
40. Edstedt, J., Athanasiadis, I., Wadenbäck, M. & Felsberg, M. (2023). "DKM: Dense Kernelized Feature Matching for Geometry Estimation." *CVPR 2023*. doi:10.1109/CVPR52729.2023.01704. arXiv:2202.00667
41. Edstedt, J., Sun, Q., Bökman, G., Wadenbäck, M. & Felsberg, M. (2024). "RoMa: Robust Dense Feature Matching." *CVPR 2024*. doi:10.1109/CVPR52733.2024.01871. arXiv:2305.15404
42. Leroy, V., Cabon, Y. & Revaud, J. (2024). "Grounding Image Matching in 3D with MASt3R." *ECCV 2024*. arXiv:2406.09756
43. He, X., Yu, H., Peng, S., Tan, D. et al. (2025). "MatchAnything: Universal Cross-Modality Image Matching with Large-Scale Pre-Training." arXiv:2501.07556
44. Zhang, Y., Keetha, N., Lyu, C., Jhamb, B. et al. (2025). "UFM: A Simple Path towards Unified Dense Correspondence with Flow." *NeurIPS 2025*. arXiv:2506.09278
45. Edstedt, J., Nordström, D., Zhang, Y., Bökman, G. et al. (2025). "RoMa v2: Harder Better Faster Denser Feature Matching." arXiv:2511.15706
46. Kroeger, T., Timofte, R., Dai, D. & Van Gool, L. (2016). "Fast Optical Flow Using Dense Inverse Search." *ECCV 2016*. doi:10.1007/978-3-319-46493-0_29. arXiv:1603.03590
47. Teed, Z. & Deng, J. (2020). "RAFT: Recurrent All-Pairs Field Transforms for Optical Flow." *ECCV 2020*. doi:10.1007/978-3-030-58536-5_24. arXiv:2003.12039
48. Gatenbee, C. D., Baker, A.-M., Prabhakaran, S., Swinyard, O. et al. (2023). "Virtual alignment of pathology image series for multi-gigapixel whole slide images" (VALIS). *Nature Communications*. doi:10.1038/s41467-023-40218-9
49. Borovec, J., Kybic, J., Arganda-Carreras, I., Sorokin, D. V. et al. (2020). "ANHIR: Automatic Non-Rigid Histological Image Registration Challenge." *IEEE TMI*. doi:10.1109/TMI.2020.2986331
50. Khan, S. J. & van Noord, N. (2024). "Stylistic Multi-Task Analysis of Ukiyo-e Woodblock Prints." *BMVC 2024*. arXiv:2410.12379
51. Oquab, M., Darcet, T., Moutakanni, T., Vo, H. V. et al. (2024). "DINOv2: Learning Robust Visual Features without Supervision." *TMLR*. arXiv:2304.07193
52. Siméoni, O., Vo, H. V., Seitzer, M., Baldassarre, F. et al. (2025). "DINOv3." arXiv:2508.10104
53. Ruifrok, A. C. & Johnston, D. A. (2001). "Quantification of histochemical staining by color deconvolution." *Anal. Quant. Cytol. Histol.* 23(4):291–299. PMID:11531144
54. Macenko, M., Niethammer, M., Marron, J. S., Borland, D. et al. (2009). "A method for normalizing histology slides for quantitative analysis." *ISBI 2009*. doi:10.1109/ISBI.2009.5193250
55. Sauvola, J. & Pietikäinen, M. (2000). "Adaptive document image binarization." *Pattern Recognition*. doi:10.1016/S0031-3203(99)00055-2
56. Zitová, B. & Flusser, J. (2003). "Image registration methods: a survey." *Image and Vision Computing*. doi:10.1016/S0262-8856(03)00137-9 (general background; not discussed above)
