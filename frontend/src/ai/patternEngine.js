export function scorePatterns(matchStats){
  let score=0; let reasons=[];
  if(matchStats.home_win_pct >= 70){ score+=20; reasons.push('Mandante dominante'); }
  if(matchStats.home_avg_gf >=2.0){ score+=12; reasons.push('Alta média de gols casa');}
  if(matchStats.away_avg_ga >=1.5){ score+=8; reasons.push('Visitante fraco defensivamente');}
  if(matchStats.corners_avg >=9){ score+=8; reasons.push('Muitos escanteios');}
  return {score, reasons};
}
