class Calculator:
    """계산기 클래스"""

    def __init__(self):
        self.memory = 0

    def add(self, a, b):
        """두 숫자를 더합니다."""
        return a + b

    def subtract(self, a, b):
        """첫 번째 숫자에서 두 번째 숫자를 뺍니다."""
        return a - b

    def multiply(self, a, b):
        """두 숫자를 곱합니다."""
        return a * b

    def divide(self, a, b):
        """첫 번째 숫자를 두 번째 숫자로 나눕니다.
        두 번째 숫자가 0일 경우 ZeroDivisionError를 발생시킵니다."""
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다.")
        return a / b

    def save_to_memory(self, value):
        """값을 메모리에 저장합니다."""
        self.memory = value

    def recall_memory(self):
        """메모리에 저장된 값을 반환합니다."""
        return self.memory

    def clear_memory(self):
        """메모리를 초기화합니다."""
        self.memory = 0
