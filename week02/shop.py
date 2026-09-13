class Customer:
    '''고객 이름, 등급, 포인트 관리'''
    def __init__(self, name, grade="basic"):
        self.name = name
        self.grade = grade
        self.points = 0

    def add_points(self, amount):
        '''구매액의 7% 적립'''
        self.points += int(amount*0.07) # 소수점 버림

    def get_discount_rate(self):
        '''고객 등급에 따라 할인율 반환'''
        if self.grade == "vip":
            return 0.15
        else:
            return 0.03

    def summary(self):
        '''고객 정보 요약(등급, 이름, 총 적립 포인트)'''
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
        '''결제 시 할인 적용 금액에서 적립율만큼 적립'''
        self.customer.add_points(self.total_price())

c1 = Customer("김철수")
c2 = Customer("이영희", "vip")

o1 = Order("01", c1, [("생수", 700)])
o1.add_item("삼각김밥", 2000) # 상품 추가
print(f"결제 금액: {o1.total_price():,}원")
o1.pay()
print(o1.customer.summary())

o2 = Order("02", c2, [("치즈", 10000), ("와인", 50000)])
print(f"결제 금액: {o2.total_price():,}원")
o2.pay()
print(o2.customer.summary())

o3 = Order("03", c2, [("위스키", 70000)])
print(f"결제 금액: {o3.total_price():,}원")
o3.pay()
print(o3.customer.summary())