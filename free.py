from datetime import date
import csv

# 家計簿クラス
class Kakeibo:
    """家計簿を管理"""
    def __init__(self):
        # リスト：支出データを保存
        self.records = []
    
    def add(self, record_date, category, money):
        """支出を1件追加"""
        self.records.append({
            "date": record_date,
            "category": category,
            "money": money
        })
    
    def total(self):
        """合計金額を計算"""
        total_money = 0
        for i in self.records:
            total_money += i["money"]
        return total_money
    
    def total_category(self):
        """カテゴリ別の合計金額を計算"""
        result = {}
        for i in self.records:
            category = i["category"]
            money = i["money"]

            if category not in result:
                result[category] = 0
            
            result[category] += money
        
        return result
    
    def save(self, filename="kakeibo.csv"):
        """家計簿データをCSVファイルに保存"""
        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["date", "category", "money"])     # 見出し
                for i in self.records:
                    writer.writerow([i["date"],i["category"],i["money"]])
        # 例外処理
        except IOError:
            print("ファイルの保存に失敗しました")
        
    def load(self, filename="kakeibo.csv"):
        """CSVファイルから家計簿データ読み込み"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.records = []
                # csvファイル：行追加
                for row in reader:
                    self.records.append({
                        "date": row["date"],
                        "category": row["category"],
                        "money": int(row["money"])
                    })
        # 初回起動時
        except FileNotFoundError:
            pass


# 表示処理
def list_records(records):
    """支出の一覧を表示"""
    print("\n   日付    | カテゴリ | 金額（円） ")
    print("-----------------------------------")
    for i in records:
        print(i["date"],  "|", i["category"], "|", i["money"])

# メイン処理
def main():
    """メイン処理"""
    kakeibo = Kakeibo()
    kakeibo.load()

    while True:
        print("\n 1: 支出追加  2: 一覧表示  3: 金額集計  0: 終了")
        choice = input("番号を入力してください（半角数字）")

        # 支出追加
        if choice == "1":
            category = input("カテゴリを入力（〇〇費）： ")

            try:
                money = int(input("金額： "))
            # 例外処理
            except ValueError:
                print("金額は数字で入力してください")
                continue 
            
            today = date.today().isoformat()
            kakeibo.add(today, category, money)
            print("追加完了")

        # 一覧表示
        elif choice == "2":
            list_records(kakeibo.records)
        
        # 金額集計表示
        elif choice == "3":
            print("\n 合計金額：", kakeibo.total(), "円")
            print("カテゴリ別金額合計")

            totals = kakeibo.total_category()
            for category in totals:
                print(category, ":", totals[category], "円")

        # 終了    
        elif choice == "0":
            kakeibo.save()
            print("保存して終了します")
            break

        else:
            print("正しい番号を入力してください")

# 実行
if __name__ == "__main__":
    main()