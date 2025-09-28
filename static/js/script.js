let myChart = null;
let uploadedData = null;

document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initFileUpload();
    initControls();
});

function initTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    const currentTheme = localStorage.getItem('theme') || 'dark';
    
    if (currentTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        document.body.setAttribute('data-theme', 'dark');
        themeToggle.checked = true;
    } else {
        document.documentElement.removeAttribute('data-theme');
        document.body.removeAttribute('data-theme');
        themeToggle.checked = false;
    }

    localStorage.setItem('theme', currentTheme);

    themeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.body.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
            document.body.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
        }
        
        if (myChart) {
            updateChartTheme();
        }
    });
}

function initFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const uploadArea = document.getElementById('uploadArea');

    uploadArea.addEventListener('click', () => fileInput.click());
    
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('drag-over');
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('drag-over');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('drag-over');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    
    fileInput.addEventListener('change', function(e) {
        if (this.files[0]) {
            handleFile(this.files[0]);
        }
    });
}

function initControls() {
    const previewBtn = document.getElementById('previewBtn');
    const visualizeBtn = document.getElementById('visualizeBtn');
    const chartType = document.getElementById('chartType');
    const xColumn = document.getElementById('xColumn');
    const yColumn = document.getElementById('yColumn');
    const categoryColumn = document.getElementById('categoryColumn');
    const valueColumn = document.getElementById('valueColumn');
    const sizeColumn = document.getElementById('sizeColumn');
    const stackColumn = document.getElementById('stackColumn'); // Add stack column

    previewBtn?.addEventListener('click', updatePreview);
    visualizeBtn?.addEventListener('click', createVisualization);
    chartType?.addEventListener('change', onChartTypeChange);
    xColumn?.addEventListener('change', updateAIRecommendations);
    yColumn?.addEventListener('change', updateAIRecommendations);
    categoryColumn?.addEventListener('change', updateAIRecommendations);
    valueColumn?.addEventListener('change', updateAIRecommendations);
    sizeColumn?.addEventListener('change', updateAIRecommendations);
    stackColumn?.addEventListener('change', updateAIRecommendations); // Add stack column listener
}

async function handleFile(file) {
    if (!file.name.match(/\.(csv|xlsx|xls)$/i)) {
        showError('Please select a CSV or Excel file');
        return;
    }

    showLoading(true);
    
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            uploadedData = data;
            displayFileInfo(data);
            showSections();
            await updatePreview();
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Upload failed: ' + error.message);
    } finally {
        showLoading(false);
    }
}

function displayFileInfo(data) {
    document.getElementById('fileName').textContent = data.filename;
    document.getElementById('fileShape').textContent = `${data.shape[0]} rows × ${data.shape[1]} columns`;
    
    // Display data type counts
    document.getElementById('numericCount').textContent = `${data.numeric_columns.length} numeric`;
    document.getElementById('categoricalCount').textContent = `${data.categorical_columns.length} categorical`;
    
    // Check for datetime columns (simple heuristic)
    const datetimeCount = data.columns.filter(col => 
        col.toLowerCase().includes('date') || 
        col.toLowerCase().includes('time') ||
        col.toLowerCase().includes('timestamp')
    ).length;
    document.getElementById('datetimeCount').textContent = `${datetimeCount} datetime`;
    
    document.getElementById('fileInfo').style.display = 'block';
}

function showSections() {
    document.getElementById('previewSection').style.display = 'block';
    document.getElementById('visualizationSection').style.display = 'block';
    document.querySelector('.welcome-card').style.display = 'none';
}

async function updatePreview() {
    showLoading(true);
    
    try {
        const tableOption = document.getElementById('tableOption').value;
        
        const response = await fetch('/preview', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tableOption: tableOption
            })
        });

        const data = await response.json();

        if (data.preview) {
            document.getElementById('previewTable').innerHTML = data.preview;
            document.getElementById('previewCard').style.display = 'block';
            document.getElementById('previewCard').classList.add('fade-in');
        }

        if (data.statistics) {
            document.getElementById('statsTable').innerHTML = data.statistics;
            document.getElementById('statsCard').style.display = 'block';
            document.getElementById('statsCard').classList.add('fade-in');
        }
    } catch (error) {
        showError('Preview failed: ' + error.message);
    } finally {
        showLoading(false);
    }
}

