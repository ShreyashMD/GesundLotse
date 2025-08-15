# src/ncbi.py
import os
import requests

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def fetch_ncbi_info(query: str) -> str:
    """
    Return a short PubMed hit for the given query.
    Uses E-utilities (ESearch + ESummary). If nothing found, returns "".
    If NCBI_API_KEY is set, it will be used to increase rate limits.
    """
    api_key = os.getenv("NCBI_API_KEY", "")
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": 1}
    if api_key:
        params["api_key"] = api_key

    try:
        search_resp = requests.get(f"{BASE_URL}esearch.fcgi", params=params, timeout=10)
        search_resp.raise_for_status()
        ids = search_resp.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return ""

        summary_params = {"db": "pubmed", "id": ids[0], "retmode": "json"}
        if api_key:
            summary_params["api_key"] = api_key

        summary_resp = requests.get(f"{BASE_URL}esummary.fcgi", params=summary_params, timeout=10)
        summary_resp.raise_for_status()

        result = summary_resp.json().get("result", {})
        info = result.get(ids[0], {})
        title = info.get("title") or ""
        source = info.get("fulljournalname") or info.get("source") or ""
        year = (info.get("pubdate") or "").split(" ")[0]

        pieces = [p for p in [title, f"({source}, {year})" if source or year else ""] if p]
        return " — ".join(pieces)
    except Exception:
        return ""
