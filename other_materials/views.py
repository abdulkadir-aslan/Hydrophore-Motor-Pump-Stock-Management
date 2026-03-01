from django.shortcuts import render,redirect,get_object_or_404
from .models import Category,CategoryStock,CategoryStockOut
from .forms import CategoryForm,CategoryStockForm,CategoryStockOutForm
from django.contrib import messages
from warehouses.views import handle_deletion,create_workshop_exit_slip
from warehouses.models import Order

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

    # listeleme için
    items = CategoryStock.objects.select_related('category').all().order_by('category__name', 'material_name')

    return render(request, "stok_form.html", {"form": form, "items": items})

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
    if request.method == "POST":
        outlet_plug = request.POST.get("outlet_plug")
        if outlet_plug:
            outlet_plug = Order.objects.filter(outlet_plug=outlet_plug).first()
            if outlet_plug:
                return redirect("new_category_stock_out", id=outlet_plug.id)
            else:
                messages.warning(request,"Çıkış fişi kayıtlarda yok.")

    queryset = CategoryStockOut.objects.all()
    # order_filter = OrderFilter(request.GET, queryset=queryset)
    # filtered_qs = order_filter.qs

    # page_obj = paginate_items(request, filtered_qs)
    # context = {
    #     # 'total': filtered_qs.count(),
    #     # 'items': page_obj,
    #     'query_string': request.GET.urlencode(),
    #     'filter': order_filter,
    # }
    context = {
        'items': queryset,
    }
    return render(request, "category_stock_out.html", context)

def new_category_stock_out(request,id):
    item = get_object_or_404(Order, id=id)
    form = CategoryStockOutForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            stock = form.save(commit=False)
            stock.order = item
            stock.save()
            create_workshop_exit_slip("other",stock)
            return redirect("category_stock_out")
        else:
            messages.warning(request, form.errors.as_ul())

    return render(request, "new_category_stock_out.html", {
        "form": form,
        "item": item,
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
        "item": item.order,
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