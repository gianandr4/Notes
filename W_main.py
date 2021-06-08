import requests

link = 'https://serpapi.com/search?api_key=265f1667504b7b1f73e5427d779a86fc7cdb2aa955d692b603db27107ef761cb&author_id=DTKGcjkAAAAJ&engine=google_scholar_author'

link = 'https://scholar.google.com/citations?user=0jkdZSsAAAAJ&hl=en'
x=requests.get(link)

print(x.text)


