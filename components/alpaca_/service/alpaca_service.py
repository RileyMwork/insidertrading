from datetime import datetime, timedelta

class AlpacaService:
    def __init__(self):
        pass

    # def timestamp_helper(self, date):
    #     # date example 2024-01-16
    #     dt = datetime.strptime(date, "%Y-%m-%d")

    #     year = dt.year
    #     month = dt.month
    #     day = dt.day

    def generate_intervals(date_str):
    # Start at 10:00 AM the next day
        start = datetime.strptime(date_str, "%Y-%m-%d") + timedelta(days=1)
        start = start.replace(hour=10, minute=0, second=0, microsecond=0)

        intervals = []

        # 1 day later @ 10am
        intervals.append(("1_day_10am", start))

        # 1-8 hours after that
        for h in range(1, 9):
            intervals.append((f"{h}_hour", start + timedelta(hours=h)))

        # 24, 28, 32, 48 hours after that
        for h in [24, 28, 32, 48]:
            intervals.append((f"{h}_hours", start + timedelta(hours=h)))

        # 3-30 days after that
        for d in range(3, 31):
            intervals.append((f"{d}_days", start + timedelta(days=d)))

        return [
            {
                "interval": name,
                "year": dt.year,
                "month": dt.month,
                "day": dt.day,
                "hour": dt.hour
            }
            for name, dt in intervals
        ]



