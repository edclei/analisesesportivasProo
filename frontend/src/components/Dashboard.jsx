import React from 'react';

export default function Dashboard({account, predictions=[]}){
  return (
    <div className="card">
      <h2>Dashboard</h2>
      <div className="small">Conta: {account?.name || '—' } — Saldo: {account?.balance ?? '0'}</div>
      <div style={{marginTop:12}}>
        <h3>Jogos Recomendados</h3>
        {predictions.map((p,i)=>(
          <div key={i} style={{padding:8,borderRadius:6,marginTop:8,background:'rgba(255,255,255,0.02)'}}>
            <strong>{p.home} vs {p.away}</strong>
            <div className="small">{Math.round(p.home_win_prob*100)}% casa • BTTS {Math.round(p.btts_prob*100)}%</div>
          </div>
        ))}
      </div>
    </div>
  );
}
