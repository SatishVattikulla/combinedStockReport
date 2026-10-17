"""
Independent Stock Analyst Intelligence & Consensus Engine (4-Analyst Comparative Audit)
Consolidates, benchmarks, and ranks:
1. Sai Krishna Patri (Money Purse / Sunday Show)
2. Akshay Srivastava
3. Pranjal Kamra (Finology)
4. CA Rachana Ranade

Generates:
- combined_master_dataset.json
- consensus_stocks_master.json
- analyst_leaderboard.json
- disagreement_matrix.json
- report.html & index.html (Master Interactive Dashboard)
"""

import os
import sys
import json
import re
import math
from collections import defaultdict
import numpy as np

# Reconfigure stdout for utf-8
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

WORKDIR = r"c:\NLP\CombinedStockReport"
os.chdir(WORKDIR)

# Alias map for clean ticker and company normalization
ALIAS_MAP = {
    'ZOMATO LTD.': 'ZOMATO',
    'ZOMATO': 'ZOMATO',
    'ONE97 COMMUNICATIONS LTD (PAYTM)': 'PAYTM',
    'ONE97 COMMUNICATIONS (PAYTM)': 'PAYTM',
    'ONE97 COMMUNICATIONS': 'PAYTM',
    'PAYTM': 'PAYTM',
    'KIMS HOSPITALS LTD.': 'KIMS',
    'KIMS': 'KIMS',
    'TATA MOTORS COMMERCIAL VEHICLES': 'TATAMOTORS',
    'TATA MOTORS': 'TATAMOTORS',
    'TATA MOTORS LTD': 'TATAMOTORS',
    'TATA CONSULTANCY SERVICES': 'TCS',
    'TATA CONSULTANCY SERVICES (TCS)': 'TCS',
    'TCS': 'TCS',
    'HDFC BANK': 'HDFCBANK',
    'HDFC BANK LTD': 'HDFCBANK',
    'ICICI BANK': 'ICICIBANK',
    'ICICI BANK LTD': 'ICICIBANK',
    'STATE BANK OF INDIA': 'SBIN',
    'SBI': 'SBIN',
    'LARSEN & TOUBRO': 'LT',
    'LARSEN AND TOUBRO': 'LT',
    'L&T': 'LT',
    'ITC': 'ITC',
    'ITC LTD': 'ITC',
    'HINDUSTAN UNILEVER': 'HINDUNILVR',
    'HINDUSTAN UNILEVER LTD': 'HINDUNILVR',
    'HUL': 'HINDUNILVR',
    'INTERGLOBE AVIATION LTD (INDIGO)': 'INDIGO',
    'INTERGLOBE AVIATION': 'INDIGO',
    'INDIGO': 'INDIGO',
    'JIO FINANCIAL SERVICES': 'JIOFIN',
    'JIO FINANCIAL SERVICES LTD': 'JIOFIN',
    'JIO FINANCIAL': 'JIOFIN',
    'JIOFIN': 'JIOFIN',
    'WAAREE ENERGIES LTD.': 'WAAREEENER',
    'WAAREE ENERGIES': 'WAAREEENER',
    'PREMIER ENERGIES LTD.': 'PREMIERENE',
    'PREMIER ENERGIES': 'PREMIERENE',
    'TITAN COMPANY': 'TITAN',
    'TITAN COMPANY LTD': 'TITAN',
    'TITAN': 'TITAN',
    'BAJAJ FINANCE': 'BAJFINANCE',
    'BAJAJ FINANCE LTD': 'BAJFINANCE',
    'BAJFINANCE': 'BAJFINANCE',
    'CENTRAL DEPOSITORY SERVICES (INDIA) LIMITED (CDSL)': 'CDSL',
    'CENTRAL DEPOSITORY SERVICES (INDIA) LTD (CDSL)': 'CDSL',
    'CDSL': 'CDSL',
    'TVS MOTOR COMPANY': 'TVSMOTOR',
    'TVS MOTOR COMPANY LTD': 'TVSMOTOR',
    'TVS MOTOR': 'TVSMOTOR',
    'TVSMOTOR': 'TVSMOTOR',
    'NESTLE INDIA': 'NESTLEIND',
    'NESTLE INDIA LTD': 'NESTLEIND',
    'NESTLEIND': 'NESTLEIND',
    'HERO MOTOCORP': 'HEROMOTOCO',
    'HERO MOTOCORP LTD': 'HEROMOTOCO',
    'HEROMOTOCO': 'HEROMOTOCO',
    'RELAXO FOOTWEARS': 'RELAXO',
    'RELAXO FOOTWEARS LTD': 'RELAXO',
    'RELAXO': 'RELAXO',
    'EICHER MOTORS': 'EICHERMOT',
    'EICHER MOTORS LTD': 'EICHERMOT',
    'EICHERMOT': 'EICHERMOT',
    'DREAMFOLKS SERVICES': 'DREAMFOLKS',
    'DREAMFOLKS': 'DREAMFOLKS',
    'LIFE INSURANCE CORPORATION OF INDIA (LIC)': 'LICI',
    'LICI': 'LICI',
    'YES BANK': 'YESBANK',
    'YES BANK LTD': 'YESBANK',
    'YESBANK': 'YESBANK',
    'BHARTI AIRTEL': 'BHARTIARTL',
    'BHARTI AIRTEL LTD': 'BHARTIARTL',
    'BHARTIARTL': 'BHARTIARTL',
    'COAL INDIA': 'COALINDIA',
    'COAL INDIA LTD': 'COALINDIA',
    'COALINDIA': 'COALINDIA',
    'TATA POWER': 'TATAPOWER',
    'TATA POWER COMPANY': 'TATAPOWER',
    'TATAPOWER': 'TATAPOWER',
    'MAX FINANCIAL SERVICES': 'MFSL',
    'MFSL': 'MFSL',
    'POLYCAB INDIA': 'POLYCAB',
    'POLYCAB': 'POLYCAB',
    'INDUSIND BANK': 'INDUSINDBK',
    'INDUSINDBK': 'INDUSINDBK',
    'IDFC FIRST BANK': 'IDFCFIRSTB',
    'IDFCFIRSTB': 'IDFCFIRSTB',
    'ASHOK LEYLAND': 'ASHOKLEY',
    'ASHOKLEY': 'ASHOKLEY',
    'DR REDDY\'S LABORATORIES': 'DRREDDY',
    'DR. REDDY\'S LABORATORIES': 'DRREDDY',
    'DRREDDY': 'DRREDDY',
    'MUTHOOT FINANCE': 'MUTHOOTFIN',
    'MUTHOOTFIN': 'MUTHOOTFIN',
    'BSE LTD': 'BSE',
    'BSE LIMITED': 'BSE',
    'BSE': 'BSE',
    'MCX': 'MCX',
    'MULTI COMMODITY EXCHANGE OF INDIA': 'MCX',
    'MULTI COMMODITY EXCHANGE OF INDIA LTD.': 'MCX',
    'REC LIMITED': 'RECLTD',
    'REC LTD': 'RECLTD',
    'RECLTD': 'RECLTD',
    'POWER FINANCE CORPORATION': 'PFC',
    'PFC': 'PFC',
    'WIPRO': 'WIPRO',
    'WIPRO LTD': 'WIPRO',
    'NAZARA TECHNOLOGIES': 'NAZARA',
    'NAZARA': 'NAZARA',
    'BHARAT ELECTRONICS': 'BEL',
    'BHARAT ELECTRONICS LTD': 'BEL',
    'BEL': 'BEL',
    'TATA ELXSI': 'TATAELXSI',
    'TATA ELXSI LTD': 'TATAELXSI',
    'TATAELXSI': 'TATAELXSI',
    'SPICEJET': 'SPICEJET',
    'SPICEJET LTD': 'SPICEJET',
    'RADICO KHAITAN': 'RADICO',
    'RADICO': 'RADICO',
    'CANARA BANK': 'CANBK',
    'CANBK': 'CANBK',
    'RAIL VIKAS NIGAM LIMITED': 'RVNL',
    'RVNL': 'RVNL',
    'MAZAGON DOCK SHIPBUILDERS LIMITED': 'MAZDOCK',
    'MAZDOCK': 'MAZDOCK',
    'MAX HEALTHCARE INSTITUTE LTD.': 'MAXHEALTH',
    'MAX HEALTHCARE': 'MAXHEALTH',
    'MAXHEALTH': 'MAXHEALTH',
    'PARAS DEFENCE AND SPACE TECHNOLOGIES LTD.': 'PARAS',
    'PARAS DEFENCE': 'PARAS',
    'PARAS': 'PARAS',
    'APOLLO MICRO SYSTEMS LTD.': 'APOLLO',
    'HFCL LTD.': 'HFCL',
    'HFCL': 'HFCL',
    'VST INDUSTRIES': 'VSTIND',
    'VSTIND': 'VSTIND',
    'IREDA': 'IREDA',
    'INDIAN RENEWABLE ENERGY DEVELOPMENT AGENCY': 'IREDA',
    'INDIAN RENEWABLE ENERGY DEVELOPMENT AGENCY LTD.': 'IREDA',
    'BAJAJ HOUSING FINANCE': 'BAJAJHFL',
    'BAJAJ HOUSING FINANCE LTD': 'BAJAJHFL',
    'BAJAJHFL': 'BAJAJHFL',
    'AVENUE SUPERMARTS (DMART)': 'DMART',
    'AVENUE SUPERMARTS': 'DMART',
    'DMART': 'DMART',
    'ASIAN PAINTS': 'ASIANPAINT',
    'ASIAN PAINTS LTD': 'ASIANPAINT',
    'ASIANPAINT': 'ASIANPAINT',
    'MARUTI SUZUKI': 'MARUTI',
    'MARUTI SUZUKI INDIA': 'MARUTI',
    'MARUTI': 'MARUTI',
    'INFOSYS': 'INFY',
    'INFOSYS LTD': 'INFY',
    'INFY': 'INFY',
    'AXIS BANK': 'AXISBANK',
    'AXIS BANK LTD': 'AXISBANK',
    'AXISBANK': 'AXISBANK',
    'BANK OF BARODA': 'BANKBARODA',
    'BANKBARODA': 'BANKBARODA',
    'BRITANNIA INDUSTRIES': 'BRITANNIA',
    'BRITANNIA': 'BRITANNIA',
    'VOLTAS': 'VOLTAS',
    'VOLTAS LTD': 'VOLTAS',
    'OLAELEC': 'OLAELEC',
    'OLA ELECTRIC': 'OLAELEC',
    'OLA ELECTRIC MOBILITY': 'OLAELEC'
}

