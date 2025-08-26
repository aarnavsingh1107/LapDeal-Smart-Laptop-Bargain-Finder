

class LaptopResaleCalculator:
    def __init__(self, base_price: float):
        self.base_price = base_price
        self.r1, self.r2, self.r3 = 0.28, 0.18, 0.12  
        self.beta = 0.15  # Floor price percentage

        # Multipliers based on condition
        self.condition_multipliers = {
            "Excellent": 1.0,
            "Good": 0.9,
            "Average": 0.8,
            "Poor": 0.65
        }

    def calculate(self, years_used: int, condition: str) -> float:
        """Calculate resale price based on years and condition."""
        k_cond = self.condition_multipliers.get(condition, 1.0)
        floor_price = self.beta * self.base_price

        # Apply depreciation
        depreciation = 1.0
        depreciation *= (1 - self.r1) ** min(years_used, 1)
        depreciation *= (1 - self.r2) ** max(0, min(years_used - 1, 2))
        depreciation *= (1 - self.r3) ** max(0, years_used - 3)

        resale_price = self.base_price * depreciation * k_cond
        return max(resale_price, floor_price)
