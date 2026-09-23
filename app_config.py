"""Configuration shared by the local server and the Vercel Python function."""
import os
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent


def load_env(path=ROOT / '.env'):
    if path.is_file():
        for line in path.read_text(encoding='utf-8-sig').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            os.environ.setdefault(key.strip(), value.strip().strip('\"\''))


def public_config():
    """Only publish the low-privilege publishable key; never a service/secret key."""
    url = os.environ.get('SUPABASE_URL', '').strip().rstrip('/')
    key = os.environ.get('SUPABASE_PUBLISHABLE_KEY', '').strip()
    if url or key:
        parsed = urlparse(url)
        if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password or parsed.path or parsed.query or parsed.fragment or not key.startswith('sb_publishable_'):
            return {'mode': 'unconfigured', 'supabaseUrl': '', 'supabaseKey': ''}
        return {'mode': 'supabase', 'supabaseUrl': url, 'supabaseKey': key}
    # A deployed site never silently exposes the local demo administrator.
    mode = 'unconfigured' if os.environ.get('VERCEL') else 'demo'
    return {'mode': mode, 'supabaseUrl': '', 'supabaseKey': ''}


SECURITY_HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'X-Frame-Options': 'DENY',
    'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
    'Content-Security-Policy': "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: blob: https:; connect-src 'self' https://*.supabase.co; frame-ancestors 'none'; base-uri 'self'; form-action 'self'; object-src 'none'",
}