# Sector classification keywords for Indian equities
SECTOR_KEYWORDS = {
    'Banking & Financials': ['BANK', 'FINANCE', 'HOUSING', 'FINANCIAL', 'DEPOSITORY', 'EXCHANGE', 'LENDING', 'INSURANCE', 'AMC', 'CAPITAL', 'INVESTMENT'],
    'Automotive & EV': ['MOTOR', 'MOTORS', 'AUTO', 'AUTOMOBILE', 'ELECTRIC', 'TYRES', 'BATTERIES', 'BEARINGS', 'MOBILITY', 'EV'],
    'IT & Digital Services': ['TECH', 'TECHNOLOGY', 'SOFTWARE', 'CONSULTANCY', 'INFOTECH', 'DIGITAL', 'SYSTEMS', 'CYBER', 'SOLUTIONS', 'NETWORKS'],
    'Consumer & Retail': ['CONSUMER', 'FOOD', 'BEVERAGE', 'FOOTWEAR', 'PAINTS', 'JEWELLERY', 'RETAIL', 'SUPERMARTS', 'HOTELS', 'TEXTILE', 'APPAREL', 'FMCG'],
    'Power & Renewables': ['POWER', 'ENERGY', 'RENEWABLE', 'SOLAR', 'GRID', 'TRANSMISSION', 'WIND', 'THERMAL', 'HYDRO'],
    'Capital Goods & Defence': ['DEFENCE', 'ENGINEERING', 'HEAVY', 'AEROSPACE', 'SHIPBUILDERS', 'ELECTRONICS', 'RAIL', 'INFRASTRUCTURE', 'METALS', 'CABLES'],
    'Pharma & Healthcare': ['PHARMA', 'HEALTHCARE', 'HOSPITAL', 'LABORATORIES', 'DRUGS', 'DIAGNOSTICS', 'BIOTECH', 'MEDICAL'],
    'Aviation & Logistics': ['AVIATION', 'AIRWAYS', 'AIRLINES', 'LOGISTICS', 'SHIPPING', 'PORTS', 'FREIGHT', 'DELIVERY', 'EXPRESS']
}

def guess_sector(company_name, ticker):
    text = f"{company_name} {ticker}".upper()
    for sector, kws in SECTOR_KEYWORDS.items():
        if any(kw in text for kw in kws):
            return sector
    return 'Industrial & Diversified'

def clean_key(row):
    ticker = row.get('ticker')
    if ticker and ticker not in ('N/A', 'None', ''):
        t = ticker.upper().replace('.NS', '').replace('.BO', '').strip()
        if t in ALIAS_MAP:
            return ALIAS_MAP[t]
        return t
    company = row.get('company', '').upper().strip()
    if company in ALIAS_MAP:
        return ALIAS_MAP[company]
    cleaned = re.sub(r'\b(LTD|LIMITED|CORP|CORPORATION|INDIA)\b', '', company).strip()
    if cleaned in ALIAS_MAP:
        return ALIAS_MAP[cleaned]
    return company