async function onChartTypeChange() {
    const chartType = document.getElementById('chartType').value;
    const chartRequirements = document.getElementById('chartRequirements');
    const requirementTitle = document.getElementById('requirementTitle');
    const requirementDescription = document.getElementById('requirementDescription');
    const requirementExample = document.getElementById('requirementExample');
    
    // Form controls
    const xColumn = document.getElementById('xColumn');
    const yColumn = document.getElementById('yColumn');
    const categoryColumn = document.getElementById('categoryColumn');
    const valueColumn = document.getElementById('valueColumn');
    const sizeColumn = document.getElementById('sizeColumn');
    const stackColumn = document.getElementById('stackColumn'); // Add stack column
    
    // Form groups
    const xColumnGroup = document.getElementById('xColumnGroup');
    const yColumnGroup = document.getElementById('yColumnGroup');
    const categoryColumnGroup = document.getElementById('categoryColumnGroup');
    const valueColumnGroup = document.getElementById('valueColumnGroup');
    const sizeColumnGroup = document.getElementById('sizeColumnGroup');
    const stackColumnGroup = document.getElementById('stackColumnGroup'); // Add stack column group
    
    // Labels and hints
    const xColumnLabel = document.getElementById('xColumnLabel');
    const yColumnLabel = document.getElementById('yColumnLabel');
    const xHint = document.getElementById('xColumnHint');
    const yHint = document.getElementById('yColumnHint');
    const visualizeBtn = document.getElementById('visualizeBtn');

    if (!chartType) {
        chartRequirements.style.display = 'none';
        resetAllControls();
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/get-compatible-columns', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                chartType: chartType
            })
        });

        const data = await response.json();

        if (data.compatible_columns) {
            const { x_columns, y_columns, requires_y, show_x, show_y, description, example } = data.compatible_columns;
            
            // Show chart requirements
            chartRequirements.style.display = 'block';
            requirementTitle.textContent = chartType.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()) + ' Requirements';
            requirementDescription.textContent = description;
            requirementExample.textContent = `Example: ${example}`;
            
            // Reset all form groups
            hideAllGroups();
            
            // Configure based on chart type
            if (['pie', 'doughnut'].includes(chartType)) {
                // Pie/Doughnut: Show category and value selectors
                categoryColumnGroup.style.display = 'block';
                valueColumnGroup.style.display = 'block';
                
                populateSelect(categoryColumn, x_columns, 'category');
                populateSelect(valueColumn, y_columns, 'values');
                
            } else if (chartType === 'bubble') {
                // Bubble: Show X, Y, and Size
                xColumnGroup.style.display = 'block';
                yColumnGroup.style.display = 'block';
                sizeColumnGroup.style.display = 'block';
                
                xColumnLabel.textContent = 'X-Axis Column (Numerical)';
                yColumnLabel.textContent = 'Y-Axis Column (Numerical)';
                
                populateSelect(xColumn, x_columns, 'X-axis');
                populateSelect(yColumn, y_columns, 'Y-axis');
                populateSelect(sizeColumn, uploadedData.numeric_columns, 'bubble size');
                
                xHint.textContent = `${x_columns.length} numerical columns available`;
                yHint.textContent = `${y_columns.length} numerical columns available`;
                
            } else if (chartType === 'stacked_bar') {
                // Stacked Bar: Show X, Y, and Stack columns
                xColumnGroup.style.display = 'block';
                yColumnGroup.style.display = 'block';
                stackColumnGroup.style.display = 'block';
                
                xColumnLabel.textContent = 'X-Axis (Primary Category)';
                yColumnLabel.textContent = 'Y-Axis (Values)';
                
                populateSelect(xColumn, x_columns, 'primary categories');
                populateSelect(yColumn, y_columns, 'values');
                populateSelect(stackColumn, uploadedData.categorical_columns, 'stack categories');
                
                xHint.textContent = `${x_columns.length} categorical columns available`;
                yHint.textContent = `${y_columns.length} numerical columns available`;
                
            } else if (chartType === 'histogram') {
                // Histogram: Only X-axis (numerical)
                xColumnGroup.style.display = 'block';
                xColumnLabel.textContent = 'Numerical Column';
                
                populateSelect(xColumn, x_columns, 'column');
                xHint.textContent = `${x_columns.length} numerical columns available`;
                
            } else if (chartType === 'heatmap') {
                // Heatmap: X and Y for correlation or categorical matrix
                xColumnGroup.style.display = 'block';
                yColumnGroup.style.display = 'block';
                
                xColumnLabel.textContent = 'X-Axis (Categories/Numbers)';
                yColumnLabel.textContent = 'Y-Axis (Categories/Numbers)';
                
                populateSelect(xColumn, x_columns, 'X-axis');
                populateSelect(yColumn, y_columns, 'Y-axis');
                
                xHint.textContent = `${x_columns.length} compatible columns available`;
                yHint.textContent = `${y_columns.length} compatible columns available`;
                
            } else if (chartType === 'box') {
                // Box plot: Can be single numerical or numerical by category
                xColumnGroup.style.display = 'block';
                if (y_columns.length > 0) {
                    yColumnGroup.style.display = 'block';
                    xColumnLabel.textContent = 'Category Column (Optional)';
                    yColumnLabel.textContent = 'Numerical Column';
                    populateSelect(yColumn, y_columns, 'numerical values');
                    yHint.textContent = `${y_columns.length} numerical columns available`;
                } else {
                    xColumnLabel.textContent = 'Numerical Column';
                }
                
                populateSelect(xColumn, x_columns, 'X-axis');
                xHint.textContent = `${x_columns.length} compatible columns available`;
                
            } else {
                // Standard X,Y charts (line, area, scatter, bar)
                if (show_x) {
                    xColumnGroup.style.display = 'block';
                    
                    // Set appropriate labels based on chart type
                    if (['line', 'area'].includes(chartType)) {
                        xColumnLabel.textContent = 'Time/Date Column';
                    } else if (chartType === 'scatter') {
                        xColumnLabel.textContent = 'X-Axis (Numerical)';
                    } else if (chartType === 'bar') {
                        xColumnLabel.textContent = 'Category Column';
                    } else {
                        xColumnLabel.textContent = 'X-Axis Column';
                    }
                    
                    populateSelect(xColumn, x_columns, 'X-axis');
                    xHint.textContent = `${x_columns.length} compatible columns available`;
                }
                
                if (show_y && requires_y) {
                    yColumnGroup.style.display = 'block';
                    yColumnLabel.textContent = 'Y-Axis (Numerical)';
                    
                    populateSelect(yColumn, y_columns, 'Y-axis');
                    yHint.textContent = `${y_columns.length} numerical columns available`;
                }
            }

            visualizeBtn.disabled = false;
        }
    } catch (error) {
        showError('Failed to get compatible columns: ' + error.message);
    } finally {
        showLoading(false);
    }
}

