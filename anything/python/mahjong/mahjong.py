from dataclasses import dataclass
import re


# 設定値
FILE_NAME = "line_talk.txt"
NAME_NAGAOKA = "永岡"
NAME_YAMASHITA = "山下弘輝"
OUTPUT_FILE_NAME = "summary.csv"

# 読み込みを行う
with open(FILE_NAME) as f:
    lines = f.read().split("\n")

results_nagaoka = {
    '1st': 0,
    '2nd': 0,
    '3rd': 0,
    '4th': 0,
    'P/L': 0,
    'results': [],
}
results_yamashita = {
    '1st': 0,
    '2nd': 0,
    '3rd': 0,
    '4th': 0,
    'P/L': 0,
    'results': [],
}


@dataclass
class Summary:
    date: str
    first: int
    second: int
    third: int
    fourth: int
    PL: int
    place: str


# このパターンにマッチするもののみ結果として解釈する
# 例：2-5-6-2 -3150
# TODO: 『さんま』や『途中に点５などの余分な情報が入ってる場合』にマッチしない
pattern = re.compile(r"\d{1,}-\d{1,}-\d{1,}-\d{1,} [+-]\d{1,}")
for i in range(len(lines)):
    line = lines[i]
    result = pattern.search(line)
    if result:
        print(lines[i-1])
        # res = "4-4-4-3", pl=+1700", なぜか pl の最後に"がつく（時もある）
        res, pl = line.split(" ")
        print(pl)
        if pl[-1] == "\"":
            pl = pl[:-1]
        print(pl)
        f, s, t, l = map(int, res.split("-"))
        # 例『1/16 藤江荘.5』の形で取れる
        # tmp = lines[i-1].split("\"")[1]
        tmp = lines[i-1].split("\t")[2]
        tmp_list = tmp.split(" ")
        if len(tmp_list) > 1:
            date, place = tmp_list[0], tmp_list[1]
        else:
            date, place = tmp[:3], tmp[3:]
        print(f, s, t, l)
        if NAME_NAGAOKA in lines[i-1]:
            data = Summary(
                date=date,
                first=f,
                second=s,
                third=t,
                fourth=l,
                PL=int(pl),
                place=place
            )
            results_nagaoka['1st'] += f
            results_nagaoka['2nd'] += s
            results_nagaoka['3rd'] += t
            results_nagaoka['4th'] += l
            results_nagaoka['P/L'] += int(pl)
            results_nagaoka['results'].append(data)
        if NAME_YAMASHITA in lines[i-1]:
            data = Summary(
                date=date,
                first=f,
                second=s,
                third=t,
                fourth=l,
                PL=int(pl),
                place=place
            )
            results_yamashita['1st'] += f
            results_yamashita['2nd'] += s
            results_yamashita['3rd'] += t
            results_yamashita['4th'] += l
            results_yamashita['P/L'] += int(pl)
            results_yamashita['results'].append(data)


print("永岡 results")
print(f"1st: {results_nagaoka['1st']}")
print(f"2nd: {results_nagaoka['2nd']}")
print(f"3rd: {results_nagaoka['3rd']}")
print(f"4th: {results_nagaoka['4th']}")
print(f"P/L: {results_nagaoka['P/L']}")
print(f"num_summary: {len(results_nagaoka['results'])}")

print("山下 results")
print(f"1st: {results_yamashita['1st']}")
print(f"2nd: {results_yamashita['2nd']}")
print(f"3rd: {results_yamashita['3rd']}")
print(f"4th: {results_yamashita['4th']}")
print(f"P/L: {results_yamashita['P/L']}")
print(f"num_summary: {len(results_yamashita['results'])}")

for summary in results_yamashita['results']:
    print(summary)

# csv 出力
with open(OUTPUT_FILE_NAME, mode='w') as f:

    f.write(NAME_YAMASHITA + "\n")

    HEADER = "date, 1st, 2nd, 3rd, 4th, P/L, place\n"
    f.write(HEADER)

    for summary in results_yamashita['results']:
        sentence = f"{summary.date}, "\
            + f"{summary.first}, {summary.second}, {summary.third}, {summary.fourth}, "\
                + f"{summary.PL}, {summary.place}\n"
        f.write(sentence)

    f.write("\n")
    f.write(NAME_NAGAOKA + "\n")

    f.write(HEADER)

    for summary in results_nagaoka['results']:
        sentence = f"{summary.date}, "\
            + f"{summary.first}, {summary.second}, {summary.third}, {summary.fourth}, "\
                + f"{summary.PL}, {summary.place}\n"
        f.write(sentence)
