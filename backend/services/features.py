import pandas as pd

def compute_basic_features(fixtures_df, history_df):
    features = []
    for _, row in fixtures_df.iterrows():
        home = row.get('home_team','Home'); away = row.get('away_team','Away')
        features.append({
            'match_id': row.get('match_id'),
            'home': home,
            'away': away,
            'home_win_pct': 60.0,
            'away_win_pct': 40.0,
            'home_avg_gf': 1.8,
            'away_avg_gf': 1.2
        })
    return pd.DataFrame(features)
