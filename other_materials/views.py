from django.shortcuts import render,redirect,get_object_or_404
from .models import Category,CategoryStock,CategoryStockOut
from .forms import CategoryForm,CategoryStockForm,CategoryStockOutForm
from django.contrib import messages
from warehouses.views import handle_deletion,paginate_items
from .filters import CategoryStockFilter,CategoryStockOutFilter

def category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, f"*{item.name}* Kayıt başarılı.")
            return redirect('category')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = CategoryForm()
    context = {
        'items': Category.objects.all().order_by("-id"),
        'form': form
    }
    return render(request, "category.html", context)

def delete_category(request, id):
    return handle_deletion(
        request,
        Category,
        id,
        'category',
        "*{0}* Kategori başarıyla silindi.",
        "Kategori bulunamadı.",
        "*{0}* Kategori kaydı {1} tabloda kullanılıyor, silinemez."
    )

def category_stock(request):
    if request.method == "POST":
        # Eğer ID varsa, mevcut ürünü güncelliyoruz.
        item_id = request.POST.get('item_id', None)
        # Eğer mevcut ürün varsa, düzenlemeye çalışıyoruz.
        if item_id:
            items = get_object_or_404(CategoryStock, id=item_id)
            form = CategoryStockForm(request.POST, instance=items)
        else:
            form = CategoryStockForm(request.POST)
        
        if form.is_valid():
            item = form.save(commit=False)
            
            # Eğer quantity_value var ise, quantity değerini formdan al
            if form.cleaned_data.get("quantity_value"):
                items.quantity = form.cleaned_data["quantity"]
                
            # Eğer material_name_value var ise, material_name değerini formdan al
            if form.cleaned_data.get("material_name_value"):
                items.material_name = form.cleaned_data["material_name"]
                
            # Eğer category_value var ise, category değerini formdan al
            if form.cleaned_data.get("category_value"):
                items.category = form.cleaned_data["category"]
            if item_id:
                items.save()
            else:
                item.save()
            messages.success(request, "Kayıt başarılı.")
            return redirect("category_stock")
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = CategoryStockForm()

    queryset = CategoryStock.objects.select_related('category').all().order_by('category__name', 'material_name')
    filterset = CategoryStockFilter(request.GET, queryset=queryset)
    filtered_qs = filterset.qs
    page_obj = paginate_items(request, filtered_qs)
    
    return render(request, "stok_form.html", {
        'filter': filterset,
        'total': filtered_qs.count(),
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
        'form' : form
    })

def delete_category_stock(request, id):
    return handle_deletion(
        request,
        CategoryStock,
        id,
        'category_stock',
        "*{0}* Malzeme kaydı başarıyla silindi.",
        "Malzeme kaydı bulunamadı.",
        "*{0}* Malzeme kaydı {1} tabloda kullanılıyor, silinemez."
    )
    
def category_stock_out(request):

    queryset = CategoryStockOut.objects.select_related(
        'stock',
        'stock__category'
    ).all().order_by('-created_at')

    filterset = CategoryStockOutFilter(request.GET, queryset=queryset)
    filtered_qs = filterset.qs
    page_obj = paginate_items(request, filtered_qs)

    context = {
        'filter': filterset,
        'total': filtered_qs.count(),
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }

    return render(request, "category_stock_out.html", context)

def new_category_stock_out(request):
    form = CategoryStockOutForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("category_stock_out")
        else:
            messages.warning(request, form.errors.as_ul())

    return render(request, "new_category_stock_out.html", {
        "form": form,
    })

def edit_category_stock_out(request,id):
    item = get_object_or_404(CategoryStockOut, id=id)
    if request.method == "POST":
        form = CategoryStockOutForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("category_stock_out")
        else:
            messages.warning(request, form.errors.as_ul())

    else:
        form = CategoryStockOutForm( instance=item)
    return render(request, "new_category_stock_out.html", {
        "form": form,
    })

def delete_category_stock_out(request, id):
    return handle_deletion(
        request,
        CategoryStockOut,
        id,
        'category_stock_out',
        "*{0}* Malzeme kaydı başarıyla silindi.",
        "Malzeme kaydı bulunamadı.",
        "*{0}* Malzeme kaydı {1} tabloda kullanılıyor, silinemez."
    )