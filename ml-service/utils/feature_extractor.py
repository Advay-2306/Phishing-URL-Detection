def extract_features(url: str) -> dict:
    """Expanded URL lexical features to better match training dataset"""
    if not url:
        return {}

    url_lower = url.lower()
    features = {
        "length_url": len(url),
        "length_hostname": len(url.split('/')[2]) if '://' in url and len(url.split('/')) > 2 else 0,
        "ip": 1 if any(part.isdigit() and len(part) >= 3 for part in url.split('.')) else 0,
        "nb_dots": url.count('.'),
        "nb_hyphens": url.count('-'),
        "nb_at": url.count('@'),
        "nb_qm": url.count('?'),
        "nb_and": url.count('&'),
        "nb_or": url.count('|'),
        "nb_eq": url.count('='),
        "nb_underscore": url.count('_'),
        "nb_tilde": url.count('~'),
        "nb_percent": url.count('%'),
        "nb_slash": url.count('/'),
        "nb_star": url.count('*'),
        "nb_colon": url.count(':'),
        "nb_comma": url.count(','),
        "nb_semicolumn": url.count(';'),
        "nb_dollar": url.count('$'),
        "nb_space": url.count(' '),
        "nb_www": 1 if 'www.' in url_lower else 0,
        "nb_com": url_lower.count('.com'),
        "nb_dslash": url_lower.count('//'),
        "http_in_path": 1 if 'http' in url_lower.split('://')[-1] else 0,
        "https_token": 1 if url.startswith("https") else 0,
        "ratio_digits_url": sum(c.isdigit() for c in url) / len(url) if url else 0,
        "ratio_digits_host": sum(c.isdigit() for c in url.split('/')[2]) / len(url.split('/')[2]) if '://' in url else 0,
        "punycode": 1 if 'xn--' in url_lower else 0,
        "port": 1 if ':' in url.split('/')[2] else 0,
        "tld_in_path": 1 if any(tld in url_lower.split('/')[3:] for tld in ['.com', '.net', '.org']) else 0,
        "abnormal_subdomain": 1 if url.count('.') > 3 else 0,
        "nb_subdomains": max(0, url.count('.') - 1),
        "prefix_suffix": 1 if '-' in url.split('/')[2] else 0,
        "shortening_service": 1 if any(s in url_lower for s in ['bit.ly', 'tinyurl', 'goo.gl']) else 0,
        "path_extension": 1 if any(ext in url_lower for ext in ['.php', '.asp', '.jsp']) else 0,
    }
    return features