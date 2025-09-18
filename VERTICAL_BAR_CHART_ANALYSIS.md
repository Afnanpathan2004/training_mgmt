# Vertical Bar Chart Analysis - Pre-Assessment Analysis Page

## Overview
The vertical bar chart in the pre-assessment analysis page (`/dashboard/analysis/pre/578/`) displays **topic-wise improvement rates** by comparing pre-training and post-training assessment scores. This document provides a complete breakdown of how the chart works, from data processing to frontend rendering.

## URL Structure and Routing

### URL Pattern
```
/dashboard/analysis/pre/{schedule_id}/
```

### Route Definition
```python
# training_mgmt/dashboard/urls.py
path('analysis/<str:category>/<int:schedule_id>/', views.analysis, name='analysis'),
```

### View Function
The URL is handled by the `analysis()` function in `views.py` with parameters:
- `category`: 'pre' (for pre-assessment analysis)
- `schedule_id`: 578 (the specific schedule being analyzed)

## Backend Data Processing

### 1. View Function: `analysis(request, category, schedule_id)`

#### Step 1: Validation and Setup
```python
@login_required
def analysis(request, category, schedule_id):
    valid_categories = ['feedback', 'pre', 'post']
    if category not in valid_categories:
        return render(request, 'dashboard/assessment/analysis_error.html', {
            'error_message': 'Invalid analysis category.'
        })
```

#### Step 2: Schedule and Training Retrieval
```python
schedule = get_object_or_404(Schedule, id=schedule_id)
training = schedule.training
```

#### Step 3: Excel File Retrieval
```python
if category in ['pre', 'post']:
    pre_upload = FeedbackExcelUpload.objects.filter(
        training=training, 
        schedule=schedule, 
        category='pre'
    ).order_by('-uploaded_at').first()
    
    post_upload = FeedbackExcelUpload.objects.filter(
        training=training, 
        schedule=schedule, 
        category='post'
    ).order_by('-uploaded_at').first()
```

#### Step 4: Data Processing for Improvement Rates
```python
if pre_upload and post_upload and pre_upload.file and post_upload.file:
    import pandas as pd
    pre_df = pd.read_excel(pre_upload.file.path)
    post_df = pd.read_excel(post_upload.file.path)
    
    # Find Pers No. column for student identification
    pers_no_col = None
    for col in pre_df.columns:
        if 'pers no' in col.lower():
            pers_no_col = col
            break
```

#### Step 5: Column Detection and Matching
```python
# Use standardized naming convention for questions and points
pre_questions, pre_points = detect_question_and_points_columns(pre_df.columns)
post_questions, post_points = detect_question_and_points_columns(post_df.columns)

# Find matching question columns between pre and post files
matching_questions = [q for q in pre_questions if q in post_questions]
```

#### Step 6: Data Merging and Improvement Calculation
```python
# Merge pre and post on Pers No.
merged = pd.merge(
    pre_df[[pers_no_col] + matching_questions], 
    post_df[[pers_no_col] + matching_questions], 
    on=pers_no_col, 
    suffixes=('_pre', '_post')
)

improvement_rates = {}
for question in matching_questions:
    pre_scores = merged[f'{question}_pre']
    post_scores = merged[f'{question}_post']
    
    # Find valid entries (non-null in both pre and post)
    valid = pre_scores.notnull() & post_scores.notnull()
    
    # Count students who improved (post > pre)
    improvement_count = ((post_scores[valid] > pre_scores[valid])).sum()
    
    # Total students with valid data
    total_students = valid.sum()
    
    # Calculate improvement rate
    rate = (improvement_count / total_students * 100) if total_students > 0 else 0
    
    # Use the question text (without "Que -" prefix) as the key
    question_text = extract_question_text(question)
    improvement_rates[question_text] = round(rate, 2)
```

### 2. Helper Functions

