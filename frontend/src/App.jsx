import BetBuilderV2 from './pages/BetBuilderV2';\nimport DemoDashboard from './pages/DemoDashboard';
import React, {useState, useEffect} from 'react';
import Dashboard from './components/Dashboard';
import MultiBuilder from './components/MultiBuilder';
import axios from 'axios';

export default function App(){
  const [account,setAccount] = useState({name:'Demo Account', balance:1000});
  const [predictions, setPredictions] = useState([]);

  useEffect(()=> {
    async function load(){
      try{
        const h = await axios.get('/api/health');
        setPredictions([
          {home:'Corinthians',away:'Palmeiras',home_win_prob:0.72,btts_prob:0.35, odds:1.9},
          {home:'Manchester City',away:'Arsenal',home_win_prob:0.65,btts_prob:0.48, odds:1.6}
        ]);
      }catch(e){}
    }
    load();
  },[]);

  return (
    <div className="app">
      <aside className="sidebar card">
        <h2>Sports Analyzer</h2>
        <div className="small">Modo: Demo</div>
        <div style={{marginTop:12}}>
          <div className="small">Saldo: {account.balance}</div>
        </div>
      </aside>

      <main className="content">
        <Dashboard account={account} predictions={predictions} />
        <MultiBuilder />
      </main>
    </div>
  );
}




// Demo route added by assistant
// Add a simple navigation link to Demo
export function DemoLink(){
  return (<div style={{position:'fixed', right:20, top:20}}>
    <a href="#demo" onClick={(e)=>{e.preventDefault(); window.location.hash='demo'; window.location.reload();}}>Demo</a>
  </div>);
}

// If hash is #demo, render DemoDashboard
if(typeof window !== 'undefined' && window.location && window.location.hash === '#demo'){
  const root = document.getElementById('root') || document.querySelector('.root') || document.body;
  import('./pages/DemoDashboard').then(m=>{
    const Comp = m.default;
    const el = document.createElement('div');
    root.prepend(el);
    // basic render
    import('react-dom').then(rd=>{
      rd.render(rd.createElement(Comp), el);
    });
  });
}
\n\n// Quick access: append #betbuilder to open this page\nif(typeof window !== 'undefined' && window.location && window.location.hash === '#betbuilder'){\n  const root = document.getElementById('root') || document.body;\n  import('./pages/BetBuilderV2').then(m=>{ const Comp = m.default; import('react-dom').then(rd=>{ rd.render(rd.createElement(Comp), root); }); });\n}\n