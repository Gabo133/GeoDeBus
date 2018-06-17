from django.db.models import Q

def paginationDataTableBus(POST, Modelo):
    if POST['search[value]'] == '':
        query = Modelo.objects.all()[int(POST['start']):int(
            POST['start']) + int(POST['length'])]
        json = {"recordsTotal": Modelo.objects.all().count(),
                "recordsFiltered": Modelo.objects.all().count()}
    else:
        query = Modelo.objects.filter(Q(empresa__icontains=POST['search[value]']) | Q(patente__icontains=POST['search[value]']) | Q(modelo__icontains=POST['search[value]']) | Q(color__icontains=POST['search[value]']))
        json = {"recordsTotal": query.count(),
                "recordsFiltered": query.count()}
    return query, json
