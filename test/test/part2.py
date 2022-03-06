from enum import Enum
from dataclasses import dataclass

"""
クエリのタイプを表すEnumクラス
"""
class Query(Enum):
    SYSTEM = 1
    RESERVATION = 2

@dataclass
class RestaurantInfo:
    open_at: str
    closed_at: str
    time_zones: list
    tables: list

def main(lines):
    # key: テーブル番号
    # value: 予約可能人数
    # e.g) tables = {'1': 4, '2': 5}
    tables = {str(i+1): int(v) for i, v in enumerate(lines[1].split(' '))}
    
    time_infos = lines[2].split(' ')
    # e.g) 09:00-15:00
    business_hour = time_infos[0]
    # e.g) ["9:00-12:00", "12:00-15:00"]
    time_zones = time_infos[2:]
    restaurant_info = RestaurantInfo(
        open_at=business_hour.split('-')[0],
        closed_at=business_hour.split('-')[1],
        time_zones=time_zones,
        tables=tables
    )

    # key: 予約番号（一意）
    # value: 受け取った情報の、issue-specified 以降すべてのリスト[予約日時, 予約時間帯, 予約人数, テーブル番号]
    # e.g) {"00001": [1, "12:00-15:00", 2, 3], "00002":  [1, "12:00-15:00", 2, 1]}
    detailed_reservations = {}
    # key: (day, timezone)
    # value: 予約番号のリスト
    # e.g) {(1, 1): ["00001", "00002"], (1, 2): ["000003"]}
    reservation_list_in_timezone = {}
    for query in lines[3:]:
        query_type = get_query_type(query)

        if query_type is Query.SYSTEM:
            do_system_query(query, restaurant_info, detailed_reservations, reservation_list_in_timezone)
        elif query_type is Query.RESERVATION:
            do_reservation_query(query, restaurant_info, detailed_reservations, reservation_list_in_timezone)


def get_query_type(query) -> Query:
    if 'time' in query:
        return Query.SYSTEM
    return Query.RESERVATION

def do_system_query(query, restaurant_info, detailed_reservations, reservation_list_in_timezone):
    delete_old_reservations(query, detailed_reservations, reservation_list_in_timezone)
    print_current_reservations(query, detailed_reservations, reservation_list_in_timezone)
    
def delete_old_reservations(query, detailed_reservations, reservation_list_in_timezone):
    d, hh_mm, _, t_z = query.split(' ')
    prev_time_zone = str(int(t_z)-1)
    # 過去の予約が存在する場合、その情報を消去する
    key = (d, prev_time_zone)
    if key in reservation_list_in_timezone:
        for reservation in reservation_list_in_timezone[key]:
            del detailed_reservations[reservation]
        del reservation_list_in_timezone[key]

def print_current_reservations(query, detailed_reservations, reservation_list_in_timezone):
    d, hh_mm, _, t_z = query.split(' ')
    # 現時刻の予約が存在する場合、その情報を表示する
    key = (d, t_z)
    if key in reservation_list_in_timezone:
        for reservation_num in reservation_list_in_timezone[key]:
            # [1, "12:00-15:00", 2, 3]
            reservation = detailed_reservations[reservation_num]
            print(f'{reservation[0]} {reservation[1]} table {reservation[3]}')

def do_reservation_query(query, restaurant_info, detailed_reservations, reservation_list_in_timezone):
    d, hh_mm, _, r_n, r_d, r_tz, r_p_n, r_t_n = query.split(' ')
    # MAYBE: 時間クエリで何が必要かに応じて変える
    detailed_info = [r_d, r_tz, r_p_n, r_t_n]

    # 現在の時刻が、予約時間帯に含まれる場合
    if is_current_timezone(d, hh_mm, r_d, r_tz, restaurant_info.time_zones):
        print(f'{d} {hh_mm} Error: a past time cannot be specified.')
    # 現在の時刻が、予約時間帯の終了時刻かそれ以降である場合
    elif hh_mm > restaurant_info.closed_at:
        print(f'{d} {hh_mm} Error: a past time cannot be specified.')
    # 予約人数がテーブル人数よりも多い場合
    elif int(r_p_n) > restaurant_info.tables[r_t_n]:
        print(f'{d} {hh_mm} Error: the maximum number of people at the table has been exceeded.')
    # すでにそのテーブルが予約されている場合
    elif is_occpied(r_d, r_tz, r_t_n, detailed_reservations, reservation_list_in_timezone):
        print(f'{d} {hh_mm} Error: the table is occpied.')
    # 予約が可能な場合
    else:
        detailed_reservations[r_n] = detailed_info
        # (日付, timezone)に入っている予約リスト
        d = reservation_list_in_timezone.get((r_d, r_tz))
        if d is None:
            reservation_list_in_timezone[(r_d, r_tz)] = []
        reservation_list_in_timezone[(r_d, r_tz)].append(r_n)

# 現在の時刻が、予約時間帯に含まれるかどうかをチェックする
def is_current_timezone(d, hh_mm, rd, r_tz, timezones):
    if d != rd:
        return False
    return str(get_timezone_num(hh_mm, timezones)) == r_tz

# e.g)
#   time = "10:00"
#   timezones = ["09:00-12:00", "12:00-15:00"]
#   => return 1    # CAUTION: 1 origin
def get_timezone_num(time: str, timezones: list) -> int:
    for i, timezone in enumerate(timezones):
        start, end = timezone.split('-')
        if time2mins(start) <= time2mins(time) <= time2mins(end):
            return i + 1  # timezon is 1 origin
    return -1   # default

# e.g) time = "09:30"
def time2mins(time: str) -> int:
    h, m = time.split(':')
    return int(h) * 60 + int(m)


# 日時、日付、テーブル番号が全て等しいものがあるかどうかチェックする
def is_occpied(r_d, r_tz, r_t_n, detailed_reservations, reservation_list_in_timezone):
    # (日付, timezone)に入っている予約リスト
    d = reservation_list_in_timezone.get((r_d, r_tz))
    if d is None:
        return False

    for reservation_num in reservation_list_in_timezone[(r_d, r_tz)]:
        reservation = detailed_reservations[reservation_num]
        if r_t_n == reservation[3]:
            return True

    return False


if __name__ == "__main__":
    # TODO: 標準入力から読み取るようにする
    lines = [
        "3",
        "2 3 5",
        "09:00-15:00 2 09:00-12:00 12:00-15:00",
        "1 09:00 time 1",
        "1 09:30 issue-specified 00003 1 2 2 3",    # 正常に予約できるケース
        "1 10:00 issue-specified 00001 1 1 2 1",    # 時間帯に含まれるケース
        "1 10:00 issue-specified 00002 1 2 2 1",    # 正常に予約できるケース
        "1 10:00 issue-specified 00004 1 2 8 3",    # 席数が足りないケース
        "1 10:00 issue-specified 00005 1 2 1 1",    # すでに予約されているケース
        "1 12:00 time 2",
        "1 15:00 time 3",
        "1 18:00 issue-specified 00006 1 1 2 1",    # 時間が遅いケース
    ]
    main(lines)
