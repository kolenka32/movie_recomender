import re
from django.db.models import Q
from django.contrib.postgres.search import TrigramSimilarity
from movies.models import Movie


def smart_search(query):
    query = query.lower().strip()
    year_match = re.search(r"(19|20)\d{2}", query)
    year = int(year_match.group()) if year_match else None

    if year:
        query = query.replace(str(year), "").strip()

    qs = Movie.objects.annotate(similarity=TrigramSimilarity("title", query))
    qs = qs.filter(Q(similarity__gt=0.2) | Q(title__icontains=query))

    if year:
        qs = qs.filter(release_date__year=year)

    qs = qs.order_by("-similarity", "-popularity")[:20]

    return qs