function populateSelect(selectElement, columns, label) {
    if (!selectElement) return; // Safety check
    
    selectElement.innerHTML = `<option value="">Select ${label}</option>`;
    columns.forEach(col => {
        const option = document.createElement('option');
        option.value = col;
        option.textContent = col;
        selectElement.appendChild(option);
    });
    selectElement.disabled = columns.length === 0;
}

function hideAllGroups() {
    document.getElementById('xColumnGroup').style.display = 'none';
    document.getElementById('yColumnGroup').style.display = 'none';
    document.getElementById('categoryColumnGroup').style.display = 'none';
    document.getElementById('valueColumnGroup').style.display = 'none';
    document.getElementById('sizeColumnGroup').style.display = 'none';
    
    // Add stack column group if it exists
    const stackColumnGroup = document.getElementById('stackColumnGroup');
    if (stackColumnGroup) {
        stackColumnGroup.style.display = 'none';
    }
}

function resetAllControls() {
    const controls = ['xColumn', 'yColumn', 'categoryColumn', 'valueColumn', 'sizeColumn', 'stackColumn'];
    controls.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            element.innerHTML = '<option value="">First select chart type</option>';
            element.disabled = true;
        }
    });
    document.getElementById('visualizeBtn').disabled = true;
    hideAllGroups();
    document.getElementById('xColumnGroup').style.display = 'block';
    document.getElementById('yColumnGroup').style.display = 'block';
}