#### Column Detection
```python
def detect_question_and_points_columns(columns):
    """Detect question and points columns using standardized naming convention"""
    questions = []
    points = []
    
    for col in columns:
        col_str = str(col).strip()
        if col_str.startswith('Que -'):
            questions.append(col)
        elif col_str.startswith('Points -'):
            points.append(col)
    
    return questions, points
```

#### Question Text Extraction
```python
def extract_question_text(column_name):
    """Extract the question text from a column name"""
    col_str = str(column_name).strip()
    if col_str.startswith('Que -'):
        return col_str[5:].strip()  # Remove "Que -" prefix
    return col_str
```

### 3. Context Data Preparation
```python
context = {
    'schedule': schedule,
    'category': category,
    'improvement_rates': improvement_rates,
    'improvement_rates_json': json.dumps(improvement_rates) if improvement_rates else '{}',
    'show_improvement_chart': improvement_rates is not None,
    'excel_info': {
        'original_name': excel_upload.original_name,
        'filename': excel_upload.file.name,
        'uploaded_at': excel_upload.uploaded_at,
    },
    # ... other context data
}
```

## Frontend Chart Rendering

### 1. Template: `feedback_analysis.html`

#### Chart Container
```html
{% if show_improvement_chart %}
<div style="max-width: 900px; margin: 40px auto 24px auto; background: #fff; padding: 32px; border-radius: 12px; box-shadow: 0 2px 12px rgba(0,0,0,0.07);">
    <h3 style="text-align: center; margin-bottom: 24px;">Topic-wise Improvement Rate (%)</h3>
    <canvas id="improvementBarChart" width="800" height="400"></canvas>
</div>
```

#### Data Storage
```html
<!-- Store improvement rates data in a data attribute -->
<div id="improvement-data" 
     data-improvement-rates="{{ improvement_rates_json }}" 
     style="display: none;"></div>
```

### 2. JavaScript Chart Creation

#### Data Extraction
```javascript
try {
    // Get improvement rates from data attribute
    const dataElement = document.getElementById('improvement-data');
    const improvementRatesText = dataElement.getAttribute('data-improvement-rates');
    const improvementRates = JSON.parse(improvementRatesText);
    
    const topics = Object.keys(improvementRates);
    const rates = Object.values(improvementRates);
    
    console.log('Improvement rates data:', improvementRates);
    console.log('Topics:', topics);
    console.log('Rates:', rates);
```

#### Chart.js Configuration
```javascript
const ctx = document.getElementById('improvementBarChart').getContext('2d');
const barChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: topics,
        datasets: [{
            label: 'Improvement Rate (%)',
            data: rates,
            backgroundColor: 'rgba(54, 162, 235, 0.7)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false },
            title: {
                display: true,
                text: 'Topic-wise Improvement Rate (%)'
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return context.parsed.y + '%';
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                title: {
                    display: true,
                    text: 'Improvement Rate (%)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Topic/Question'
                },
                ticks: {
                    autoSkip: false,
                    maxRotation: 60,
                    minRotation: 30
                }
            }
        }
    }
});
```

## Data Flow Summary

### 1. Request Processing
```
User clicks "View Analysis" → URL: /dashboard/analysis/pre/578/
→ Django routes to analysis() function
→ Validates category and schedule_id
```

### 2. Data Retrieval
```
→ Retrieves Schedule and Training objects
→ Finds pre and post assessment Excel files
→ Loads Excel files using pandas
```

### 3. Data Processing
```
→ Identifies Pers No. column for student matching
→ Detects question columns using naming convention
→ Matches questions between pre and post files
→ Merges data on Pers No. with suffixes
```

### 4. Improvement Rate Calculation
```
For each matching question:
→ Extracts pre and post scores
→ Filters valid entries (non-null in both)
→ Counts students where post_score > pre_score
→ Calculates: (improved_students / total_valid_students) × 100
→ Rounds to 2 decimal places
```

