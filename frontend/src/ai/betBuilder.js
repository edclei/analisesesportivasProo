import { MARKETS } from '../config/markets';

export function buildAutoTicket(candidates, accountBalance, maxSelections=10){
  const picks = candidates.filter(c=>c.pred && c.pred.home_win_prob >= 0.8).slice(0,maxSelections);
  const totalOdd = picks.reduce((acc,p)=>acc*(p.odds||1),1);
  const stake = Math.max(1, +(accountBalance * 0.02).toFixed(2));
  return { type:'multiple', selections:picks, totalOdd, stake, expectedReturn: +(stake*totalOdd).toFixed(2) };
}
