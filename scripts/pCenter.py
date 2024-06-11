import os
import sys
import pandas as pd
import pulp
import geopandas
import random
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")


def main():
    network_distance = pd.read_csv(
        "data/csv/network_distance.csv"
    )
    facility_points = pd.read_csv(
        "data/csv/facility_points.csv"
    )
    study_area = geopandas.read_file(
        "data/shapefile/Thuyhe_HCM_motphan_DISSOLVE_Line5/Thuyhe_HCM_motphan_DISSOLVE_Line5_84.shp"
    ).dissolve()

    pivot_table = network_distance.pivot_table(
        values="Distance", index="EndPoint", columns="StartPoint", fill_value=0
    )
    cost_matrix = pivot_table.astype(int)

    p_facilities = int(input("Nhập số lượng facilities cần tìm: "))
    num_points = cost_matrix.shape[0]
    model = pulp.LpProblem("p-Center Problem", pulp.LpMinimize)

    x = pulp.LpVariable.dicts(
        "x", (range(num_points), range(num_points)), 0, 1, pulp.LpBinary
    )
    y = pulp.LpVariable.dicts("y", range(num_points), 0, 1, pulp.LpBinary)
    z = pulp.LpVariable("z", 0)
    model += z

    for i in range(num_points):
        model += pulp.lpSum(x[i][j] for j in range(num_points)) == 1

    model += pulp.lpSum(y[j] for j in range(num_points)) == p_facilities

    for i in range(num_points):
        for j in range(num_points):
            model += x[i][j] <= y[j]
            model += z >= cost_matrix.iloc[i, j] * x[i][j]

    model.solve()

    print(f"Trạng thái giải: {pulp.LpStatus[model.status]}")
    print(f"Khoảng cách tối ưu: {pulp.value(z)}")
    print("Các điểm được chọn làm facility:")

    selected_facilities = []
    for j in range(num_points):
        if pulp.value(y[j]) == 1:
            facility_info = facility_points.iloc[j]
            selected_facilities.append(
                {
                    "id": facility_info["Id"],
                    "facilities": facility_info["FacilityPoints"],
                    "XX": facility_info["XX"],
                    "YY": facility_info["YY"],
                }
            )

    selected_facilities_df = pd.DataFrame(selected_facilities)
    print(selected_facilities_df)

    for facility in range(len(selected_facilities)):
        facility_id = int(selected_facilities[facility]["facilities"])
        points_covered = []

        for point in range(num_points):
            if pulp.value(x[point][facility_id]) == 1:
                points_covered.append(point)

        print(
            f"Điểm {facility_points.iloc[facility_id]['FacilityPoints']} bao phủ các điểm: {points_covered}"
        )

    directory = "DB_Results/DB_Result_PCenter_Rescue_Station"
    os.makedirs(directory, exist_ok=True)

    current_time = datetime.now().strftime("%H%M%S_%d%m%Y")
    random_number = random.randint(1000, 9999)
    file_name = f"ketqua_{p_facilities}pCenter_{current_time}_{random_number}.csv"
    file_path = os.path.join(directory, file_name)

    selected_facilities_df.to_csv(file_path, index=False)
    print(f"File đã được lưu tại: {file_path}")


if __name__ == "__main__":
    main()
