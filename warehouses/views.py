from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import ProtectedError,Q,Sum,Count
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from .models import Power, Mark, Engine
from .filters import InventoryFilter,NewPumpFilter,EngineFilter,GeneralEngineFilter,PumpFilter,OrderFilter,SeconhandFilter,WorkshopExitSlipFilter
from .forms import *
from hydrophore.models import OutboundWorkOrder,WorkshopExit,RepairReturn
from django.http import JsonResponse
from django.template.loader import render_to_string

def handle_deletion(request, model, object_id, redirect_url, success_message, error_message, protected_error_message):
    try:
        obj = model.objects.get(id=object_id)
        obj.delete() 
        messages.success(request, success_message.format(obj))
    except model.DoesNotExist:
        messages.warning(request, error_message)
    except ProtectedError as e:
        model_name = e.args[0].split(' ')[-1] 
        messages.warning(request, protected_error_message.format(obj, model_name))
    return redirect(redirect_url)

def paginate_items(request, items, per_page=10):
    paginator = Paginator(items, per_page)  
    page_number = request.GET.get('page') 
    page_obj = paginator.get_page(page_number)  

    return page_obj

def engine_locations_update(id,location):
    item =Engine.objects.get(id=id)
    item.location = location
    item.save()

def newMark(request):
    if request.method == "POST":
        form = MarkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"*{form.data['engine_mark']}* Kayıt başarılı.")
            return redirect('add_mark')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = MarkForm()
    context = {
        'items': Mark.objects.all().order_by("-id"),
        'form': form
    }
    return render(request, "new_mark.html", context)

def markDelete(request, myid):
    return handle_deletion(
        request,
        Mark,
        myid,
        'add_mark',
        "*{0}* Markası başarıyla silindi.",
        "Marka bulunamadı.",
        "*{0}* Marka kaydı {1} tabloda kullanılıyor, silinemez."
    )

def newPower(request):
    if request.method == "POST":
        form = PowerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"*{form.data['engine_power']}* Kayıt başarılı.")
            return redirect('add_power')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = PowerForm()

    context = {
        'items': Power.objects.all().order_by("-id"),
        'form': form
    }
    return render(request, "new_power.html", context)

def powerDelete(request, myid):
    return handle_deletion(
        request,
        Power,
        myid,
        'add_power',
        "*{0}* Güç değeri başarıyla silindi.",
        "Güç değeri bulunamadı.",
        "*{0}* Güç kaydı {1} tabloda kullanılıyor, silinemez."
    )

def engineDelete(request, myid):
    redirect_url = request.GET.get('next', 'engine_homepage')
    return handle_deletion(
        request,
        Engine,
        myid,
        redirect_url,
        "*{0}* Motor kaydı başarıyla silindi.",
        "Motor kaydı bulunamadı.",
        "*{0}* Motor kaydı {1} tabloda kullanılıyor, silinemez."
    )
    
def engine_homepage(request):
    # Tüm motorlar
    engine_list = Engine.objects.all().order_by("-id")
    
    # Filtreleme (opsiyonel)
    engine_filter = EngineFilter(request.GET, queryset=engine_list)
    filtered_qs = engine_filter.qs

    # Pagination
    page_obj = paginate_items(request, filtered_qs)

    # Lokasyon bazlı sayılar
    location_counts = (
        Engine.objects.values('location')
        .annotate(count=Count('id'))
        .order_by('location')
    )
    # Lokasyonları sözlük haline getirme
    location_dict = {str(item['location']): item['count'] for item in location_counts}

    context = {
        'well': location_dict.get("1", 0),
        'repair': location_dict.get("2", 0),
        'secondhand': location_dict.get("3", 0),
        'unusable': location_dict.get("4", 0),
        'new': location_dict.get("5", 0),
        'contractor' : location_dict.get("6", 0),
        'total': filtered_qs.count(),
        'items': page_obj,
        'query_string': request.GET.urlencode(),
        'filter': engine_filter,  # template’de filtre formunu göstermek için
    }

    return render(request, "engine_homepage.html", context)

