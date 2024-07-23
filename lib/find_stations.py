import pandas as pd
import pulp
import spopt
from spopt.locate import LSCP, PCenter
from lib.utils import network_distance, facility_points_calulator


def find_stations_LSCP(req):
    firstStation = int(req["firstStation"])
    lastStation = int(req["lastStation"])
    SERVICE_RADIUS = int(req["numberStation"])

    network = network_distance(firstStation, lastStation)

    facility_points = facility_points_calulator(network)

    pivot_table = network.pivot_table(
        values="Distance", index="EndPoint", columns="StartPoint"
    )
    cost_matrix = pivot_table.fillna(0).astype(int)

    # total_net_length = network["net_length"].sum()
    # SERVICE_RADIUS = total_net_length / (P_FACILITIES * 2)
    # SERVICE_RADIUS = round(SERVICE_RADIUS, 2)

    lscp = LSCP.from_cost_matrix(cost_matrix, SERVICE_RADIUS)
    lscp = lscp.solve(pulp.PULP_CBC_CMD(msg=False))

    lscp_objval = lscp.problem.objective.value()

    selected_facilities = [i for i, dv in enumerate(lscp.fac_vars) if dv.varValue]
    selected_facilities_df = facility_points.iloc[selected_facilities].reset_index(
        drop=True
    )

    unselected_facilities = facility_points[
        ~facility_points.index.isin(selected_facilities)
    ].reset_index(drop=True)
    response = {
        "selected": selected_facilities_df.to_dict(orient="records"),
        "unselected": unselected_facilities.to_dict(orient="records"),
    }
    return response


def find_stations_PCenter(req):
    firstStation = int(req["firstStation"])
    lastStation = int(req["lastStation"])
    p_facilities = int(req["numberStation"])

    network = network_distance(firstStation, lastStation)
    facility_points = facility_points_calulator(network)

    # pivot_table = network.pivot_table(
    #     values="Distance", index="EndPoint", columns="StartPoint"
    # )
    # cost_matrix = pivot_table.fillna(0).astype(int)

    # num_points = cost_matrix.shape[0]
    # model = pulp.LpProblem("p-Center Problem", pulp.LpMinimize)

    # x = pulp.LpVariable.dicts(
    #     "x", (range(num_points), range(num_points)), 0, 1, pulp.LpBinary
    # )
    # y = pulp.LpVariable.dicts("y", range(num_points), 0, 1, pulp.LpBinary)
    # z = pulp.LpVariable("z", 0)
    # model += z

    # for i in range(num_points):
    #     model += pulp.lpSum(x[i][j] for j in range(num_points)) == 1

    # model += pulp.lpSum(y[j] for j in range(num_points)) == p_facilities

    # for i in range(num_points):
    #     for j in range(num_points):
    #         model += x[i][j] <= y[j]
    #         model += z >= cost_matrix.iloc[i, j] * x[i][j]

    # model.solve()

    # selected_facilities = []
    # for j in range(num_points):
    #     if pulp.value(y[j]) == 1:
    #         facility_info = facility_points.iloc[j]
    #         selected_facilities.append(
    #             {
    #                 "Id": facility_info["Id"],
    #                 "FacilityPoints": facility_info["FacilityPoints"],
    #                 "XX": facility_info["XX"],
    #                 "YY": facility_info["YY"],
    #             }
    #         )

    # selected_facilities_df = pd.DataFrame(selected_facilities)

    # Tạo bảng pivot từ dataframe
    pivot_table = network.pivot_table(
        values="Distance", index="EndPoint", columns="StartPoint", fill_value=0
    )

    # Chuyển đổi thành ma trận numpy để sử dụng với spopt và pulp
    cost_matrix = pivot_table.values.astype(int)

    # Khởi tạo và giải quyết bài toán LSCP
    pcenter = PCenter.from_cost_matrix(cost_matrix, p_facilities)
    pcenter = pcenter.solve(pulp.PULP_CBC_CMD(msg=False))

    # Lấy giá trị objective
    pcenter_objval = pcenter.problem.objective.value()

    # Tạo danh sách các điểm được chọn trong pcenter_objval
    selected_facilities = [i for i, dv in enumerate(pcenter.fac_vars) if dv.varValue]

    # Tạo DataFrame từ danh sách các điểm được chọn
    selected_facilities_df = facility_points.iloc[selected_facilities].reset_index(
        drop=True
    )
    unselected_facilities = facility_points[
        ~facility_points.index.isin(selected_facilities)
    ].reset_index(drop=True)
    response = {
        "selected": selected_facilities_df.to_dict(orient="records"),
        "unselected": unselected_facilities.to_dict(orient="records"),
    }
    return response
