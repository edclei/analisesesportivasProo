import React from 'react';

export default function AccountToggle({mode, onChange}){
  return (
    <div style={{display:'flex',gap:8}}>
      <button className={`button ${mode==='demo'?'active':''}`} onClick={()=>onChange('demo')}>Conta Demo</button>
      <button className={`button ${mode==='real'?'active':''}`} onClick={()=>onChange('real')}>Conta Real</button>
    </div>
  );
}