def engine_edit(request, pk):
    engine = get_object_or_404(Engine, pk=pk)

    # next'i al
    next_url = request.GET.get('next')

    if request.method == 'POST':
        form = EngineForm(request.POST, instance=engine)

        # POST'tan tekrar al
        next_url = request.POST.get('next')

        if form.is_valid():
            form.save()
            messages.success(request, "Motor bilgileri güncellendi.")
            return redirect(next_url or 'engine_homepage')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = EngineForm(instance=engine)

    return render(request, 'new_engine.html', {
        'form': form,
        'next': next_url
    })

def newPump(request):
    if request.method == "POST":
        form = PumpForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(
                request,
                f'*{ item }* Pompa kaydı başarılı bir şekilde oluşturuldu.'
            )
            return redirect('add_pump')  
            
        else:
            messages.warning(
                request,
                f"Formda hatalar var. Lütfen kontrol edin: {form.errors.as_ul()}"
            )
    else:
        form = PumpForm()  
    context = {
        'form': form
    }
    return render(request, "new_pump.html", context)

def pumpDelete(request, myid):
    return handle_deletion(
        request,
        Pump,
        myid,
        'pump_homepage',
        "*{0}* Pompa kaydı başarıyla silindi.",
        "Pompa kaydı bulunamadı.",
        "*{0}* Pompa kaydı {1} tabloda kullanılıyor, silinemez."
    )
    
def pump_edit(request, pk):
    pump = get_object_or_404(Pump, pk=pk)
    if request.method == 'POST':
        form = PumpEditForm(request.POST, instance=pump)
        if form.is_valid():
            form.save()
            messages.success(request, f"Pompa bilgileri güncellendi.")
            return redirect('pump_homepage')
    else:
        form = PumpEditForm(instance=pump)
    return render(request, 'new_pump.html', {'form': form})

def pump_homepage(request):
    pump_list = Pump.objects.all().order_by("-id")

    # 🔍 Filtreleme
    pump_filter = PumpFilter(request.GET, queryset=pump_list)
    filtered_qs = pump_filter.qs

    # Pagination
    page_obj = paginate_items(request, filtered_qs)

    context = {
        'well': Inventory.objects.filter(pump__isnull=False).count(),
        'repair': Repair.objects.filter(pump__isnull=False).count(),
        'secondhand': Seconhand.objects.filter(pump__isnull=False).count(),
        'unusable': Unusable.objects.filter(pump__isnull=False).count(),
        'new': NewWarehousePump.objects.aggregate(total=Sum('quantity'))['total'] or 0,
        'total': filtered_qs.count(),
        'items': page_obj,
        'query_string': request.GET.urlencode(),
        'filter': pump_filter,
    }
    return render(request, "pump_homepage.html", context)

def inventory_homepage(request):
    queryset = Inventory.objects.all().order_by("id")

    inventory_filter = InventoryFilter(request.GET, queryset=queryset)
    
    filtered_qs = inventory_filter.qs

    page_obj = paginate_items(request, filtered_qs)

    context = {
        'filter': inventory_filter,
        'items': page_obj,
        'total': filtered_qs.count(),
        'query_string': request.GET.urlencode(),
    }
    return render(request, "inventory_homepage.html", context)

