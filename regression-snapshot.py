import ..distributed-pipeline.orca.proj.exoplanet_pipeline as exoplanet_pipeline
from ..distributed-pipeline.orca.proj.celery import group
from ..distributed-pipeline.orca.metadata.pathsmanagers import OfflinePathsManager
import os

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# TO BE FIXED
#             - add wsclean command as final step of processing_pipeline
#             - think about fast (import test?) / slow (full science pipeline output) cases
def regression_snapshot(keyname: str, is_ref: bool = False):
    """
    Run regression test for exoplanet / snapshot pipeline.
    keyname: Name for directory where data products are written.
    is_ref: If True, create the reference dataset. If True, {keyname} argument is ignored.
    """
    if is_ref:
        working_dir = f'/lustre/pipeline/regression/exoplanet/reference'
    else:
        working_dir = f'/lustre/pipeline/regression/exoplanet/{keyname}'

    if os.path.exists(working_dir):
        raise FileExistsError(f'Directory already exists: {working_dir}')
    else:
        os.mkdir(working_dir)
        
    pm_regression = OfflinePathsManager(
                        utc_times_txt_path='/lustre/pipeline/regression/exoplanet/utc_times.txt',
                        dadafile_dir='/lustre/pipeline/regression/exoplanet'
                        working_dir=working_dir,
                        gaintable_dir=f'{working_dir}/BCAL')

    start_time_LSTnopeel = datetime(2020,1,22,9,30,0)
    end_time_LSTnopeel = datetime(2020,1,22,11,30,0)

    start_time_CasCyghigh = datetime(2020,1,22,18,30,0)
    end_time_CasCyghigh = datetime(2020,1,22,20,30,0)

    start_time_CasCyglow = datetime(2020,1,22,14,0,0)
    end_time_CasCyglow = datetime(2020,1,22,16,0,0)

    BCALdate = exoplanet_pipeline.calibration_pipeline(start_time_CasCyghigh, end_time_CasCyghigh, pathman = pm_regression)
    exoplanet_pipeline.processing_pipeline(BCALdate, start_time_LSTnopeel, end_time_LSTnopeel, pathman = pm_regression)
    exoplanet_pipeline.processing_pipeline(BCALdate, start_time_CasCyghigh, end_time_CasCyghigh, pathman = pm_regression)
    exoplanet_pipeline.processing_pipeline(BCALdate, start_time_CasCyglow, end_time_CasCyglow, pathman = pm_regression)