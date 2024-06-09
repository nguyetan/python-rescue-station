import os
import sys
import pandas as pd
import geopandas
import pulp
from spopt.locate import LSCP
from shapely.geometry import Point
import random
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

def main():
    network_distance = pd.read_csv("data/csv/network_distance.csv")
    facility_points = pd.read_csv(
        "data/csv/facility_points.csv"
    )
    study_area = geopandas.read_file(
        "data/shapefile/Thuyhe_HCM_motphan_DISSOLVE_Line5/Thuyhe_HCM_motphan_DISSOLVE_Line5_84.shp"
    ).dissolve()

    pivot_table = network_distance.pivot_table(
        values="Distance", index="EndPoint", columns="StartPoint"
    )
    cost_matrix = pivot_table.fillna(0).astype(int)

    print(cost_matrix)

    P_FACILITIES = int(
        input("Enter the number of candidate facilities (P_FACILITIES): ")
    )

    total_net_length = network_distance["net_length"].sum()
    SERVICE_RADIUS = total_net_length / (P_FACILITIES * 2)
    SERVICE_RADIUS = round(SERVICE_RADIUS, 2)

    print(f"P_FACILITIES: {P_FACILITIES}")
    print(f"SERVICE_RADIUS: {SERVICE_RADIUS}")

    lscp = LSCP.from_cost_matrix(cost_matrix, SERVICE_RADIUS)
    lscp = lscp.solve(pulp.GLPK(msg=False))

    lscp_objval = lscp.problem.objective.value()

    selected_facilities = [i for i, dv in enumerate(lscp.fac_vars) if dv.varValue]
    selected_facilities_df = facility_points.iloc[selected_facilities].reset_index(
        drop=True
    )

    print("Objective value:", lscp_objval)
    print("Các điểm được chọn làm facility:")
    print(selected_facilities_df)

    serve_dict = {facility: [] for facility in selected_facilities}

    for i in range(len(cost_matrix)):
        min_distance = float("inf")
        selected_facility = None
        for facility in selected_facilities:
            if cost_matrix.iloc[i, facility] < min_distance:
                min_distance = cost_matrix.iloc[i, facility]
                selected_facility = facility
        serve_dict[selected_facility].append(i)

    for facility, points in serve_dict.items():
        print(
            f"Điểm {facility_points.iloc[facility]['FacilityPoints']} bao phủ các điểm: {points}"
        )

    current_time = datetime.now().strftime("%H%M%S_%d%m%Y")
    random_number = random.randint(1000, 9999)
    file_name = f"ketqua_{lscp_objval}LSCP_{current_time}_{random_number}.csv"

    directory = "DB_Results/DB_Result_LSCP_Rescue_Station"
    os.makedirs(directory, exist_ok=True)
    file_path = os.path.join(directory, file_name)

    selected_facilities_df.to_csv(file_path, index=False)
    print(f"File đã được lưu tại: {file_path}")


if __name__ == "__main__":
    main()
