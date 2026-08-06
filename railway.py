import json
import os

class RailwaySystem:
    def __init__(self):
        # Sample Initial Train Data according to required specifications
        self.trains = [
            {
                "train_number": "T101",
                "route": "New York - Boston",
                "total_seats": 200,
                "booked_seats": 180,
                "waiting_list_count": 15,
                "ticket_fare": 50.0,
                "cancellation_count": 10,
                "distance": 350
            },
            {
                "train_number": "T102",
                "route": "Los Angeles - San Francisco",
                "total_seats": 300,
                "booked_seats": 120,
                "waiting_list_count": 0,
                "ticket_fare": 75.0,
                "cancellation_count": 5,
                "distance": 610
            },
            {
                "train_number": "T103",
                "route": "Chicago - Detroit",
                "total_seats": 150,
                "booked_seats": 145,
                "waiting_list_count": 25,
                "ticket_fare": 40.0,
                "cancellation_count": 12,
                "distance": 450
            },
            {
                "train_number": "T104",
                "route": "Miami - Orlando",
                "total_seats": 250,
                "booked_seats": 240,
                "waiting_list_count": 30,
                "ticket_fare": 60.0,
                "cancellation_count": 8,
                "distance": 370
            }
        ]
        self.report_filename = "reservation_analytics_report.json"

    # 1. Calculate occupancy ratio
    def get_occupancy_ratio(self, train):
        return (train["booked_seats"] / train["total_seats"]) * 100

    # 2. Calculate actual revenue after cancellations
    def get_actual_revenue(self, train):
        # Net booked tickets = booked seats minus cancelled seats
        net_seats = max(0, train["booked_seats"] - train["cancellation_count"])
        return net_seats * train["ticket_fare"]

    # 3. Identify overbooked or high-demand trains
    def get_high_demand_trains(self):
        # High demand if occupancy ratio >= 90% or there is a waiting list
        high_demand = []
        for t in self.trains:
            if self.get_occupancy_ratio(t) >= 90.0 or t["waiting_list_count"] > 0:
                high_demand.append(t["train_number"])
        return high_demand

    # 4. Calculate revenue per kilometer
    def get_revenue_per_km(self, train):
        revenue = self.get_actual_revenue(train)
        return revenue / train["distance"] if train["distance"] > 0 else 0

    # 5. Find the route with maximum revenue
    def get_max_revenue_route(self):
        if not self.trains:
            return None
        max_train = max(self.trains, key=self.get_actual_revenue)
        return max_train["route"], self.get_actual_revenue(max_train)

    # 6. Display trains with occupancy below 50%
    def display_low_occupancy_trains(self):
        print("\n--- Trains with Occupancy Below 50% ---")
        found = False
        for t in self.trains:
            ratio = self.get_occupancy_ratio(t)
            if ratio < 50.0:
                print(f"Train {t['train_number']} ({t['route']}) - Occupancy: {ratio:.2f}%")
                found = True
        if not found:
            print("No trains found with occupancy below 50%.")

    # 7. Sort trains by revenue
    def sort_trains_by_revenue(self):
        return sorted(self.trains, key=self.get_actual_revenue, reverse=True)

    # 8. Generate a reservation analytics report
    def generate_report(self):
        report = {}
        for t in self.trains:
            report[t["train_number"]] = {
                "Route": t["route"],
                "Occupancy Ratio (%)": round(self.get_occupancy_ratio(t), 2),
                "Actual Revenue ($)": round(self.get_actual_revenue(t), 2),
                "Revenue per KM ($)": round(self.get_revenue_per_km(t), 2),
                "Demand Status": "High Demand" if t["train_number"] in self.get_high_demand_trains() else "Normal"
            }
        return report

    # 9. Save and read the report from a file
    def save_and_read_report(self):
        report_data = self.generate_report()
        # Writing to file
        with open(self.report_filename, 'w') as file:
            json.dump(report_data, file, indent=4)
        print(f"\n[Success] Report saved successfully to '{self.report_filename}'")

        # Reading from file
        if os.path.exists(self.report_filename):
            with open(self.report_filename, 'r') as file:
                loaded_report = json.load(file)
            print("\n--- Read Data from Analytics Report File ---")
            print(json.dumps(loaded_report, indent=4))

    # 10. Display top three revenue-generating trains
    def display_top_three_trains(self):
        sorted_list = self.sort_trains_by_revenue()
        print("\n--- Top 3 Revenue-Generating Trains ---")
        for i, t in enumerate(sorted_list[:3], 1):
            print(f"{i}. Train {t['train_number']} | Route: {t['route']} | Revenue: ${self.get_actual_revenue(t):.2f}")

    # Orchestrator metric runtime execution
    def run_all_metrics(self):
        print("=== SMART RAILWAY SYSTEM METRICS PERFORMANCE ===")
        
        # Metric 1 & 2 Demo
        print("\n--- Individual Train Analytics (Occupancy & Revenue) ---")
        for t in self.trains:
            print(f"Train {t['train_number']}: Occupancy = {self.get_occupancy_ratio(t):.2f}%, "
                  f"Net Revenue = ${self.get_actual_revenue(t):.2f}")
            
        # Metric 3 Demo
        print(f"\nHigh Demand Trains (Overbooked/Waiting List): {self.get_high_demand_trains()}")
        
        # Metric 4 Demo
        print("\n--- Revenue Per Kilometer ---")
        for t in self.trains:
            print(f"Train {t['train_number']}: ${self.get_revenue_per_km(t):.2f}/km")
            
        # Metric 5 Demo
        route, max_rev = self.get_max_revenue_route()
        print(f"\nRoute with Maximum Revenue: {route} (${max_rev:.2f})")
        
        # Metric 6 Demo
        self.display_low_occupancy_trains()
        
        # Metric 7 Demo
        print("\n--- Trains Sorted by Revenue (Highest to Lowest) ---")
        for t in self.sort_trains_by_revenue():
            print(f"Train {t['train_number']}: ${self.get_actual_revenue(t):.2f}")
            
        # Metric 10 Demo
        self.display_top_three_trains()
        
        # Metric 8 & 9 Demo
        self.save_and_read_report()

if __name__ == "__main__":
    system = RailwaySystem()
    system.run_all_metrics()
