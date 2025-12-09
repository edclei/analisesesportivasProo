import json
from .db import cursor

def save_justification(betslip_id, summary_obj):
    cur = cursor()
    cur.execute("""      INSERT INTO bet_justifications (betslip_id, summary, meta, created_at, expire_at)
      VALUES (%s,%s,%s,now(), now() + interval '24 hours')
    """, (betslip_id, summary_obj.get('text',''), json.dumps(summary_obj.get('meta',{}))))
    cur.connection.commit()
