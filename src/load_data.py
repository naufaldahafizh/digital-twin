import pandas as pd
import os

def load_and_merge_sensor_data(data_dir="../data/raw"):
    sensor_files = [f for f in os.listdir(data_dir) if f.endswith('.txt') and f not in ['profile.txt', 'description.txt', 'documentation.txt']]
    sensor_dfs = []

    for file in sorted(sensor_files):
        path = os.path.join(data_dir, file)
        base_name = file.replace(".txt", "").lower()
        df = pd.read_csv(path, sep="\t", header=None)
        # Rename columns to include sensor name and column index
        df.columns = [f"{base_name}_{i+1}" for i in range(df.shape[1])]
        sensor_dfs.append(df)

    merged_sensors = pd.concat(sensor_dfs, axis=1)
    return merged_sensors

def load_profile(data_dir="../data/raw"):
    profile_path = os.path.join(data_dir, "profile.txt")
    profile_df = pd.read_csv(profile_path, sep="\t", header=None)
    profile_df.columns = ["cooler", "valve", "leakage", "acc", "stable"]
    return profile_df

def merge_all(data_dir="../data/raw"):
    sensor_df = load_and_merge_sensor_data(data_dir)
    profile_df = load_profile(data_dir)
    merged = pd.concat([sensor_df, profile_df], axis=1)
    return merged