def inventory_edit(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    # next'i al
    next_url = request.GET.get('next')
    
    if request.method == 'POST':
        # POST'tan tekrar al
        next_url = request.POST.get('next')
        form = InventoryEditForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            messages.success(request, "Kuyu bilgileri güncellendi.")
            return redirect(next_url or 'inventory')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = InventoryEditForm(instance=inventory)
    return render(request, 'new_inventory.html', {
        'form': form,
        'pump_list': Pump.objects.all(),
        'selected_pump': inventory.pump,
        'next': next_url
    })

def seconhand_row_edit(request,model,data):
    if model == "engine":
        datas = data.split("-")
        row = Seconhand.objects.get(row_identifier=datas[0].strip())
        row.engine = None
        row.save()
    elif model == "pump":
        datas = data.split("-")
        row = Seconhand.objects.get(row_identifier=datas[0].strip())
        row.pump = None
        row.save()
    else:
        messages.warning(request, "Formda hatalar var tekrar giriniz.")
        return redirect("add_inventory")

def add_inventory(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        next_url = request.GET.get('next')
        form = InventoryForm(request.POST)
        if form.is_valid(): 
            obj = form.save()
            seconhand_row_edit(request,"engine",form.data["engine_row_identifier"])
            seconhand_row_edit(request,"pump",form.data["pump_row_identifier"])
            messages.success(request, f"*{obj.well_number}* Kuyu kaydı başarıyla eklendi ve ilgili alanlar güncellendi.")
            return redirect('inventory')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = InventoryForm()

    context = {'form': form ,'next': next_url}
    return render(request, 'new_inventory.html', context)

def delete_inventory(request, id):
    return handle_deletion(
        request,
        Inventory,
        id,
        'inventory',
        "*{0}* Nolu kuyu kaydı başarıyla silindi.",
        "Kuyu kaydı bulunamadı.",
        "*{0}* Kuyu kaydı {1} tabloda kullanılıyor, silinemez."
    )

def seconhand(request):
    queryset = Seconhand.objects.filter(
        Q(engine__isnull=False) | Q(pump__isnull=False)
    ).select_related('engine','pump').order_by('row_identifier')

    # 🔍 FILTER
    seconhand_filter = SeconhandFilter(request.GET, queryset=queryset)

    # 📄 PAGINATION
    page_obj = paginate_items(request, seconhand_filter.qs)

    engine_form = EngineForm(request.POST or None)
    pump_form = PumpForm(request.POST or None)

    if request.method == 'POST':
        secondhand_id = request.POST.get("secondhand_row")

        if secondhand_id:
            item = Seconhand.objects.get(id=secondhand_id)
            engine_valid = False
            if engine_form.is_valid():
                engine = engine_form.save(commit=False)
                engine.location = "3"
                engine.save()
                item.engine = engine
                engine_valid = True
            try:
                pump_valid = False
                existing_pump = Pump.objects.filter(
                    pump_type=pump_form.data["pump_type"],
                    pump_breed=pump_form.data["pump_breed"],
                    pump_mark=pump_form.data["pump_mark"]
                ).first()

                if existing_pump:
                    item.pump = existing_pump
                else:
                    item.pump = pump_form.save()
                pump_valid = True
            except MultiValueDictKeyError:
                pass
            
            if engine_valid or pump_valid:
                item.save()
                messages.success(request,f"{item.row_identifier} Sırası güncellendi.")
                return redirect('seconhand')
            
        messages.warning(
            request,
            engine_form.errors.as_ul() or pump_form.errors.as_ul()
        )

    context = {
        'engine_form': engine_form,
        'pump_form': pump_form,

        'items': page_obj,
        'filter': seconhand_filter,

        'null_list': Seconhand.objects.filter(
            Q(engine__isnull=True) | Q(pump__isnull=True)
        ).select_related('engine','pump'),
        'total': seconhand_filter.qs.count(),
        'query_string': request.GET.urlencode(),
    }

    return render(request, "secondhand_page.html", context)

def warehouses_repair(request):
    repair_list = Repair.objects.filter(status="active")
    page_obj = paginate_items(request, repair_list)

    contex = {
        'total': repair_list.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "repair_page.html",contex)

def repair(request):
    repair_list = Repair.objects.filter(status="active")
    page_obj = paginate_items(request, repair_list)

    contex = {
        'total': repair_list.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "repair_page.html",contex)

def all_repair(request):
    repair_list = Repair.objects.filter(status="passive")
    page_obj = paginate_items(request, repair_list)

    contex = {
        'total': repair_list.count(),  
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
    }
    return render(request, "repair_page.html",contex)

def repair_edit(request, id):
    repair = get_object_or_404(Repair, order__pk=id)
    if repair.engine:
        engine = Engine.objects.filter(location="6",engine_type=repair.engine.engine_type,engine_power=repair.engine.engine_power)
    else:
        engine =None
    row_identifier = Seconhand.objects.filter(engine__isnull=True,pump__isnull=True)
    next_url = request.GET.get('next')
    if request.method == "POST":
        next_url = request.POST.get('next')
        engine_choice = request.POST.get("engine")
        pump_choice = request.POST.get("pump")

        engine_row_id = request.POST.get("engine_secondhand_row")
        pump_row_id = request.POST.get("pump_secondhand_row")
        engine_contractor_row_id = request.POST.get("engine_contractor")

        # -------- PERT --------
        if engine_choice == "unusable" or pump_choice == "unusable":
            Unusable.objects.create(
                well_number=repair.order.inventory,
                engine=repair.engine if engine_choice == "unusable" else None,
                pump=repair.pump if pump_choice == "unusable" else None
            )
            repair.engine_info = 'Pert Depo' if engine_choice == "unusable" else None
            repair.pump_info = 'Pert Depo' if pump_choice == "unusable" else None
            
            if engine_choice == "unusable" and repair.engine:
                engine_locations_update(repair.engine.id, "4")

        # -------- 2.EL --------
        if engine_choice == "secondhand" and engine_row_id:
            row = Seconhand.objects.get(id=engine_row_id)
            row.engine = repair.engine
            row.save()
            repair.engine_info = f"2.El Depo | {row.row_identifier}"
            if repair.engine:
                engine_locations_update(repair.engine.id, "3")

        if pump_choice == "secondhand" and pump_row_id:
            row = Seconhand.objects.get(id=pump_row_id)
            row.pump = repair.pump
            row.save()
            repair.pump_info = f"2.El Depo | {row.row_identifier}"

        #---------- Mütahit ------
        if engine_choice == "contractor" and engine_contractor_row_id and engine_row_id:
            row = Seconhand.objects.get(id=engine_row_id)
            row.engine = Engine.objects.get(id=engine_contractor_row_id)
            row.save()
            engine_locations_update(row.engine.id, "3")
            repair.engine_info = f"Mütahit Depo | {row.engine.serialnumber} | {row.row_identifier}"
            if repair.engine:
                engine_locations_update(repair.engine.id, "6")
        
        repair.status = 'passive'
        repair.save()
        order = repair.order
        if order.situation == "dismantling":
            order.operation_type = "5"
            messages.success(request, "Tamir bilgileri eklendi.\n Malzemler İlgili depoya aktarıldı.\n Montaj emri oluşturuldu.")
        else:
            order.operation_type = "10"
            order.status ="passive"
            messages.success(request, "Tamir bilgileri eklendi.\n Malzemler İlgili depoya aktarıldı.\n İş emri kapandı.")
        order.save()
        return redirect(next_url or "engine_repair")

    return render(request, "repair_edit.html", {
        "repair": repair,"engine":engine ,
        "row_identifier": row_identifier,
        'next': next_url
    })

def repair_delete(request, id):
    return handle_deletion(
        request,
        Repair,
        id,
        'order_page',
        "*{0}* Tamir İş Emri kaydı başarıyla silindi.",
        "Tamir İş Emri kaydı bulunamadı.",
        "*{0}* Tamir İş Emri kaydı {1} tabloda kullanılıyor, silinemez."
    )
    
def contractor_warehouse(request):
    if request.method == "POST":
        form = EngineForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.location= "6" #Mütahit depo
            item.save()
            messages.success(request, f"Motor kaydı başarılı.")
            return redirect('contractor_warehouse')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = EngineForm()
    
    queryset = Engine.objects.filter(location="6")
    engine_filter = GeneralEngineFilter(request.GET, queryset=queryset)
    filtered_qs = engine_filter.qs
    page_obj = paginate_items(request, filtered_qs)
    
    contex = {
        'filter': engine_filter,
        'total': filtered_qs.count(),
        'items': page_obj, 
        'query_string': request.GET.urlencode(),
        'form' : form
    }
    return render(request, "contractor_warehouse.html",contex)

def unusable(request):
    
    context = {
        'items' : Unusable.objects.all()
    }
    return render(request, "unusable_page.html",context)

def new_warehouse_engine(request):
    if request.method == "POST":
        form = EngineForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Kayıt başarılı.")
            return redirect('new_warehouse_engine')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = EngineForm()
        
    queryset = Engine.objects.filter(location="5").order_by("-id")
    engine_filter = GeneralEngineFilter(request.GET, queryset=queryset)
    filtered_qs = engine_filter.qs
    page_obj = paginate_items(request, filtered_qs)
    
    context = {
        'filter': engine_filter,
        'total': filtered_qs.count(),
        'items': page_obj,  
        'query_string': request.GET.urlencode(),
        'form' : form,
        'null_list': Seconhand.objects.filter(engine__isnull=True,pump__isnull=True)

    }
    return render(request, "new_warehouse_engine.html",context)

def new_warehouse_pump(request):
    if request.method == "POST":
        form = WarehousePumpForm(request.POST)
        if form.is_valid():
            item = form.save(False)
            if form.data["quantity_value"]:
                item.quantity = form.data["quantity"]
            item.save()
            messages.success(request, f"Kayıt başarılı.")
            return redirect('new_warehouse_pump')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = WarehousePumpForm()
    
    queryset = NewWarehousePump.objects.all()

    inventory_filter = NewPumpFilter(request.GET, queryset=queryset)
    
    filtered_qs = inventory_filter.qs

    page_obj = paginate_items(request, filtered_qs)

    context = {
        'filter': inventory_filter,
        'items': page_obj,
        'total': filtered_qs.count(),
        'query_string': request.GET.urlencode(),
        'form' : form,
        'null_list': Seconhand.objects.filter(engine__isnull=True,pump__isnull=True)
    }
    
    return render(request, "new_warehouse_pump.html",context)

def transfer_warehouse(request):
    if request.method == "POST":
        item = get_object_or_404(Seconhand,row_identifier=request.POST.get("row_identifier"))
        if request.POST.get("modal_value") == "pump":
            pump = get_object_or_404(NewWarehousePump,pump=request.POST.get("pump_value"))
            item.pump = pump.pump
            pump.quantity -=1
            pump.save()
            messages.success(request, f"*{request.POST.get('row_identifier')}* Sırasına {item.pump} Pompa Eklendi.")
            item.save()
            return redirect('new_warehouse_pump')
        elif request.POST.get("modal_value") == "engine":
            engine = get_object_or_404(Engine,pk=request.POST.get("engine_value"))
            item.engine = engine
            engine.location = "3"
            engine.save()
            messages.success(request, f"*{request.POST.get('row_identifier')}* Sırasına {item.engine} Motor Eklendi.")
            item.save()
        else:
            messages.warning(request, f"Değer Girilmedi..")
    return redirect('new_warehouse_engine')

def new_warehouse_pump_delete(request, id):
    return handle_deletion(
        request,
        NewWarehousePump,
        id,
        'new_warehouse_pump',
        "*{0}* Pompa kaydı başarıyla silindi.",
        "Pompa kaydı bulunamadı.",
        "*{0}* Pompa kaydı {1} tabloda kullanılıyor, silinemez."
    )

#------------İş Emirleri----------
def delete_order(request, id):
    return handle_deletion(
        request,
        Order,
        id,
        'order_page',
        "*E{0}* Nolu İş Emri kaydı başarıyla silindi.",
        "İş Emri kaydı bulunamadı.",
        "*{0}* İş Emri kaydı {1} tabloda kullanılıyor, silinemez."
    )

def form_control(request):#*
    if request.method != "POST":
        messages.warning(request, "Hatalı seçim yapıldı.")
        return redirect("order_page")

    order = get_object_or_404(Order, pk=request.POST["id"])

    if order.operation_type == "1": #Demontaj
        """1 -> 2"""
        form = DisassemblyForm(request.POST, instance=order)
        if form.is_valid():
            item = form.save()
            order.complete_disassembly(item.disassembly_plug)
            messages.success(request, "Demontaj bilgileri eklendi.\n Malzemler kurtarıcı depoya aktarıldı.")
        else:
            messages.warning(request, form.errors.as_ul())
            return redirect("order_page")

    elif order.operation_type == "2":
        """2 -> 3"""
        order.arrive_workshop()
        messages.success(request, "Kurtarıcı bilgileri eklendi.\n Malzemler Atölye depoya aktarıldı.")
    
    elif order.operation_type == "3":
        """3 -> 4"""
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            order.start_repair()
            messages.success(request, "Atölye bilgileri eklendi.\n Malzemler Tamir depoya aktarıldı.")
        else:
            messages.warning(request, form.errors.as_ul())
            return redirect("order_page")
        
    elif order.operation_type == "6": #Montaj
        """6 -> 10"""
        form = MountingForm(request.POST, instance=order)
        if form.is_valid():
            item = form.save()
            order.complete_assembly(item.assembly_plug)
            create_workshop_exit_slip("diver",order)
            messages.success(request, "Montaj bilgileri eklendi.\n İş Emri Kapatıldı.")
        else:
            messages.warning(request, form.errors.as_ul())
            return redirect("order_page")

    return redirect("order_page")

def order_page(request):
    if request.method == "POST":
        well_number = request.POST.get("well_number").strip().upper()
        if well_number:
            try:
                well = Inventory.objects.get(well_number=well_number)
                if well.status == "passive":
                    messages.info(request, "Bu kuyu numarası *PASİF* durumda iş emri oluşturamazsınız.")
                    return redirect("order_page")
                active_order = Order.objects.filter(inventory=well, status="active").exists()
                if active_order:
                    messages.info(request, "Bu kuyu numarasında aktif iş emri mevcut.")
                else:
                    return redirect("transactions", id=well.id)
            except Inventory.DoesNotExist:
                messages.warning(request, "Bu kuyu numarası bulunamadı.")
                return redirect("order_page")

    queryset = Order.objects.filter(status="active").select_related('inventory')
    order_filter = OrderFilter(request.GET, queryset=queryset)
    filtered_qs = order_filter.qs

    page_obj = paginate_items(request, filtered_qs)
    context = {
        'total': filtered_qs.count(),
        'items': page_obj,
        'query_string': request.GET.urlencode(),
        'filter': order_filter,
    }
    return render(request, "order_page.html", context)

def order_show(request, pk):
    order = get_object_or_404(Order, pk=pk)
    data = dict()
    repair = Repair.objects.filter(order=order).first()
    if request.POST:
        order.comment = request.POST.get('comment', None)
        order.save()
        messages.success(request,"İş emrine açıklama eklendi.")
        return redirect("order_page")
    context = {
        'order': order,
        'repair' : repair if repair else None,
        }
    data['html_form'] = render_to_string('modal/order_edit.html', context, request=request, )
    return JsonResponse(data)

def order_edit(request, pk):#*
    order = get_object_or_404(Order, pk=pk)
    data = {}
    context = {"order": order}

    if order.operation_type == "1":
        form = DisassemblyForm()
        context['form'] = form
        data['html_form'] = render_to_string('modal/disassembly.html', context, request=request)

    elif order.operation_type == "2":
        data['html_form'] = render_to_string('modal/workshop.html', context, request=request)

    elif order.operation_type == "3":
        form = OrderEditForm()
        context['form'] = form
        data['html_form'] = render_to_string('modal/disassembly.html', context, request=request)
    
    elif order.operation_type == "6":
        form = MountingForm()
        context['form'] = form
        data['html_form'] = render_to_string('modal/disassembly.html', context, request=request)


    return JsonResponse(data)

@transaction.atomic
def seconhand_order_go_back(request, id):
    order = get_object_or_404(Order, pk=id)

    if request.method == "POST":

        engine_row_id = request.POST.get("engine_secondhand_row")
        pump_row_id = request.POST.get("pump_secondhand_row")

        # ENGINE
        if engine_row_id and order.mounted_engine:
            try:
                item = Seconhand.objects.filter(id=engine_row_id).first()
                if item:
                    item.engine = order.mounted_engine
                    item.save()
                    engine_locations_update(item.engine.id, "3")
                else:
                    messages.warning(request, "Seçilen motor satırı bulunamadı.")
            except Exception as e:
                messages.error(request, f"Motor geri alınırken hata oluştu: {e}")

        # PUMP
        if pump_row_id and order.mounted_pump:
            try:
                item = Seconhand.objects.filter(id=pump_row_id).first()
                if item:
                    item.pump = order.mounted_pump
                    item.save()
                else:
                    messages.warning(request, "Seçilen pompa satırı bulunamadı.")
            except Exception as e:
                messages.error(request, f"Pompa geri alınırken hata oluştu: {e}")

        # Order temizleme
        order.mounted_engine = None
        order.mounted_pump = None
        order.outlet_plug = None
        order.operation_type = "5"
        order.save()
        messages.success(request,"İş emri geri alındı.")
        return redirect("order_page")

    return render(request, "seconhand_order_go_back.html", {
        "order": order,
        "row_identifier": Seconhand.objects.filter(
            engine__isnull=True,
            pump__isnull=True
        )
    })
    
def order_go_back(request, pk):#*
    order = get_object_or_404(Order, pk=pk)
    if order.operation_type == "1":
        return redirect("seconhand_order_go_back",id=order.id)
    elif order.operation_type == "6" and order.situation == "dismantling":
        return redirect("seconhand_order_go_back",id=order.id)
        
    success, message = order.go_back()
    if success:
        messages.success(request, message)
    else:
        messages.warning(request, message)
    return redirect("order_page")

def handle_engine(order):
    if not order.mounted_engine:
        raise ValueError("Motor seçilmedi.")
    engine = Engine.objects.get(id=order.mounted_engine.id)
    if str(engine.location) == "3": 
        item = Seconhand.objects.get(engine=engine)
        order.engine_info = item.row_identifier
        item.engine = None
        item.save()
    engine.location = "1" 
    engine.save()

def handle_pump(order, pump_display):
    if not order.mounted_pump or not pump_display:
        raise ValueError("Pompa seçilmedi.")

    row_identifier = pump_display.split("-")[0].strip()
    try:
        item = Seconhand.objects.get(
            pump_id=order.mounted_pump,
            row_identifier=row_identifier
        )
        order.pump_info = item.row_identifier
        item.pump=None
        item.save()

    except Seconhand.DoesNotExist:
        try:
            new_pump = NewWarehousePump.objects.get(pump=order.mounted_pump)
            if new_pump.quantity <= 0:
                raise ValueError("Seçilen pompa stoğu yok.")
            new_pump.quantity -= 1
            new_pump.save()
        except NewWarehousePump.DoesNotExist:
            raise ValueError("Seçilen pompa bulunamadı.")

def new_assembly_order(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == "POST":
        form = AssemblyForm(request.POST, instance=order)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    if order.operation_engine == "engine":
                        order.mounted_pump = None
                        handle_engine(order)
                        
                    elif order.operation_engine == "pump":
                        order.mounted_engine = None
                        handle_pump(order,request.POST.get("mounted_pump_display"))
                    else:
                        handle_engine(order)
                        handle_pump(order,request.POST.get("mounted_pump_display"))
                    
                    if order.situation == "dismantling":
                        order.operation_type = "6"
                        messages.success(request, " Çıkış Fişi bilgileri eklendi.\n Montaj bilgilerine aktarıldı.")
                    else:
                        order.operation_type = "1"
                        messages.success(request, "Malzemeler Kuyuya Gönderildi.")
                    order.save()
                    return redirect("order_page")

            except ValueError as ve:
                messages.error(request, f"Hata: {str(ve)}")
            except Exception as e:
                messages.error(request, f"İşlem sırasında beklenmedik hata oluştu: {str(e)}")
        else:
            messages.warning(request, form.errors.as_ul())
    else:
        form = AssemblyForm()

    return render(request, "new_order.html", {
        "order" :order,
        "form": form,
        "seconhand": Seconhand.objects.all(),
        "new_engine": Engine.objects.filter(location=5),
        "new_pump": NewWarehousePump.objects.filter(quantity__gt=0),
    })

def all_order_page(request):
    queryset = Order.objects.filter(status="passive").select_related('inventory').order_by("-id")

    order_filter = OrderFilter(request.GET, queryset=queryset)
    filtered_qs = order_filter.qs

    page_obj = paginate_items(request, filtered_qs)
    context = {
        'total': filtered_qs.count(),
        'items': page_obj,
        'query_string': request.GET.urlencode(),
        'filter': order_filter,
    }
    return render(request, "all_order_page.html", context)

def transactions(request,id):
    inventory = get_object_or_404(Inventory, id=id)
    form = OperationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            order = form.save(commit=False)
            order.inventory = inventory
            item = form.cleaned_data.get("situation")
        else:
            messages.warning(request, form.errors.as_ul())
            return redirect("order_page")
        
        if item == "installation":
            order.operation_type = "5"
        elif item == "dismantling":
            order.operation_type = "1"
        elif item == "length_extension":
            order.operation_type = "8"
        elif item == "well_cancellation":
            order.operation_type = "9"
        else:
            messages.warning(request, "Hatalı seçim yapıldı.")
            return redirect("order_page")
        
        order.save()
        messages.success(request, f"*{inventory.well_number}* Nolu kuyu için *E{order.work_order_plug}* iş emri oluşturuldu.")
        return redirect("order_page")

    return render(request, "transactions.html", {
        "form": form,
        "inventory": inventory,
        "end_order" : Order.objects.filter(inventory=inventory).order_by("id").first()
    })

def create_workshop_exit_slip(modalname, modal):
    if modalname == 'hydrophore':
        workshop_exit_slip = WorkshopExitSlip.objects.create(
            date=modal.dispatch_date,
            slip_no=modal.dispatch_slip_number,
            well_no="",
            district=modal.get_district_display(),
            address=modal.neighborhood,
            motor_type="HİDROFOR",
            hydrofor_no=modal.mounted_hydrophore.serial_number if modal.mounted_hydrophore else None,
            brand=modal.mounted_hydrophore.engine_brand if modal.mounted_hydrophore else None,
            power=modal.mounted_hydrophore.engine_power if modal.mounted_hydrophore else None,
            pump_type=modal.mounted_hydrophore.pump_type if modal.mounted_hydrophore else None,
            pump_brand="",
            submersible=None,
            motor=None,
            pump=None,
            hydrofor="1",
            overall_status="",
        )
    elif modalname == 'diver':
        workshop_exit_slip = WorkshopExitSlip.objects.create(
            date=modal.outlet_plug_date,
            slip_no=modal.outlet_plug,
            well_no=modal.inventory.well_number,
            district=modal.inventory.get_district_display(),
            address=modal.inventory.address,
            motor_type=modal.mounted_engine.get_engine_type_display() if modal.mounted_engine else None,
            hydrofor_no=modal.mounted_engine.serialnumber if modal.mounted_engine else None,
            brand=modal.mounted_engine.engine_mark if modal.mounted_engine else None,
            power=modal.mounted_engine.engine_power if modal.mounted_engine else None,
            pump_type=modal.mounted_pump.pump_type if modal.mounted_pump else None,
            pump_brand=modal.mounted_pump.pump_mark if modal.mounted_pump else None,
            submersible="1" if modal.mounted_engine and modal.mounted_pump else None,
            motor="2.EL-"+modal.engine_info if modal.engine_info else None,
            pump="2.EL-"+modal.pump_info if modal.pump_info else None,
            hydrofor=None,
            overall_status=modal.comment,
        )

    return

def workshop_exit_slip(request):
    order_list = WorkshopExitSlip.objects.all()
    
    order_filter = WorkshopExitSlipFilter(request.GET, queryset=order_list)
    filtered_order_list = order_filter.qs

    paginator = Paginator(filtered_order_list, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'total': filtered_order_list.count(),
        'items': page_obj,
        'query_string': request.GET.urlencode(),
        'filter': order_filter,
    }
    return render(request, "workshop_exit_slip.html", context)

def new_workshop_exit_slip(request):
    if request.method == 'POST':
        form = WorkshopExitSlipForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "İş Emri Eklendi.")
            return redirect('workshop_exit_slip')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
            form = WorkshopExitSlipForm()
    return render(request, 'new_workshop_exit_slip.html', {'form': form})

def workshop_exit_slip_edit(request,id):
    order = get_object_or_404(WorkshopExitSlip, pk=id)
    if request.method == 'POST':
        form = WorkshopExitSlipForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "İş Emri Güncellendi.")
            return redirect('workshop_exit_slip')
        else:
            messages.warning(request, form.errors.as_ul())
    else:
            form = WorkshopExitSlipForm(instance=order)
    return render(request, 'new_workshop_exit_slip.html', {'form': form})

def workshop_exit_slip_delete(request, id):
    return handle_deletion(
        request=request,
        model=WorkshopExitSlip,
        object_id=id,
        redirect_url="workshop_exit_slip",
        success_message="{} Kuyusu için iş emri başarıyla silindi.",
        error_message="İş emri bulunamadı.",
        protected_error_message="*{0}* İş Emri kaydı {1} tabloda kullanılıyor, silinemez."
    )

def work_order_reporting(request):
    order = None
    hydrophore = None
    repair = None
    workshop = None
    repair_return = None

    if request.method == 'POST':
        item = request.POST.get("number")

        order = Order.objects.filter(outlet_plug=item).first()
        hydrophore = OutboundWorkOrder.objects.filter(dispatch_slip_number=item).first()

        if order:
            repair = Repair.objects.filter(order=order).first()

        elif hydrophore:
            workshop = WorkshopExit.objects.filter(outbound_work_order=hydrophore).first()
            if workshop:
                repair_return = RepairReturn.objects.filter(workshop_exit=workshop).first()

        else:
            messages.warning(request, "Çıkış fiş numarası bulunamadı.")

    context = {
        'order': order,
        'hydrophore': hydrophore,
        'repair': repair,
        'workshop': workshop,
        'repair_return': repair_return,
    }

    return render(request, 'work_order_reporting.html', context)
