class BillAnalysis:
    def __init__(self, bills):
        self.bills = bills

    def analyze(self):
        total_bills = len(self.bills)
        payment_modes = {"UPI": 0, "Cash": 0, "Card": 0}
        total_revenue = 0
        items_count = 0
        max_items = 0
        min_items = float('inf')
        max_transaction = 0
        min_transaction = float('inf')
        items_by_payment_mode = {"UPI": 0, "Cash": 0, "Card": 0}
        revenue_by_payment_mode = {"UPI": 0, "Cash": 0, "Card": 0}

        for bill in self.bills:
            items = bill["items"]
            amount = int(bill["totalAmount"].replace("₹", ""))
            payment_mode = bill["paymentMode"]

            # Aggregate metrics
            payment_modes[payment_mode] += 1
            total_revenue += amount
            items_count += items
            max_items = max(max_items, items)
            min_items = min(min_items, items)
            max_transaction = max(max_transaction, amount)
            min_transaction = min(min_transaction, amount)
            items_by_payment_mode[payment_mode] += items
            revenue_by_payment_mode[payment_mode] += amount

        # Calculate averages
        average_transaction_value = total_revenue / total_bills
        average_items_per_bill = items_count / total_bills
        payment_mode_distribution = {
            mode: f"{(count / total_bills) * 100:.2f}%" for mode, count in payment_modes.items()
        }
        average_revenue_by_payment_mode = {
            mode: revenue / count if count > 0 else 0 for mode, (revenue, count) in
            zip(revenue_by_payment_mode.keys(), zip(revenue_by_payment_mode.values(), payment_modes.values()))
        }

        # Create the analysis results
        analysis_results = {
            "Total Bills": total_bills,
            "Payment Mode Distribution": payment_mode_distribution,
            "Total Revenue": total_revenue,
            "Revenue by Payment Mode": revenue_by_payment_mode,
            "Average Transaction Value": average_transaction_value,
            "Total Items Sold": items_count,
            "Average Items Per Bill": average_items_per_bill,
            "Maximum Items in a Single Bill": max_items,
            "Minimum Items in a Single Bill": min_items,
            "Highest Transaction Amount": max_transaction,
            "Lowest Transaction Amount": min_transaction,
            "Items by Payment Mode": items_by_payment_mode,
        }

        # Generate insights based on analysis
        insights = self.generate_insights(analysis_results)
        return {"Analysis Results": analysis_results, "Insights": insights}

    def generate_insights(self, results):
        insights = []
        payment_mode_distribution = results["Payment Mode Distribution"]

        # Convert percentages to floats for comparison
        max_payment_mode = max(payment_mode_distribution, key=lambda x: float(payment_mode_distribution[x][:-1]))
        min_payment_mode = min(payment_mode_distribution, key=lambda x: float(payment_mode_distribution[x][:-1]))

        # Insights based on payment mode
        insights.append(
            f"Most commonly used payment mode: {max_payment_mode} ({payment_mode_distribution[max_payment_mode]}).")
        insights.append(
            f"Least commonly used payment mode: {min_payment_mode} ({payment_mode_distribution[min_payment_mode]}).")

        # Revenue insights
        revenue_by_payment_mode = results["Revenue by Payment Mode"]
        max_revenue_mode = max(revenue_by_payment_mode, key=revenue_by_payment_mode.get)
        insights.append(
            f"Highest revenue is generated through {max_revenue_mode} payments, contributing ₹{revenue_by_payment_mode[max_revenue_mode]:,}.")

        # Transaction amount insights
        insights.append(f"The highest transaction value recorded is ₹{results['Highest Transaction Amount']}.")
        insights.append(f"The lowest transaction value recorded is ₹{results['Lowest Transaction Amount']}.")

        # Items insights
        max_items = results["Maximum Items in a Single Bill"]
        min_items = results["Minimum Items in a Single Bill"]
        average_items = results["Average Items Per Bill"]
        insights.append(f"Highest number of items in a single bill is {max_items}.")
        insights.append(f"Lowest number of items in a single bill is {min_items}.")
        insights.append(f"On average, {average_items:.2f} items are sold per bill.")

        return insights


