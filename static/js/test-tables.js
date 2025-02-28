/**
 * Creates a test table to display test results
 * @param {string} testName - Name of the test
 * @param {string} testPath - Path to the test file
 * @returns {string} - ID of the created table
 */
function createTestTable(testName, testPath) {
    const tableId = `test-table-${testName.replace(/\s+/g, '-').replace(/[^a-zA-Z0-9-]/g, '')}`;
    
    // Check if table already exists
    if (document.getElementById(tableId)) {
        return tableId;
    }
    
    const testTable = document.createElement('div');
    testTable.id = tableId;
    testTable.className = 'test-table card';
    
    testTable.innerHTML = `
        <div class="card-header d-flex justify-content-between align-items-center">
            <div>
                <h6 class="mb-0">${testName}</h6>
                <small class="text-muted">${testPath}</small>
            </div>
            <div class="test-status">
                <span class="function-status status-pending">Pending</span>
            </div>
        </div>
        <div class="card-body p-0">
            <div class="progress test-progress">
                <div class="progress-bar bg-success" role="progressbar" style="width: 0%" 
                     aria-valuenow="0" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
            <table class="table table-hover mb-0">
                <thead>
                    <tr>
                        <th style="width: 70%">Function</th>
                        <th style="width: 30%">Status</th>
                    </tr>
                </thead>
                <tbody>
                </tbody>
            </table>
        </div>
    `;
    
    document.getElementById('detailed-results-container').appendChild(testTable);
    document.getElementById('no-results-message').style.display = 'none';
    
    return tableId;
}

/**
 * Adds a function row to a test table
 * @param {string} tableId - ID of the table
 * @param {string} functionName - Name of the function
 * @returns {string} - ID of the created row
 */

function addFunctionRow(tableId, functionName) {
    const table = document.getElementById(tableId);
    if (!table) return null;
    
    const tbody = table.querySelector('tbody');
    
    // Normalize function name to prevent duplicates
    let normalizedName = functionName;
    if (normalizedName.startsWith('test_')) {
        normalizedName = normalizedName.substring(5);
    }
    
    // Create a unique ID for this row
    const rowId = `${tableId}-func-${normalizedName.replace(/\s+/g, '-').replace(/[^a-zA-Z0-9-]/g, '')}`;
    
    // Check if row already exists
    if (document.getElementById(rowId)) {
        return rowId;
    }
    
    const row = document.createElement('tr');
    row.id = rowId;
    row.className = 'function-row-running';
    
    row.innerHTML = `
        <td>${normalizedName}</td>
        <td><span class="function-status status-running">Running</span></td>
    `;
    
    tbody.appendChild(row);
    return rowId;
}

/**
 * Updates the status of a function row
 * @param {string} rowId - ID of the row
 * @param {string} status - Status (passed, failed, running, pending)
 * @param {string} errorMessage - Error message if failed
 */
function updateFunctionStatus(rowId, status, errorMessage = null) {
    const row = document.getElementById(rowId);
    if (!row) return;
    
    // Remove existing status class
    row.className = '';
    
    // Add new status class
    if (status === 'passed') {
        row.classList.add('function-row-passed');
    } else if (status === 'failed') {
        row.classList.add('function-row-failed');
    } else if (status === 'running') {
        row.classList.add('function-row-running');
    }
    
    // Update status badge
    const statusBadge = row.querySelector('.function-status');
    statusBadge.className = 'function-status';
    
    if (status === 'passed') {
        statusBadge.classList.add('status-passed');
        statusBadge.textContent = 'PASSED';
    } else if (status === 'failed') {
        statusBadge.classList.add('status-failed');
        statusBadge.textContent = 'FAILED';
        
        // Make row clickable if there's an error message
        if (errorMessage) {
            row.style.cursor = 'pointer';
            row.setAttribute('data-error-message', errorMessage);
            
            row.addEventListener('click', function() {
                showErrorModal(this.getAttribute('data-error-message'));
            });
        }
    } else if (status === 'running') {
        statusBadge.classList.add('status-running');
        statusBadge.textContent = 'RUNNING';
    } else if (status === 'pending') {
        statusBadge.classList.add('status-pending');
        statusBadge.textContent = 'PENDING';
    }
}

/**
 * Updates the status of a test table
 * @param {string} tableId - ID of the table
 * @param {string} status - Status (passed, failed, running, pending)
 * @param {number} completed - Number of completed tests
 * @param {number} total - Total number of tests
 */
function updateTestTableStatus(tableId, status, completed = 0, total = 0) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    // Update progress bar
    if (total > 0) {
        const progressPercent = Math.floor((completed / total) * 100);
        const progressBar = table.querySelector('.progress-bar');
        progressBar.style.width = `${progressPercent}%`;
        progressBar.setAttribute('aria-valuenow', progressPercent);
    }
    
    // Update status badge
    const statusBadge = table.querySelector('.test-status .function-status');
    statusBadge.className = 'function-status';
    
    if (status === 'passed') {
        statusBadge.classList.add('status-passed');
        statusBadge.textContent = 'PASSED';
    } else if (status === 'failed') {
        statusBadge.classList.add('status-failed');
        statusBadge.textContent = 'FAILED';
    } else if (status === 'running') {
        statusBadge.classList.add('status-running');
        statusBadge.textContent = `RUNNING (${completed}/${total})`;
    } else if (status === 'pending') {
        statusBadge.classList.add('status-pending');
        statusBadge.textContent = 'PENDING';
    }
}

/**
 * Shows the error modal with details
 * @param {string} errorMessage - Error message to display
 * @param {string} screenshot - Path to the screenshot
 */
function showErrorModal(errorMessage, screenshot = null) {
    errorMessage = errorMessage || 'No error details available';
    document.getElementById('error-message').textContent = errorMessage;
    
    const screenshotContainer = document.getElementById('screenshot-container');
    if (screenshot) {
        document.getElementById('error-screenshot').src = `/screenshots/${screenshot}`;
        screenshotContainer.style.display = 'block';
    } else {
        screenshotContainer.style.display = 'none';
    }
    
    const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));
    errorModal.show();
}