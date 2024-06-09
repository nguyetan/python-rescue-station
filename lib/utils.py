import pandas as pd
import networkx as nx

def network_distance(firstStation: int, lastStation: int):
    data = pd.read_csv("data/csv/Thuyhe_HCM_motphan_test_graph.csv")

    df_first_5_rows = data.iloc[:9845]
    df_selected = df_first_5_rows[["Id", "FromPoint", "ToPoint", "chieudai"]]
    filtered_df = df_selected[(df_selected["Id"] >= firstStation) & (df_selected["Id"] <= lastStation)]

    filtered_df_copy = filtered_df.copy()
    net_length_value = filtered_df_copy["chieudai"].sum()

    filtered_df_copy.loc[filtered_df_copy.index[0], "net_length"] = net_length_value
    filtered_df_copy.loc[filtered_df_copy.index[1:], "net_length"] = float("0")

    G = nx.from_pandas_edgelist(filtered_df, "FromPoint", "ToPoint", ["chieudai"])

    distances = []
    for source in filtered_df["FromPoint"]:
        for target in filtered_df["ToPoint"]:
            if source != target:
                distance = nx.shortest_path_length(
                    G, source=source, target=target, weight="chieudai"
                )
                distances.append(
                    {"FromPoint": source, "ToPoint": target, "chieudai": distance}
                )

    distance_df = pd.DataFrame(distances)

    merged_df = pd.concat(
        [filtered_df[["FromPoint", "ToPoint", "chieudai"]], distance_df]
    )

    merged_df.reset_index(drop=True, inplace=True)

    df = merged_df.rename(
        columns={
            "FromPoint": "StartPoint",
            "ToPoint": "EndPoint",
            "chieudai": "Distance",
        }
    )

    df["net_length"] = 0.0
    df.loc[0, "net_length"] = net_length_value
    return df

def facility_points():
    data1 = pd.read_csv("data/csv/network_distance.csv")

    unique_destinations = set(data1["StartPoint"])
    unique_destinations_df = pd.DataFrame({"StartPoint": list(unique_destinations)})

    data2 = pd.read_csv("data/csv/Thuyhe_Diemven2_84.csv")

    merged_df = pd.merge(
        unique_destinations_df,
        data2[["Id", "XX", "YY"]],
        left_on="StartPoint",
        right_on="Id",
    )
    df_sorted = merged_df[["Id", "StartPoint", "XX", "YY"]]
    df1 = df_sorted.rename(columns={"StartPoint": "FacilityPoints"})
    return df1