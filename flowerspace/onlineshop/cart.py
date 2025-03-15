from .models import Product


SESSION_CART_ID = "cart"

class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(SESSION_CART_ID)
        if not isinstance(cart, dict):
            cart = {}
            self.session[SESSION_CART_ID] = cart
        self.cart = cart

    def save(self):
        self.session[SESSION_CART_ID] = self.cart
        self.session.modified = True


    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            if self.cart[product_id]["quantity"] > 1:
                self.cart[product_id]["quantity"] -= 1
            else:
                del self.cart[product_id]
            self.save()

    def items(self):
        for product_id, details in self.cart.items():
            product = Product.objects.get(id=product_id)
            yield {
                'product': product,
                'quantity': details['quantity'],
                'price': float(details['price']),
                'total_price': float(details['price']) * details['quantity'],
            }

    def add(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}
        self.cart[product_id]["quantity"] += quantity
        self.save()

    def get_total_price(self):
        return sum(int(item["price"]) * item["quantity"] for item in self.cart.values())

    def get_total_quantity(self):
        return sum(item["quantity"] for item in self.cart.values())

    def clear(self):
        if SESSION_CART_ID in self.session:
            del self.session[SESSION_CART_ID]
            self.session.modified = True


    def get_data(self):  # Changed to instance method
        cart_data = {
            "items": [
                {
                    "product": {
                        "id": item['product'].id,
                        "title": item['product'].title,
                        "image": item['product'].image.url,
                        "price": item['product'].price
                    },
                    "quantity": item['quantity'],
                    "instance": Product.objects.get(id=item['product'].id)
                }
                for item in self.items()
            ],
            "total_price": self.get_total_price(),
            "total_quantity": self.get_total_quantity(),
        }
        return cart_data