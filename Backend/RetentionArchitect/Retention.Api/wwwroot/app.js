const backendStatus = document.getElementById('backendStatus');
const mlStatus = document.getElementById('mlStatus');
const refreshHealthBtn = document.getElementById('refreshHealthBtn');

const singleTabBtn = document.getElementById('singleTabBtn');
const batchTabBtn = document.getElementById('batchTabBtn');
const singleFormSection = document.getElementById('singleFormSection');
const batchFormSection = document.getElementById('batchFormSection');

const singleForm = document.getElementById('singleForm');
const batchForm = document.getElementById('batchForm');
const singleFillDemoBtn = document.getElementById('singleFillDemoBtn');
const batchFillDemoBtn = document.getElementById('batchFillDemoBtn');
const clearResultsBtn = document.getElementById('clearResultsBtn');

const userIdInput = document.getElementById('userId');
const batchUserIdsInput = document.getElementById('batchUserIds');

const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const emptyState = document.getElementById('emptyState');
const resultsContainer = document.getElementById('resultsContainer');

function setTab(isSingle) {
    singleTabBtn.classList.toggle('tab-button--active', isSingle);
    batchTabBtn.classList.toggle('tab-button--active', !isSingle);
    singleFormSection.classList.toggle('hidden', !isSingle);
    batchFormSection.classList.toggle('hidden', isSingle);
    clearError();
}

function setPill(element, text, kind) {
    element.textContent = text;
    element.className = `pill ${kind}`;
}

async function checkHealth() {
    setPill(backendStatus, 'Checking...', 'pill--idle');
    setPill(mlStatus, 'Checking...', 'pill--idle');

    try {
        const backendResponse = await fetch('/api/prediction/health');
        if (backendResponse.ok) {
            setPill(backendStatus, 'Online', 'pill--success');
        } else {
            setPill(backendStatus, 'Issue', 'pill--danger');
        }
    } catch {
        setPill(backendStatus, 'Offline', 'pill--danger');
    }

    try {
        const mlResponse = await fetch('/api/prediction/health/ml');
        if (mlResponse.ok) {
            setPill(mlStatus, 'Online', 'pill--success');
        } else {
            setPill(mlStatus, 'Issue', 'pill--warning');
        }
    } catch {
        setPill(mlStatus, 'Offline', 'pill--danger');
    }
}

function showLoading() {
    loadingState.classList.remove('hidden');
    errorState.classList.add('hidden');
    emptyState.classList.add('hidden');
}

function hideLoading() {
    loadingState.classList.add('hidden');
}

function showError(message) {
    errorState.textContent = message;
    errorState.classList.remove('hidden');
}

function clearError() {
    errorState.textContent = '';
    errorState.classList.add('hidden');
}

function clearResults() {
    resultsContainer.innerHTML = '';
    hideLoading();
    clearError();
    emptyState.classList.remove('hidden');
}

function escapeHtml(value) {
    return String(value ?? '')
        .replaceAll('&', '&amp;')
        .replaceAll('<', '&lt;')
        .replaceAll('>', '&gt;')
        .replaceAll('"', '&quot;')
        .replaceAll("'", '&#39;');
}

function toPercent(value) {
    if (typeof value !== 'number' || Number.isNaN(value)) {
        return '—';
    }
    return `${(value * 100).toFixed(1)}%`;
}

function getClassBadge(predictedClass) {
    const normalized = (predictedClass || '').toLowerCase();
    if (normalized.includes('involuntary')) {
        return { text: 'Involuntary churn', kind: 'pill--danger' };
    }
    if (normalized.includes('voluntary')) {
        return { text: 'Voluntary churn', kind: 'pill--warning' };
    }
    return { text: predictedClass || 'Unknown', kind: 'pill--success' };
}

function buildList(items, emptyText) {
    if (!Array.isArray(items) || items.length === 0) {
        return `<p class="muted">${escapeHtml(emptyText)}</p>`;
    }

    return `<ul>${items.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`;
}

