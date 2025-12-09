
import React, { useState } from 'react';
import axios from 'axios';

export default function BetBuilderV2(){
  const [teamsText, setTeamsText] = useState('Corinthians\nSantos\nFlamengo');
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(false);

  async function createTicket(){
    const teams = teamsText.split('\n').map(s=>s.trim()).filter(Boolean);
    setLoading(true);
    try{
      const r = await axios.post('/betbuilder/create', { teams: teams, markets_per_team:2, max_teams:10 });
      setTicket(r.data);
    }catch(e){
      console.error(e);
      alert('Erro ao criar ticket');
    }finally{ setLoading(false); }
  }

  async function openSporting(){
    if(!ticket) return;
    const tj = JSON.stringify(ticket);
    const url = '/betbuilder/redirect_url?ticket_id='+ticket.ticket_id+'&ticket_json='+encodeURIComponent(tj);
    const r = await axios.get(url);
    if(r.data && r.data.url){
      window.open(r.data.url, '_blank');
    }
  }

  async function applyEdit(){
    if(!ticket) return;
    const overrides = {};
    // example: override first selection odd
    overrides['0'] = prompt('Override odd for selection 0 (leave blank to skip)');
    const r = await axios.post('/betbuilder/apply_edits', { ticket: ticket, edits: { overrides }});
    setTicket(r.data);
  }

  return (
    <div style={{padding:20}}>
      <h2>BetBuilder V2 (Multi-markets)</h2>
      <textarea rows={6} cols={40} value={teamsText} onChange={e=>setTeamsText(e.target.value)} />
      <div>
        <button onClick={createTicket} disabled={loading}>Criar Ticket</button>
        <button onClick={applyEdit} disabled={!ticket}>Aplicar Edit</button>
        <button onClick={openSporting} disabled={!ticket}>Abrir na Sportingbet</button>
      </div>

      {ticket && (
        <div style={{marginTop:20}}>
          <h3>Ticket Preview</h3>
          <div><strong>Ticket id:</strong> {ticket.ticket_id}</div>
          <div><strong>Confidence:</strong> {ticket.confidence}</div>
          <div><strong>Total Odd:</strong> {ticket.total_odd}</div>
          <div style={{marginTop:10}}>
            {ticket.matches.map((m,mi)=>(
              <div key={mi} style={{border:'1px solid #ddd', padding:8, marginBottom:6}}>
                <div><strong>Team:</strong> {m.team}</div>
                <div>
                  {m.selections.map((s,si)=>(
                    <div key={si} style={{paddingLeft:8}}>
                      <div><em>Market:</em> {s.market}</div>
                      <div>Prob: {s.probability} | Odd: {s.recommended_odd} | Conf: {s.confidence}</div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
