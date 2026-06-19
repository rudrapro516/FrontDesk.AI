import pandas as pd
import streamlit as st
import re
import os

def normalize_timing(time_str):
    if pd.isna(time_str) or str(time_str).strip() in ['nan', 'Not specified', '']:
        return "Not specified"
    
    t = str(time_str).lower()
    t_clean = re.sub(r'[^a-z0-9]', '', t)
    
    if ('8am' in t_clean or '800am' in t_clean) and ('2pm' in t_clean or '200pm' in t_clean):
        return "Winter 8 AM to 2 PM, Summer 8 AM to 2 PM"
    
    return str(time_str).strip()

@st.cache_data
def load_data():
    try:
        # Check local directory first (for deployment), fallback to hardcoded path (for local dev)
        local_path = "hospital_data.xlsx"
        hardcoded_path = r"c:\Users\ASUS\Desktop\challenges\code\HOSPITAL DATA - Copy.xlsx"
        
        file_path = local_path if os.path.exists(local_path) else hardcoded_path
        
        # Read ALL sheets without a header to dynamically find it
        all_sheets = pd.read_excel(file_path, sheet_name=None, header=None)
        dfs = []
        
        col_mapping = {
            'name of doctor': 'Doctor Name',
            'doctor': 'Doctor Name',
            'name': 'Doctor Name',
            'department': 'Department',
            'special': 'Specialization',
            'speciliza': 'Specialization',
            'hosp': 'Hospital',
            'desig': 'Designation',
            'unit/ time': 'Unit',
            'unit': 'Unit',
            'opd time': 'OPD Timing',
            'opd timing': 'OPD Timing',
            'time': 'OPD Timing',
            'timing': 'OPD Timing',
            'opd': 'OPD Days',
            'o p d': 'OPD Days',
            'ot': 'OT Days',
            'o t': 'OT Days',
            'days': 'OPD Days'
        }
        
        for sheet_name, sheet_df in all_sheets.items():
            if sheet_df.empty:
                continue
                
            # Find the header row
            header_idx = 0
            for i in range(min(15, len(sheet_df))):
                row_str = ' '.join(sheet_df.iloc[i].dropna().astype(str).str.lower())
                if 'name' in row_str or 'doctor' in row_str or 'designation' in row_str or 'opd' in row_str:
                    header_idx = i
                    break
                    
            # Set the header
            sheet_df.columns = sheet_df.iloc[header_idx].astype(str).str.strip().str.title()
            sheet_df = sheet_df.iloc[header_idx+1:].reset_index(drop=True)
            
            # Drop columns that have NaN or 'Nan' as the column name
            sheet_df = sheet_df.loc[:, [str(c).lower() != 'nan' for c in sheet_df.columns]]
            
            # RENAME COLUMNS BEFORE CONCATENATION to avoid duplicate columns later
            new_cols = []
            for col in sheet_df.columns:
                matched = False
                # Remove dots, underscores, and extra spaces for robust matching
                clean_col = str(col).lower().replace('.', '').replace('_', ' ').strip()
                clean_col = ' '.join(clean_col.split())
                
                for key, val in col_mapping.items():
                    if key in clean_col:
                        new_cols.append(val)
                        matched = True
                        break
                if not matched:
                    new_cols.append(col)
            sheet_df.columns = new_cols
            
            # Drop duplicate columns within the same sheet
            sheet_df = sheet_df.loc[:, ~sheet_df.columns.duplicated()]
            
            # Tag the dataframe with its sheet name to use as Department if needed
            sheet_df['_Sheet_Name'] = sheet_name
            dfs.append(sheet_df)
                
        if not dfs:
            return pd.DataFrame()
            
        # Now concat perfectly aligned dataframes
        df = pd.concat(dfs, ignore_index=True)
        
        # Drop rows that are completely empty
        df.dropna(how='all', inplace=True)
        
        # Ensure 'Doctor Name' column exists and drop rows missing it
        if 'Doctor Name' not in df.columns:
            valid_cols = [c for c in df.columns if c != '_Sheet_Name']
            if valid_cols:
                df.rename(columns={valid_cols[0]: 'Doctor Name'}, inplace=True)
        
        if 'Doctor Name' in df.columns:
            df.dropna(subset=['Doctor Name'], inplace=True)
            # Safe str casting because duplicate columns are impossible now
            df = df[df['Doctor Name'].astype(str).str.strip() != '']
            df = df[df['Doctor Name'].astype(str).str.strip().str.lower() != 'nan']
            df = df[df['Doctor Name'].astype(str).str.strip().str.lower() != 'name of doctor']
            
            # Filter out non-doctor entries (clinics, departments listed in the doctor name column)
            invalid_kws = ['clinic', 'oncology', 'neurology,', 'urology', 'andrology', 'others:', 'echo', 'respiratory', 'gastroenterology', 'endocrinology', 'wellbaby', 'immunizaton', 'nephrology', 'cardiology', 'pediatrics', 'medicine']
            for kw in invalid_kws:
                df = df[~df['Doctor Name'].astype(str).str.lower().str.contains(kw, na=False)]
        # Guarantee all expected keys exist to prevent KeyErrors
        required_cols = ['Doctor Name', 'Department', 'Specialization', 'Hospital', 'Designation', 'Unit', 'OPD Days', 'OT Days', 'OPD Timing']
        for col in required_cols:
            if col not in df.columns:
                df[col] = "Not specified"
                
        # Fill missing Departments using the Sheet Name
        if '_Sheet_Name' in df.columns:
            df['Department'] = df.apply(
                lambda row: row['_Sheet_Name'] if pd.isna(row['Department']) or str(row['Department']).strip() in ['', 'Not specified', 'nan'] else row['Department'], 
                axis=1
            )
            
        # Normalize Unit and OPD Timings
        if 'Unit' in df.columns:
            df['Unit'] = df['Unit'].apply(normalize_timing)
        if 'OPD Timing' in df.columns:
            df['OPD Timing'] = df['OPD Timing'].apply(normalize_timing)
            
        # Fill remaining NA values for all columns
        df = df.fillna("Not specified")
                
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()
