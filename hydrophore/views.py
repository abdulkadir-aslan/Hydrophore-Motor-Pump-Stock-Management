from django.shortcuts import render,redirect
from .models import Hydrophore,PumpType,Power,OutboundWorkOrder,RepairReturn,WorkshopExit,DistrictFieldPersonnel
from .forms import PumpTypeForm,RepairReturnForm,PowerForm,HydrophoreForm,OutboundWorkOrderForm,DistrictFieldPersonnelForm,WorkshopExitForm
from warehouses.views import handle_deletion,paginate_items,IntegrityError,get_object_or_404,transaction,create_workshop_exit_slip
from .filters import HydrophoreFilter,HydrophoreAllFilter,OutboundWorkOrderFilter
from django.contrib import messages
from django.http import JsonResponse

def pump_type(request):
    if request.method == "POST":
        form = PumpTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"*{form.data['type']}* Kayıt başarılı.")
            return redirect('pump_type')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = PumpTypeForm()
    context = {
        'items': PumpType.objects.all().order_by("-id"),
        'form': form
    }
    return render(request, "pump_type.html", context)

def pump_type_delete(request, id):
    return handle_deletion(
        request,
        PumpType,
        id,
        'pump_type',
        "*{0}* Pompa Tipi başarıyla silindi.",
        "Pompa Tipi bulunamadı.",
        "*{0}* Pompa kaydı {1} tabloda kullanılıyor, silinemez."
    )

def new_power(request):
    if request.method == "POST":
        form = PowerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"*{form.data['power']}* Kayıt başarılı.")
            return redirect('new_power')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = PowerForm()

    context = {
        'items': Power.objects.all().order_by("-id"),
        'form': form
    }
    return render(request, "power.html", context)

def hydrophore_power_delete(request, id):
    return handle_deletion(
        request,
        Power,
        id,
        'new_power',
        "*{0}* Güç değeri başarıyla silindi.",
        "Güç değeri bulunamadı.",
        "*{0}* Güç kaydı {1} tabloda kullanılıyor, silinemez."
    )

def hydrophore_homepage(request):
    queryset = Hydrophore.objects.all().order_by("serial_number")
    
    hydrophore_filter = HydrophoreAllFilter(request.GET, queryset=queryset)
    filtered_qs = hydrophore_filter.qs
    
    page_obj = paginate_items(request, filtered_qs)

    contex = {
        'filter': hydrophore_filter,
        'total': filtered_qs.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "hydrophore_homepage.html",contex)

def hydrophore_delete(request, id):
    return handle_deletion(
        request,
        Hydrophore,
        id,
        'hydrophore_homepage',
        "*{0}* Hidrofor kaydı başarıyla silindi.",
        "Hidrofor kaydı bulunamadı.",
        "*{0}* Hidrofor kaydı {1} tabloda kullanılıyor, silinemez."
    )
    
def hydrophore_edit(request, pk):
    item = get_object_or_404(Hydrophore, pk=pk)

    # next'i al (GET)
    next_url = request.GET.get('next')

    if request.method == 'POST':
        form = HydrophoreForm(request.POST, instance=item)

        # next'i POST'tan tekrar al
        next_url = request.POST.get('next')

        if form.is_valid():
            item = form.save()
            messages.success(request, f"*{item.serial_number}* Hidrofor bilgileri güncellendi.")
            return redirect(next_url or 'hydrophore_homepage')
        else:
            messages.warning(
                request,
                form.errors.as_ul()
            )
    else:
        form = HydrophoreForm(instance=item)

    return render(request, 'new_hydrophore.html', {
        'form': form,
        'next': next_url
    })

################ İş Emirleri ################
def district_field_personnel(request, id=None):
    items = DistrictFieldPersonnel.objects.all().order_by('-id')
    page_obj = paginate_items(request, items)
    instance = get_object_or_404(DistrictFieldPersonnel, id=id) if id else None
    form = DistrictFieldPersonnelForm(request.POST or None, instance=instance)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Personel bilgileri kaydedildi.")
        return redirect('district_field_personnel')

    context = {
        'total': items.count(),
        'items': page_obj,
        'form': form,
    }
    return render(request, "district_field_personnel.html", context)

