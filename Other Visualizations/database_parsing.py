import sqlite3
import pandas as pd

def main():
    db_path = "/home/nference/Desktop/302968/302968.db"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    query = " select aoi_name, hue_bins from aoi"
    c.execute(query)
    df = pd.read_sql_query("SELECT * FROM table_name", conn)
    aoi_info = c.fetchall()
    for i in range(0, len(aoi_info)):
        aoi_details = aoi_info[i]
        print(aoi_details)
    # #     aoi_name = aoi_details[0]
    # #     hue_bins = aoi_details[1]
    # #     biopsy_ratio = aoi_details[2]
    # #     debris_ratio = aoi_details[3]
    # #     if biopsy_ratio > debris_ratio:
    # #         biopsy_count += 1
    # #     else:
    # #         debris_count += 1
    # # print("biopsy count: ", biopsy_count)
    # # print("Debris count: ", debris_count)



if __name__ =="__main__":
    main()