async function updateAIRecommendations() {
    const chartType = document.getElementById('chartType').value;
    const xColumn = document.getElementById('xColumn').value;
    const yColumn = document.getElementById('yColumn').value;
    const categoryColumn = document.getElementById('categoryColumn').value;
    const valueColumn = document.getElementById('valueColumn').value;
    const sizeColumn = document.getElementById('sizeColumn').value;
    const stackColumn = document.getElementById('stackColumn')?.value; // Add stack column
    const recommendationsList = document.getElementById('aiRecommendationsList');

    if (!chartType) {
        recommendationsList.innerHTML = 'Select chart type and columns to get AI-powered recommendations';
        return;
    }

    try {
        const response = await fetch('/ai-recommendations', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                chartType: chartType,
                xColumn: xColumn || categoryColumn,
                yColumn: yColumn || valueColumn,
                sizeColumn: sizeColumn,
                stackColumn: stackColumn // Include stack column
            })
        });

        const data = await response.json();
        
        if (data.recommendations) {
            const html = data.recommendations.map(rec => `<div>${rec}</div>`).join('');
            recommendationsList.innerHTML = html;
        }
    } catch (error) {
        console.error('Failed to get AI recommendations:', error);
        recommendationsList.innerHTML = 'Failed to load AI recommendations';
    }
}

async function createVisualization() {
    const chartType = document.getElementById('chartType').value;
    const xColumn = document.getElementById('xColumn').value;
    const yColumn = document.getElementById('yColumn').value;
    const categoryColumn = document.getElementById('categoryColumn').value;
    const valueColumn = document.getElementById('valueColumn').value;
    const sizeColumn = document.getElementById('sizeColumn').value;
    const stackColumn = document.getElementById('stackColumn')?.value; // Add stack column

    // Determine final columns based on chart type
    let finalXColumn, finalYColumn, finalSizeColumn, finalStackColumn;
    
    if (['pie', 'doughnut'].includes(chartType)) {
        finalXColumn = categoryColumn;
        finalYColumn = valueColumn;
    } else if (chartType === 'bubble') {
        finalXColumn = xColumn;
        finalYColumn = yColumn;
        finalSizeColumn = sizeColumn;
    } else if (chartType === 'stacked_bar') {
        finalXColumn = xColumn;
        finalYColumn = yColumn;
        finalStackColumn = stackColumn;
    } else {
        finalXColumn = xColumn;
        finalYColumn = yColumn;
    }

    if (!chartType || (!finalXColumn && chartType !== 'gauge')) {
        showError('Please select chart type and required columns');
        return;
    }

    showLoading(true);

    try {
        const requestBody = {
            chartType: chartType,
            xColumn: finalXColumn,
            yColumn: finalYColumn
        };

        // Add optional columns if they exist
        if (finalSizeColumn) requestBody.sizeColumn = finalSizeColumn;
        if (finalStackColumn) requestBody.stackColumn = finalStackColumn;

        const response = await fetch('/visualize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();

        if (data.success && data.chart_config) {
            renderChart(data.chart_config);
            document.getElementById('chartCard').style.display = 'block';
            document.getElementById('chartCard').classList.add('fade-in');
            
            // Scroll to chart
            setTimeout(() => {
                document.getElementById('chartCard').scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' 
                });
            }, 300);
        } else {
            showError(data.error || 'Failed to create visualization');
        }
    } catch (error) {
        showError('Visualization failed: ' + error.message);
    } finally {
        showLoading(false);
    }
}

function renderChart(config) {
    const ctx = document.getElementById('myChart').getContext('2d');
    
    if (myChart) {
        myChart.destroy();
    }

    applyThemeToChart(config);
    myChart = new Chart(ctx, config);
}

function applyThemeToChart(config) {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    
    // Set theme colors
    const textColor = isDark ? '#f8f9fa' : '#212529';
    const gridColor = isDark ? '#3d4146' : '#dee2e6';
    const tickColor = isDark ? '#adb5bd' : '#6c757d';
    
    config.options.plugins = config.options.plugins || {};
    config.options.plugins.legend = config.options.plugins.legend || {};
    config.options.plugins.legend.labels = {
        color: textColor,
        font: { family: 'Inter', size: 12 }
    };

    if (config.options.scales) {
        Object.keys(config.options.scales).forEach(scale => {
            config.options.scales[scale].ticks = {
                color: tickColor,
                font: { family: 'Inter', size: 11 }
            };
            config.options.scales[scale].grid = {
                color: gridColor,
                lineWidth: 1
            };
            if (config.options.scales[scale].title) {
                config.options.scales[scale].title.color = textColor;
            }
        });
    }

    if (config.options.plugins.title) {
        config.options.plugins.title.color = textColor;
    }
}

function updateChartTheme() {
    if (myChart) {
        applyThemeToChart(myChart.config);
        myChart.update('none'); // Update without animation
    }
}

function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.style.display = show ? 'flex' : 'none';
    }
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    
    if (errorDiv && errorText) {
        errorText.textContent = message;
        errorDiv.style.display = 'flex';
        
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }
}
