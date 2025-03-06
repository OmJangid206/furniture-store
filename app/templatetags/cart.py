from django import template

register = template.Library()


@register.filter(name="is_in_cart")
def is_in_cart(product, cart):
    for cart_item in cart:
        if cart_item.product.id == product.id:
            return True
    return False

@register.filter(name="cart_quantity")
def cart_quantity(product, cart):
    for cart_item in cart:
        if cart_item.product.id == product.id:
            return cart_item.product_qty
    return 0

@register.filter(name="total_price")
def total_price(product, cart):
    return product.price * cart_quantity(product, cart)


@register.filter(name="total_cart_price")
def total_cart_price(products, cart):
    total = 0
    for p in products:
        total += p.price * cart_quantity(p, cart)
    return total
