from google import google
num_page = 3
search_results = google.search("This is my query", num_page)
for result in search_results:
    print(result.description)