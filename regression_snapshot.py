import orca.proj.exoplanet_pipeline as exoplanet_pipeline
from celery import group
from orca.metadata.pathsmanagers import OfflinePathsManager
from orca.transform.image_sub import getimrms
from orca.utils.fitsutils import co_add
import logging, sys, os
from datetime import date, datetime

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# TO BE FIXED
#             - think about fast (import test?) / slow (full science pipeline output) cases
def regression_snapshot(keyname: str, is_ref: bool = False, use_refcal: bool = False):
    """
    Run regression test for exoplanet / snapshot pipeline.
    keyname: Name for directory where data products are written.
    is_ref: If True, create the reference dataset. If True, {keyname} argument is ignored.
    use_refcal: If True, use the calibration tables in the reference dataset.
    """
    ref_dir = '/lustre/pipeline/regression/exoplanet/reference'
    keyname_dir = f'/lustre/pipeline/regression/exoplanet/{keyname}'
    if is_ref:
        working_dir = ref_dir
        bcal_dir    = f'{ref_dir}/BCAL'
    elif not is_ref and use_refcal:
        working_dir = keyname_dir
        bcal_dir    = f'{ref_dir}/BCAL'
    else:
        working_dir = keyname_dir
        bcal_dir    = f'{keyname_dir}/BCAL'

    if os.path.exists(working_dir):
        raise FileExistsError(f'Directory already exists: {working_dir}')
    else:
        os.mkdir(working_dir)
        os.mkdir(bcal_dir)
    if use_refcal and not os.path.exists(bcal_dir):
        raise FileNotFoundError(f'Reference calibration data does not exist: {bcal_dir}')
        
    pm_regression = OfflinePathsManager(
                        utc_times_txt_path='/lustre/pipeline/regression/exoplanet/utc_times.txt',
                        dadafile_dir='/lustre/pipeline/regression/exoplanet',
                        working_dir=working_dir,
                        gaintable_dir=bcal_dir)

    start_time_LSTnopeel = datetime(2020,1,22,9,30,0)
    end_time_LSTnopeel = datetime(2020,1,22,11,30,0)

    start_time_CasCyghigh = datetime(2020,1,22,18,30,0)
    end_time_CasCyghigh = datetime(2020,1,22,20,30,0)

    start_time_CasCyglow = datetime(2020,1,22,14,0,0)
    end_time_CasCyglow = datetime(2020,1,22,16,0,0)

    if use_refcal:
        BCALdate = date(2020,1,22)
    else:
        BCALdate = exoplanet_pipeline.calibration_pipeline(start_time_CasCyghigh, end_time_CasCyghigh, pathman = pm_regression)
    LSTnopeelfits = exoplanet_pipeline.processing_pipeline2(BCALdate, start_time_LSTnopeel, end_time_LSTnopeel, pathman = pm_regression)
    #CasCyghighfits = exoplanet_pipeline.processing_pipeline2(BCALdate, start_time_CasCyghigh, end_time_CasCyghigh, pathman = pm_regression)
    #CasCyglowfits = exoplanet_pipeline.processing_pipeline2(BCALdate, start_time_CasCyglow, end_time_CasCyglow, pathman = pm_regression)
    
    rmsLSTnopeel, medLSTnopeel, frqLSTnopeel, timeLSTnopeel = getimrms(LSTnopeelfits, radius=5/0.03125)
    #co_add(LSTnopeelfits, f'{pm_regression.get_working_dir}/twohourconcat/')
