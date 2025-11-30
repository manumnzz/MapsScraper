from django.shortcuts import render
from .forms import SearchForm
from .models import Business
from serpapi import GoogleSearch
import csv
from django.http import HttpResponse

API_KEY = "d825e407114772feb451fa684813d1cc068d67cf738ee4492ba1c4510ba29567"

def buscar_negocios(request):
    resultados = []

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            consulta = form.cleaned_data["consulta"]
            ciudad = form.cleaned_data["ciudad"]

            # SerpAPI
            params = {
                "engine": "google_maps",
                "q": f"{consulta} {ciudad}",
                "type": "search",
                "hl": "es",
                "api_key": API_KEY,
            }

            search = GoogleSearch(params)
            data = search.get_dict()
            negocios = data.get("local_results", [])

            for n in negocios:
                if not n.get("website"):
                    negocio = Business.objects.create(
                        nombre=n.get("title"),
                        direccion=n.get("address"),
                        telefono=n.get("phone"),
                        rating=n.get("rating"),
                        categoria=n.get("type"),
                        ciudad=ciudad,
                        web=None
                    )
                    resultados.append(negocio)

            return render(request, "scraper/resultados.html", {
                "resultados": resultados,
                "consulta": consulta,
                "ciudad": ciudad,
            })

    else:
        form = SearchForm()

    return render(request, "scraper/buscar.html", {
        "form": form
    })

def exportar_csv(request):
    # Filtrar solo los negocios sin web
    negocios = Business.objects.filter(web__isnull=True)

    # Crear respuesta tipo archivo CSV
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="negocios_sin_web.csv"'

    writer = csv.writer(response)

    # Cabeceras del CSV
    writer.writerow(["Nombre", "Dirección", "Teléfono", "Rating", "Categoría", "Ciudad", "Fecha scraping"])

    # Filas
    for n in negocios:
        writer.writerow([
            n.nombre,
            n.direccion,
            n.telefono,
            n.rating,
            n.categoria,
            n.ciudad,
            n.fecha_scraping.strftime("%Y-%m-%d %H:%M")
        ])

    return response
