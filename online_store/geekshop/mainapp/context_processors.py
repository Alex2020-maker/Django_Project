from cartapp.models import Cart

def cart(request):
   cart = []

   if request.user.is_authenticated:
       cart = Cart.objects.filter(user=request.user)

   return {
       'cart': cart,
   }