function buildExplanations(explanations) {
    if (!Array.isArray(explanations) || explanations.length === 0) {
        return '<p class="muted">No explanation details were returned.</p>';
    }

    return `
        <div class="explanation-list">
            ${explanations.map(explanation => `
                <div class="explanation-item">
                    <div class="explanation-top">
                        <strong>${escapeHtml(explanation.feature || 'Feature')}</strong>
                        <span>${escapeHtml(explanation.direction || 'n/a')} · impact ${escapeHtml(explanation.impact ?? 'n/a')}</span>
                    </div>
                    <div>${escapeHtml(explanation.description || 'No description provided.')}</div>
                </div>
            `).join('')}
        </div>
    `;
}

function renderPredictionCard(prediction) {
    const badge = getClassBadge(prediction.predictedClass);
    const probabilities = prediction.classProbabilities || {};

    return `
        <article class="prediction-card">
            <div class="card-header">
                <h3>User ${escapeHtml(prediction.userId || 'Unknown')}</h3>
                <span class="pill ${badge.kind}">${escapeHtml(badge.text)}</span>
            </div>

            <div class="badge-row">
                <span class="pill pill--idle">Risk ${escapeHtml(toPercent(prediction.churnProbability))}</span>
            </div>

            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-label">Stay</div>
                    <div class="metric-value">${escapeHtml(toPercent(probabilities.stay))}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Voluntary churn</div>
                    <div class="metric-value">${escapeHtml(toPercent(probabilities.voluntaryChurn))}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Involuntary churn</div>
                    <div class="metric-value">${escapeHtml(toPercent(probabilities.involuntaryChurn))}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Predicted class</div>
                    <div class="metric-value" style="font-size:1rem; line-height:1.3;">${escapeHtml(prediction.predictedClass || '—')}</div>
                </div>
            </div>

            <div class="section-stack">
                <div class="section-card">
                    <strong>Top drivers</strong>
                    ${buildList(prediction.topDrivers, 'No drivers were returned.')}
                </div>

                <div class="section-card">
                    <strong>Recommended actions</strong>
                    ${buildList(prediction.recommendedActions, 'No recommendations were returned.')}
                </div>

                <div class="section-card">
                    <strong>Explanation details</strong>
                    ${buildExplanations(prediction.explanations)}
                </div>
            </div>
        </article>
    `;
}

function renderPredictions(data) {
    const predictions = Array.isArray(data) ? data : [data];

    resultsContainer.innerHTML = predictions.map(renderPredictionCard).join('');
    emptyState.classList.add('hidden');
}

async function postJson(url, payload) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    });

    const text = await response.text();
    let data = null;

    if (text) {
        try {
            data = JSON.parse(text);
        } catch {
            data = text;
        }
    }

    if (!response.ok) {
        const message = typeof data === 'string' && data.trim().length > 0
            ? data
            : `Request failed with status ${response.status}.`;
        throw new Error(message);
    }

    return data;
}

singleForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearError();
    showLoading();

    try {
        const userId = userIdInput.value.trim();
        const data = await postJson('/api/prediction/user', { userId });
        renderPredictions(data);
    } catch (error) {
        resultsContainer.innerHTML = '';
        emptyState.classList.add('hidden');
        showError(error.message || 'Something went wrong while predicting the user.');
    } finally {
        hideLoading();
    }
});

batchForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    clearError();
    showLoading();

    try {
        const userIds = batchUserIdsInput.value
            .split(/\r?\n/)
            .map(value => value.trim())
            .filter(Boolean);

        const data = await postJson('/api/prediction/batch', { userIds });
        renderPredictions(data);
    } catch (error) {
        resultsContainer.innerHTML = '';
        emptyState.classList.add('hidden');
        showError(error.message || 'Something went wrong while predicting the batch.');
    } finally {
        hideLoading();
    }
});

singleFillDemoBtn.addEventListener('click', () => {
    userIdInput.value = '12345';
});

batchFillDemoBtn.addEventListener('click', () => {
    batchUserIdsInput.value = ['12345', '45678', '99999'].join('\n');
});

clearResultsBtn.addEventListener('click', clearResults);
singleTabBtn.addEventListener('click', () => setTab(true));
batchTabBtn.addEventListener('click', () => setTab(false));
refreshHealthBtn.addEventListener('click', checkHealth);

clearResults();
setTab(true);
checkHealth();
