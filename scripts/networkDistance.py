import pandas as pd
import networkx as nx
import sys
import os


def main():

    sys.stdout.reconfigure(encoding="utf-8")

    data = pd.read_csv(
        "data/csv/Thuyhe_HCM_motphan_test_graph.csv"
    )

    # Lấy 5 hàng đầu tiên
    df_first_5_rows = data.iloc[:9845]

    # Chọn 3 cột và sắp xếp lại thứ tự cột
    df_selected = df_first_5_rows[["Id", "FromPoint", "ToPoint", "chieudai"]]

    # Nhập id x và id y từ command line
    x = int(input("Nhập id x: "))
    y = int(input("Nhập id y: "))

    # Lọc ra các dòng có Id nằm trong khoảng từ id x đến id y
    filtered_df = df_selected[(df_selected["Id"] >= x) & (df_selected["Id"] <= y)]

    # Tạo một bản sao độc lập của DataFrame filtered_df
    filtered_df_copy = filtered_df.copy()

    # Tính tổng của cột 'chieudai'
    net_length_value = filtered_df_copy["chieudai"].sum()

    # Gán giá trị của tổng vào cột 'net_length' của hàng đầu tiên
    filtered_df_copy.loc[filtered_df_copy.index[0], "net_length"] = net_length_value

    # Gán giá trị NaN cho các hàng còn lại của cột 'net_length'
    filtered_df_copy.loc[filtered_df_copy.index[1:], "net_length"] = float("0")

    # Tạo đồ thị từ dataframe
    G = nx.from_pandas_edgelist(filtered_df, "FromPoint", "ToPoint", ["chieudai"])

    # Tính toán khoảng cách giữa các cặp đỉnh
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

    # Tạo dataframe từ kết quả
    distance_df = pd.DataFrame(distances)

    # Trộn các kết quả vào chung 3 cột chieudai, FromPoint, ToPoint
    merged_df = pd.concat(
        [filtered_df[["FromPoint", "ToPoint", "chieudai"]], distance_df]
    )

    # Reset index để tránh index trùng lặp
    merged_df.reset_index(drop=True, inplace=True)

    # Đổi tên các cột
    df = merged_df.rename(
        columns={
            "FromPoint": "StartPoint",
            "ToPoint": "EndPoint",
            "chieudai": "Distance",
        }
    )

    # Thêm cột 'net_length' vào DataFrame 2
    df["net_length"] = 0.0  # Khởi tạo cột với giá trị 0
    df.loc[0, "net_length"] = net_length_value  # Gán giá trị của tổng vào hàng đầu tiên

    # Đường dẫn đến thư mục
    folder_path = r"data/csv"

    # Kiểm tra nếu thư mục không tồn tại, tạo mới
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Lưu dataframe thành file CSV trong thư mục mới
    file_path = os.path.join(folder_path, "network_distance.csv")
    df.to_csv(file_path, index=False)

    # Hiển thị kết quả
    print("File CSV đã được lưu thành công vào thư mục:", folder_path)


if __name__ == "__main__":
    main()
