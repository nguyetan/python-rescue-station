## Cấu trúc thư mục

```
webgis_project/
│
├── static/ (Thư mục chứa các tệp tĩnh như CSS, JavaScript)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── templates/ (Thư mục chứa các tệp template HTML)
│   └── index.html (trang chủ giới thiệu)
│   └── map.html
│
├── data/ (Thư mục chứa dữ liệu địa lý)
│   └── shapefiles/
│   │   └── Thuyhe_Diemven2/
│   │   └── Thuyhe_HCM_motphan_DISSOLVE_Line5/
│   │   └── Thuyhe_HCM_motphan_DISSOLVE/
│   │   └── TPThuDuc/
│
│   └── csv/
│   │   └── Thuyhe_Diemven2.csv (dùng để tạo file facility_points.csv)
│   │   └── Thuyhe_HCM_motphan_test_graph.csv (dùng để tạo file network_distance.csv)
│   │   └── network_distance.csv
│   │   └── facility_points.csv
│
│   └── geoserver/
│   │   └── qgis (file lưu trữ bản vẽ qgis)
│   │   └── style (các file định dạng màu cho map)
│
├── scripts/ (Thư mục chứa các script Python để export csv)
│   └── pCenter.py
│   └── LSCP.py
│   └── networkDistance.py
│   └── facilityPoints.py
│
├── DB_Results/
│   └── DB_Result_LSCP_Rescue_Station/ (Thư mục chứa các file kết quả tính theo thuật toán LSCP)
│   │   └── ketqua_10LSCP_....csv
│
│   └── DB_Result_PCenter_Rescue_Station/ (Thư mục chứa các file kết quả tính theo thuật toán PCenter)
│   │   └── ketqua_10pCenter_....csv
│
├── app.py (File chính của Flask)
├── requirements.txt (Danh sách các gói Python cần thiết)
├── README.md (Tài liệu hướng dẫn)
└── desc_project (mô tả webgis)
```

# Cài đặt

## Setup enviroment

- Cài những gói pakage cần thiết

```
pip install -r requirements.txt
```

- Connect firebase

Tạo file servirceAccount.json và để tại `configs/servirceAccount.json`

- Start server

```
python app.py
```

## Thao tác chạy các file python theo thứ tự 1 đến 4

1. Khi run file networkDistance.py -> export network_distance.csv

2. Khi run file facilityPoints.py -> export facility_points.csv

3. Khi run file pCenter.py -> export ketqua_2pCenter_221901_28052024_2146.csv

4. Khi run file lSCP.py -> export ketqua_2LSCP_223515_28052024_5349.csv

## Các gói Python cần cài đặt trước khi run:

1. Matplotlib: Tạo biểu đồ và trực quan hóa dữ liệu.

2. Random: Tạo các số ngẫu nhiên -> Tạo tên tệp ngẫu nhiên.

3. Pandas: Đọc và xử lý dữ liệu từ các tệp CSV, tạo bảng pivot.

4. Datetime: Xử lý và định dạng ngày giờ -> Tạo tên tệp với thời gian hiện tại.

5. Shapely: Thao tác và phân tích các hình học phẳng -> Tạo đối tượng Point từ tọa độ.

6. os: Cung cấp các hàm để tương tác với hệ điều hành -> Kiểm tra và tạo thư mục, xây dựng đường dẫn tệp.

7. Geopandas: Hỗ trợ dữ liệu không gian (spatial data) và các phép toán địa lý -> Đọc shapefile, tạo GeoDataFrame

8. CBC: làm solver giải quyết bài toán PCenter và LSCP -> tìm ra các vị trí tối ưu cho các points dựa trên các ràng buộc đã được định nghĩa.

9. LGPK: tương tự CBC

10. Spopt: Cung cấp các công cụ và thuật toán cho tối ưu hóa không gian -> Giải quyết bài toán LSCP (Location Set Covering Problem).

11. PULP: Cung cấp công cụ để lập trình tuyến tính và lập trình nguyên (linear and integer programming) -> Giải quyết bài toán tối ưu hóa vị trí.

12. Networkx: Tạo đồ thị, Thêm/xóa các nút (nodes) và cạnh (edges), Cung cấp các thuật toán tiêu chuẩn cho các bài toán đồ thị, Phân tích các thuộc tính mạng lưới, vẽ đồ thị, trực quan hoá.
