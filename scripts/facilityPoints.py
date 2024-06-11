import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")


def main():
    data1 = pd.read_csv(
        "data/csv/network_distance.csv"
    )

    unique_destinations = set(data1["StartPoint"])
    unique_destinations_df = pd.DataFrame({"StartPoint": list(unique_destinations)})

    data2 = pd.read_csv(
        "data/csv/Thuyhe_Diemven2_84.csv"
    )

    merged_df = pd.merge(
        unique_destinations_df,
        data2[["Id", "XX", "YY"]],
        left_on="StartPoint",
        right_on="Id",
    )
    df_sorted = merged_df[["Id", "StartPoint", "XX", "YY"]]
    df = df_sorted.rename(columns={"StartPoint": "FacilityPoints"})

    folder_path = r"data/csv"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, "facility_points.csv")
    df.to_csv(file_path, index=False)

    print("File CSV đã được lưu thành công vào thư mục:", folder_path)


if __name__ == "__main__":
    main()
