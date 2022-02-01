


def output_header(msg, linelen, scenario, rep_num):
    header = f"\n{msg} (scenario={scenario} rep={rep_num})\n{'-' * linelen}\n"
    return header

def compute_occ_stats(obsystem, end_time, egress=False, log_path=None, warmup=0,
                      quantiles=(0.05, 0.25, 0.5, 0.75, 0.95, 0.99)):
    occ_stats_dfs = []
    occ_dfs = []
    for unit in obsystem.obunits:
        if len(unit.occupancy_list) > 1:
            occ = unit.occupancy_list

            df = pd.DataFrame(occ, columns=['timestamp', 'occ'])
            df['occ_weight'] = -1 * df['timestamp'].diff(periods=-1)

            last_weight = end_time - df.iloc[-1, 0]
            df.fillna(last_weight, inplace=True)
            df['unit'] = unit.name
            occ_dfs.append(df)

            # Filter out recs before warmup
            df = df[df['timestamp'] > warmup]

            weighted_stats = DescrStatsW(df['occ'], weights=df['occ_weight'], ddof=0)

            occ_quantiles = weighted_stats.quantile(quantiles)
            occ_unit_stats_df = pd.DataFrame([{'unit': unit.name, 'capacity': unit.capacity,
                                               'mean_occ': weighted_stats.mean, 'sd_occ': weighted_stats.std,
                                               'min_occ': df['occ'].min(), 'max_occ': df['occ'].max()}])

            quantiles_df = pd.DataFrame(occ_quantiles).transpose()
            quantiles_df.rename(columns=lambda x: f"p{100 * x:02.0f}_occ", inplace=True)

            occ_unit_stats_df = pd.concat([occ_unit_stats_df, quantiles_df], axis=1)
            occ_stats_dfs.append(occ_unit_stats_df)

    occ_stats_df = pd.concat(occ_stats_dfs)

    if log_path is not None:
        occ_df = pd.concat(occ_dfs)
        if egress:
            occ_df.to_csv(log_path, index=False)
        else:
            occ_df[(occ_df['unit'] != 'ENTRY') &
                   (occ_df['unit'] != 'EXIT')].to_csv(log_path, index=False)

    return occ_stats_df

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



    # # Read inputs from config file
    # with open(args.config, 'rt') as yaml_file:
    #     yaml_config = yaml.safe_load(yaml_file)
    #
    # return yaml_config, args.loglevel