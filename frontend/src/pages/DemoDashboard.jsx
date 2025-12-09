import React, { useState, useEffect } from 'react';
import axios from 'axios';

export default function DemoDashboard(){
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState(localStorage.getItem('APP_MODE') || 'demo');

  useEffect(()=>{
    fetchEntries();
  }, [mode]);

  function toggleMode(){
    const next = mode === 'demo' ? 'real' : 'demo';
    setMode(next);
    localStorage.setItem('APP_MODE', next);
    fetchEntries(next);
  }

  async function fetchEntries(m=mode){
    setLoading(true);
    try{
      const res = await axios.get('/api/predict', { params: { mode: m } });
      if(res && res.data){
        // demo returns a single prediction; normalize to array
        const pred = res.data.prediction ? [res.data.prediction] : [];
        setEntries(pred);
      }
    }catch(err){
      console.error(err);
    }finally{
      setLoading(false);
    }
  }

  return (
    <div style={{padding:20}}>
      <h2>Demo Dashboard (Mode: {mode})</h2>
      <button onClick={toggleMode}>Toggle Demo/Real</button>
      <button onClick={()=>fetchEntries()}>Generate</button>
      {loading && <p>Loading...</p>}
      <div style={{marginTop:20}}>
        {entries.map((e, idx)=>(
          <div key={idx} style={{border:'1px solid #ddd', padding:10, marginBottom:10}}>
            <div><strong>Match:</strong> {e.event && (e.event.home + ' vs ' + e.event.away)}</div>
            <div><strong>Market:</strong> {e.market}</div>
            <div><strong>Probability:</strong> {e.probability}</div>
            <div><strong>Odd:</strong> {e.recommended_odd}</div>
            <div><strong>Reason:</strong> {e.reason}</div>
          </div>
        ))}
      </div>
    </div>
  );
}