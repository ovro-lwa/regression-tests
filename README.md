# regression-tests
End to end testing for science data processing pipelines.

We currently plan for three science pipelines:
1. All-sky snapshot imaging
2. All-sky sidereal subtraction imaging
3. M-mode power spectrum

Each pipeline will have a single script that runs some (or all) of the analysis from recorded data to science products. The final step is to compare some reference statistic between the science products to a reference set of science products. Ideally, the difference will be zero within machine precision.


# Step-by-step procedure

Instructions to run the analysis scripts are provided here. Ideally, scripts will have options to run "fast" (simple checks) or "slow" (more complete, high-sensitivity checks).

## All-sky snapshot

1. Log in to astm
2. `cd /lustre/pipeline/regression/exoplanet` and check that only data and the utc time file are present.
3. `python /lustre/pipeline/regression/regression-tests/regression-snapshot.py`
4. [Compare to reference in `/lustre/pipeline/regression/exoplanet/reference`]
5. [move new output to `/lustre/pipeline/regression/exoplanet/[date]`

## All-sky sidereal


## M-mode power spectrum
