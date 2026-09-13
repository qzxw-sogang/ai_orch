class Customer:
    '''고객 이름, 등급, 할인율, 적립율 관리'''
    def __init__(self, name, grade = "basic"):
        self.name = name
        self.grade = grade
        self.points = 0

    def add_points(self, amount):
        '''구매액의 5% 적립'''
        self.points += int(amount*0.05) # 소수점 버림

    def get_discount_rate(self):
        '''고객 등급에 따라 할인율 반환'''
        if self.grade == "vip":
            return 0.10
        else:
            return 0.03

    def summary(self):
        '''고객 정보 요약'''
        return f"[{self.grade}] {self.name} (포인트: {self.points:,})"

class Order:
    '''주문 상품, 가격, 결제 관리'''
    def __init__(self, order_id, customer, items):
        self.order_id = order_id
        self.customer = customer
        self.items = list(items)

    def total_price(self):
        '''할인 적용 후 총 금액 반환'''
        total = sum(price for _, price in self.items)
        discount = self.customer.get_discount_rate()
        return int(total*(1-discount))

    def add_item(self, name, price):
        '''구매 상품 추가'''
        self.items.append((name, price))

    def pay(self):
        '''결제 시 할인 적용 금액에서 5% 포인트 적립'''
        self.customer.add_points(self.total_price())
        return f"포인트: {self.customer.points:,}원"
