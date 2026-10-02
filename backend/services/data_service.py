from __future__ import annotations
import json
from datetime import date
from pathlib import Path
import pandas as pd
from backend.config import DATA_DIR, STALE_AFTER_DAYS

FILES = {
    'native': DATA_DIR/'forecast_native.csv',
    'native_all': DATA_DIR/'native_all_models.csv',
    'live': DATA_DIR/'forecast_live_demo.csv',
    'metadata': DATA_DIR/'model_metadata.json',
    'comparison': DATA_DIR/'model_comparison.json',
    'analysis': DATA_DIR/'analysis_summary.json',
    'correlations': DATA_DIR/'meteorological_correlations.json',
    'native_accuracy': DATA_DIR/'native_7day_accuracy.json',
}

def require(path):
    if not path.exists(): raise FileNotFoundError(f'Missing dashboard artifact: {path.name}')

def load_json(name):
    path=FILES[name]; require(path)
    return json.loads(path.read_text(encoding='utf-8'))

def load_metadata(): return load_json('metadata')
def load_analysis(): return load_json('analysis')
def load_correlations(): return load_json('correlations')
def load_comparison(): return load_json('comparison')
def load_native_accuracy(): return load_json('native_accuracy')

def load_csv(name):
    path=FILES[name]; require(path)
    df=pd.read_csv(path)
    if 'Date' in df.columns: df['Date']=pd.to_datetime(df['Date'],errors='coerce')
    return df.dropna(subset=['Date']).sort_values('Date').reset_index(drop=True)

def records(df):
    out=[]
    for _,row in df.iterrows():
        d={}
        for k,v in row.items():
            d[k]=v.date().isoformat() if k=='Date' and pd.notna(v) else (float(v) if isinstance(v,(float,int)) else v)
        out.append(d)
    return out

def staleness_info():
    m=load_metadata(); training=pd.to_datetime(m.get('last_training_date'),errors='coerce')
    today=pd.Timestamp(date.today())
    gap=max(0,(today.normalize()-training.normalize()).days) if pd.notna(training) else None
    return {'is_stale': gap is None or gap>STALE_AFTER_DAYS,'gap_days':gap,'last_training_date':training.date().isoformat() if pd.notna(training) else None,
            'message':f'REMA air-quality data end on {training.date().isoformat()}; the current dashboard date is {today.date().isoformat()}. Gap: {gap} days.' if pd.notna(training) else 'Training date unavailable.'}

def native_payload():
    df=load_csv('native'); m=load_metadata()
    return {'mode':'native','demo_only':False,'selected_model':m['final_model'],'last_training_date':m['last_training_date'],'records':records(df),'staleness':staleness_info()}

def live_payload():
    return {'mode':'capability_demo','demo_only':True,'selected_model':'Random Forest','last_training_date':load_metadata()['last_training_date'],'records':records(load_csv('live')),'staleness':staleness_info()}

def csv_bytes(name): return load_csv(name).to_csv(index=False).encode('utf-8')