# Example Usage
mockBills = [
    {"billId": "1012025", "phoneNumber": "9876543210", "items": 5, "totalAmount": "₹1500", "paymentMode": "UPI"},
    {"billId": "1012026", "phoneNumber": "9876543211", "items": 3, "totalAmount": "₹850", "paymentMode": "Cash"},
    {"billId": "1012027", "phoneNumber": "9876543212", "items": 7, "totalAmount": "₹2100", "paymentMode": "Card"},
    {"billId": "1012028", "phoneNumber": "9876543213", "items": 4, "totalAmount": "₹1200", "paymentMode": "UPI"},
    {"billId": "1012029", "phoneNumber": "9876543214", "items": 6, "totalAmount": "₹1800", "paymentMode": "Cash"},
    {"billId": "1012030", "phoneNumber": "9876543215", "items": 2, "totalAmount": "₹500", "paymentMode": "Card"},
    {"billId": "1012031", "phoneNumber": "9876543216", "items": 9, "totalAmount": "₹3500", "paymentMode": "UPI"},
    {"billId": "1012032", "phoneNumber": "9876543217", "items": 1, "totalAmount": "₹200", "paymentMode": "Cash"},
    {"billId": "1012033", "phoneNumber": "9876543218", "items": 8, "totalAmount": "₹2700", "paymentMode": "Card"},
    {"billId": "1012034", "phoneNumber": "9876543219", "items": 3, "totalAmount": "₹750", "paymentMode": "UPI"},
    {"billId": "1012035", "phoneNumber": "9876543220", "items": 4, "totalAmount": "₹1400", "paymentMode": "Cash"},
    {"billId": "1012036", "phoneNumber": "9876543221", "items": 5, "totalAmount": "₹1600", "paymentMode": "Card"},
    {"billId": "1012037", "phoneNumber": "9876543222", "items": 6, "totalAmount": "₹1950", "paymentMode": "UPI"},
    {"billId": "1012038", "phoneNumber": "9876543223", "items": 7, "totalAmount": "₹2300", "paymentMode": "Cash"},
    {"billId": "1012039", "phoneNumber": "9876543224", "items": 2, "totalAmount": "₹600", "paymentMode": "Card"},
    {"billId": "1012040", "phoneNumber": "9876543225", "items": 8, "totalAmount": "₹3200", "paymentMode": "UPI"},
    {"billId": "1012041", "phoneNumber": "9876543226", "items": 1, "totalAmount": "₹150", "paymentMode": "Cash"},
    {"billId": "1012042", "phoneNumber": "9876543227", "items": 9, "totalAmount": "₹4000", "paymentMode": "Card"},
    {"billId": "1012043", "phoneNumber": "9876543228", "items": 10, "totalAmount": "₹5000", "paymentMode": "UPI"},
    {"billId": "1012044", "phoneNumber": "9876543229", "items": 3, "totalAmount": "₹950", "paymentMode": "Cash"},
    {"billId": "1012045", "phoneNumber": "9876543230", "items": 5, "totalAmount": "₹2200", "paymentMode": "Card"},
    {"billId": "1012046", "phoneNumber": "9876543231", "items": 4, "totalAmount": "₹1700", "paymentMode": "UPI"},
    {"billId": "1012047", "phoneNumber": "9876543232", "items": 2, "totalAmount": "₹550", "paymentMode": "Cash"},
    {"billId": "1012048", "phoneNumber": "9876543233", "items": 6, "totalAmount": "₹2800", "paymentMode": "Card"},
    {"billId": "1012049", "phoneNumber": "9876543234", "items": 1, "totalAmount": "₹300", "paymentMode": "UPI"},
    {"billId": "1012050", "phoneNumber": "9876543235", "items": 7, "totalAmount": "₹3100", "paymentMode": "Cash"},
    {"billId": "1012051", "phoneNumber": "9876543236", "items": 8, "totalAmount": "₹3500", "paymentMode": "Card"},
    {"billId": "1012052", "phoneNumber": "9876543237", "items": 9, "totalAmount": "₹4500", "paymentMode": "UPI"},
    {"billId": "1012053", "phoneNumber": "9876543238", "items": 3, "totalAmount": "₹800", "paymentMode": "Cash"},
    {"billId": "1012054", "phoneNumber": "9876543239", "items": 4, "totalAmount": "₹1300", "paymentMode": "Card"},
]


bills = mockBills
analysis = BillAnalysis(bills)
results = analysis.analyze()

# Print results and insights
print("Analysis Results:")
for key, value in results["Analysis Results"].items():
    print(f"{key}: {value}")

print("\nInsights:")
for insight in results["Insights"]:
    print(insight)
