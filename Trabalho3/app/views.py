"""
Definition of views.
"""
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
import pywikibot
import re
from app.functions import functions

f = functions()

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)  
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def queries(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/queries.html',
        {
            'title':'Queries',
            'message':'Implementar as queries',
        }
    )

def inferencies(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/inferencies.html',
        {
            'title':'inferencies',
            'message':'Implementar as inferencias',
        }
    )

def operations(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/operations.html',
        {
            'title':'operations',
            'message':'adicionar, remover e listar',
        }
    )

def information(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)

    clubes = {'Estoril':'G.D. Estoril Praia','Setubal':'Vitória F.C.','Porto':'FC Porto','Guimaraes':'Vitória S.C.','Pacos Ferreira':'F.C. Paços de Ferreira','Sp Lisbon':'Sporting Clube de Portugal','Belenenses':'C.F. Os Belenenses','Boavista':'Boavista F.C.','Moreirense':'Moreirense F.C.','Academica':'Associação Académica de Coimbra – O.A.F.','Gil Vicente':'Gil Vicente F.C.','Benfica':'S.L. Benfica','Nacional':'C.D. Nacional','Penafiel':'F.C. Penafiel','Rio Ave':'Rio Ave F.C.','Sp Braga':'S.C. Braga','Arouca':'F.C. Arouca','Maritimo':'C.S. Marítimo'}

    if 'convert' in request.POST :
        TeamSelected = request.POST['chooseTeam']
        DictTeam = clubes[TeamSelected]

        #Regex para as linguagens
        en = re.compile("en") #Verificar se tem em ingles
        pt = re.compile("pt") #Verificar se tem em portugues
        es = re.compile("es") #Verificar se tem em espanhol
        #Regex para as propriedades
        P571 = re.compile("P571") #Data de criação do clube
        P115 = re.compile("P115") #Nome do estadio
        P159 = re.compile("P159") #De onde o clube é
        P856 = re.compile("P856") #Founding Date

        site = pywikibot.Site("en", "wikipedia")
        page = pywikibot.Page(site, DictTeam) #<--- Para inserir o nome do país
        item = pywikibot.ItemPage.fromPage(page)

        item_dict = item.get()
        checklang = str(item_dict["aliases"])
        #caso que em "aliases" nao tenha a lingua inglesa ou portuguesa (assim escolhese a espanhola)
        if en.search(checklang):
            Aliases = str(item_dict["aliases"]["en"])
        elif pt.search(checklang):
            Aliases = str(item_dict["aliases"]["pt"])
        elif es.search(checklang):
            Aliases = str(item_dict["aliases"]["es"])

        Labels = str(item_dict["labels"]["en"])
        Description = str(item_dict["descriptions"]["en"])

        clm_dict = item_dict["claims"]
        checkClaim= str(clm_dict)

        if P571.search(checkClaim):
            #Data de criação do clube
            clm_foundingYear = clm_dict["P571"]

            for clm in clm_foundingYear:
                clm_trgt = clm.getTarget()
                ola = clm_trgt
                aux3 = str(ola).split(",")
                data = aux3[4].replace('\n','').replace('{', '').replace('}', '').replace(' ', '')
                getData = data.split(":")
                finalDate = str(getData[1]).replace('"','').replace("+0000000","").replace("T00","")
                dateTreat = finalDate.split("-")
                if dateTreat[1]=='00':
                    year = dateTreat[0]
                else:
                    year = finalDate
        else:
            year = "The date was not found"

        if P115.search(checkClaim):
            #Nome do estadio
            clm_list = clm_dict["P115"]

            for clm in clm_list:
                clm_trgt = clm.getTarget()
                stadium = f.search(str(clm_trgt))
        else:
            stadium = "The stadium data was not found"

        if P159.search(checkClaim):
            #de onde o clube é
            clm_hq = clm_dict["P159"]

            for clm in clm_hq:
                clm_trgt = clm.getTarget()
                headquarters = f.search(str(clm_trgt))
        else:
            headquarters = "Headquarter was not found"

        if P856.search(checkClaim):
            #website
            clm_website = clm_dict["P856"]

            for clm in clm_website:
                clm_trgt = clm.getTarget()
                WebSite = str(clm_trgt)
        else:
            WebSite = "Website was not found"
        return render(
        request,
        'app/information.html',
        {
            'title':'information',
            'Aliases':Aliases,
            'Labels':Labels,
            'Description':Description,
            'year':year,
            'stadium':stadium,
            'headquarters':headquarters,
            'WebSite':WebSite,
        }
    )
    return render(
        request,
        'app/information.html',
        {
            'title':'information',
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
