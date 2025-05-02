from urllib.parse import urlsplit, urlparse

urls = [
    "dashboard",
    "/dashboard",
    "dashboard/settings",
    "http://evil.com/phish",
    "https://yourdomain.com/dashboard",
    "//cdn.example.com/assets",
    "/login?next=/dashboard",
    "https://example.com:8000/path/to/page?user=isaac&next=/profile#bio"
]

for url in urls:
    print(f"\nTesting URL: {url}")
    split = urlsplit(url)
    print("SCHEME  :", split.scheme)
    print("NETLOC  :", split.netloc)
    print("PATH    :", split.path)
    print("QUERY   :", split.query)
    print("FRAGMENT:", split.fragment)