def get_personnel_by_district(request):
    district = request.GET.get('district')
    if district:
        personnel = DistrictFieldPersonnel.objects.filter(district=district, is_active=True)
        data = [{"id": p.id, "name": p.full_name} for p in personnel]
        return JsonResponse({"personnel": data})
    return JsonResponse({"personnel": []})

def district_field_personnel_delete(request, id):
    return handle_deletion(
        request,
        DistrictFieldPersonnel,
        id,
        'district_field_personnel',
        "*{0}* Personel bilgileri başarıyla silindi.",
        "Personel bilgisi bulunamadı.",
        "*{0}* Personel kaydı {1} tabloda kullanılıyor, silinemez."
    )

def search_hydrophore(request):
    serial_number = request.GET.get('serial_number', '').strip().upper()
    if not serial_number:
        return JsonResponse({'error': 'Lütfen bir seri numarası giriniz.'}, status=400)

    try:
        hydrophore = Hydrophore.objects.get(serial_number=serial_number)
        if hydrophore.location == "4":
            data = {
                'id': hydrophore.id,
                'serial_number': hydrophore.serial_number,
                'engine_power': str(hydrophore.engine_power),
                'pump_type': str(hydrophore.pump_type),
                'location': hydrophore.get_location_display(),
                'district': hydrophore.get_district_display(),
                'neighborhood' :hydrophore.neighborhood
            }
            return JsonResponse({'hydrophore': data})
        else:
           return JsonResponse({'error': f'Hidrofor Lokasyonu: *{hydrophore.get_location_display()}* --- Bu hidroforu kullanamazsınız kullanabilmeniz için lokasyonun *Arazi* veya *Sıfır* depo olması gerekiyor.'}, status=404)
    except Hydrophore.DoesNotExist:
        return JsonResponse({'error': 'Hidrofor bulunamadı!'}, status=404)

def new_outbound_work_order(request, id):
    hydrophore = get_object_or_404(Hydrophore, id=id)

    if request.method == "POST":
        form = OutboundWorkOrderForm(request.POST)
        if form.is_valid():
            
            with transaction.atomic():
                order = form.save(commit=False)
                order.mounted_hydrophore = hydrophore
                if form.data["action"] == "close":
                    hydrophore.location = "4"
                    hydrophore.district = order.district
                    hydrophore.neighborhood = order.neighborhood
                    order.status = "passive"
                    order.save()
                    create_workshop_exit_slip("hydrophore",order)
                    hydrophore.save()
                    messages.success(request, f"İş Emri Kapandı.")
                    return redirect("outbound_work_order")
                
                # Varsayılan durum
                hydrophore.location = "3"

                disassembled = order.disassembled_hydrophore
                if disassembled:
                    order.status = "passive"
                    hydrophore.location = "4"
                    hydrophore.district = order.district
                    hydrophore.neighborhood = order.neighborhood
                    disassembled.location = "2"
                    disassembled.save()
                    order.save()
                    create_workshop_exit_slip("hydrophore",order)
                    WorkshopExit.objects.create(
                        hydrophore=disassembled,
                        outbound_work_order=order,
                    )
                    messages.success(request, f"İş Emri Kapandı.")
                else:
                    order.save()
                    messages.success(request, f"İş Emri Oluşturuldu.")
                hydrophore.save()

            return redirect("outbound_work_order")

        messages.warning(
            request,
            f"Formda hatalar var. Lütfen kontrol edin: {form.errors.as_ul()}"
        )
    else:
        form = OutboundWorkOrderForm()

    return render(
        request,
        "new_outbound_work_order.html",
        {"form": form, "hydrophore": hydrophore}
    )

def all_outbound_work_order(request):
    queryset = OutboundWorkOrder.objects.filter(status="passive").order_by('-id')
    hydrophore_filter = OutboundWorkOrderFilter(request.GET, queryset=queryset)
    filtered_qs = hydrophore_filter.qs
    
    page_obj = paginate_items(request, filtered_qs)
    
    contex = {
        'filter': hydrophore_filter,
        'total': queryset.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "all_outbound_work_order.html",contex)

