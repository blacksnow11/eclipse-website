#!/usr/bin/env python3
import json, os

BASE     = "/Users/mac/eclipse-website"
PASSWORD = "eclipsecompanions"

# ── Known models (slug, display name, starting price, photo count) ────────────
models = [
    ("sophia",    "Sophia",    700,   5),
    ("isabella",  "Isabella",  500,   3),
    ("valentina", "Valentina", 900,   5),
    ("camila",    "Camila",    900,   4),
    ("aaliyah",   "Aaliyah",   600,   5),
    ("jasmine",   "Jasmine",   900,   7),
    ("gabrielle", "Gabrielle", 1400,  8),
    ("luna",      "Luna",      500,   9),
    ("serena",    "Serena",    1200, 10),
    ("naomi",     "Naomi",     800,   7),
    ("zara",      "Zara",      400,   6),
    ("kehlani",   "Kehlani",   650,   9),
]

model_lookup = {slug: (name, price, count) for slug, name, price, count in models}

IMAGE_EXTS = (".jpeg", ".jpg", ".png", ".webp")


def sanitize_slug(raw):
    """Normalize to a clean URL-safe slug (lowercase, no spaces)."""
    return raw.strip().lower().replace(" ", "")


def find_image_folder(slug):
    """
    Locate the images/<folder> directory for a slug, handling
    case differences and spaces in folder names.
    Returns the full path, or None if not found.
    """
    images_dir = os.path.join(BASE, "images")
    exact = os.path.join(images_dir, slug)
    if os.path.isdir(exact):
        return exact
    for d in os.listdir(images_dir):
        if d.lower().replace(" ", "") == slug:
            return os.path.join(images_dir, d)
    return None


def prepare_images(img_dir, slug):
    """
    Ensure images in img_dir are:
      1. Named 1.jpeg, 2.jpeg, ... (renamed if needed, sorted alphabetically)
      2. Compressed as JPEG (quality 85, max 1500 px on longest side)
    Skips processing if files are already numbered .jpeg (already done).
    Returns (count, ext) — ext is always '.jpeg'.
    """
    from collections import Counter
    from PIL import Image

    MAX_PX  = 1500
    QUALITY = 85

    files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(IMAGE_EXTS)])
    if not files:
        return 0, ".jpeg"

    # Already processed? (all numbered .jpeg files)
    if all(os.path.splitext(f)[0].isdigit() and f.lower().endswith(".jpeg") for f in files):
        return len(files), ".jpeg"

    # ── Step 1: rename to numbered temp names ──────────────────────────────
    if not all(os.path.splitext(f)[0].isdigit() for f in files):
        ext_counts = Counter(os.path.splitext(f)[1].lower() for f in files)
        tmp_ext = ext_counts.most_common(1)[0][0]
        print("    Auto-renaming {} image(s) in images/{}/...".format(len(files), slug))
        tmp_names = []
        for i, fname in enumerate(files):
            src = os.path.join(img_dir, fname)
            tmp = os.path.join(img_dir, "__tmp_{:04d}{}".format(i, os.path.splitext(fname)[1].lower()))
            os.rename(src, tmp)
            tmp_names.append(tmp)
        for i, tmp in enumerate(sorted(tmp_names), 1):
            os.rename(tmp, os.path.join(img_dir, "{}{}".format(i, tmp_ext)))
        files = sorted([f for f in os.listdir(img_dir) if f.lower().endswith(IMAGE_EXTS)])

    # ── Step 2: compress to JPEG ────────────────────────────────────────────
    print("    Compressing {} image(s) in images/{}/...".format(len(files), slug))
    for fname in files:
        src = os.path.join(img_dir, fname)
        dst = os.path.join(img_dir, os.path.splitext(fname)[0] + ".jpeg")
        with Image.open(src) as img:
            img = img.convert("RGB")
            if max(img.size) > MAX_PX:
                img.thumbnail((MAX_PX, MAX_PX), Image.LANCZOS)
            img.save(dst, "JPEG", quality=QUALITY, optimize=True)
        if src != dst:
            os.remove(src)
    print("    Done. {} image(s) compressed to JPEG.".format(len(files)))
    return len(files), ".jpeg"


