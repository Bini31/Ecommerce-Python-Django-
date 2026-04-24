from django.shortcuts import render
from django.views import View
from shop.models import Category,Product
from django.db.models import Q
# Create your views here.
class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')

        p = Product.objects.filter(Q(name__icontains=query) |
                                Q(description__icontains=query) |
                                Q(price__icontains=query))
                                # Q(pages__icontains=query) |
                                # Q(language__icontains=query))
        context = {'products': p}
        return render(request, "search.html", context)
