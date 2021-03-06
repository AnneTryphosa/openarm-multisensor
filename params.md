# Optical Flow Hyperparameters

This document contains a description of all hyperparameters used in optical flow tracking, as well as a list of all values used for each tracking algorithm in this codebase's associated [publication](https://people.eecs.berkeley.edu/~lhallock/publication/hallock2020biorob/).

## Hyperparameter descriptions

Included below are descriptions of all hyperparameters used in the four available optical flow tracking algorithms. Note that each parameter description appears only once, but later algorithms may use parameters described in an earlier section; a full list of parameters used be each algorithm is available [here](#publication-values).

### Naive Lucas&ndash;Kanade (LK)

`LK_WINDOW` (*int*): window size for Lucas&ndash;Kanade

`PYR_LEVEL` (*int*): level of image pyramiding for Lucas&ndash;Kanade

`FIX_TOP` (*bool*): whether to maintain the top set of contour points across tracking (mitigates downward drift)

`RESET_FREQUENCY` (*int*): how often to reset contour points to ground truth (used to analyze when and how often tracking drift occurs; set to number larger thans number of frames if no resets are required)

### Feature-Refined Lucas&ndash;Kanade (FRLK)

`BLOCK_SIZE` (*int*): block size used for Sobel derivative kernel in Shi&ndash;Tomasi corner scoring

`POINT_FRAC` (*float*): fraction of top points (based on Shi&ndash;Tomasi corner score) to keep during FRLK tracking

### Bilaterally-Filtered Lucas&ndash;Kanade (BFLK)

`COARSE_DIAM` (*int*): bilateral filter diameter for coarse (i.e., less aggressive) filter

`COARSE_SIGMA_COLOR` (*int*): bilateral filter color sigma parameter for coarse (i.e., less aggressive) filter

`COARSE_SIGMA_SPACE` (*int*): bilateral filter spatial sigma parameter for coarse (i.e., less aggressive) filter

`FINE_DIAM` (*int*): bilateral filter diameter for fine (i.e., more aggressive) filter

`FINE_SIGMA_COLOR` (*int*): bilateral filter color sigma parameter for fine (i.e., more aggressive) filter

`FINE_SIGMA_SPACE` (*int*): bilateral filter spatial sigma parameter for fine (i.e., more aggressive) filter

`PERCENT_FINE` (*float*): fraction of points (ordered by Shi&ndash;Tomasi corner score) to track using fine bilateral filter

`PERCENT_COARSE` (*float*): fraction of points (ordered by Shi&ndash;Tomasi corner score) to track using coarse bilateral filter

### Supporter-Based Lucas&ndash;Kanade (SBLK)

`DISPLACEMENT_WEIGHT` (*float*): offset (alpha) used in weighting function for supporter points

`QUALITY_LEVEL` (*float*): quality level of supporter points chosen via Shi&ndash;Tomasi corner detection

`MIN_DISTANCE` (*int*): minimum pixel distance between supporters chosen via Shi&ndash;Tomasi corner detection

`MAX_CORNERS` (*int*): maximum number of supporter points chosen by Shi&ndash;Tomasi corner detection

`FINE_THRESHOLD` (*float*): fraction of points to track without using supporter points (i.e., to track using pure Lucas&ndash;Kanade)

`UPDATE_RATE` (*float*): update rate for exponential moving average

`NUM_BOTTOM` (*int*): number of (spatially) bottom-most contour points to keep (used to ensure points along the entire contour are tracked)

## Publication values

The following sections contain the tuned hyperparameter values used in publication. Note that for more sophisticated algorithms (BFLK and SBLK), both per-trial "tuned" and "untuned" runs were performed. The charts below contain the values used in "tuned" runs; for "untuned" runs, the values tuned on the *Sub1* trial were used (bolded columns below).

All values below were tuned on subject data at waypoint 5 (~69&deg; elbow flexion, as measured from full distinction). This is only a meaningful distinction on *Sub1* data, as only one trial was collected from all other subjects. For additional *Sub1* trials (included in the data release but not publication), the same *Sub1* values below were used for both tuned and untuned trials and were not re-tuned for additional elbow angles.

### Naive Lucas&ndash;Kanade (LK)

| **Parameter**     | **All Subjects** |
|-------------------|------------------|
| `LK_WINDOW`       | 35               |
| `PYR_LEVEL`       | 3                |
| `FIX_TOP`         | False            |
| `RESET_FREQUENCY` | 1e04             |

### Feature-Refined Lucas&ndash;Kanade (FRLK)

| **Parameter**     | **All Subjects** |
|-------------------|------------------|
| `LK_WINDOW`       | 35               |
| `PYR_LEVEL`       | 3                |
| `BLOCK_SIZE`      | 7                |
| `POINT_FRAC`      | 0.7              |
| `FIX_TOP`         | False            |
| `RESET_FREQUENCY` | 1e04             |

### Bilaterally-Filtered Lucas&ndash;Kanade (BFLK)

| **Parameter**        | ***Sub1*** | ***Sub2*** | ***Sub3*** | ***Sub4*** | ***Sub5*** |
|----------------------|------------|------------|------------|------------|------------|
| `LK_WINDOW`          | **35**     | 35         | 35         | 35         | 35         |
| `PYR_LEVEL`          | **3**      | 3          | 3          | 3          | 3          |
| `COARSE_DIAM`        | **15**     | 15         | 15         | 5          | 5          |
| `COARSE_SIGMA_COLOR` | **40**     | 40         | 100        | 40         | 25         |
| `COARSE_SIGMA_SPACE` | **40**     | 40         | 100        | 40         | 25         |
| `FINE_DIAM`          | **30**     | 35         | 35         | 35         | 20         |
| `FINE_SIGMA_COLOR`   | **100**    | 100        | 80         | 100        | 100        |
| `FINE_SIGMA_SPACE`   | **100**    | 100        | 80         | 100        | 100        |
| `PERCENT_FINE`       | **0.2**    | 0.2        | 0.2        | 0.2        | 0.5        |
| `PERCENT_COARSE`     | **0.8**    | 0.8        | 1          | 0.8        | 0.8        |
| `FIX_TOP`            | **False**  | False      | False      | False      | False      |
| `RESET_FREQUENCY`    | **1e04**   | 1e04       | 1e04       | 1e04       | 1e04       |

### Supporter-Based Lucas&ndash;Kanade (SBLK)

| **Parameter**         | ***Sub1*** | ***Sub 2*** | ***Sub 3*** | ***Sub 4*** | ***Sub 5*** |
|-----------------------|------------|-------------|-------------|-------------|-------------|
| `DISPLACEMENT_WEIGHT` | **40**     | 0           | 40          | 10          | 10          |
| `QUALITY_LEVEL`       | **0.4**    | 0.3         | 0.4         | 0.3         | 0.15        |
| `MIN_DISTANCE`        | **0**      | 2           | 0           | 2           | 2           |
| `MAX_CORNERS`         | **300**    | 300         | 300         | 300         | 300         |
| `COARSE_DIAM`         | **5**      | 10          | 5           | 10          | 10          |
| `COARSE_SIGMA_COLOR`  | **100**    | 100         | 100         | 100         | 100         |
| `COARSE_SIGMA_SPACE`  | **100**    | 100         | 100         | 100         | 100         |
| `FINE_DIAM`           | **20**     | 20          | 10          | 20          | 20          |
| `FINE_SIGMA_COLOR`    | **80**     | 80          | 80          | 80          | 80          |
| `FINE_SIGMA_SPACE`    | **80**     | 80          | 80          | 80          | 80          |
| `LK_WINDOW`           | **35**     | 35          | 35          | 35          | 35          |
| `PYR_LEVEL`           | **3**      | 3           | 3           | 5           | 3           |
| `BLOCK_SIZE`          | **7**      | 7           | 7           | 7           | 7           |
| `FINE_THRESHOLD`      | **0.45**   | 0.7         | 0.45        | 0.7         | 0.7         |
| `UPDATE_RATE`         | **0.7**    | 0.7         | 0.7         | 0.7         | 0.7         |
| `NUM_BOTTOM`          | **0**      | 10          | 0           | 10          | 10          |
| `FIX_TOP`             | **False**  | False       | False       | False       | False       |
| `RESET_FREQUENCY`     | **1e04**   | 1e04        | 1e04        | 1e04        | 1e04        |

