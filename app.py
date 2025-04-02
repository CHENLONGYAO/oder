import json
from typing import List, Dict, Tuple

# 常數定義
INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"

def load_data(filename: str) -> List[Dict]:
    """讀取指定檔案的 JSON 資料，若檔案不存在則返回空列表"""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_orders(filename: str, orders: List[Dict]) -> None:
    """將訂單列表儲存為 JSON 檔案"""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(orders, file, indent=4, ensure_ascii=False)

def calculate_order_total(order: Dict) -> int:
    """計算單筆訂單的總金額"""
    total = 0
    for item in order["items"]:
        total += item["price"] * item["quantity"]
    return total

def print_order_report(data: List[Dict], title: str = "訂單報表", single: bool = False) -> None:
    """顯示訂單報表，可顯示單筆訂單或多筆訂單"""
    print(f"\n==================== {title} ====================")
    if single:
        orders = [data]
    else:
        orders = data

    for idx, order in enumerate(orders, 1):
        if not single:
            print(f"\n訂單 #{idx}")
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("--------------------------------------------------")
        print("商品名稱\t單價\t數量\t小計")
        print("--------------------------------------------------")
        for item in order["items"]:
            subtotal = item["price"] * item["quantity"]
            print(f"{item['name']}\t{item['price']}\t{item['quantity']}\t{subtotal}")
        print("--------------------------------------------------")
        total = calculate_order_total(order)
        print(f"訂單總額: {total:,}")
        print("==================================================")

def add_order(orders: List[Dict]) -> str:
    """新增訂單至列表，若訂單編號重複則返回錯誤訊息"""
    order_id = input("請輸入訂單編號：").upper()
    if any(order["order_id"] == order_id for order in orders):
        return f"=> 錯誤：訂單編號 {order_id} 已存在！"

    customer = input("請輸入顧客姓名：")
    items = []

    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：")
        if not name:
            break
        try:
            price = int(input("請輸入價格："))
            if price < 0:
                print("=> 錯誤：價格不能為負數，請重新輸入")
                continue
            quantity = int(input("請輸入數量："))
            if quantity <= 0:
                print("=> 錯誤：數量必須為正整數，請重新輸入")
                continue
            items.append({"name": name, "price": price, "quantity": quantity})
        except ValueError:
            print("=> 錯誤：價格或數量必須為整數，請重新輸入")
            continue

    if not items:
        return "=> 至少需要一個訂單項目"

    orders.append({"order_id": order_id, "customer": customer, "items": items})
    return f"=> 訂單 {order_id} 已新增！"

def process_order(orders: List[Dict]) -> Tuple[str, Dict | None]:
    """處理訂單並將其轉移到已完成訂單，返回處理結果訊息和處理的訂單"""
    if not orders:
        return "=> 目前沒有待處理訂單", None

    print("\n======== 待處理訂單列表 ========")
    for idx, order in enumerate(orders, 1):
        print(f"{idx}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("================================")

    choice = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ")
    if not choice:
        return "=> 已取消出餐", None

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(orders):
            completed_order = orders.pop(idx)
            return f"=> 訂單 {completed_order['order_id']} 已出餐完成", completed_order
        else:
            return "=> 錯誤：請輸入有效的數字", None
    except ValueError:
        return "=> 錯誤：請輸入有效的數字", None

def main() -> None:
    """程式主流程，包含選單迴圈和各功能的調用"""
    orders = load_data(INPUT_FILE)
    output_orders = load_data(OUTPUT_FILE)

    while True:
        print("\n***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")
        choice = input("請選擇操作項目(Enter 離開)：").strip()

        if choice == "":
            break
        elif choice == "1":
            result = add_order(orders)
            print(result)
            save_orders(INPUT_FILE, orders)
        elif choice == "2":
            if orders:
                print_order_report(orders)
            else:
                print("=> 目前沒有訂單")
        elif choice == "3":
            result, completed_order = process_order(orders)
            print(result)
            if completed_order:
                output_orders.append(completed_order)
                save_orders(INPUT_FILE, orders)
                save_orders(OUTPUT_FILE, output_orders)
                print_order_report(completed_order, title="出餐訂單", single=True)
        elif choice == "4":
            break
        else:
            print("=> 請輸入有效的選項（1-4）")

if __name__ == "__main__":
    main()
