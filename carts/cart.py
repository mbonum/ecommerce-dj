from django.conf import settings

from shop.models import Item


CART_ID = getattr(settings, "CART_SESSION_ID", "cart")

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_ID)

        if not cart:
            cart = self.session[CART_ID] = {}

        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        product_clean_ids = []
        for p in product_ids:
            product_clean_ids.append(p)
            self.cart[str(p)]["product"] = Item.objects.get(pk=p)
        for i in self.cart.values():
            i["total_price"] = float(i["price"]) * int(i["quantity"])
            yield i

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        price = float(product.price)
        if product_id not in self.cart:
            self.cart[product_id] = {"id": product_id, "price": price, "quantity": 0}
        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] = self.cart[product_id]["quantity"] + 1
        self.save()

    def has_product(self, product_id):
        if str(product_id) in self.cart:
            return True
        else:
            return False

    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_length(self):
        return sum(int(i["quantity"]) for i in self.cart.values())

    def get_total_cost(self):
        return sum(float(i["total_price"]) for i in self)