def outbound_work_order_edit(request,pk):
    item = get_object_or_404(OutboundWorkOrder, pk=pk)
    if request.method == 'POST':
        form = OutboundWorkOrderForm(request.POST, instance=item)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)

                disassembled = order.disassembled_hydrophore
                mounted = order.mounted_hydrophore
                if form.data["action"] == "close":
                    mounted.location = "4"
                    mounted.district = order.district
                    mounted.neighborhood = order.neighborhood
                    order.status = "passive"
                    order.save()
                    mounted.save()
                    create_workshop_exit_slip("hydrophore",order)
                    messages.success(request, f"İş Emri Kapandı.")
                    return redirect("outbound_work_order")
                
                if disassembled:
                    order.status = "passive"
                    mounted.location = "4"
                    disassembled.location = "2"
                    mounted.save()
                    disassembled.save()

                    order.save()  
                    WorkshopExit.objects.create(
                        hydrophore=disassembled,
                        outbound_work_order=order,
                    )
                    messages.success(request, f"İş Emri Kapandı.")
                else:
                    order.save()
                    messages.success(request, f"İş Emri Güncellendi.")
                order.save()

            return redirect("outbound_work_order")

        messages.warning(
            request,
            f"Formda hatalar var. Lütfen kontrol edin: {form.errors.as_ul()}"
        )
    else:
        form = OutboundWorkOrderForm(instance=item)
    return render(
        request,
        "new_outbound_work_order.html",
        {"form": form, "hydrophore": item.mounted_hydrophore, "form_edit":True}
    )

def outbound_work_order(request):
    queryset = OutboundWorkOrder.objects.filter(status="active").order_by('-id')
    if request.method == "POST":
        hydrophore = Hydrophore.objects.filter(serial_number=request.POST.get("hydropore").upper().strip()).first()
        if not hydrophore:
            messages.warning(request, "Bu Hidrofor numarası bulunamadı.")
            return redirect("outbound_work_order")

        if hydrophore.location not in ["1", "6"]:
            messages.info(request, f"Bu hidroforun mevcut lokasyonu: {hydrophore.get_location_display()}")
        else:
            return redirect("new_outbound_work_order", id=hydrophore.id)
    
    hydrophore_filter = OutboundWorkOrderFilter(request.GET, queryset=queryset)
    filtered_qs = hydrophore_filter.qs
    
    page_obj = paginate_items(request, filtered_qs)

    contex = {
        'filter': hydrophore_filter,
        'total': queryset.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "outbound_work_order.html",contex)

def outbound_work_order_delete(request, id):
    return handle_deletion(
        request,
        OutboundWorkOrder,
        id,
        'outbound_work_order',
        "*{0}* İş Emri Kaydı başarıyla silindi.",
        "İş Emri kaydı bulunamadı.",
        "*{0}* İş Emri kaydı {1} tabloda kullanılıyor, silinemez."
    )

def workshop_exit(request):
    item = WorkshopExit.objects.filter(status="active").order_by('-id')
    page_obj = paginate_items(request, item)

    contex = {
        'total': item.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "workshop_exit.html",contex)

def workshop_exit_edit(request, pk):
    item = get_object_or_404(WorkshopExit, pk=pk)
    if request.method == 'POST':
        form = WorkshopExitForm(request.POST, instance=item)
        if form.is_valid():
            order = form.save(commit=False)
            hydrophore = order.hydrophore
            hydrophore.location = "5" #Tamirde
            order.status = "passive"
            hydrophore.save()
            order.save()
            RepairReturn.objects.create(
                        hydrophore=hydrophore,
                        workshop_exit=order,
                    )
            messages.success(request, f"{item.hydrophore} Hidrofor tamire gönderildi.")
            return redirect('workshop_exit')
        else:
            messages.warning(
            request,
            f"Formda hatalar var. Lütfen kontrol edin: {form.errors.as_ul()}"
        )
    else:
        form = WorkshopExitForm(instance=item)
    return render(request, 'workshop_exit_edit.html', {'form': form,'workshop':item})