# ── Template: individual model page ─────────────────────────────────────────
MODEL_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eclipse &mdash; __NAME__</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        :root {
            --bg: #0c0c0c;
            --card-bg: #141414;
            --border: #242424;
            --gold: #c9a455;
            --gold-light: #e8c978;
            --text: #ffffff;
            --muted: #777;
        }

        html { scroll-behavior: smooth; }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'Montserrat', 'Segoe UI', sans-serif;
            min-height: 100vh;
        }

        /* ── NAV ─────────────────────────────────────── */
        .site-nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1.2rem 2rem;
            background: rgba(12,12,12,0.88);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(36,36,36,0.6);
        }

        .back-link {
            color: var(--muted);
            text-decoration: none;
            font-size: 0.68rem;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: color 0.2s;
        }

        .back-link:hover { color: var(--gold); }

        .nav-brand {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.4rem;
            font-weight: 300;
            letter-spacing: 0.4em;
            padding-right: 0.4em;
            text-transform: uppercase;
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
        }

        .nav-brand em {
            font-style: normal;
            color: var(--gold);
        }

        .nav-spacer { width: 120px; }

        /* ── HERO ─────────────────────────────────────── */
        .model-hero {
            position: relative;
            height: 92vh;
            min-height: 520px;
            overflow: hidden;
            margin-top: 0;
        }

        .hero-img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: top center;
            display: block;
        }

        .hero-overlay {
            position: absolute;
            inset: 0;
            background: linear-gradient(
                to bottom,
                rgba(12,12,12,0.35) 0%,
                rgba(12,12,12,0.1) 30%,
                rgba(12,12,12,0.3) 60%,
                rgba(12,12,12,0.92) 100%
            );
        }

        .hero-info {
            position: absolute;
            bottom: 3.5rem;
            left: 0;
            right: 0;
            text-align: center;
            padding: 0 2rem;
        }

        .hero-name {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: clamp(3rem, 10vw, 6.5rem);
            font-weight: 300;
            letter-spacing: 0.15em;
            line-height: 1;
            color: #fff;
        }

        .hero-divider {
            width: 80px;
            height: 1px;
            background: linear-gradient(to right, transparent, var(--gold), transparent);
            margin: 1.4rem auto;
        }

        .hero-price {
            font-size: 0.72rem;
            font-weight: 500;
            letter-spacing: 0.45em;
            color: var(--gold);
            text-transform: uppercase;
        }

        /* ── GALLERY SECTION ─────────────────────────── */
        .gallery-section {
            padding: 5rem 2rem 6rem;
            max-width: 1200px;
            margin: 0 auto;
        }

        .gallery-header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .gallery-title {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.8rem;
            font-weight: 300;
            letter-spacing: 0.3em;
            text-transform: uppercase;
            color: #fff;
        }

        .gallery-divider {
            width: 50px;
            height: 1px;
            background: linear-gradient(to right, transparent, var(--gold), transparent);
            margin: 1rem auto 0;
        }

        .photo-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.75rem;
        }

        @media (max-width: 768px) {
            .photo-grid { grid-template-columns: repeat(2, 1fr); }
        }

        @media (max-width: 480px) {
            .photo-grid { grid-template-columns: 1fr; }
        }

        .photo-item {
            position: relative;
            overflow: hidden;
            border-radius: 2px;
            border: 1px solid var(--border);
            aspect-ratio: 3/4;
            cursor: pointer;
            background: var(--card-bg);
            transition: border-color 0.3s ease, box-shadow 0.3s ease;
        }

        .photo-item:hover {
            border-color: var(--gold);
            box-shadow: 0 8px 30px rgba(0,0,0,0.5);
        }

        .photo-item img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: top center;
            display: block;
            transition: transform 0.45s ease;
        }

        .photo-item:hover img {
            transform: scale(1.06);
        }

        .photo-item-zoom {
            position: absolute;
            inset: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(0,0,0,0);
            transition: background 0.3s ease;
        }

        .photo-item:hover .photo-item-zoom {
            background: rgba(0,0,0,0.2);
        }

        .zoom-icon {
            width: 44px;
            height: 44px;
            border: 1px solid rgba(201,164,85,0.7);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--gold);
            font-size: 1rem;
            opacity: 0;
            transition: opacity 0.3s ease, transform 0.3s ease;
            transform: scale(0.8);
        }

        .photo-item:hover .zoom-icon {
            opacity: 1;
            transform: scale(1);
        }

        /* ── LIGHTBOX ────────────────────────────────── */
        .lightbox {
            display: none;
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,0.96);
            z-index: 9999;
            align-items: center;
            justify-content: center;
            animation: lbFadeIn 0.2s ease;
        }

        .lightbox.active {
            display: flex;
        }

        @keyframes lbFadeIn {
            from { opacity: 0; }
            to   { opacity: 1; }
        }

        .lb-img-wrap {
            position: relative;
            max-width: 90vw;
            max-height: 90vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        #lb-img {
            max-width: 90vw;
            max-height: 88vh;
            object-fit: contain;
            display: block;
            border-radius: 2px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.8);
        }

        .lb-close {
            position: fixed;
            top: 1.5rem;
            right: 1.5rem;
            background: none;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 50%;
            color: #fff;
            font-size: 1rem;
            width: 40px;
            height: 40px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: border-color 0.2s, color 0.2s;
            z-index: 10000;
        }

        .lb-close:hover {
            border-color: var(--gold);
            color: var(--gold);
        }

        .lb-nav-btn {
            position: fixed;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 50%;
            color: #fff;
            font-size: 1.6rem;
            width: 52px;
            height: 52px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: border-color 0.2s, color 0.2s, background 0.2s;
            z-index: 10000;
        }

        .lb-nav-btn:hover {
            border-color: var(--gold);
            color: var(--gold);
            background: rgba(201,164,85,0.08);
        }

        .lb-prev { left: 1.5rem; }
        .lb-next { right: 1.5rem; }

        .lb-counter {
            position: fixed;
            bottom: 1.5rem;
            left: 50%;
            transform: translateX(-50%);
            font-size: 0.65rem;
            letter-spacing: 0.3em;
            color: var(--muted);
            text-transform: uppercase;
            z-index: 10000;
        }

        /* ── FOOTER ──────────────────────────────────── */
        .site-footer {
            text-align: center;
            padding: 2rem;
            border-top: 1px solid var(--border);
            font-size: 0.6rem;
            letter-spacing: 0.25em;
            color: #2e2e2e;
            text-transform: uppercase;
        }

        @media (max-width: 600px) {
            .site-nav { padding: 1rem 1.2rem; }
            .hero-info { bottom: 2rem; }
            .gallery-section { padding: 4rem 1.2rem 5rem; }
            .lb-prev { left: 0.8rem; }
            .lb-next { right: 0.8rem; }
        }
    </style>
