from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Schedule, ChartAnalysis
from .assessment_models import FeedbackExcelUpload
import json

@login_required
def analysis(request, category, schedule_id):
    valid_categories = ['feedback', 'pre', 'post']
    if category not in valid_categories:
        return render(request, 'dashboard/assessment/analysis_error.html', {
            'error_message': 'Invalid analysis category.'
        })
    import re
    def is_english_only(text):
        return all(c.isascii() and (c.isalpha() or c.isdigit() or c in ' .,-()[]') for c in text) and any(c.isalpha() for c in text)
    def extract_english(col):
        match = re.search(r'\(([^)]+)\)', col)
        if match and is_english_only(match.group(1)):
            return match.group(1).strip()
        if is_english_only(col):
            return col.strip()
        if '-' in col:
            parts = [p.strip() for p in col.split('-')]
            for part in parts:
                if is_english_only(part):
                    return part
        return None
    try:
        schedule = get_object_or_404(Schedule, id=schedule_id)
        training = schedule.training
        improvement_rates = None
        idi_data = None
        
        # Initialize variables
        grouped_improvement_json = '{}'
        normalized_gain_json = '{}'
        normalized_gain_data = None
        
        if category in ['pre', 'post']:
            pre_upload = FeedbackExcelUpload.objects.filter(training=training, schedule=schedule, category='pre').order_by('-uploaded_at').first()
            post_upload = FeedbackExcelUpload.objects.filter(training=training, schedule=schedule, category='post').order_by('-uploaded_at').first()
            if pre_upload and post_upload and pre_upload.file and post_upload.file:
                import pandas as pd
                pre_df = pd.read_excel(pre_upload.file.path)
                post_df = pd.read_excel(post_upload.file.path)
                # Robustly find Pers No. column (English only, case-insensitive)
                pers_no_col = None
                for col in pre_df.columns:
                    if 'pers no' in col.lower():
                        pers_no_col = col
                        break
                if pers_no_col:
                    print("Columns in pre_df:", list(pre_df.columns))
                    print("Columns in post_df:", list(post_df.columns))
                    print("pers_no_col:", pers_no_col)
                    
                    # Force string conversion for Pers No. column to avoid merge issues
                    pre_df[pers_no_col] = pre_df[pers_no_col].astype(str)
                    post_df[pers_no_col] = post_df[pers_no_col].astype(str)
                    
                    # Use new standardized naming convention for questions and points
                    from .views import detect_question_and_points_columns, extract_question_text
                    pre_questions, pre_points = detect_question_and_points_columns(pre_df.columns)
                    post_questions, post_points = detect_question_and_points_columns(post_df.columns)
                    
                    # Find matching question columns between pre and post files
                    matching_questions = [q for q in pre_questions if q in post_questions]
                    
                    print("Pre questions:", pre_questions)
                    print("Post questions:", post_questions)
                    print("Matching questions:", matching_questions)
                    
                    # Calculate improvement rates (existing logic)
                    if matching_questions:
                        # Merge pre and post on Pers No.
                        merged = pd.merge(pre_df[[pers_no_col] + matching_questions], \
                                        post_df[[pers_no_col] + matching_questions], \
                                        on=pers_no_col, suffixes=('_pre', '_post'))
                        
                        improvement_rates = {}
                        for question in matching_questions:
                            pre_scores = merged[f'{question}_pre']
                            post_scores = merged[f'{question}_post']
                            valid = pre_scores.notnull() & post_scores.notnull()
                            improvement_count = ((post_scores[valid] > pre_scores[valid])).sum()
                            total_students = valid.sum()
                            rate = (improvement_count / total_students * 100) if total_students > 0 else 0
                            
                            # Use the question text (without "Que -" prefix) as the key
                            question_text = extract_question_text(question)
                            improvement_rates[question_text] = round(rate, 2)
                    
                    # Calculate IDI (Item Difficulty Index) - NEW ADDITION
                    matching_points = [p for p in pre_points if p in post_points]
                    if matching_points:
                        idi_data = {}
                        
                        for points_col in matching_points:
                            # Get the corresponding question text for display
                            question_text = extract_question_text(points_col.replace('Points -', 'Que -'))
                            
                            # Use the same logic as improvement chart - only count students in both files
                            # Get the corresponding question column for merging
                            question_col = points_col.replace('Points -', 'Que -')
                            
                            # Merge pre and post data for this specific question
                            merged_question = pd.merge(
                                pre_df[[pers_no_col, points_col]], \
                                post_df[[pers_no_col, points_col]], \
                                on=pers_no_col, suffixes=('_pre', '_post')
                            )
                            
                            # Calculate Pre-test IDI using only students in both files
                            pre_scores = merged_question[f'{points_col}_pre']
                            pre_valid = pre_scores.notnull()
                            pre_correct = (pre_scores[pre_valid] == 1).sum()  # Count students who scored 1 (correct)
                            pre_total = pre_valid.sum()  # Count students with valid scores in both files
                            pre_idi = (pre_correct / pre_total * 100) if pre_total > 0 else 0
                            
                            # Calculate Post-test IDI using only students in both files
                            post_scores = merged_question[f'{points_col}_post']
                            post_valid = post_scores.notnull()
                            post_correct = (post_scores[post_valid] == 1).sum()  # Count students who scored 1 (correct)
                            post_total = post_valid.sum()  # Count students with valid scores in both files
                            post_idi = (post_correct / post_total * 100) if post_total > 0 else 0
                            
                            # Store IDI data
                            idi_data[question_text] = {
                                'pre_idi': round(pre_idi, 2),
                                'post_idi': round(post_idi, 2),
                                'pre_correct': int(pre_correct),
                                'pre_total': int(pre_total),
                                'post_correct': int(post_correct),
                                'post_total': int(post_total),
                                'improvement': round(post_idi - pre_idi, 2)
                            }
                        
                        # Determine color scheme based on IDI patterns
                        def get_idi_status(pre_idi, post_idi):
                            if post_idi > 70:
                                return 'good'  # Green: >70% Good (Well understood)
                            elif post_idi >= 50:
                                return 'moderate'  # Yellow: 50-70% Moderate
                            else:
                                return 'needs_attention'  # Red: <50% Poor understanding (Needs attention)
                        
                        # Add status to each question
                        for question, data in idi_data.items():
                            data['status'] = get_idi_status(data['pre_idi'], data['post_idi'])
                    
                    # Find Total Points column in both files (existing logic)
                    total_points_col_pre = None
                    total_points_col_post = None
                    for col in pre_df.columns:
                        if str(col).strip().lower() == 'total points':
                            total_points_col_pre = col
                            break
                    for col in post_df.columns:
                        if str(col).strip().lower() == 'total points':
                            total_points_col_post = col
                            break
                    employee_name_col = None
                    for col in pre_df.columns:
                        if str(col).strip().lower() == 'employee name':
                            employee_name_col = col
                            break 
                    columns_to_merge_pre = [pers_no_col, total_points_col_pre]
                    if employee_name_col:
                        columns_to_merge_pre.append(employee_name_col)    
                    merged = pd.merge(
                        pre_df[columns_to_merge_pre],
                        post_df[[pers_no_col, total_points_col_post]],
                        on=pers_no_col,
                        suffixes=('_pre', '_post')   
                    )
                    pre_scores = merged[f'{total_points_col_pre}_pre']
                    post_scores = merged[f'{total_points_col_post}_post']
                    valid = pre_scores.notnull() & post_scores.notnull()
                    improvement_count = ((post_scores[valid] > pre_scores[valid])).sum()
                    total_students = valid.sum()
                    rate = (improvement_count / total_students * 100) if total_students > 0 else 0
                    print(f"Improvement Count (Total Points): {improvement_count}")
                    print(f"Total Valid Students (Total Points): {total_students}")
                    print(f"Improvement Rate (Total Points): {rate:.2f}%")
                    if employee_name_col and employee_name_col in merged.columns:
                        print("Employee Names of Valid Students:")
                        print(merged.loc[valid, employee_name_col].tolist())
                        # Print valid पदनाम क्रमांक (Pers No.)
                        if 'पदनाम क्रमांक (Pers No.)' in merged.columns:
                            print("Valid पदनाम क्रमांक (Pers No.) of Valid Students:")
                            print(merged.loc[valid, 'पदनाम क्रमांक (Pers No.)'].tolist())
                    else:
                        print("Employee Name column not found in merged data.")
                    improvement_rates = {'Total Points': round(rate, 2)} 
                    
                    # IDI chart logic ends here. Now add grouped improvement logic for Total Points (date-wise and combined)
                    import pandas as pd
                    from datetime import datetime
                    import re as _re
                    import json as _json

                    grouped_improvement = {}

                    # Find Start time columns in pre and post
                    start_time_col_pre = None
                    start_time_col_post = None
                    for col in pre_df.columns:
                        if 'start time' in col.lower():
                            start_time_col_pre = col
                            break
                    for col in post_df.columns:
                        if 'start time' in col.lower():
                            start_time_col_post = col
                            break

                    if (
                        pers_no_col and total_points_col_pre and total_points_col_post
                        and start_time_col_pre and start_time_col_post
                    ):
                        # Ensure string type for merge
                        pre_df[pers_no_col] = pre_df[pers_no_col].astype(str)
                        post_df[pers_no_col] = post_df[pers_no_col].astype(str)

                        # Robust date extraction
                        def extract_date(val):
                            if pd.isnull(val):
                                return None
                            if isinstance(val, pd.Timestamp):
                                return val.strftime("%d-%m-%Y")
                            try:
                                s = str(val).strip()
                                s = _re.sub(r'\s+', ' ', s)
                                s = s.strip()
                                dt = datetime.strptime(s, "%d-%m-%Y %I:%M:%S %p")
                                return dt.strftime("%d-%m-%Y")
                            except Exception:
                                try:
                                    date_part = s.split()[0]
                                    dt = datetime.strptime(date_part, "%d-%m-%Y")
                                    return dt.strftime("%d-%m-%Y")
                                except Exception:
                                    return None

                        pre_df['__date'] = pre_df[start_time_col_pre].apply(extract_date)
                        post_df['__date'] = post_df[start_time_col_post].apply(extract_date)

                        # Combined
                        faculty_name_col = None
                        for col in pre_df.columns:
                            if 'faculty name' in col.lower():
                                faculty_name_col = col
                                break
                        merged_combined = pd.merge(
                            pre_df[[pers_no_col, total_points_col_pre] + ([faculty_name_col] if faculty_name_col else [])],
                            post_df[[pers_no_col, total_points_col_post]],
                            on=pers_no_col,
                            suffixes=('_pre', '_post')
                        )
                        pre_scores = merged_combined[f'{total_points_col_pre}_pre']
                        post_scores = merged_combined[f'{total_points_col_post}_post']
                        valid = pre_scores.notnull() & post_scores.notnull()
                        improvement_count = ((post_scores[valid] > pre_scores[valid])).sum()
                        total_students = valid.sum()
                        rate = (improvement_count / total_students * 100) if total_students > 0 else 0
                        # Faculty names for combined
                        if faculty_name_col and faculty_name_col in merged_combined.columns:
                            faculty_names_combined = merged_combined.loc[valid, faculty_name_col].dropna().unique().tolist()
                        else:
                            faculty_names_combined = []
                        grouped_improvement['Combined'] = {
                            'rate': round(rate, 2),
                            'valid_students': int(total_students),
                            'faculty_names': faculty_names_combined,
                            'date': 'Combined',
                            'improvement_count': int(improvement_count),
                            'total_students': int(total_students)
                        }
                        # Date-wise
                        all_dates = sorted(set(pre_df['__date'].dropna()) | set(post_df['__date'].dropna()))
                        for date in all_dates:
                            pre_sub = pre_df[pre_df['__date'] == date]
                            post_sub = post_df[post_df['__date'] == date]
                            merged = pd.merge(
                                pre_sub[[pers_no_col, total_points_col_pre] + ([faculty_name_col] if faculty_name_col else [])],
                                post_sub[[pers_no_col, total_points_col_post]],
                                on=pers_no_col,
                                suffixes=('_pre', '_post')
                            )
                            pre_scores = merged[f'{total_points_col_pre}_pre']
                            post_scores = merged[f'{total_points_col_post}_post']
                            valid = pre_scores.notnull() & post_scores.notnull()
                            improvement_count = ((post_scores[valid] > pre_scores[valid])).sum()
                            total_students = valid.sum()
                            # Faculty names for this date
                            if faculty_name_col and faculty_name_col in merged.columns:
                                faculty_names = merged.loc[valid, faculty_name_col].dropna().unique().tolist()
                            else:
                                faculty_names = []
                            if total_students > 0:
                                rate = (improvement_count / total_students * 100)
                                grouped_improvement[date] = {
                                    'rate': round(rate, 2),
                                    'valid_students': int(total_students),
                                    'faculty_names': faculty_names,
                                    'date': date,
                                    'improvement_count': int(improvement_count),
                                    'total_students': int(total_students)
                                }

                        grouped_improvement_json = _json.dumps(grouped_improvement)
                        
                        # NEW: Normalized Gain (Hake's Gain) Calculation (NEW FORMULA)
                        normalized_gain_data = {}
                        
                        # --- Combined Analysis ---
                        # Use all valid students across all dates
                        merged_combined = pd.merge(
                            pre_df[[pers_no_col, total_points_col_pre]],
                            post_df[[pers_no_col, total_points_col_post]],
                            on=pers_no_col,
                            suffixes=('_pre', '_post')
                        )
                        pre_scores_combined = merged_combined[f'{total_points_col_pre}_pre']
                        post_scores_combined = merged_combined[f'{total_points_col_post}_post']
                        valid_combined = pre_scores_combined.notnull() & post_scores_combined.notnull()
                        valid_pre_combined = pre_scores_combined[valid_combined]
                        valid_post_combined = post_scores_combined[valid_combined]
                        total_students_combined = valid_combined.sum()
                        if total_students_combined > 0:
                            avg_pre_combined = valid_pre_combined.mean()
                            avg_post_combined = valid_post_combined.mean()
                            pre_max_combined = valid_pre_combined.max() if not valid_pre_combined.empty else 0
                            post_max_combined = valid_post_combined.max() if not valid_post_combined.empty else 0
                            norm_pre_combined = avg_pre_combined / pre_max_combined if pre_max_combined > 0 else 0
                            norm_post_combined = avg_post_combined / post_max_combined if post_max_combined > 0 else 0
                            denom = 1 - norm_pre_combined
                            if pre_max_combined == 0 or post_max_combined == 0 or denom == 0:
                                gain_combined = 0
                            else:
                                gain_combined = (norm_post_combined - norm_pre_combined) / denom
                            normalized_gain_data['Combined'] = {
                                'gain': round(gain_combined, 4),
                                'avg_pre_test': round(avg_pre_combined, 2),
                                'avg_post_test': round(avg_post_combined, 2),
                                'pre_max': float(pre_max_combined),
                                'post_max': float(post_max_combined),
                                'norm_pre': round(norm_pre_combined, 4),
                                'norm_post': round(norm_post_combined, 4),
                                'valid_students': int(total_students_combined)
                            }
                        
                        # --- Date-wise Analysis ---
                        for date in all_dates:
                            pre_sub = pre_df[pre_df['__date'] == date]
                            post_sub = post_df[post_df['__date'] == date]
                            merged = pd.merge(
                                pre_sub[[pers_no_col, total_points_col_pre]],
                                post_sub[[pers_no_col, total_points_col_post]],
                                on=pers_no_col,
                                suffixes=('_pre', '_post')
                            )
                            pre_scores = merged[f'{total_points_col_pre}_pre']
                            post_scores = merged[f'{total_points_col_post}_post']
                            valid = pre_scores.notnull() & post_scores.notnull()
                            valid_pre = pre_scores[valid]
                            valid_post = post_scores[valid]
                            total_students = valid.sum()
                            if total_students > 0:
                                avg_pre = valid_pre.mean()
                                avg_post = valid_post.mean()
                                pre_max = valid_pre.max() if not valid_pre.empty else 0
                                post_max = valid_post.max() if not valid_post.empty else 0
                                norm_pre = avg_pre / pre_max if pre_max > 0 else 0
                                norm_post = avg_post / post_max if post_max > 0 else 0
                                denom = 1 - norm_pre
                                if pre_max == 0 or post_max == 0 or denom == 0:
                                    gain = 0
                                else:
                                    gain = (norm_post - norm_pre) / denom
                                normalized_gain_data[date] = {
                                    'gain': round(gain, 4),
                                    'avg_pre_test': round(avg_pre, 2),
                                    'avg_post_test': round(avg_post, 2),
                                    'pre_max': float(pre_max),
                                    'post_max': float(post_max),
                                    'norm_pre': round(norm_pre, 4),
                                    'norm_post': round(norm_post, 4),
                                    'valid_students': int(total_students)
                                }
                        
                        normalized_gain_json = _json.dumps(normalized_gain_data)
                    else:
                        grouped_improvement_json = '{}'
                        normalized_gain_json = '{}'
        
        excel_upload = FeedbackExcelUpload.objects.filter(
            training=training,
            schedule=schedule,
            category=category,
        ).order_by('-uploaded_at').first()
        if not excel_upload or not excel_upload.file:
            return render(request, 'dashboard/assessment/analysis_error.html', {
                'error_message': f'No Excel file found for {category} analysis for this schedule.'
            })
        file_path = excel_upload.file.path
        import pandas as pd
        df = pd.read_excel(file_path)
        original_columns = list(df.columns)
        
        missing_assessment_table = []
        if category in ['pre', 'post'] and pre_upload and post_upload and pre_upload.file and post_upload.file:
           pre_df = pd.read_excel(pre_upload.file.path)
           post_df = pd.read_excel(post_upload.file.path)

           def find_col(df, search):
               for col in df.columns:
                   if search in col.lower().replace(' ', ''):
                       return col
               return None

           missing_assessment_table = []
           pers_no_col_pre = find_col(pre_df, 'persno')
           emp_name_col_pre = find_col(pre_df, 'employeename')
           pers_no_col_post = find_col(post_df, 'persno')
           emp_name_col_post = find_col(post_df, 'employeename')

           pre_pnos = set(pre_df[pers_no_col_pre].dropna().astype(str)) if pers_no_col_pre else set()
           post_pnos = set(post_df[pers_no_col_post].dropna().astype(str)) if pers_no_col_post else set()
           only_in_pre = pre_pnos - post_pnos
           only_in_post = post_pnos - pre_pnos
           sr_no = 1
           # Students who missed post assessment (look up name in pre)
           for pno in only_in_pre:
               row = pre_df[pre_df[pers_no_col_pre].astype(str) == pno].iloc[0] if pers_no_col_pre else None
               employee_name = row.get(emp_name_col_pre, '') if row is not None and emp_name_col_pre else ''
               missing_assessment_table.append({
                   'sr_no': sr_no,
                   'pers_no': pno,
                   'employee_name': employee_name if pd.notnull(employee_name) else '',
                   'missing': 'Post Assessment'
               })
               sr_no += 1
           # Students who missed pre assessment (look up name in post)
           for pno in only_in_post:
               row = post_df[post_df[pers_no_col_post].astype(str) == pno].iloc[0] if pers_no_col_post else None
               employee_name = row.get(emp_name_col_post, '') if row is not None and emp_name_col_post else ''
               missing_assessment_table.append({
                   'sr_no': sr_no,
                   'pers_no': pno,
                   'employee_name': employee_name if pd.notnull(employee_name) else '',
                   'missing': 'Pre Assessment'
               })
               sr_no += 1
        # Use new standardized naming convention
        from .views import detect_question_and_points_columns, extract_question_text, extract_points_text
        questions, points = detect_question_and_points_columns(df.columns)
        
        # Extract question and points texts for display
        question_texts = [extract_question_text(q) for q in questions]
        points_texts = [extract_points_text(p) for p in points]
        
        # Create English columns list (for backward compatibility)
        english_columns = question_texts + points_texts
        
        data_rows = df.to_dict(orient='records') if not df.empty else []
        total_rows = int(len(df))
        total_columns = int(len(df.columns))
        column_info = []
        for col in df.columns:
            col_data = df[col].dropna()
            column_info.append({
                'name': str(col),
                'type': str(df[col].dtype),
                'non_null_count': int(len(col_data)),
                'null_count': int(df[col].isnull().sum()),
                'unique_values': int(df[col].nunique()) if df[col].dtype in ['object', 'string'] else None
            })
        data_quality = {
            'total_cells': int(total_rows * total_columns),
            'null_cells': int(df.isnull().sum().sum()),
            'completeness_rate': float(((total_rows * total_columns) - df.isnull().sum().sum()) / (total_rows * total_columns) * 100)
        }
        chart_data = {
            'improvement_rates': improvement_rates,
            'idi_data': idi_data
        }
        dropdown_options = [{'label': col, 'value': col} for col in english_columns]
        context = {
            'schedule': schedule,
            'category': category,
            'missing_assessment_table': missing_assessment_table,
            'improvement_rates': improvement_rates,
            'improvement_rates_json': json.dumps(improvement_rates) if improvement_rates else '{}',  # Properly serialize for JavaScript
            'show_improvement_chart': improvement_rates is not None,  # Show chart if improvement rates are calculated
            'idi_data': idi_data,
            'idi_data_json': json.dumps(idi_data) if idi_data else '{}',  # NEW: IDI data
            'show_idi_chart': idi_data is not None,  # NEW: Show IDI chart if data available
            'excel_info': {
                'original_name': excel_upload.original_name,
                'filename': excel_upload.file.name,
                'uploaded_at': excel_upload.uploaded_at,
            },
            'analysis_data': {
                'total_rows': total_rows,
                'total_columns': total_columns,
                'column_info': column_info,
                'data_quality': data_quality,
                'chart_data': chart_data
            },
            'original_columns': original_columns,
            'english_columns': english_columns,
            'dropdown_options': dropdown_options,
            'data_rows': data_rows,
            'grouped_improvement_json': grouped_improvement_json,
            'normalized_gain_json': normalized_gain_json,
            'show_normalized_gain_chart': normalized_gain_data is not None and len(normalized_gain_data) > 0,
        }
        # Save improvement chart analysis (keep only latest per training, schedule, type)
        try:
            ChartAnalysis.objects.filter(
                training=training,
                schedule=schedule,
                analysis_type='improvement'
            ).delete()
            ChartAnalysis.objects.create(
                training=training,
                schedule=schedule,
                analysis_type='improvement',
                input_files={
                    'pre': pre_upload.file.name if pre_upload and pre_upload.file else None,
                    'post': post_upload.file.name if post_upload and post_upload.file else None,
                },
                chart_data=grouped_improvement,
                run_by=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                notes='Auto-saved from analysis view'
            )
        except Exception as e:
            print('Error saving improvement analysis:', e)
        # Save idi chart analysis (keep only latest per training, schedule, type)
        try:
            if idi_data:
                ChartAnalysis.objects.filter(
                    training=training,
                    schedule=schedule,
                    analysis_type='idi'
                ).delete()
                ChartAnalysis.objects.create(
                    training=training,
                    schedule=schedule,
                    analysis_type='idi',
                    input_files={
                        'pre': pre_upload.file.name if pre_upload and pre_upload.file else None,
                        'post': post_upload.file.name if post_upload and post_upload.file else None,
                    },
                    chart_data=idi_data,
                    run_by=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                    notes='Auto-saved from analysis view'
                )
        except Exception as e:
            print('Error saving idi analysis:', e)
        # Save normalized gain chart analysis (keep only latest per training, schedule, type)
        try:
            if normalized_gain_data:
                ChartAnalysis.objects.filter(
                    training=training,
                    schedule=schedule,
                    analysis_type='normalized_gain'
                ).delete()
                ChartAnalysis.objects.create(
                    training=training,
                    schedule=schedule,
                    analysis_type='normalized_gain',
                    input_files={
                        'pre': pre_upload.file.name if pre_upload and pre_upload.file else None,
                        'post': post_upload.file.name if post_upload and post_upload.file else None,
                    },
                    chart_data=normalized_gain_data,
                    run_by=request.user if hasattr(request, 'user') and request.user.is_authenticated else None,
                    notes='Auto-saved from analysis view'
                )
        except Exception as e:
            print('Error saving normalized gain analysis:', e)
        # Robust feedback column detection and debug for feedback category
        detected_feedback_columns = None
        final_weighted_average = None
        faculty_training_ratings = []
        if category == 'feedback':
            def clean_col(col):
                return str(col).replace('\xa0', ' ').replace('\u200c', '').strip()
            f1_col = next((c for c in df.columns if clean_col(c).startswith('F1Que')), None)
            f2_col = next((c for c in df.columns if clean_col(c).startswith('F2Que')), None)
            f3_col = next((c for c in df.columns if clean_col(c).startswith('F3Que')), None)
            f4_col = next((c for c in df.columns if clean_col(c).startswith('F4Que')), None)
            if not (f1_col and f2_col and f3_col and f4_col):
                f1_col = f1_col or next((c for c in df.columns if clean_col(c) == 'F1'), None)
                f2_col = f2_col or next((c for c in df.columns if clean_col(c) == 'F2'), None)
                f3_col = f3_col or next((c for c in df.columns if clean_col(c) == 'F3'), None)
                f4_col = f4_col or next((c for c in df.columns if clean_col(c) == 'F4'), None)
            detected_feedback_columns = {
                'f1_col': f1_col,
                'f2_col': f2_col,
                'f3_col': f3_col,
                'f4_col': f4_col,
            }
            valid_row_count = 0
            weighted_scores = []
            if f1_col and f2_col and f3_col and f4_col:
                for _, row in df.iterrows():
                    try:
                        f1 = float(row[f1_col]) if pd.notnull(row[f1_col]) else None
                        f2 = float(row[f2_col]) if pd.notnull(row[f2_col]) else None
                        f3 = float(row[f3_col]) if pd.notnull(row[f3_col]) else None
                        f4 = float(row[f4_col]) if pd.notnull(row[f4_col]) else None
                        if None not in (f1, f2, f3, f4):
                            weighted = (f1 * 0.30) + (f2 * 0.25) + (f3 * 0.25) + (f4 * 0.20)
                            weighted_scores.append(weighted)
                            valid_row_count += 1
                    except Exception:
                        continue
                if weighted_scores:
                    final_weighted_average = round(sum(weighted_scores) / len(weighted_scores), 2)
            # For the chart: show a single bar for this training
            faculty_training_ratings = []
            if final_weighted_average is not None:
                faculty_training_ratings.append({
                    'training': str(schedule.training.training_name),
                    'date': str(schedule.date),
                    'score': final_weighted_average
                })
        context['detected_feedback_columns'] = detected_feedback_columns
        context['final_weighted_average'] = final_weighted_average
        context['faculty_training_ratings_json'] = json.dumps(faculty_training_ratings)
        return render(request, 'dashboard/assessment/feedback_analysis.html', context)
    except Exception as e:
        messages.error(request, f'Error analyzing Excel file: {str(e)}')
        return redirect('dashboard:feedback_form') 