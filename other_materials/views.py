from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Category,CategoryStock,CategoryStockOut
from .forms import CategoryForm,CategoryStockForm,CategoryStockOutForm
from django.contrib import messages
from warehouses.views import handle_deletion,paginate_items
from .filters import CategoryStockFilter,CategoryStockOutFilter
from account.decorators import administrator,admin

@admin
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

@administrator
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
    queryset = CategoryStock.objects.select_related('category').all().order_by('category__name', 'material_name')
    filterset = CategoryStockFilter(request.GET, queryset=queryset)
    filtered_qs = filterset.qs
    page_obj = paginate_items(request, filtered_qs)
    
    return render(request, "stok_form.html", {
        'filter': filterset,
        'total': filtered_qs.count(),
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    })

@admin
def new_category_stock(request):
    initial_data = {}

    category_id = request.GET.get("category")
    if category_id:
        initial_data["category"] = category_id

    form = CategoryStockForm(request.POST or None, initial=initial_data)

    if request.method == "POST":
        if form.is_valid():
            obj = form.save()

            messages.success(
                request, 
                f"{obj.category} - {obj.material_name} - {obj.quantity} Adet Malzeme başarıyla kaydedildi."
            )

            if "save_and_add" in request.POST:
                # Sadece category parametresi gönderiyoruz
                params = urlencode({"category": obj.category.id})
                return redirect(f"{reverse('new_category_stock')}?{params}")

            return redirect("category_stock")
        else:
            messages.warning(request, form.errors.as_ul())

    return render(request, "new_stock.html", {"form": form})

@administrator
def edit_category_stock(request,id):
    item = get_object_or_404(CategoryStock, id=id)
    if request.method == "POST":
        form = CategoryStockForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("category_stock")
        else:
            messages.warning(request, form.errors.as_ul())

    else:
        form = CategoryStockForm( instance=item)
    return render(request, "new_stock.html", {
        "form": form,
    })

@administrator
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

from urllib.parse import urlencode
@admin
def new_category_stock_out(request):
    initial_data = {}

    # Eğer GET ile değer geldiyse forma doldur
    outlet_plug = request.GET.get("outlet_plug")
    well_number = request.GET.get("well_number")
    district = request.GET.get("district")
    address = request.GET.get("address")

    if outlet_plug:
        initial_data["outlet_plug"] = outlet_plug
    if well_number:
        initial_data["well_number"] = well_number
    if district:
        initial_data["district"] = district
    if address:
        initial_data["address"] = address

    form = CategoryStockOutForm(request.POST or None, initial=initial_data)

    if request.method == "POST":
        if form.is_valid():
            obj = form.save()

            messages.success(request, f"{obj.outlet_plug} - {obj.stock} - {obj.quantity} Adet \n Malzeme çıkışı başarıyla kaydedildi.")
            if "save_and_add" in request.POST:
                params = urlencode({
                    "outlet_plug": obj.outlet_plug,
                    "well_number": obj.well_number,
                    "district": obj.district,
                    "address": obj.address
                })

                return redirect(f"/malzeme_cikis_islemler/?{params}")

            return redirect("category_stock_out")

        else:
            messages.warning(request, form.errors.as_ul())

    return render(request, "new_category_stock_out.html", {
        "form": form,
    })

@administrator
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

@administrator
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