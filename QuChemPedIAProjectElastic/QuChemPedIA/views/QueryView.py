from django.shortcuts import render
from QuChemPedIA.forms.QueryForm import QueryForm
from QuChemPedIA.models.QueryModel import Query
from datetime import datetime
from QuChemPedIA.search import *
from django.http.response import HttpResponseRedirect
from django.urls import reverse


def query(request):
    form = QueryForm(request.POST or None)
    results = []
    date_dep = datetime.now()
    try:
        # switch on what we are looking for
        if 'CID' in request.POST.get('typeQuery'):
            results =list(Query.objects.filter(cid__contains=int(request.POST.get('search'))))

        if 'IUPAC' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(iupac=request.POST.get('search')).order_by('id_log')[:5])

        if 'InChi' in request.POST.get('typeQuery'):
            # here we looking for inchi wich contain a part of what we looking for
            # results = list(Query.objects.filter(inchi=request.POST.get('search')).order_by('id_log')[:25])
            results = search_inchi(inchi_value=request.POST.get('search'))

        if 'Formula' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(formula=request.POST.get('search')))

        if 'SMILES' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(smiles=request.POST.get('search')))

        if 'id_log' in request.POST.get('typeQuery'):
            url = reverse('details', kwargs={'id': request.POST.get('search'), })
            return HttpResponseRedirect(url)

        if 'homo_alpha_energy' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(homo_alpha_energy=request.POST.get('search')))

        if 'homo_beta_energy' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(homo_beta_energy=request.POST.get('search')))

        if 'lumo_alpha_energy' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(lumo_alpha_energy=request.POST.get('search')))

        if 'lumo_beta_energy' in request.POST.get('typeQuery'):
            results = list(Query.objects.filter(lumo_beta_energy=request.POST.get('search')))

    except Exception as error:
        print("error :")
        print(error)
    date_fin = datetime.now()
    temp = date_fin-date_dep
    # if we have only one result we display the details of the molecule
    if results is None:
        results = []
    if len(results) == 1:
        url = reverse('details', kwargs={'id': results[0].id_log})
        return HttpResponseRedirect(url)
    return render(request, 'QuChemPedIA/query.html', locals())