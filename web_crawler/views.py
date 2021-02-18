from django.shortcuts import render
from .forms import SearchForm
from bs4 import BeautifulSoup
import requests


def search(request):

    results = []

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            search_query = form.cleaned_data['search']
            url = 'https://www.ask.com/web?q='+search_query
            response = requests.get(url)
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')

            page = soup.find_all('div', {'class': 'PartialSearchResults-item'})

            for section in page:
                heading = section.find(class_='PartialSearchResults-item-title').text
                link = section.find('a').get('href')
                description = section.find(class_='PartialSearchResults-item-abstract').text

                results.append((heading, link, description))

                # print(heading)
                # print(link)
                # print(description)




    else:
        form = SearchForm()

    context = {
        'form': form,
        'results': results
    }

    return render(request, 'search.html', context)