</head>
<body>

    <!-- NAV -->
    <nav class="site-nav">
        <a href="../../__GALLERY_SLUG__/" class="back-link">&#8592;&nbsp; All Models</a>
        <div class="nav-brand">E<em>C</em>LIPSE</div>
        <div class="nav-spacer"></div>
    </nav>

    <!-- HERO -->
    <div class="model-hero">
        <img class="hero-img" src="../../images/__SLUG__/1__EXT__" alt="__NAME__">
        <div class="hero-overlay"></div>
        <div class="hero-info">
            <div class="hero-name">__NAME__</div>
            <div class="hero-divider"></div>
            <div class="hero-price">Starting at __PRICE__</div>
        </div>
    </div>

    <!-- GALLERY -->
    <section class="gallery-section">
        <div class="gallery-header">
            <h2 class="gallery-title">Gallery</h2>
            <div class="gallery-divider"></div>
        </div>
        <div class="photo-grid" id="photo-grid"></div>
    </section>

    <footer class="site-footer">&copy; 2026 Eclipse &mdash; Private Access Only</footer>

    <!-- LIGHTBOX -->
    <div id="lightbox" class="lightbox">
        <button class="lb-close" id="lb-close">&#10005;</button>
        <button class="lb-nav-btn lb-prev" id="lb-prev">&#8249;</button>
        <div class="lb-img-wrap">
            <img id="lb-img" src="" alt="__NAME__">
        </div>
        <button class="lb-nav-btn lb-next" id="lb-next">&#8250;</button>
        <div class="lb-counter" id="lb-counter"></div>
    </div>

    <script>
        // Auth guard — redirect to gallery if not authenticated
        if (sessionStorage.getItem('eclipse_auth') !== 'true') {
            window.location.replace('../../__GALLERY_SLUG__/');
        }

        const photos = __PHOTOS_JS__;
        let current = 0;

        // Build photo grid
        const grid = document.getElementById('photo-grid');
        photos.forEach(function(src, i) {
            const item = document.createElement('div');
            item.className = 'photo-item';

            const img = document.createElement('img');
            img.src = src;
            img.alt = '__NAME__ photo ' + (i + 1);
            img.loading = 'lazy';

            const overlay = document.createElement('div');
            overlay.className = 'photo-item-zoom';
            overlay.innerHTML = '<div class="zoom-icon">&#43;</div>';

            item.appendChild(img);
            item.appendChild(overlay);
            item.addEventListener('click', function() { openLb(i); });
            grid.appendChild(item);
        });

        // Lightbox
        const lb      = document.getElementById('lightbox');
        const lbImg   = document.getElementById('lb-img');
        const lbCnt   = document.getElementById('lb-counter');

        function setPhoto(i) {
            current = (i + photos.length) % photos.length;
            lbImg.src = photos[current];
            lbCnt.textContent = (current + 1) + ' \u2014 ' + photos.length;
        }

        function openLb(i) {
            setPhoto(i);
            lb.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeLb() {
            lb.classList.remove('active');
            document.body.style.overflow = '';
        }

        document.getElementById('lb-close').addEventListener('click', closeLb);
        document.getElementById('lb-prev').addEventListener('click', function() { setPhoto(current - 1); });
        document.getElementById('lb-next').addEventListener('click', function() { setPhoto(current + 1); });

        lb.addEventListener('click', function(e) {
            if (e.target === lb || e.target.className === 'lb-img-wrap') closeLb();
        });

        document.addEventListener('keydown', function(e) {
            if (!lb.classList.contains('active')) return;
            if (e.key === 'Escape')      closeLb();
            if (e.key === 'ArrowLeft')   setPhoto(current - 1);
            if (e.key === 'ArrowRight')  setPhoto(current + 1);
        });
    </script>
</body>
</html>
"""

# ── Template: gallery / listing page ─────────────────────────────────────────
GALLERY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eclipse \u2014 Models</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Montserrat:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        :root {
            --bg: #0c0c0c;
            --card-bg: #141414;
            --border: #242424;
            --gold: #c9a455;
            --gold-light: #e8c978;
            --text: #ffffff;
            --muted: #777;
        }

        html { scroll-behavior: smooth; }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'Montserrat', 'Segoe UI', sans-serif;
            min-height: 100vh;
        }

        #auth-overlay {
            position: fixed;
            inset: 0;
            background: #0c0c0c;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 9999;
        }

        #auth-overlay::before {
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(ellipse at 50% 40%, #1c1008 0%, #0c0c0c 65%);
        }

        .auth-box {
            position: relative;
            z-index: 1;
            text-align: center;
            padding: 3rem 2rem;
            max-width: 380px;
            width: 100%;
            animation: fadeUp 0.8s ease forwards;
        }

        @keyframes fadeUp {
            from { opacity: 0; transform: translateY(20px); }
            to   { opacity: 1; transform: translateY(0); }
        }

        .auth-brand {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: clamp(2.8rem, 10vw, 4.5rem);
            font-weight: 300;
            letter-spacing: 0.5em;
            padding-right: 0.5em;
            color: #fff;
            text-transform: uppercase;
        }

        .auth-brand em { font-style: normal; color: var(--gold); }

        .auth-divider {
            width: 80px;
            height: 1px;
            background: linear-gradient(to right, transparent, var(--gold), transparent);
            margin: 1.8rem auto;
        }

        .auth-subtitle {
            font-size: 0.62rem;
            letter-spacing: 0.4em;
            color: var(--muted);
            text-transform: uppercase;
            margin-bottom: 2.5rem;
        }

        #auth-form { display: flex; flex-direction: column; gap: 1rem; }

        #password-input {
            background: #181818;
            border: 1px solid var(--border);
            border-radius: 2px;
            color: #fff;
            font-family: 'Montserrat', sans-serif;
            font-size: 0.8rem;
            letter-spacing: 0.15em;
            padding: 1rem 1.2rem;
            outline: none;
            text-align: center;
            transition: border-color 0.2s;
        }

        #password-input:focus { border-color: var(--gold); }
        #password-input::placeholder { color: #444; letter-spacing: 0.25em; }

        .auth-btn {
            background: var(--gold);
            color: #0c0c0c;
            border: none;
            border-radius: 2px;
            font-family: 'Montserrat', sans-serif;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.35em;
            padding: 1rem 2rem;
            text-transform: uppercase;
            cursor: pointer;
            transition: background 0.2s, transform 0.1s;
        }

        .auth-btn:hover { background: var(--gold-light); }
        .auth-btn:active { transform: scale(0.98); }

        .error-msg {
            color: #e05252;
            font-size: 0.68rem;
            letter-spacing: 0.15em;
            display: none;
            margin-top: 0.25rem;
        }

        #gallery-content { display: none; min-height: 100vh; }

        .site-header {
            text-align: center;
            padding: 4rem 2rem 3rem;
            border-bottom: 1px solid var(--border);
        }

        .site-brand {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: clamp(2rem, 6vw, 3.5rem);
            font-weight: 300;
            letter-spacing: 0.5em;
            padding-right: 0.5em;
            text-transform: uppercase;
        }

        .site-brand em { font-style: normal; color: var(--gold); }

        .site-tagline {
            font-size: 0.62rem;
            letter-spacing: 0.4em;
            color: var(--muted);
            text-transform: uppercase;
            margin-top: 1rem;
        }

        .header-divider {
            width: 60px;
            height: 1px;
            background: linear-gradient(to right, transparent, var(--gold), transparent);
            margin: 1.5rem auto 0;
        }

        .models-section {
            padding: 3rem 2rem 5rem;
            max-width: 1280px;
            margin: 0 auto;
        }

        .models-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
        }

        .model-card {
            position: relative;
            border-radius: 3px;
            overflow: hidden;
            background: var(--card-bg);
            border: 1px solid var(--border);
            cursor: pointer;
            text-decoration: none;
            display: block;
            aspect-ratio: 3/4;
            transition: transform 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
        }

        .model-card:hover {
            transform: translateY(-6px);
            border-color: var(--gold);
            box-shadow: 0 20px 60px rgba(0,0,0,0.7), 0 0 0 1px rgba(201,164,85,0.15);
        }

        .model-card-photo {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: top center;
            display: block;
            transition: transform 0.5s ease;
        }

        .model-card:hover .model-card-photo { transform: scale(1.05); }

        .model-card-overlay {
            position: absolute;
            bottom: 0; left: 0; right: 0;
            background: linear-gradient(to top, rgba(0,0,0,0.92) 0%, rgba(0,0,0,0.5) 50%, transparent 100%);
            padding: 2.5rem 1.4rem 1.4rem;
        }

        .model-card-name {
            font-family: 'Cormorant Garamond', Georgia, serif;
            font-size: 1.7rem;
            font-weight: 400;
            letter-spacing: 0.08em;
            color: #fff;
            line-height: 1.1;
        }

        .model-card-price {
            font-size: 0.68rem;
            font-weight: 500;
            letter-spacing: 0.28em;
            color: var(--gold);
            text-transform: uppercase;
            margin-top: 0.4rem;
        }

        .model-card-arrow {
            position: absolute;
            top: 1.2rem; right: 1.2rem;
            width: 32px; height: 32px;
            border: 1px solid rgba(201,164,85,0.4);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            color: var(--gold);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .model-card:hover .model-card-arrow { opacity: 1; }

        .site-footer {
            text-align: center;
            padding: 2rem;
            border-top: 1px solid var(--border);
            font-size: 0.6rem;
            letter-spacing: 0.25em;
            color: #2e2e2e;
            text-transform: uppercase;
        }
    </style>
</head>
<body>

    <div id="auth-overlay">
        <div class="auth-box">
            <div class="auth-brand">E<em>C</em>LIPSE</div>
            <div class="auth-divider"></div>
            <p class="auth-subtitle">Private Access Required</p>
            <form id="auth-form" autocomplete="off">
                <input type="password" id="password-input" placeholder="Enter Password" />
                <button type="submit" class="auth-btn">Enter</button>
                <p class="error-msg" id="error-msg">&#10005; &nbsp;Incorrect password. Please try again.</p>
            </form>
        </div>
    </div>

    <div id="gallery-content">
        <header class="site-header">
            <div class="site-brand">E<em>C</em>LIPSE</div>
            <div class="header-divider"></div>
            <p class="site-tagline">Our Models</p>
        </header>
        <section class="models-section">
            <div class="models-grid">
__CARDS__
            </div>
        </section>
        <footer class="site-footer">&copy; 2026 Eclipse &mdash; Private Access Only</footer>
    </div>

    <script>
        const PASSWORD = '__PASSWORD__';
        const overlay  = document.getElementById('auth-overlay');
        const content  = document.getElementById('gallery-content');
        const form     = document.getElementById('auth-form');
        const input    = document.getElementById('password-input');
        const errorMsg = document.getElementById('error-msg');

        function unlock() {
            sessionStorage.setItem('eclipse_auth', 'true');
            overlay.style.display = 'none';
            content.style.display = 'block';
        }

        if (sessionStorage.getItem('eclipse_auth') === 'true') { unlock(); }

        form.addEventListener('submit', function(e) {
            e.preventDefault();
            if (input.value === PASSWORD) {
                unlock();
            } else {
                errorMsg.style.display = 'block';
                input.value = '';
                input.focus();
                input.style.borderColor = '#e05252';
                setTimeout(() => { input.style.borderColor = ''; }, 1500);
            }
        });
    </script>
</body>
</html>
"""


def generate_model_page(slug, name, price, count, ext, gallery_slug):
    """Generate an individual model page and write it to disk."""
    price_fmt = "${:,}".format(price)
    photos_js = json.dumps(["../../images/{}/{}{}".format(slug, i, ext) for i in range(1, count + 1)])

    html = MODEL_TEMPLATE
    html = html.replace("__NAME__",         name)
    html = html.replace("__PRICE__",        price_fmt)
    html = html.replace("__SLUG__",         slug)
    html = html.replace("__EXT__",          ext)
    html = html.replace("__PHOTOS_JS__",    photos_js)
    html = html.replace("__GALLERY_SLUG__", gallery_slug)

    path = "{}/models/{}/index.html".format(BASE, slug)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html)
    print("  Generated model page: {}/models/{}/".format(BASE, slug))