def workshop_exit_delete(request, id):
    return handle_deletion(
        request,
        WorkshopExit,
        id,
        'outbound_work_order',
        "*{0}* Demontaj Edilen Hidrofor kaydı başarıyla silindi. \n İş emirleri sekmesine yönlendirildiniz mevcut iş emri üzerinden işlemlere devam edebilirsiniz.",
        "Hidrofor kaydı bulunamadı.",
        "*{0}* Hidrofor kaydı {1} tabloda kullanılıyor, silinemez."
    )

def all_workshop_exit(request):
    item = WorkshopExit.objects.filter(status="passive").order_by('-id')
    page_obj = paginate_items(request, item)
    
    contex = {
        'total': item.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "all_workshop_exit.html",contex)

def repair_return(request):
    item = RepairReturn.objects.filter(status="active").order_by('-id')
    page_obj = paginate_items(request, item)

    contex = {
        'total': item.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "repair_return.html",contex)

def repair_return_delete(request, id):
    return handle_deletion(
        request,
        RepairReturn,
        id,
        'workshop_exit',
        "*{0}* Tamire Gelen Hidrofor kaydı başarıyla silindi. \n Tamire Gidecek İş Emirleri sekmesine yönlendirildiniz mevcut iş emri üzerinden işlemlere devam edebilirsiniz.",
        "Hidrofor kaydı bulunamadı.",
        "*{0}* Hidrofor kaydı {1} tabloda kullanılıyor, silinemez."
    )

def repair_return_edit(request, pk):
    item = get_object_or_404(RepairReturn, pk=pk)
    if request.method == 'POST':

        form = RepairReturnForm(request.POST, instance=item)
        if form.is_valid():
            order = form.save(commit=False)
            hydrophore = order.hydrophore
            action = request.POST.get("action")
            if action == "pert":
                hydrophore.location = "7"
            elif action == "workshop":
                hydrophore.location = "1"

            order.status = "passive"
            hydrophore.save()
            order.save()
            messages.success(request, f"{item.hydrophore} Hidrofor ilgili depoya gönderildi.")
            return redirect('repair_return')
        else:
            messages.warning(
            request,
            f"Formda hatalar var. Lütfen kontrol edin: {form.errors.as_ul()}"
        )
    else:
        form = RepairReturnForm(instance=item)
    return render(request, 'repair_return_edit.html', {'form': form,'repair':item})

def all_repair_return(request):
    item = RepairReturn.objects.filter(status="passive").order_by('-id')
    page_obj = paginate_items(request, item)
    
    contex = {
        'total': item.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "all_repair_return.html",contex)

######## Depolar ###########################33
def workshop_stock(request):
    queryset = Hydrophore.objects.filter(location="1").order_by("serial_number")
    
    hydrophore_filter = HydrophoreFilter(request.GET, queryset=queryset)
    filtered_qs = hydrophore_filter.qs
    
    page_obj = paginate_items(request, filtered_qs)

    if request.method == "POST":
        form = HydrophoreForm(request.POST)
        if form.is_valid():
            try:
                item = form.save()
                messages.success(
                    request,
                    f'*{item}* Hidrofor kaydı başarılı bir şekilde oluşturuldu.'
                )
                return redirect('workshop_stock')
            except IntegrityError:
                messages.warning(
                    request,
                    'Bu seri numarası daha önce kullanılmış.'
                )
        else:
            messages.warning(
                request,
                f"Formda hatalar var. Lütfen kontrol edin: {form.errors.as_ul()}"
            )
    else:
        form = HydrophoreForm()
    
    contex = {
        'form' : form,
        'filter': hydrophore_filter,
        'total': filtered_qs.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "warehouse/workshop_stock.html",contex)

def repair_stock(request):
    queryset = Hydrophore.objects.filter(location="2").order_by("serial_number")
    
    hydrophore_filter = HydrophoreFilter(request.GET, queryset=queryset)
    filtered_qs = hydrophore_filter.qs
    
    page_obj = paginate_items(request, filtered_qs)

    contex = {
        'filter': hydrophore_filter,
        'total': filtered_qs.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "warehouse/repair_stock.html",contex)

