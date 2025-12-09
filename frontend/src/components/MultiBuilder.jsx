import React, {useState} from 'react';
import axios from 'axios';
import AccountToggle from './AccountToggle';
import { MARKETS } from '../config/markets';

export default function MultiBuilder(){
  const [mode,setMode]=useState('demo');
  const [accountId,setAccountId]=useState('');
  const [selections,setSelections]=useState([]);
  const [combinedOdd,setCombinedOdd]=useState(1.0);
  const [prob,setProb]=useState(0.85);

  async function placeDemo(){
    if(!accountId) return alert('crie conta demo');
    const payload = { account_id:accountId, selections, combined_odd:combinedOdd, prob };
    try{
      const r = await axios.post('/api/bet/place_demo', payload);
      alert(JSON.stringify(r.data));
    }catch(e){ alert('erro: '+(e.response?.data?.detail||e.message)); }
  }

  return (
    <div className="card">
      <h3>Gerador de Múltiplas IA</h3>
      <AccountToggle mode={mode} onChange={(m)=>setMode(m)} />
      <div style={{marginTop:10}}>
        <label className="small">Conta ID</label>
        <input value={accountId||''} onChange={e=>setAccountId(e.target.value)} style={{width:'100%',padding:8,borderRadius:6,marginTop:6}} />
      </div>
      <div style={{marginTop:10}}>
        <label className="small">Escolhas (JSON)</label>
        <textarea rows={6} value={JSON.stringify(selections,null,2)} onChange={e=>{ try{ setSelections(JSON.parse(e.target.value||'[]')) }catch(err){} }} style={{width:'100%',padding:8,borderRadius:6,marginTop:6}} />
      </div>
      <div style={{display:'flex',gap:8,marginTop:10}}>
        <button className="button" onClick={placeDemo}>Enviar Demo</button>
      </div>
    </div>
  );
}