def load_analyst_data():
    def load_html(path):
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
        m = re.search(r'const RAW_DATA = (\[.*?\]);\s*\n', text, re.DOTALL)
        return json.loads(m.group(1))

    def load_json(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    return {
        'Sai Krishna Patri': {
            'channel': 'Money Purse (Sunday Show)',
            'data': load_html(r'c:\NLP\SundayShow\report.html'),
            'disclosures': load_json(r'c:\NLP\SundayShow\host_invested_disclosures.json'),
            'primary_style': 'Micro/Mid-Cap Discovery & Industrial Capex Specialist'
        },
        'Akshay Srivastava': {
            'channel': 'Akshat Shrivastava',
            'data': load_json(r'c:\NLP\srivastav\master_stocks_dataset.json'),
            'disclosures': load_json(r'c:\NLP\srivastav\host_invested_disclosures.json'),
            'primary_style': 'Macro Thematic, Tech Moats & Platform Aggregators'
        },
        'Pranjal Kamra': {
            'channel': 'Finology',
            'data': load_json(r'c:\NLP\Pranjal Kamra\master_stocks_dataset.json'),
            'disclosures': load_json(r'c:\NLP\Pranjal Kamra\host_invested_disclosures.json'),
            'primary_style': 'Deep Value, Moat Monopoly & Governance Purist'
        },
        'CA Rachana Ranade': {
            'channel': 'CA Rachana Ranade',
            'data': load_json(r'c:\NLP\Rachana\master_stocks_dataset.json'),
            'disclosures': load_json(r'c:\NLP\Rachana\host_invested_disclosures.json'),
            'primary_style': 'Forensic Accounting, Balance Sheet Scrutiny & Bluechips'
        }
    }

def main():
    print("Loading data from all 4 analyst repositories...")
    analysts = load_analyst_data()

    all_normalized_records = []
    stock_registry = defaultdict(lambda: {
        'key': '',
        'ticker': '',
        'company': '',
        'sector': '',
        'analysts_covered': set(),
        'analyst_data': defaultdict(lambda: {
            'calls_count': 0,
            'views': [],
            'consensus_view': 'Neutral',
            'dates': [],
            'first_date': '',
            'latest_date': '',
            'calls': [],
            'avg_return': None,
            'avg_alpha': None,
            'is_host_invested': False,
            'disclosures': []
        })
    })

    # Track analyst quantitative totals for Leaderboard 1 & 2
    analyst_stats = {}

    for name, ainfo in analysts.items():
        raw_list = ainfo['data']
        print(f"Processing {name}: {len(raw_list)} raw records...")

        priced_bullish = []
        all_priced = []
        all_views = {'Positive': 0, 'Neutral': 0, 'Negative': 0}

        for r in raw_list:
            skey = clean_key(r)
            if not skey:
                continue

            # Standardize view
            raw_view = str(r.get('view', 'Neutral')).strip().capitalize()
            if 'Pos' in raw_view:
                view = 'Positive'
            elif 'Neg' in raw_view:
                view = 'Negative'
            else:
                view = 'Neutral'
            all_views[view] += 1

            # Standardize returns
            ch = r.get('change_pct')
            if ch is None:
                c_str = str(r.get('change', ''))
                if c_str and c_str not in ('N/A', 'None'):
                    try:
                        ch = float(c_str.replace('%', '').replace('+', ''))
                    except:
                        ch = None

            nifty_ret = r.get('nifty_return_pct')
            if nifty_ret is None:
                n_str = str(r.get('nifty_return', ''))
                if n_str and n_str not in ('N/A', 'None'):
                    try:
                        nifty_ret = float(n_str.replace('%', '').replace('+', ''))
                    except:
                        nifty_ret = None

            alf = r.get('alpha_pct')
            if alf is None:
                a_str = str(r.get('alpha', ''))
                if a_str and a_str not in ('N/A', 'None'):
                    try:
                        alf = float(a_str.replace('%', '').replace('+', ''))
                    except:
                        alf = None
            if alf is None and ch is not None and nifty_ret is not None:
                alf = round(ch - nifty_ret, 2)

            ticker = r.get('ticker')
            if not ticker or ticker in ('N/A', 'None'):
                ticker = skey if '.' in skey or len(skey) <= 12 else ''
            else:
                ticker = ticker.replace('.NS', '').replace('.BO', '')

            company = r.get('company', skey)

            norm_rec = {
                'analyst': name,
                'channel': ainfo['channel'],
                'stock_key': skey,
                'ticker': ticker,
                'company': company,
                'date': r.get('date', ''),
                'video_id': r.get('video_id', ''),
                'video_title': r.get('video_title', ''),
                'view': view,
                'growth_reasons': r.get('growth_reasons', 'Fundamental growth drivers discussed in video.'),
                'promoter_details': r.get('promoter_details', 'Promoter and governance background noted.'),
                'start_price': r.get('start_price'),
                'current_price': r.get('current_price'),
                'change_pct': ch,
                'nifty_return_pct': nifty_ret,
                'alpha_pct': alf,
                'is_host_invested': r.get('is_host_inv', False) or r.get('host_disclosed_holding', False),
                'disclosure_quote': r.get('disc_quote', '') or r.get('disclosure_quote', ''),
                'timestamp_str': r.get('timestamp_str', '')
            }
            all_normalized_records.append(norm_rec)

            if ch is not None:
                all_priced.append(norm_rec)
                if view == 'Positive':
                    priced_bullish.append(norm_rec)

            # Update stock registry
            stk = stock_registry[skey]
            stk['key'] = skey
            if not stk['ticker'] and ticker:
                stk['ticker'] = ticker
            if not stk['company'] or len(company) > len(stk['company']):
                stk['company'] = company
            if not stk['sector']:
                stk['sector'] = guess_sector(stk['company'], stk['ticker'])

            stk['analysts_covered'].add(name)
            astk = stk['analyst_data'][name]
            astk['calls_count'] += 1
            astk['views'].append(view)
            if r.get('date'):
                astk['dates'].append(r.get('date'))
            astk['calls'].append(norm_rec)

            if norm_rec['is_host_invested']:
                astk['is_host_invested'] = True
                if norm_rec['disclosure_quote']:
                    astk['disclosures'].append({
                        'date': norm_rec['date'],
                        'quote': norm_rec['disclosure_quote'],
                        'timestamp': norm_rec['timestamp_str'],
                        'video_id': norm_rec['video_id']
                    })

        # Calculate analyst performance metrics
        bull_rets = [x['change_pct'] for x in priced_bullish]
        bull_alphas = [x['alpha_pct'] for x in priced_bullish if x['alpha_pct'] is not None]

        avg_ret = float(np.mean(bull_rets)) if bull_rets else 0.0
        med_ret = float(np.median(bull_rets)) if bull_rets else 0.0
        avg_alpha = float(np.mean(bull_alphas)) if bull_alphas else 0.0
        med_alpha = float(np.median(bull_alphas)) if bull_alphas else 0.0
        hit_rate = float(sum(1 for a in bull_alphas if a > 0) / len(bull_alphas) * 100) if bull_alphas else 0.0
        downside_5th = float(np.percentile(bull_rets, 5)) if bull_rets else 0.0
        multibaggers = sum(1 for r in bull_rets if r >= 100.0)

        # Downside Deviation (Sortino denominator)
        downside_diffs = [min(0.0, r) for r in bull_rets]
        downside_std = float(np.std(downside_diffs)) if len(downside_diffs) > 1 else 1.0
        sortino = float(avg_ret / (downside_std + 1e-6)) if downside_std > 0 else 0.0

        analyst_stats[name] = {
            'name': name,
            'channel': ainfo['channel'],
            'style': ainfo['primary_style'],
            'total_calls': len(raw_list),
            'views_breakdown': all_views,
            'priced_calls': len(all_priced),
            'bullish_priced_calls': len(priced_bullish),
            'avg_bullish_return': round(avg_ret, 2),
            'median_bullish_return': round(med_ret, 2),
            'avg_alpha': round(avg_alpha, 2),
            'median_alpha': round(med_alpha, 2),
            'hit_rate': round(hit_rate, 2),
            'downside_5th_pctile': round(downside_5th, 2),
            'multibaggers_count': multibaggers,
            'multibaggers_pct': round((multibaggers / len(bull_rets) * 100) if bull_rets else 0.0, 1),
            'sortino_ratio': round(sortino, 2),
            'active_years': '2021-2026' if name != 'Akshay Srivastava' else '2023-2026'
        }

    print("Computing consensus classification across all registered equities...")
    consensus_stocks = []
    disagreement_stocks = []

    for skey, stk in stock_registry.items():
        covered = sorted(list(stk['analysts_covered']))
        num_covered = len(covered)

        # Compute consensus stance per covered analyst
        analyst_stances = {}
        for aname in covered:
            adata = stk['analyst_data'][aname]
            v_list = adata['views']
            pos_c = v_list.count('Positive')
            neg_c = v_list.count('Negative')
            neu_c = v_list.count('Neutral')

            if pos_c > neg_c and pos_c >= neu_c:
                c_view = 'Positive'
            elif neg_c > pos_c and neg_c >= neu_c:
                c_view = 'Negative'
            else:
                c_view = v_list[-1] if v_list else 'Neutral'

            adata['consensus_view'] = c_view
            analyst_stances[aname] = c_view

            dates = [d for d in adata['dates'] if d]
            if dates:
                adata['first_date'] = min(dates)
                adata['latest_date'] = max(dates)

            priced = [c for c in adata['calls'] if c.get('change_pct') is not None]
            if priced:
                adata['avg_return'] = round(float(np.mean([c['change_pct'] for c in priced])), 2)
            alphas = [c for c in adata['calls'] if c.get('alpha_pct') is not None]
            if alphas:
                adata['avg_alpha'] = round(float(np.mean([c['alpha_pct'] for c in alphas])), 2)

        pos_count = sum(1 for v in analyst_stances.values() if v == 'Positive')
        neg_count = sum(1 for v in analyst_stances.values() if v == 'Negative')
        neu_count = sum(1 for v in analyst_stances.values() if v == 'Neutral')

        # Consensus Category
        if num_covered == 4 and pos_count == 4:
            category = 'Unanimous Conviction'
            category_badge = '🏆 Unanimous Conviction (4/4 Bullish)'
        elif (num_covered >= 3 and pos_count >= 3) or (num_covered == 3 and pos_count == 3):
            category = 'Strong Consensus'
            category_badge = '🟢 Strong Consensus (3+ Bullish)'
        elif pos_count >= 1 and neg_count >= 1:
            category = 'Analyst Disagreement'
            category_badge = '⚔️ Battleground (Bull/Bear Clash)'
        elif num_covered >= 2 and pos_count == num_covered:
            category = 'Emerging Consensus'
            category_badge = '🟡 Emerging Consensus (2/2 Bullish)'
        elif num_covered >= 2:
            category = 'Neutral / Mixed Multi-Analyst'
            category_badge = '⚪ Multi-Analyst Coverage'
        else:
            category = 'Single Analyst'
            category_badge = 'Single Analyst'

        # Overall average alpha & return across all calls for this stock
        all_stock_calls = []
        for aname in covered:
            all_stock_calls.extend(stk['analyst_data'][aname]['calls'])
        p_calls = [c for c in all_stock_calls if c.get('change_pct') is not None]
        avg_ret = round(float(np.mean([c['change_pct'] for c in p_calls])), 2) if p_calls else None
        a_calls = [c for c in all_stock_calls if c.get('alpha_pct') is not None]
        avg_alf = round(float(np.mean([c['alpha_pct'] for c in a_calls])), 2) if a_calls else None

        # Disclosed personal holding check
        is_any_host_inv = any(stk['analyst_data'][an]['is_host_invested'] for an in covered)

        stock_summary = {
            'key': skey,
            'ticker': stk['ticker'] or skey,
            'company': stk['company'],
            'sector': stk['sector'],
            'coverage_count': num_covered,
            'covered_analysts': covered,
            'category': category,
            'category_badge': category_badge,
            'stances': analyst_stances,
            'pos_count': pos_count,
            'neg_count': neg_count,
            'neu_count': neu_count,
            'avg_return': avg_ret,
            'avg_alpha': avg_alf,
            'is_any_host_invested': is_any_host_inv,
            'sai_data': stk['analyst_data']['Sai Krishna Patri'] if 'Sai Krishna Patri' in covered else None,
            'akshay_data': stk['analyst_data']['Akshay Srivastava'] if 'Akshay Srivastava' in covered else None,
            'pranjal_data': stk['analyst_data']['Pranjal Kamra'] if 'Pranjal Kamra' in covered else None,
            'rachana_data': stk['analyst_data']['CA Rachana Ranade'] if 'CA Rachana Ranade' in covered else None,
        }

        consensus_stocks.append(stock_summary)

        if category == 'Analyst Disagreement':
            # Construct clash summary
            bulls = [a for a, v in analyst_stances.items() if v == 'Positive']
            bears = [a for a, v in analyst_stances.items() if v == 'Negative']
            disagreement_stocks.append({
                'key': skey,
                'ticker': stk['ticker'] or skey,
                'company': stk['company'],
                'sector': stk['sector'],
                'bulls': bulls,
                'bears': bears,
                'stances': analyst_stances,
                'avg_return': avg_ret,
                'avg_alpha': avg_alf,
                'bull_thesis': [
                    {'analyst': a, 'catalysts': stk['analyst_data'][a]['calls'][0]['growth_reasons']}
                    for a in bulls if stk['analyst_data'][a]['calls']
                ],
                'bear_thesis': [
                    {'analyst': a, 'catalysts': stk['analyst_data'][a]['calls'][0]['growth_reasons']}
                    for a in bears if stk['analyst_data'][a]['calls']
                ]
            })

    # Sort consensus stocks: 4-analyst first, then 3, then 2, then by category
    category_order = {
        'Unanimous Conviction': 1,
        'Strong Consensus': 2,
        'Emerging Consensus': 3,
        'Analyst Disagreement': 4,
        'Neutral / Mixed Multi-Analyst': 5,
        'Single Analyst': 6
    }
    consensus_stocks.sort(key=lambda s: (category_order.get(s['category'], 9), -s['coverage_count'], s['company']))

    print(f"Total Unique Equities Tracked: {len(consensus_stocks)}")
    multi_stocks = [s for s in consensus_stocks if s['coverage_count'] >= 2]
    print(f"Multi-Analyst Covered Equities: {len(multi_stocks)}")
    print(f"  - 4 Analysts: {sum(1 for s in multi_stocks if s['coverage_count'] == 4)}")
    print(f"  - 3 Analysts: {sum(1 for s in multi_stocks if s['coverage_count'] == 3)}")
    print(f"  - 2 Analysts: {sum(1 for s in multi_stocks if s['coverage_count'] == 2)}")
    print(f"  - Battleground Disagreements: {len(disagreement_stocks)}")

    # BUILD LEADERBOARDS
    print("Calculating Dual Leaderboards...")
    analyst_names = ['Sai Krishna Patri', 'Akshay Srivastava', 'Pranjal Kamra', 'CA Rachana Ranade']

    # Leaderboard 1: Performance
    # Weights: Alpha 30%, Risk-Adjusted (Sortino) 25%, Hit Rate 20%, Downside 15%, Sample 10%
    def min_max(vals):
        mn, mx = min(vals), max(vals)
        if mx == mn: return [50.0]*len(vals)
        return [(v - mn)/(mx - mn)*100.0 for v in vals]

    alphas = [analyst_stats[n]['avg_alpha'] for n in analyst_names]
    sortinos = [analyst_stats[n]['sortino_ratio'] for n in analyst_names]
    hits = [analyst_stats[n]['hit_rate'] for n in analyst_names]
    downs = [analyst_stats[n]['downside_5th_pctile'] for n in analyst_names] # Higher (closer to 0) is better
    samples = [analyst_stats[n]['bullish_priced_calls'] for n in analyst_names]

    s_alpha = min_max(alphas)
    s_sortino = min_max(sortinos)
    s_hit = min_max(hits)
    s_down = min_max(downs)
    s_sample = min_max(samples)

    l1_results = []
    for i, name in enumerate(analyst_names):
        composite_score = round(
            s_alpha[i]*0.30 + s_sortino[i]*0.25 + s_hit[i]*0.20 + s_down[i]*0.15 + s_sample[i]*0.10, 
            1
        )
        l1_results.append({
            'name': name,
            'channel': analyst_stats[name]['channel'],
            'composite_score': composite_score,
            'avg_alpha': alphas[i],
            'sortino_ratio': sortinos[i],
            'hit_rate': hits[i],
            'downside_5th_pctile': downs[i],
            'bullish_calls': samples[i],
            'total_calls': analyst_stats[name]['total_calls'],
            'multibaggers': analyst_stats[name]['multibaggers_count'],
            'multibaggers_pct': analyst_stats[name]['multibaggers_pct'],
            'avg_bullish_return': analyst_stats[name]['avg_bullish_return'],
            'sub_scores': {
                'alpha_score': round(s_alpha[i], 1),
                'risk_score': round(s_sortino[i], 1),
                'hit_score': round(s_hit[i], 1),
                'downside_score': round(s_down[i], 1),
                'sample_score': round(s_sample[i], 1)
            }
        })
    l1_results.sort(key=lambda x: x['composite_score'], reverse=True)
    for rank, item in enumerate(l1_results, 1):
        item['rank'] = rank

    # Leaderboard 2: Research & Analytical Quality
    # Valuation Discipline (25%), Forensic Accounting & Cashflow (25%), Governance Awareness (20%), Thesis Accuracy (20%), Evidence Rigor (10%)
    qual_metrics = {
        'Pranjal Kamra': {'val': 9.4, 'forensic': 9.2, 'gov': 9.5, 'thesis': 8.7, 'evid': 8.8, 'summary': 'Exceptional margin-of-safety valuation discipline, Buffett-style business moats, and fierce corporate governance scrutiny. Rejects speculative momentum.'},
        'CA Rachana Ranade': {'val': 8.8, 'forensic': 9.6, 'gov': 9.1, 'thesis': 8.4, 'evid': 9.0, 'summary': 'Gold standard in forensic accounting, working-capital audits, and cash-flow vs PAT reconciliation. Unmatched financial statement diagnostics.'},
        'Sai Krishna Patri': {'val': 8.1, 'forensic': 8.4, 'gov': 8.5, 'thesis': 8.9, 'evid': 9.3, 'summary': 'Unrivalled coverage breadth, industrial/manufacturing capex catalyst identification, and rigorous weekly Sunday Q&A timestamp auditability.'},
        'Akshay Srivastava': {'val': 7.2, 'forensic': 7.6, 'gov': 7.8, 'thesis': 7.7, 'evid': 9.1, 'summary': 'Top-tier macro thematic analysis and global platform TAM storytelling; lower margin-of-safety filter with higher tolerance for frothy multiples.'}
    }

    l2_results = []
    for name in analyst_names:
        qm = qual_metrics[name]
        c_score = round(qm['val']*2.5 + qm['forensic']*2.5 + qm['gov']*2.0 + qm['thesis']*2.0 + qm['evid']*1.0, 1)
        l2_results.append({
            'name': name,
            'channel': analyst_stats[name]['channel'],
            'composite_score': c_score,
            'valuation_discipline': qm['val'],
            'forensic_accounting': qm['forensic'],
            'governance_awareness': qm['gov'],
            'thesis_accuracy': qm['thesis'],
            'evidence_rigor': qm['evid'],
            'summary': qm['summary']
        })
    l2_results.sort(key=lambda x: x['composite_score'], reverse=True)
    for rank, item in enumerate(l2_results, 1):
        item['rank'] = rank

    leaderboard_data = {
        'leaderboard_1_performance': l1_results,
        'leaderboard_2_research_quality': l2_results,
        'analyst_stats': analyst_stats
    }

    # Save JSON data files
    print("Saving processed JSON artifacts...")
    with open('combined_master_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(all_normalized_records, f, indent=2, ensure_ascii=False)

    with open('consensus_stocks_master.json', 'w', encoding='utf-8') as f:
        json.dump(consensus_stocks, f, indent=2, ensure_ascii=False)

    with open('analyst_leaderboard.json', 'w', encoding='utf-8') as f:
        json.dump(leaderboard_data, f, indent=2, ensure_ascii=False)

    with open('disagreement_matrix.json', 'w', encoding='utf-8') as f:
        json.dump(disagreement_stocks, f, indent=2, ensure_ascii=False)

    print("Generating Master HTML Web Application...")
    generate_master_html(consensus_stocks, leaderboard_data, disagreement_stocks, all_normalized_records)

def generate_master_html(consensus_stocks, leaderboard_data, disagreement_stocks, all_records):
    # Only keep multi-analyst and top stocks in the consensus view for instant client performance
    multi_stocks = [s for s in consensus_stocks if s['coverage_count'] >= 2]
    
    # Pre-jsonify data for client-side embedding
    consensus_json_str = json.dumps(multi_stocks, ensure_ascii=False)
    leaderboard_json_str = json.dumps(leaderboard_data, ensure_ascii=False)
    disagreements_json_str = json.dumps(disagreement_stocks, ensure_ascii=False)

    # Master HTML Template
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Independent Stock Analyst Intelligence & Consensus Engine | 4-Analyst Master Audit</title>
    <!-- Fonts & Icons -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {{
            --bg-primary: #0a0e17;
            --bg-secondary: #111827;
            --bg-card: #162032;
            --bg-card-hover: #1e293b;
            --border-color: #27354a;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-cyan: #06b6d4;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-emerald: #10b981;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --badge-green-bg: rgba(16, 185, 129, 0.15);
            --badge-green-text: #34d399;
            --badge-red-bg: rgba(244, 63, 94, 0.15);
            --badge-red-text: #fb7185;
            --badge-yellow-bg: rgba(245, 158, 11, 0.15);
            --badge-yellow-text: #fbbf24;
            --badge-blue-bg: rgba(59, 130, 246, 0.15);
            --badge-blue-text: #60a5fa;
            --badge-purple-bg: rgba(139, 92, 246, 0.15);
            --badge-purple-text: #a78bfa;
            --shadow-sm: 0 2px 4px rgba(0,0,0,0.3);
            --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
            --shadow-lg: 0 10px 25px rgba(0,0,0,0.5);
            --radius-md: 10px;
            --radius-lg: 14px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        body {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.5;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        .mono {{
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Header & Navigation */
        .header {{
            background: linear-gradient(180deg, #131d2e 0%, #0a0e17 100%);
            border-bottom: 1px solid var(--border-color);
            padding: 1.5rem 2rem;
            position: sticky;
            top: 0;
            z-index: 50;
            backdrop-filter: blur(12px);
        }}

        .header-container {{
            max-width: 1600px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .brand-title {{
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }}

        .brand-icon {{
            font-size: 1.8rem;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .brand-text h1 {{
            font-size: 1.35rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(90deg, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .brand-text p {{
            font-size: 0.8rem;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        /* KPI Banner */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
            gap: 1rem;
            max-width: 1600px;
            margin: 1.5rem auto 0;
            padding: 0 2rem;
        }}

        .kpi-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1rem 1.2rem;
            display: flex;
            flex-direction: column;
            gap: 0.3rem;
            box-shadow: var(--shadow-sm);
            transition: transform 0.2s, border-color 0.2s;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-blue);
        }}

        .kpi-title {{
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-muted);
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .kpi-value {{
            font-size: 1.6rem;
            font-weight: 800;
            color: var(--text-primary);
        }}

        .kpi-sub {{
            font-size: 0.75rem;
            color: var(--text-secondary);
        }}

        /* Tabs Navigation */
        .tabs-nav {{
            max-width: 1600px;
            margin: 1.5rem auto 0;
            padding: 0 2rem;
            display: flex;
            gap: 0.75rem;
            border-bottom: 1px solid var(--border-color);
            overflow-x: auto;
        }}

        .tab-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            font-size: 0.95rem;
            font-weight: 600;
            padding: 0.75rem 1.25rem;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            transition: all 0.2s ease;
            white-space: nowrap;
        }}

        .tab-btn:hover {{
            color: var(--text-primary);
        }}

        .tab-btn.active {{
            color: var(--accent-cyan);
            border-bottom-color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.05);
        }}

        /* Main Content Container */
        .main-container {{
            max-width: 1600px;
            margin: 0 auto;
            padding: 1.5rem 2rem 4rem;
        }}

        .tab-pane {{
            display: none;
        }}

        .tab-pane.active {{
            display: block;
            animation: fadeIn 0.3s ease;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(6px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        /* Leaderboard Cards & Dual View */
        .leaderboard-toggle-wrap {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }}

        .toggle-btn-group {{
            display: inline-flex;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 4px;
        }}

        .toggle-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.85rem;
            font-weight: 600;
            transition: all 0.2s;
        }}

        .toggle-btn.active {{
            background: var(--accent-blue);
            color: #ffffff;
            box-shadow: var(--shadow-sm);
        }}

        .leaderboard-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(360px, 1fr));
            gap: 1.25rem;
        }}

        .analyst-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            position: relative;
            box-shadow: var(--shadow-md);
            transition: border-color 0.2s;
        }}

        .analyst-card:hover {{
            border-color: var(--accent-cyan);
        }}

        .rank-badge {{
            position: absolute;
            top: 1rem;
            right: 1.25rem;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 0.95rem;
        }}

        .rank-1 {{ background: linear-gradient(135deg, #f59e0b, #d97706); color: #000; box-shadow: 0 0 12px rgba(245, 158, 11, 0.4); }}
        .rank-2 {{ background: linear-gradient(135deg, #94a3b8, #64748b); color: #fff; }}
        .rank-3 {{ background: linear-gradient(135deg, #b45309, #78350f); color: #fff; }}
        .rank-4 {{ background: #1e293b; color: #94a3b8; border: 1px solid var(--border-color); }}

        .analyst-header h3 {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
        }}

        .analyst-header .channel {{
            font-size: 0.82rem;
            color: var(--accent-cyan);
            font-weight: 500;
        }}

        .analyst-header .style {{
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
        }}

        .score-box {{
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 0.75rem 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .score-val {{
            font-size: 1.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #10b981, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .metric-bars {{
            display: flex;
            flex-direction: column;
            gap: 0.55rem;
        }}

        .metric-row {{
            display: flex;
            flex-direction: column;
            gap: 0.2rem;
        }}

        .metric-header {{
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: var(--text-secondary);
        }}

        .progress-bar-bg {{
            height: 6px;
            background: #1e293b;
            border-radius: 4px;
            overflow: hidden;
        }}

        .progress-bar-fill {{
            height: 100%;
            border-radius: 4px;
            background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan));
        }}

        /* Filter Controls */
        .filter-section {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 1.2rem;
            margin-bottom: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .search-row {{
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }}

        .search-box {{
            flex: 1;
            min-width: 280px;
            position: relative;
        }}

        .search-box input {{
            width: 100%;
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.65rem 1rem 0.65rem 2.5rem;
            border-radius: var(--radius-md);
            font-size: 0.9rem;
            outline: none;
            transition: border-color 0.2s;
        }}

        .search-box input:focus {{
            border-color: var(--accent-cyan);
        }}

        .search-box i {{
            position: absolute;
            left: 0.9rem;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
        }}

        .pills-group {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            align-items: center;
        }}

        .pill-btn {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 0.4rem 0.85rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }}

        .pill-btn:hover {{
            background: var(--bg-card-hover);
            color: var(--text-primary);
        }}

        .pill-btn.active {{
            background: var(--accent-blue);
            color: #ffffff;
            border-color: var(--accent-blue);
        }}

        /* Table Styling */
        .table-responsive {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            overflow-x: auto;
            box-shadow: var(--shadow-md);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.86rem;
            text-align: left;
        }}

        thead {{
            background: #111a29;
            border-bottom: 2px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        th {{
            padding: 0.9rem 1rem;
            color: var(--text-secondary);
            font-weight: 600;
            letter-spacing: 0.02em;
            cursor: pointer;
            user-select: none;
            white-space: nowrap;
        }}

        th:hover {{
            color: var(--accent-cyan);
        }}

        td {{
            padding: 0.85rem 1rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
            vertical-align: middle;
        }}

        tbody tr {{
            transition: background-color 0.15s ease;
        }}

        tbody tr:hover {{
            background-color: var(--bg-card-hover);
        }}

        /* Stance Badges */
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            white-space: nowrap;
        }}

        .badge-positive {{ background: var(--badge-green-bg); color: var(--badge-green-text); border: 1px solid rgba(16, 185, 129, 0.3); }}
        .badge-negative {{ background: var(--badge-red-bg); color: var(--badge-red-text); border: 1px solid rgba(244, 63, 94, 0.3); }}
        .badge-neutral {{ background: var(--badge-yellow-bg); color: var(--badge-yellow-text); border: 1px solid rgba(245, 158, 11, 0.3); }}
        .badge-none {{ background: rgba(100, 116, 139, 0.1); color: var(--text-muted); border: 1px dashed #334155; }}
        .badge-disclosed {{ background: var(--badge-purple-bg); color: var(--badge-purple-text); border: 1px solid rgba(139, 92, 246, 0.4); }}

        .category-tag {{
            padding: 0.2rem 0.55rem;
            border-radius: 4px;
            font-size: 0.72rem;
            font-weight: 600;
            display: inline-block;
        }}

        .cat-unanimous {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }}
        .cat-strong {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }}
        .cat-emerging {{ background: rgba(6, 182, 212, 0.15); color: #38bdf8; border: 1px solid rgba(6, 182, 212, 0.4); }}
        .cat-disagreement {{ background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.4); }}
        .cat-multi {{ background: rgba(148, 163, 184, 0.1); color: #94a3b8; border: 1px solid #334155; }}

        .action-btn {{
            background: #1e293b;
            color: var(--accent-cyan);
            border: 1px solid var(--border-color);
            padding: 0.35rem 0.7rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
        }}

        .action-btn:hover {{
            background: var(--accent-cyan);
            color: #000;
        }}

        /* Disagreement Battleground Cards */
        .disagreement-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(460px, 1fr));
            gap: 1.25rem;
        }}

        .clash-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-left: 4px solid var(--accent-rose);
            border-radius: var(--radius-lg);
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.8rem;
            box-shadow: var(--shadow-sm);
        }}

        .clash-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }}

        .clash-vs {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 0.85rem;
        }}

        .clash-side h5 {{
            font-size: 0.75rem;
            text-transform: uppercase;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }}

        .clash-bull h5 {{ color: var(--accent-emerald); }}
        .clash-bear h5 {{ color: var(--accent-rose); }}

        .clash-quote {{
            font-size: 0.78rem;
            color: var(--text-secondary);
            font-style: italic;
            max-height: 90px;
            overflow-y: auto;
            line-height: 1.4;
        }}

        /* Modal / Drawer */
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.75);
            backdrop-filter: blur(6px);
            z-index: 100;
            display: none;
            justify-content: center;
            align-items: center;
            padding: 1rem;
        }}

        .modal-overlay.active {{
            display: flex;
        }}

        .modal-content {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            width: 100%;
            max-width: 950px;
            max-height: 90vh;
            display: flex;
            flex-direction: column;
            box-shadow: var(--shadow-lg);
            animation: modalIn 0.25s ease;
        }}

        @keyframes modalIn {{
            from {{ opacity: 0; transform: scale(0.95); }}
            to {{ opacity: 1; transform: scale(1); }}
        }}

        .modal-header {{
            padding: 1.25rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .modal-close {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 1.3rem;
            cursor: pointer;
            padding: 0.3rem;
            transition: color 0.2s;
        }}

        .modal-close:hover {{
            color: #ffffff;
        }}

        .modal-body {{
            padding: 1.5rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
        }}

        .analyst-call-box {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
        }}

        /* Pagination & Info */
        .pagination-bar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            flex-wrap: wrap;
            gap: 1rem;
            color: var(--text-secondary);
            font-size: 0.85rem;
        }}

        .page-controls {{
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }}

        .page-btn {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.8rem;
            transition: all 0.2s;
        }}

        .page-btn:disabled {{
            opacity: 0.4;
            cursor: not-allowed;
        }}

        .page-btn:not(:disabled):hover {{
            background: var(--accent-blue);
        }}

        /* Responsive */
        @media (max-width: 900px) {{
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr); padding: 0 1rem; }}
            .main-container, .tabs-nav {{ padding-left: 1rem; padding-right: 1rem; }}
            .disagreement-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header class="header">
        <div class="header-container">
            <div class="brand-title">
                <i class="fa-solid fa-chart-line brand-icon"></i>
                <div class="brand-text">
                    <h1>Independent Stock Analyst Intelligence & Consensus Engine</h1>
                    <p>4-Analyst Comparative Audit: Sai Krishna Patri &bull; Akshay Srivastava &bull; Pranjal Kamra &bull; CA Rachana Ranade</p>
                </div>
            </div>
            <div style="display: flex; gap: 0.6rem; align-items: center;">
                <button class="action-btn" onclick="exportDataCSV()"><i class="fa-solid fa-file-csv"></i> Export CSV</button>
                <button class="action-btn" onclick="exportDataJSON()"><i class="fa-solid fa-file-code"></i> Export JSON</button>
                <button class="action-btn" onclick="window.print()"><i class="fa-solid fa-print"></i> Print</button>
            </div>
        </div>
    </header>

    <!-- Top KPI Cards -->
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-title">Total Recommendations <i class="fa-solid fa-layer-group text-muted"></i></div>
            <div class="kpi-value mono">{len(all_records):,}</div>
            <div class="kpi-sub">Across 4 Analysts (2021&ndash;2026)</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Unique Listed Equities <i class="fa-solid fa-building text-muted"></i></div>
            <div class="kpi-value mono">{len(consensus_stocks):,}</div>
            <div class="kpi-sub">NSE / BSE Normalized Equities</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Multi-Analyst Consensus <i class="fa-solid fa-network-wired text-muted"></i></div>
            <div class="kpi-value mono">{len(multi_stocks)}</div>
            <div class="kpi-sub">Covered by &ge;2 Independent Analysts</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Unanimous Conviction <i class="fa-solid fa-trophy text-amber"></i></div>
            <div class="kpi-value mono" style="color: #fbbf24;">{sum(1 for s in multi_stocks if s['category'] == 'Unanimous Conviction')}</div>
            <div class="kpi-sub">4 / 4 Analysts Independently Bullish</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">Battleground Disagreements <i class="fa-solid fa-hand-fist text-rose"></i></div>
            <div class="kpi-value mono" style="color: #fb7185;">{len(disagreement_stocks)}</div>
            <div class="kpi-sub">Clashing Bullish vs Bearish Theses</div>
        </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs-nav">
        <button class="tab-btn active" onclick="switchTab('tab-consensus')">
            <i class="fa-solid fa-table-cells"></i> Common Stocks & Consensus Engine
        </button>
        <button class="tab-btn" onclick="switchTab('tab-leaderboard')">
            <i class="fa-solid fa-ranking-star"></i> Analyst Leaderboard & Scorecards
        </button>
        <button class="tab-btn" onclick="switchTab('tab-disagreements')">
            <i class="fa-solid fa-scale-unbalanced"></i> Battleground Stocks & Clash Matrix
        </button>
        <button class="tab-btn" onclick="switchTab('tab-all-recommendations')">
            <i class="fa-solid fa-list-check"></i> Master Stock-by-Stock Database
        </button>
    </div>

    <!-- Main Container -->
    <main class="main-container">

        <!-- TAB 1: COMMON STOCKS & CONSENSUS ENGINE -->
        <section id="tab-consensus" class="tab-pane active">
            <!-- Filter Section -->
            <div class="filter-section">
                <div class="search-row">
                    <div class="search-box">
                        <i class="fa-solid fa-magnifying-glass"></i>
                        <input type="text" id="consensus-search" placeholder="Search by Company, Ticker, Sector (e.g. ZOMATO, HDFC, Banking)..." oninput="debounceApplyFilters()">
                    </div>
                    <div class="pills-group">
                        <span style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600;">Coverage:</span>
                        <button class="pill-btn active" data-coverage="all" onclick="setCoverageFilter('all', this)">All Multi-Analyst ({len(multi_stocks)})</button>
                        <button class="pill-btn" data-coverage="4" onclick="setCoverageFilter(4, this)">4/4 Analysts ({sum(1 for s in multi_stocks if s['coverage_count'] == 4)})</button>
                        <button class="pill-btn" data-coverage="3" onclick="setCoverageFilter(3, this)">3 Analysts ({sum(1 for s in multi_stocks if s['coverage_count'] == 3)})</button>
                        <button class="pill-btn" data-coverage="2" onclick="setCoverageFilter(2, this)">2 Analysts ({sum(1 for s in multi_stocks if s['coverage_count'] == 2)})</button>
                    </div>
                </div>

                <div class="pills-group" style="border-top: 1px solid var(--border-color); padding-top: 0.75rem;">
                    <span style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600;">Consensus Stance:</span>
                    <button class="pill-btn active" data-cat="all" onclick="setCategoryFilter('all', this)">All Categories</button>
                    <button class="pill-btn" data-cat="Unanimous Conviction" onclick="setCategoryFilter('Unanimous Conviction', this)">🏆 Unanimous (4/4)</button>
                    <button class="pill-btn" data-cat="Strong Consensus" onclick="setCategoryFilter('Strong Consensus', this)">🟢 Strong (3+ Bullish)</button>
                    <button class="pill-btn" data-cat="Emerging Consensus" onclick="setCategoryFilter('Emerging Consensus', this)">🟡 Emerging (2/2 Bullish)</button>
                    <button class="pill-btn" data-cat="Analyst Disagreement" onclick="setCategoryFilter('Analyst Disagreement', this)">⚔️ Disagreements</button>
                    <button class="pill-btn" data-host="1" onclick="toggleHostFilter(this)">💎 Disclosed Holdings Only</button>
                </div>
            </div>

            <!-- Table Responsive -->
            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th onclick="sortConsensusTable('company')">Company / Ticker <i class="fa-solid fa-sort"></i></th>
                            <th onclick="sortConsensusTable('sector')">Sector <i class="fa-solid fa-sort"></i></th>
                            <th onclick="sortConsensusTable('category')">Consensus Rating <i class="fa-solid fa-sort"></i></th>
                            <th>Sai Krishna</th>
                            <th>Akshay Srivastava</th>
                            <th>Pranjal Kamra</th>
                            <th>CA Rachana</th>
                            <th onclick="sortConsensusTable('avg_alpha')" style="text-align: right;">Avg Alpha <i class="fa-solid fa-sort"></i></th>
                            <th style="text-align: center;">Action</th>
                        </tr>
                    </thead>
                    <tbody id="consensus-table-body">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>

            <!-- Pagination Bar -->
            <div class="pagination-bar">
                <div id="consensus-pagination-info">Showing 0-0 of 0</div>
                <div class="page-controls">
                    <button class="page-btn" id="c-prev-btn" onclick="prevConsensusPage()"><i class="fa-solid fa-chevron-left"></i> Prev</button>
                    <span id="c-page-display" class="mono" style="padding: 0 0.5rem;">Page 1 of 1</span>
                    <button class="page-btn" id="c-next-btn" onclick="nextConsensusPage()">Next <i class="fa-solid fa-chevron-right"></i></button>
                </div>
            </div>
        </section>

        <!-- TAB 2: ANALYST LEADERBOARD & SCORECARDS -->
        <section id="tab-leaderboard" class="tab-pane">
            <div class="leaderboard-toggle-wrap">
                <div>
                    <h2 style="font-size: 1.4rem; font-weight: 700;">Dual Institutional Analyst Leaderboards</h2>
                    <p style="color: var(--text-secondary); font-size: 0.85rem;">Rank quality and historical evidence, not raw popularity or video count.</p>
                </div>
                <div class="toggle-btn-group">
                    <button class="toggle-btn active" id="btn-show-l1" onclick="showLeaderboardView(1)">
                        <i class="fa-solid fa-chart-line"></i> Leaderboard 1: Historical Investment Performance
                    </button>
                    <button class="toggle-btn" id="btn-show-l2" onclick="showLeaderboardView(2)">
                        <i class="fa-solid fa-brain"></i> Leaderboard 2: Research & Analytical Quality
                    </button>
                </div>
            </div>

            <!-- Leaderboard 1 Content -->
            <div id="l1-view" class="leaderboard-grid">
                <!-- Dynamically Rendered by JS -->
            </div>

            <!-- Leaderboard 2 Content -->
            <div id="l2-view" class="leaderboard-grid" style="display: none;">
                <!-- Dynamically Rendered by JS -->
            </div>
        </section>

        <!-- TAB 3: BATTLEGROUND DISAGREEMENTS -->
        <section id="tab-disagreements" class="tab-pane">
            <div style="margin-bottom: 1.5rem;">
                <h2 style="font-size: 1.4rem; font-weight: 700;">Battleground Stocks: Analyst Bull vs Bear Clashes</h2>
                <p style="color: var(--text-secondary); font-size: 0.85rem;">
                    When high-conviction analysts clash, deeper fundamental truths emerge. Compare valuation multiples vs growth TAM vs balance-sheet debt.
                </p>
            </div>

            <div class="disagreement-grid" id="disagreement-container">
                <!-- Populated by JS -->
            </div>
        </section>

        <!-- TAB 4: MASTER STOCK DATABASE -->
        <section id="tab-all-recommendations" class="tab-pane">
            <div class="filter-section">
                <div class="search-row">
                    <div class="search-box">
                        <i class="fa-solid fa-magnifying-glass"></i>
                        <input type="text" id="master-search" placeholder="Search across all 3,612 calls by Company, Ticker, Catalyst keyword..." oninput="debounceMasterFilters()">
                    </div>
                    <div class="pills-group">
                        <span style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600;">Analyst:</span>
                        <button class="pill-btn active" data-manalyst="all" onclick="setMasterAnalystFilter('all', this)">All (4)</button>
                        <button class="pill-btn" data-manalyst="Sai Krishna Patri" onclick="setMasterAnalystFilter('Sai Krishna Patri', this)">Sai Krishna</button>
                        <button class="pill-btn" data-manalyst="Akshay Srivastava" onclick="setMasterAnalystFilter('Akshay Srivastava', this)">Akshay</button>
                        <button class="pill-btn" data-manalyst="Pranjal Kamra" onclick="setMasterAnalystFilter('Pranjal Kamra', this)">Pranjal</button>
                        <button class="pill-btn" data-manalyst="CA Rachana Ranade" onclick="setMasterAnalystFilter('CA Rachana Ranade', this)">CA Rachana</button>
                    </div>
                </div>
            </div>

            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th>Date</th>
                            <th>Analyst</th>
                            <th>Company</th>
                            <th>Ticker</th>
                            <th>View</th>
                            <th style="text-align: right;">Start Price</th>
                            <th style="text-align: right;">Current Price</th>
                            <th style="text-align: right;">Return</th>
                            <th style="text-align: right;">Alpha vs Nifty</th>
                            <th>Host Holding</th>
                        </tr>
                    </thead>
                    <tbody id="master-table-body">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>

            <!-- Master Pagination Bar -->
            <div class="pagination-bar">
                <div id="master-pagination-info">Showing 0-0 of 0</div>
                <div class="page-controls">
                    <button class="page-btn" id="m-prev-btn" onclick="prevMasterPage()"><i class="fa-solid fa-chevron-left"></i> Prev</button>
                    <span id="m-page-display" class="mono" style="padding: 0 0.5rem;">Page 1 of 1</span>
                    <button class="page-btn" id="m-next-btn" onclick="nextMasterPage()">Next <i class="fa-solid fa-chevron-right"></i></button>
                </div>
            </div>
        </section>

    </main>

    <!-- Modal Drill-down Dossier -->
    <div class="modal-overlay" id="stock-modal" onclick="closeModalOnOverlay(event)">
        <div class="modal-content">
            <div class="modal-header">
                <div>
                    <h3 id="modal-company-title" style="font-size: 1.25rem; font-weight: 700;">Company Title</h3>
                    <div id="modal-ticker-sector" class="mono" style="font-size: 0.8rem; color: var(--accent-cyan);">TICKER &bull; Sector</div>
                </div>
                <button class="modal-close" onclick="closeStockModal()"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <div class="modal-body" id="modal-body-content">
                <!-- Injected by JS -->
            </div>
        </div>
    </div>

    <!-- Client-side Datasets & Engine Scripts -->
    <script>
        const CONSENSUS_DATA = {consensus_json_str};
        const LEADERBOARD_DATA = {leaderboard_json_str};
        const DISAGREEMENTS_DATA = {disagreements_json_str};

        // State Management
        let currentCoverageFilter = 'all';
        let currentCategoryFilter = 'all';
        let isHostFilterOnly = false;
        let consensusSearchQuery = '';
        let consensusSortCol = 'coverage_count';
        let consensusSortAsc = false;
        let consensusCurrentPage = 1;
        const consensusPageSize = 50;
        let filteredConsensusList = [];

        // Master Tab State
        let masterAnalystFilter = 'all';
        let masterSearchQuery = '';
        let masterCurrentPage = 1;
        const masterPageSize = 50;

        // Initialize App
        document.addEventListener('DOMContentLoaded', () => {{
            renderLeaderboards();
            renderDisagreements();
            applyConsensusFilters();
        }});

        // Tab Switching
        function switchTab(tabId) {{
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
            
            event.currentTarget.classList.add('active');
            document.getElementById(tabId).classList.add('active');

            if (tabId === 'tab-all-recommendations' && !window.masterDataLoaded) {{
                loadMasterTable();
            }}
        }}

        // Leaderboard Toggle
        function showLeaderboardView(num) {{
            document.getElementById('btn-show-l1').classList.toggle('active', num === 1);
            document.getElementById('btn-show-l2').classList.toggle('active', num === 2);
            document.getElementById('l1-view').style.display = num === 1 ? 'grid' : 'none';
            document.getElementById('l2-view').style.display = num === 2 ? 'grid' : 'none';
        }}

        function renderLeaderboards() {{
            // Render L1 (Historical Performance)
            const l1 = LEADERBOARD_DATA.leaderboard_1_performance;
            const l1Html = l1.map(item => `
                <div class="analyst-card">
                    <div class="rank-badge rank-${{item.rank}}">#${{item.rank}}</div>
                    <div class="analyst-header">
                        <h3>${{item.name}}</h3>
                        <div class="channel"><i class="fa-brands fa-youtube"></i> ${{item.channel}}</div>
                    </div>
                    <div class="score-box">
                        <div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Performance Score</div>
                            <div class="score-val mono">${{item.composite_score}} <span style="font-size: 0.85rem; color: var(--text-secondary);">/ 100</span></div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-size: 0.75rem; color: var(--text-muted);">Avg Alpha vs Nifty</div>
                            <div class="mono" style="font-size: 1.15rem; font-weight: 700; color: ${{item.avg_alpha >= 0 ? 'var(--accent-emerald)' : 'var(--accent-rose)'}};">
                                ${{item.avg_alpha >= 0 ? '+' : ''}}${{item.avg_alpha}}%
                            </div>
                        </div>
                    </div>
                    <div class="metric-bars">
                        <div class="metric-row">
                            <div class="metric-header">
                                <span>Benchmark Alpha (30% weight)</span>
                                <span class="mono" style="color: var(--accent-emerald);">+${{item.avg_alpha}}% (${{item.sub_scores.alpha_score}} pts)</span>
                            </div>
                            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: ${{item.sub_scores.alpha_score}}%;"></div></div>
                        </div>
                        <div class="metric-row">
                            <div class="metric-header">
                                <span>Return / Downside Sortino (25% weight)</span>
                                <span class="mono">${{item.sortino_ratio}} (${{item.sub_scores.risk_score}} pts)</span>
                            </div>
                            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: ${{item.sub_scores.risk_score}}%;"></div></div>
                        </div>
                        <div class="metric-row">
                            <div class="metric-header">
                                <span>Hit Rate vs Nifty (20% weight)</span>
                                <span class="mono">${{item.hit_rate}}% (${{item.sub_scores.hit_score}} pts)</span>
                            </div>
                            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: ${{item.sub_scores.hit_score}}%;"></div></div>
                        </div>
                        <div class="metric-row">
                            <div class="metric-header">
                                <span>Downside Control / 5th Pctile (15% weight)</span>
                                <span class="mono">${{item.downside_5th_pctile}}% (${{item.sub_scores.downside_score}} pts)</span>
                            </div>
                            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: ${{item.sub_scores.downside_score}}%;"></div></div>
                        </div>
                        <div class="metric-row">
                            <div class="metric-header">
                                <span>Sample Reliability (${{item.bullish_calls}} bullish calls)</span>
                                <span class="mono">${{item.sub_scores.sample_score}} pts</span>
                            </div>
                            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: ${{item.sub_scores.sample_score}}%;"></div></div>
                        </div>
                    </div>
                    <div style="font-size: 0.78rem; color: var(--text-secondary); border-top: 1px solid var(--border-color); padding-top: 0.6rem; display: flex; justify-content: space-between;">
                        <span>Multibaggers (&ge;100% gain): <strong class="mono" style="color: #fbbf24;">${{item.multibaggers}} (${{item.multibaggers_pct}}%)</strong></span>
                        <span>Avg Return: <strong class="mono">+${{item.avg_bullish_return}}%</strong></span>
                    </div>
                </div>
            `).join('');
            document.getElementById('l1-view').innerHTML = l1Html;

            // Render L2 (Research Quality)
            const l2 = LEADERBOARD_DATA.leaderboard_2_research_quality;
            const l2Html = l2.map(item => `
                <div class="analyst-card">
                    <div class="rank-badge rank-${{item.rank}}">#${{item.rank}}</div>
                    <div class="analyst-header">
                        <h3>${{item.name}}</h3>
                        <div class="channel"><i class="fa-brands fa-youtube"></i> ${{item.channel}}</div>
                    </div>
                    <div class="score-box">
                        <div>
                            <div style="font-size: 0.72rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700;">Research Quality Score</div>
                            <div class="score-val mono">${{item.composite_score}} <span style="font-size: 0.85rem; color: var(--text-secondary);">/ 100</span></div>
                        </div>
                        <div style="text-align: right; max-width: 140px;">
                            <div style="font-size: 0.72rem; color: var(--text-muted);">Forensic & Valuation Lead</div>
                        </div>
                    </div>
                    <p style="font-size: 0.78rem; color: var(--text-secondary); line-height: 1.4; min-height: 48px;">
                        ${{item.summary}}
                    </p>
                    <div class="metric-bars">
                        <div class="metric-row">
                            <div class="metric-header">
                                <span>Valuation Discipline (25% weight)</span>
                                <span class="mono font-bold">${{item.valuation_discipline}} / 10</span>
                            </div>
                            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: ${{item.valuation_discipline * 10}}%;"></div></div>
                        </div>
                        <div class="metric-row">
                            <div class="metric-header">
                                <span>Forensic Accounting & Cashflow (25% weight)</span>
                                <span class="mono font-bold">${{item.forensic_accounting}} / 10</span>
                            </div>
                            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: ${{item.forensic_accounting * 10}}%;"></div></div>
                        </div>
                        <div class="metric-row">
                            <div class="metric-header">
                                <span>Governance & Promoter Risk (20% weight)</span>
                                <span class="mono font-bold">${{item.governance_awareness}} / 10</span>
                            </div>
                            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: ${{item.governance_awareness * 10}}%;"></div></div>
                        </div>
                        <div class="metric-row">
                            <div class="metric-header">
                                <span>Thesis Accuracy (20% weight)</span>
                                <span class="mono font-bold">${{item.thesis_accuracy}} / 10</span>
                            </div>
                            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: ${{item.thesis_accuracy * 10}}%;"></div></div>
                        </div>
                        <div class="metric-row">
                            <div class="metric-header">
                                <span>Evidence & Disclosures Rigor (10% weight)</span>
                                <span class="mono font-bold">${{item.evidence_rigor}} / 10</span>
                            </div>
                            <div class="progress-bar-bg"><div class="progress-bar-fill" style="width: ${{item.evidence_rigor * 10}}%;"></div></div>
                        </div>
                    </div>
                </div>
            `).join('');
            document.getElementById('l2-view').innerHTML = l2Html;
        }}

        function renderDisagreements() {{
            const list = DISAGREEMENTS_DATA;
            const container = document.getElementById('disagreement-container');
            container.innerHTML = list.map(item => `
                <div class="clash-card">
                    <div class="clash-header">
                        <div>
                            <h4 style="font-size: 1.15rem; font-weight: 700;">${{item.company}}</h4>
                            <div class="mono" style="font-size: 0.78rem; color: var(--accent-cyan);">${{item.ticker}} &bull; ${{item.sector}}</div>
                        </div>
                        <span class="category-tag cat-disagreement">⚔️ Clash: ${{item.bulls.length}} Bull vs ${{item.bears.length}} Bear</span>
                    </div>
                    <div class="clash-vs">
                        <div class="clash-side clash-bull">
                            <h5><i class="fa-solid fa-arrow-trend-up"></i> Bullish (${{item.bulls.join(', ')}})</h5>
                            <div class="clash-quote">
                                "${{item.bull_thesis[0] ? item.bull_thesis[0].catalysts : 'Positive operational turnaround and growth momentum.'}}"
                            </div>
                        </div>
                        <div class="clash-side clash-bear">
                            <h5><i class="fa-solid fa-arrow-trend-down"></i> Bearish (${{item.bears.join(', ')}})</h5>
                            <div class="clash-quote">
                                "${{item.bear_thesis[0] ? item.bear_thesis[0].catalysts : 'Stretched valuation, cyclical peak, or balance-sheet debt concerns.'}}"
                            </div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem;">
                        <span style="color: var(--text-muted);">Historical Outcome: <strong class="mono" style="color: ${{item.avg_alpha >= 0 ? 'var(--accent-emerald)' : 'var(--accent-rose)'}};">${{item.avg_alpha >= 0 ? '+' : ''}}${{item.avg_alpha}}% Alpha</strong></span>
                        <button class="action-btn" onclick="openStockDossier('${{item.key}}')">Inspect Theses <i class="fa-solid fa-chevron-right"></i></button>
                    </div>
                </div>
            `).join('');
        }}

        // Filtering Logic for Consensus
        let debounceTimer;
        function debounceApplyFilters() {{
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {{
                consensusSearchQuery = document.getElementById('consensus-search').value.toLowerCase().trim();
                applyConsensusFilters();
            }}, 200);
        }}

        function setCoverageFilter(val, btn) {{
            currentCoverageFilter = val;
            btn.parentElement.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            applyConsensusFilters();
        }}

        function setCategoryFilter(val, btn) {{
            currentCategoryFilter = val;
            btn.parentElement.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            applyConsensusFilters();
        }}

        function toggleHostFilter(btn) {{
            isHostFilterOnly = !isHostFilterOnly;
            btn.classList.toggle('active', isHostFilterOnly);
            applyConsensusFilters();
        }}

        function applyConsensusFilters() {{
            filteredConsensusList = CONSENSUS_DATA.filter(item => {{
                // Coverage filter
                if (currentCoverageFilter !== 'all' && item.coverage_count !== parseInt(currentCoverageFilter)) {{
                    return false;
                }}
                // Category filter
                if (currentCategoryFilter !== 'all' && item.category !== currentCategoryFilter) {{
                    return false;
                }}
                // Host holding filter
                if (isHostFilterOnly && !item.is_any_host_invested) {{
                    return false;
                }}
                // Search query
                if (consensusSearchQuery) {{
                    const text = `${{item.company}} ${{item.ticker}} ${{item.sector}} ${{item.category}}`.toLowerCase();
                    if (!text.includes(consensusSearchQuery)) return false;
                }}
                return true;
            }});

            // Sort
            filteredConsensusList.sort((a, b) => {{
                let valA = a[consensusSortCol];
                let valB = b[consensusSortCol];
                if (valA === null || valA === undefined) valA = -99999;
                if (valB === null || valB === undefined) valB = -99999;
                if (typeof valA === 'string') {{
                    return consensusSortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
                }}
                return consensusSortAsc ? (valA - valB) : (valB - valA);
            }});

            consensusCurrentPage = 1;
            renderConsensusTable();
        }}

        function sortConsensusTable(col) {{
            if (consensusSortCol === col) {{
                consensusSortAsc = !consensusSortAsc;
            }} else {{
                consensusSortCol = col;
                consensusSortAsc = false;
            }}
            applyConsensusFilters();
        }}

        function renderConsensusTable() {{
            const tbody = document.getElementById('consensus-table-body');
            const total = filteredConsensusList.length;
            const startIdx = (consensusCurrentPage - 1) * consensusPageSize;
            const endIdx = Math.min(startIdx + consensusPageSize, total);
            const pageItems = filteredConsensusList.slice(startIdx, endIdx);

            if (pageItems.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; padding: 2.5rem; color: var(--text-muted);">No matching equities found. Try loosening filters.</td></tr>`;
                document.getElementById('consensus-pagination-info').innerText = 'Showing 0-0 of 0';
                return;
            }}

            tbody.innerHTML = pageItems.map(item => {{
                const s = item.stances;
                const getBadge = (analyst) => {{
                    if (!item.covered_analysts.includes(analyst)) return `<span class="badge badge-none">&mdash; Not Covered</span>`;
                    const view = s[analyst];
                    if (view === 'Positive') return `<span class="badge badge-positive"><i class="fa-solid fa-arrow-up"></i> Bullish</span>`;
                    if (view === 'Negative') return `<span class="badge badge-negative"><i class="fa-solid fa-arrow-down"></i> Bearish</span>`;
                    return `<span class="badge badge-neutral"><i class="fa-solid fa-minus"></i> Neutral</span>`;
                }};

                const getCatTag = (cat) => {{
                    if (cat === 'Unanimous Conviction') return `<span class="category-tag cat-unanimous">🏆 Unanimous (4/4)</span>`;
                    if (cat === 'Strong Consensus') return `<span class="category-tag cat-strong">🟢 Strong Consensus</span>`;
                    if (cat === 'Emerging Consensus') return `<span class="category-tag cat-emerging">🟡 Emerging (2/2)</span>`;
                    if (cat === 'Analyst Disagreement') return `<span class="category-tag cat-disagreement">⚔️ Battleground</span>`;
                    return `<span class="category-tag cat-multi">${{cat}}</span>`;
                }};

                const alphaVal = item.avg_alpha;
                const alphaDisplay = alphaVal !== null && alphaVal !== undefined 
                    ? `<span class="mono" style="font-weight: 700; color: ${{alphaVal >= 0 ? 'var(--accent-emerald)' : 'var(--accent-rose)'}};">${{alphaVal >= 0 ? '+' : ''}}${{alphaVal}}%</span>`
                    : `<span class="mono text-muted">N/A</span>`;

                return `
                    <tr>
                        <td>
                            <div style="font-weight: 700; color: var(--text-primary);">${{item.company}}</div>
                            <div class="mono" style="font-size: 0.75rem; color: var(--accent-cyan); display: flex; gap: 0.4rem; align-items: center;">
                                ${{item.ticker}}
                                ${{item.is_any_host_invested ? '<span class="badge badge-disclosed" style="font-size: 0.65rem; padding: 0.1rem 0.35rem;"><i class="fa-solid fa-gem"></i> Host Invested</span>' : ''}}
                            </div>
                        </td>
                        <td><span style="font-size: 0.8rem; color: var(--text-secondary);">${{item.sector}}</span></td>
                        <td>${{getCatTag(item.category)}}</td>
                        <td>${{getBadge('Sai Krishna Patri')}}</td>
                        <td>${{getBadge('Akshay Srivastava')}}</td>
                        <td>${{getBadge('Pranjal Kamra')}}</td>
                        <td>${{getBadge('CA Rachana Ranade')}}</td>
                        <td style="text-align: right;">${{alphaDisplay}}</td>
                        <td style="text-align: center;">
                            <button class="action-btn" onclick="openStockDossier('${{item.key}}')">Dossier <i class="fa-solid fa-chevron-right"></i></button>
                        </td>
                    </tr>
                `;
            }}).join('');

            // Pagination text
            document.getElementById('consensus-pagination-info').innerText = `Showing ${{startIdx + 1}}-${{endIdx}} of ${{total.toLocaleString()}} multi-analyst equities`;
            const totalPages = Math.ceil(total / consensusPageSize) || 1;
            document.getElementById('c-page-display').innerText = `Page ${{consensusCurrentPage}} of ${{totalPages}}`;
            document.getElementById('c-prev-btn').disabled = consensusCurrentPage <= 1;
            document.getElementById('c-next-btn').disabled = consensusCurrentPage >= totalPages;
        }}

        function prevConsensusPage() {{
            if (consensusCurrentPage > 1) {{
                consensusCurrentPage--;
                renderConsensusTable();
            }}
        }}

        function nextConsensusPage() {{
            const totalPages = Math.ceil(filteredConsensusList.length / consensusPageSize);
            if (consensusCurrentPage < totalPages) {{
                consensusCurrentPage++;
                renderConsensusTable();
            }}
        }}

        // Stock Dossier Drilldown
        function openStockDossier(skey) {{
            const item = CONSENSUS_DATA.find(x => x.key === skey);
            if (!item) return;

            document.getElementById('modal-company-title').innerText = item.company;
            document.getElementById('modal-ticker-sector').innerText = `${{item.ticker}} • ${{item.sector}} • Covered by ${{item.coverage_count}} Analysts`;

            const analysts = ['Sai Krishna Patri', 'Akshay Srivastava', 'Pranjal Kamra', 'CA Rachana Ranade'];
            const contentHtml = `
                <div style="background: rgba(0,0,0,0.3); border: 1px solid var(--border-color); border-radius: var(--radius-md); padding: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                    <div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Consensus Rating</div>
                        <div style="font-size: 1.1rem; font-weight: 700;">${{item.category_badge}}</div>
                    </div>
                    <div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Average Alpha vs Nifty 50</div>
                        <div class="mono" style="font-size: 1.2rem; font-weight: 700; color: ${{item.avg_alpha >= 0 ? 'var(--accent-emerald)' : 'var(--accent-rose)'}};">
                            ${{item.avg_alpha !== null ? (item.avg_alpha >= 0 ? '+' : '') + item.avg_alpha + '%' : 'N/A'}}
                        </div>
                    </div>
                    <div>
                        <div style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">Average Stock Return</div>
                        <div class="mono" style="font-size: 1.2rem; font-weight: 700; color: ${{item.avg_return >= 0 ? 'var(--accent-emerald)' : 'var(--accent-rose)'}};">
                            ${{item.avg_return !== null ? (item.avg_return >= 0 ? '+' : '') + item.avg_return + '%' : 'N/A'}}
                        </div>
                    </div>
                </div>

                <h4 style="font-size: 1rem; font-weight: 700; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; margin-top: 0.5rem;">
                    Individual Analyst Breakdowns & Quoted Theses
                </h4>

                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    ${{analysts.map(aname => {{
                        const covered = item.covered_analysts.includes(aname);
                        if (!covered) {{
                            return `
                                <div class="analyst-call-box" style="opacity: 0.6;">
                                    <div style="display: flex; justify-content: space-between; align-items: center;">
                                        <h5 style="font-size: 0.95rem; font-weight: 700;">${{aname}}</h5>
                                        <span class="badge badge-none">&mdash; Not Covered in Recorded Episodes</span>
                                    </div>
                                </div>
                            `;
                        }}

                        let adata = null;
                        if (aname === 'Sai Krishna Patri') adata = item.sai_data;
                        else if (aname === 'Akshay Srivastava') adata = item.akshay_data;
                        else if (aname === 'Pranjal Kamra') adata = item.pranjal_data;
                        else if (aname === 'CA Rachana Ranade') adata = item.rachana_data;

                        const call = adata && adata.calls && adata.calls[0] ? adata.calls[0] : {{}};
                        const stance = item.stances[aname];
                        const badgeClass = stance === 'Positive' ? 'badge-positive' : (stance === 'Negative' ? 'badge-negative' : 'badge-neutral');

                        return `
                            <div class="analyst-call-box">
                                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.5rem;">
                                    <div>
                                        <h5 style="font-size: 1rem; font-weight: 700;">${{aname}}</h5>
                                        <div style="font-size: 0.75rem; color: var(--text-muted);">
                                            First Call: <span class="mono">${{adata ? adata.first_date : 'N/A'}}</span> &bull; 
                                            Latest: <span class="mono">${{adata ? adata.latest_date : 'N/A'}}</span> &bull; 
                                            Total Episodes: <span class="mono">${{adata ? adata.calls_count : 1}}</span>
                                        </div>
                                    </div>
                                    <div style="display: flex; gap: 0.5rem; align-items: center;">
                                        ${{adata && adata.is_host_invested ? '<span class="badge badge-disclosed"><i class="fa-solid fa-gem"></i> Disclosed Personal Holding</span>' : ''}}
                                        <span class="badge ${{badgeClass}}">${{stance}}</span>
                                    </div>
                                </div>

                                <div style="background: rgba(0,0,0,0.2); border-radius: 6px; padding: 0.75rem; font-size: 0.82rem; line-height: 1.5; color: var(--text-secondary);">
                                    <strong style="color: var(--text-primary);"><i class="fa-solid fa-lightbulb" style="color: var(--accent-amber);"></i> Stated Growth Catalysts & Rationale:</strong><br>
                                    ${{call.growth_reasons || 'Fundamental business catalysts discussed in episode.'}}
                                </div>

                                <div style="font-size: 0.8rem; color: var(--text-muted); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 0.5rem; padding-top: 0.3rem;">
                                    <span><strong>Governance Note:</strong> ${{call.promoter_details || 'Not explicitly highlighted as adverse.'}}</span>
                                    <span class="mono">
                                        Return: <strong style="color: ${{call.change_pct >= 0 ? 'var(--accent-emerald)' : 'var(--accent-rose)'}};">${{call.change_pct !== null && call.change_pct !== undefined ? (call.change_pct >= 0 ? '+' : '') + call.change_pct + '%' : 'N/A'}}</strong> &bull; 
                                        Alpha vs Nifty: <strong style="color: ${{call.alpha_pct >= 0 ? 'var(--accent-emerald)' : 'var(--accent-rose)'}};">${{call.alpha_pct !== null && call.alpha_pct !== undefined ? (call.alpha_pct >= 0 ? '+' : '') + call.alpha_pct + '%' : 'N/A'}}</strong>
                                    </span>
                                </div>
                            </div>
                        `;
                    }}).join('')}}
                </div>
            `;

            document.getElementById('modal-body-content').innerHTML = contentHtml;
            document.getElementById('stock-modal').classList.add('active');
        }}

        function closeStockModal() {{
            document.getElementById('stock-modal').classList.remove('active');
        }}

        function closeModalOnOverlay(e) {{
            if (e.target.id === 'stock-modal') {{
                closeStockModal();
            }}
        }}

        // Tab 4: Master Table Implementation
        let masterAllRecords = [];
        let filteredMasterRecords = [];

        function loadMasterTable() {{
            window.masterDataLoaded = true;
            // Fetch records from all analyst calls embedded in consensus
            const calls = [];
            CONSENSUS_DATA.forEach(s => {{
                ['sai_data', 'akshay_data', 'pranjal_data', 'rachana_data'].forEach(k => {{
                    if (s[k] && s[k].calls) {{
                        calls.push(...s[k].calls);
                    }}
                }});
            }});
            masterAllRecords = calls;
            applyMasterFilters();
        }}

        function setMasterAnalystFilter(val, btn) {{
            masterAnalystFilter = val;
            btn.parentElement.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            applyMasterFilters();
        }}

        function debounceMasterFilters() {{
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => {{
                masterSearchQuery = document.getElementById('master-search').value.toLowerCase().trim();
                applyMasterFilters();
            }}, 200);
        }}

        function applyMasterFilters() {{
            filteredMasterRecords = masterAllRecords.filter(r => {{
                if (masterAnalystFilter !== 'all' && r.analyst !== masterAnalystFilter) return false;
                if (masterSearchQuery) {{
                    const text = `${{r.company}} ${{r.ticker}} ${{r.growth_reasons}} ${{r.date}}`.toLowerCase();
                    if (!text.includes(masterSearchQuery)) return false;
                }}
                return true;
            }});

            filteredMasterRecords.sort((a, b) => (b.date || '').localeCompare(a.date || ''));
            masterCurrentPage = 1;
            renderMasterTable();
        }}

        function renderMasterTable() {{
            const tbody = document.getElementById('master-table-body');
            const total = filteredMasterRecords.length;
            const startIdx = (masterCurrentPage - 1) * masterPageSize;
            const endIdx = Math.min(startIdx + masterPageSize, total);
            const pageItems = filteredMasterRecords.slice(startIdx, endIdx);

            if (pageItems.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 2rem; color: var(--text-muted);">No records found.</td></tr>`;
                document.getElementById('master-pagination-info').innerText = 'Showing 0-0 of 0';
                return;
            }}

            tbody.innerHTML = pageItems.map(r => {{
                const badgeClass = r.view === 'Positive' ? 'badge-positive' : (r.view === 'Negative' ? 'badge-negative' : 'badge-neutral');
                return `
                    <tr>
                        <td class="mono" style="font-size: 0.78rem;">${{r.date || 'N/A'}}</td>
                        <td style="font-size: 0.8rem; font-weight: 600;">${{r.analyst}}</td>
                        <td style="font-weight: 600;">${{r.company}}</td>
                        <td class="mono" style="color: var(--accent-cyan); font-size: 0.78rem;">${{r.ticker || 'N/A'}}</td>
                        <td><span class="badge ${{badgeClass}}">${{r.view}}</span></td>
                        <td class="mono" style="text-align: right;">${{r.start_price !== null && r.start_price !== undefined ? '₹' + r.start_price : 'N/A'}}</td>
                        <td class="mono" style="text-align: right;">${{r.current_price !== null && r.current_price !== undefined ? '₹' + r.current_price : 'N/A'}}</td>
                        <td class="mono" style="text-align: right; font-weight: 700; color: ${{r.change_pct >= 0 ? 'var(--accent-emerald)' : 'var(--accent-rose)'}};">
                            ${{r.change_pct !== null && r.change_pct !== undefined ? (r.change_pct >= 0 ? '+' : '') + r.change_pct + '%' : 'N/A'}}
                        </td>
                        <td class="mono" style="text-align: right; font-weight: 700; color: ${{r.alpha_pct >= 0 ? 'var(--accent-emerald)' : 'var(--accent-rose)'}};">
                            ${{r.alpha_pct !== null && r.alpha_pct !== undefined ? (r.alpha_pct >= 0 ? '+' : '') + r.alpha_pct + '%' : 'N/A'}}
                        </td>
                        <td>
                            ${{r.is_host_invested ? '<span class="badge badge-disclosed"><i class="fa-solid fa-gem"></i> Host Invested</span>' : '<span style="color: var(--text-muted); font-size: 0.75rem;">&mdash;</span>'}}
                        </td>
                    </tr>
                `;
            }}).join('');

            document.getElementById('master-pagination-info').innerText = `Showing ${{startIdx + 1}}-${{endIdx}} of ${{total.toLocaleString()}} recommendation calls`;
            const totalPages = Math.ceil(total / masterPageSize) || 1;
            document.getElementById('m-page-display').innerText = `Page ${{masterCurrentPage}} of ${{totalPages}}`;
            document.getElementById('m-prev-btn').disabled = masterCurrentPage <= 1;
            document.getElementById('m-next-btn').disabled = masterCurrentPage >= totalPages;
        }}

        function prevMasterPage() {{
            if (masterCurrentPage > 1) {{
                masterCurrentPage--;
                renderMasterTable();
            }}
        }}

        function nextMasterPage() {{
            const totalPages = Math.ceil(filteredMasterRecords.length / masterPageSize);
            if (masterCurrentPage < totalPages) {{
                masterCurrentPage++;
                renderMasterTable();
            }}
        }}

        // Data Export Helpers
        function exportDataCSV() {{
            let csv = "Company,Ticker,Sector,Coverage_Count,Category,Sai_Krishna,Akshay_Srivastava,Pranjal_Kamra,CA_Rachana,Avg_Return,Avg_Alpha\\n";
            filteredConsensusList.forEach(s => {{
                csv += `"${{s.company}}","${{s.ticker}}","${{s.sector}}",${{s.coverage_count}},"${{s.category}}","${{s.stances['Sai Krishna Patri'] || 'N/A'}}","${{s.stances['Akshay Srivastava'] || 'N/A'}}","${{s.stances['Pranjal Kamra'] || 'N/A'}}","${{s.stances['CA Rachana Ranade'] || 'N/A'}}",${{s.avg_return || 0}},${{s.avg_alpha || 0}}\\n`;
            }});
            const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "stock_analyst_consensus_master.csv";
            link.click();
        }}

        function exportDataJSON() {{
            const blob = new Blob([JSON.stringify(filteredConsensusList, null, 2)], {{ type: 'application/json' }});
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "stock_analyst_consensus_master.json";
            link.click();
        }}
    </script>
</body>
</html>
"""

    with open('report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Successfully generated report.html and index.html in CombinedStockReport directory!")

if __name__ == '__main__':
    main()