def repair_list(request):
    queryset = Hydrophore.objects.filter(location="5").order_by("serial_number")
    
    hydrophore_filter = HydrophoreFilter(request.GET, queryset=queryset)
    filtered_qs = hydrophore_filter.qs
    
    page_obj = paginate_items(request, filtered_qs)

    contex = {
        'filter': hydrophore_filter,
        'total': filtered_qs.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "warehouse/repair_list.html",contex)

def field_stock(request):
    queryset = Hydrophore.objects.filter(location="4").order_by("serial_number")
    
    hydrophore_filter = HydrophoreFilter(request.GET, queryset=queryset)
    filtered_qs = hydrophore_filter.qs
    
    page_obj = paginate_items(request, filtered_qs)
    if request.method == "POST":
        form = HydrophoreForm(request.POST)
        if form.is_valid():
            try:
                item = form.save(commit=False)
                item.location = "4"
                item.save()
                messages.success(
                    request,
                    f'*{item}* Hidrofor kaydı başarılı bir şekilde oluşturuldu.'
                )
                return redirect('field_stock')
            except IntegrityError:
                messages.warning(
                    request,
                    'Bu seri numarası daha önce kullanılmış.'
                )
        else:
            messages.warning(
                request,
                f"Formda hatalar var. Lütfen kontrol edin: {form.errors.as_ul()}"
            )
    else:
        form = HydrophoreForm()
    
    contex = {
        'form' : form,
        'filter': hydrophore_filter,
        'total': filtered_qs.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "warehouse/field_stock.html",contex)

def electrical_stock(request):
    queryset = Hydrophore.objects.filter(location="3").order_by("serial_number")
    
    hydrophore_filter = HydrophoreFilter(request.GET, queryset=queryset)
    filtered_qs = hydrophore_filter.qs
    
    page_obj = paginate_items(request, filtered_qs)

    contex = {
        'filter': hydrophore_filter,
        'total': filtered_qs.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "warehouse/electrical_stock.html",contex)

def new_stock(request):
    queryset = Hydrophore.objects.filter(location="6").order_by("serial_number")
    
    hydrophore_filter = HydrophoreFilter(request.GET, queryset=queryset)
    filtered_qs = hydrophore_filter.qs
    
    page_obj = paginate_items(request, filtered_qs)

    if request.method == "POST":
        form = HydrophoreForm(request.POST)
        if form.is_valid():
            try:
                item = form.save(commit=False)
                item.location = "6"
                item.save()
                messages.success(
                    request,
                    f'*{item}* Hidrofor kaydı başarılı bir şekilde oluşturuldu.'
                )
                return redirect('workshop_stock')
            except IntegrityError:
                messages.warning(
                    request,
                    'Bu seri numarası daha önce kullanılmış.'
                )
        else:
            messages.warning(
                request,
                f"Formda hatalar var. Lütfen kontrol edin: {form.errors.as_ul()}"
            )
    else:
        form = HydrophoreForm()
    
    contex = {
        'form' : form,
        'filter': hydrophore_filter,
        'total': filtered_qs.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "warehouse/new_stock.html",contex)

def scrap_stock(request):
    queryset = Hydrophore.objects.filter(location="7").order_by("serial_number")
    
    hydrophore_filter = HydrophoreFilter(request.GET, queryset=queryset)
    filtered_qs = hydrophore_filter.qs
    
    page_obj = paginate_items(request, filtered_qs)

    if request.method == "POST":
        form = HydrophoreForm(request.POST)
        if form.is_valid():
            try:
                item = form.save(commit=False)
                item.location = "7"
                item.save()
                messages.success(
                    request,
                    f'*{item}* Hidrofor kaydı başarılı bir şekilde oluşturuldu.'
                )
                return redirect('workshop_stock')
            except IntegrityError:
                messages.warning(
                    request,
                    'Bu seri numarası daha önce kullanılmış.'
                )
        else:
            messages.warning(
                request,
                f"Formda hatalar var. Lütfen kontrol edin: {form.errors.as_ul()}"
            )
    else:
        form = HydrophoreForm()
    
    contex = {
        'form' : form,
        'filter': hydrophore_filter,
        'total': filtered_qs.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "warehouse/scrap_stock.html",contex)
