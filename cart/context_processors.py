from cart.models import Cart


def cart_items(request):
    total=0
    u=request.user
    try:
        c=Cart.objects.filter(user=u)
        for i in c:
           total+=i.quantity
    except:
        total=0
    return {'count':total}