import sys
from pathlib import Path
import logging

import yaml
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def rvs_tocsv(rvs, _output):
    """
    Export random variates to csv

    This would often be a pandas dataframe. Simple 1d array, for now, is written.

    Parameters
    ----------
    rvs : ndarray
    args : namespace

    Returns
    -------
    No return value, the ``rvs`` data written to ``args.output``.

    """
    np.savetxt(_output, rvs, delimiter=',')
    logger.info(f'random variates written to {_output}')


def read_yaml_config(config_file):
    """

    Parameters
    ----------
    config_file

    Returns
    -------

    """

    with open(config_file, 'rt') as yaml_file:
        yaml_config = yaml.safe_load(yaml_file)

    return yaml_config


def output_header(msg, linelen, scenario, rep_num):
    header = f"\n{msg} (scenario={scenario} rep={rep_num})\n{'-' * linelen}\n"
    return header


def write_stop_log(csv_path, obsystem, egress=False):
    timestamp_df = pd.DataFrame(obsystem.stops_timestamps_list)
    if egress:
        timestamp_df.to_csv(csv_path, index=False)
    else:
        timestamp_df[(timestamp_df['unit'] != 'ENTRY') &
                     (timestamp_df['unit'] != 'EXIT')].to_csv(csv_path, index=False)

    if egress:
        timestamp_df.to_csv(csv_path, index=False)
    else:
        timestamp_df[(timestamp_df['unit'] != 'ENTRY') &
                     (timestamp_df['unit'] != 'EXIT')].to_csv(csv_path, index=False)