def generate_gallery_page(gallery_slug, page_models):
    """Generate a gallery/listing page for the given models."""
    cards_html = ""
    for slug, name, price, ext in page_models:
        price_str = "${:,}".format(price)
        cards_html += (
            "\n                <!-- {name} -->"
            "\n                <a class=\"model-card\" href=\"../models/{slug}/\">"
            "\n                    <img class=\"model-card-photo\" src=\"../images/{slug}/1{ext}\" alt=\"{name}\" loading=\"lazy\">"
            "\n                    <div class=\"model-card-overlay\">"
            "\n                        <div class=\"model-card-name\">{name}</div>"
            "\n                        <div class=\"model-card-price\">From {price}</div>"
            "\n                    </div>"
            "\n                    <div class=\"model-card-arrow\">&#8599;</div>"
            "\n                </a>"
        ).format(name=name, slug=slug, price=price_str, ext=ext)

    html = GALLERY_TEMPLATE
    html = html.replace("__CARDS__",    cards_html)
    html = html.replace("__PASSWORD__", PASSWORD)

    gallery_dir  = "{}/{}".format(BASE, gallery_slug)
    gallery_path = "{}/index.html".format(gallery_dir)
    os.makedirs(gallery_dir, exist_ok=True)
    with open(gallery_path, "w") as f:
        f.write(html)
    print("\nGallery page created: {}/".format(gallery_slug))
    print("  -> {}\n".format(gallery_path))