### 5. Template Rendering
```
→ Passes improvement_rates to template
→ Serializes data as JSON for JavaScript
→ Renders chart container and data storage
```

### 6. Frontend Chart Creation
```
→ Extracts data from HTML data attribute
→ Parses JSON improvement rates
→ Creates Chart.js bar chart
→ Configures styling and interactions
```

## Key Features

### 1. Data Validation
- **File Existence**: Checks if both pre and post files exist
- **Column Detection**: Robust Pers No. column identification
- **Question Matching**: Only processes questions present in both files
- **Data Integrity**: Handles missing/null values gracefully

### 2. Calculation Logic
- **Improvement Definition**: post_score > pre_score
- **Valid Data**: Only students with scores in both assessments
- **Percentage Calculation**: (improved_count / total_valid) × 100
- **Rounding**: Results rounded to 2 decimal places

### 3. Chart Customization
- **Responsive Design**: Adapts to screen size
- **Color Scheme**: Blue theme with transparency
- **Axis Configuration**: Y-axis 0-100%, X-axis topic names
- **Tooltips**: Shows percentage values on hover
- **Text Rotation**: X-axis labels rotated for readability

### 4. Error Handling
- **JavaScript Try-Catch**: Graceful error handling in chart creation
- **Console Logging**: Debug information for troubleshooting
- **Fallback Display**: Shows error messages if chart fails

## Example Data Structure

### Input Excel Files
**Pre-Assessment File:**
```
Pers No. | Que - Safety Procedures | Que - Equipment Operation
12345    | 3                      | 4
12346    | 4                      | 2
12347    | 2                      | 5
```

**Post-Assessment File:**
```
Pers No. | Que - Safety Procedures | Que - Equipment Operation
12345    | 4                      | 4
12346    | 4                      | 3
12347    | 3                      | 5
```

### Calculated Improvement Rates
```python
improvement_rates = {
    'Safety Procedures': 66.67,  # 2 out of 3 students improved
    'Equipment Operation': 33.33  # 1 out of 3 students improved
}
```

### JSON Output
```json
{
    "Safety Procedures": 66.67,
    "Equipment Operation": 33.33
}
```

### Chart Display
- **X-axis**: "Safety Procedures", "Equipment Operation"
- **Y-axis**: 0-100% scale
- **Bars**: Blue bars showing 66.67% and 33.33% respectively

## Performance Considerations

### 1. Data Processing
- **Pandas Operations**: Efficient vectorized operations
- **Memory Management**: Processes files in chunks if large
- **Column Detection**: Optimized column matching algorithms

### 2. Frontend Performance
- **Chart.js**: Efficient canvas-based rendering
- **Data Serialization**: JSON for fast JavaScript parsing
- **Responsive Design**: Optimized for different screen sizes

### 3. Scalability
- **File Size Limits**: Handles Excel files up to 10MB
- **Student Count**: Efficiently processes hundreds of students
- **Question Count**: Scales with number of assessment topics

## Usage Workflow

### 1. Upload Process
```
User → Upload Pre-assessment Excel → System stores file
User → Upload Post-assessment Excel → System stores file
```

### 2. Analysis Process
```
User → Click "View Analysis" → System loads both files
System → Merges data on Pers No. → Calculates improvement rates
System → Renders bar chart → Displays results
```

### 3. Chart Interaction
```
User → Hover over bars → Tooltips show exact percentages
User → Resize window → Chart adapts responsively
User → Navigate page → Chart maintains state
```

## Summary

The vertical bar chart in the pre-assessment analysis page provides a **quantitative visualization** of training effectiveness by:

1. **Comparing pre and post scores** for each topic/question
2. **Calculating improvement rates** as percentages of students who improved
3. **Displaying results** in an interactive, responsive bar chart
4. **Handling edge cases** like missing data and file errors
5. **Providing insights** into which topics showed the most improvement

This approach gives training administrators a clear, data-driven view of training effectiveness across different topics and helps identify areas where training was most/least effective. 