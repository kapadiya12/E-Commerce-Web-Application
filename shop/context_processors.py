from .models import Cart

def cart_count(request):
    """
    Global cart count for navbar.
    Returns TOTAL QUANTITY of items in cart (2+3+1 = 6)
    """

    try:
        # Ensure session exists
        if not request.session.session_key:
            request.session.create()

        session_key = request.session.session_key

        # If user is logged in, get cart by user
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            # Guest cart by session
            cart = Cart.objects.filter(session_key=session_key, user=None).first()

        if cart:
            return {"cart_item_count": cart.get_item_count()}

        return {"cart_item_count": 0}

    except Exception:
        return {"cart_item_count": 0}