# ═══════════════════════════════════════════════════════
#  Interactive prompts
# ═══════════════════════════════════════════════════════
print("=" * 52)
print("  Eclipse \u2014 Page Generator")
print("=" * 52)

gallery_slug = sanitize_slug(input("\nPage name (e.g. 'vip' \u2192 domain.com/vip): "))
if not gallery_slug:
    print("No page name entered. Exiting.")
    exit(1)

raw_input = input("Models to include (comma-separated image folder names): ").strip()
if not raw_input:
    print("No models specified. Exiting.")
    exit(1)

# Resolve model data; prompt for unknowns
print()
page_models  = []  # (slug, name, price, ext) for gallery cards
new_models   = []  # new models that also need individual pages

for slug_raw in raw_input.split(","):
    slug = sanitize_slug(slug_raw)
    if not slug:
        continue
    if slug in model_lookup:
        name, price, count = model_lookup[slug]
        page_models.append((slug, name, price, ".jpeg"))
    else:
        img_dir = find_image_folder(slug)
        if img_dir is None:
            print("  WARNING: images/{} not found \u2014 skipping.".format(slug))
            continue
        print("  New model '{}' \u2014 enter details:".format(slug))
        name  = input("    Display name: ").strip()
        price = int(input("    Starting price ($ numbers only): ").strip())
        count, ext = prepare_images(img_dir, slug)
        print("    Auto-detected {} photo(s) in images/{}/".format(count, slug))
        page_models.append((slug, name, price, ext))
        new_models.append((slug, name, price, count, ext))

if not page_models:
    print("No valid models resolved. Exiting.")
    exit(1)

# Generate individual pages for any new (unknown) models
if new_models:
    print("Generating individual pages for new models...")
    for slug, name, price, count, ext in new_models:
        generate_model_page(slug, name, price, count, ext, gallery_slug)

# Generate the gallery page
generate_gallery_page(gallery_slug, page_models)
print("Done!")
