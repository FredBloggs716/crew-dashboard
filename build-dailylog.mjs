// Generates dailylog.js from the published Daily Log CSV.
// Node can read the CSV directly (no browser CORS), so this sidesteps the
// redirect/CORS block that stops the dashboard fetching it in-browser.
// Run:  node build-dailylog.mjs      (or double-click refresh-dailylog.bat)
import { writeFileSync } from 'node:fs';

const CSV = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRCjO3JU9gG1rMZK1mwKTbUHsEJT6-3C2Aeyi_k5-ngzH4FuDgIu4vvy0AIe-0OmnM-pmhl4TJ5Jp8J/pub?gid=1045940438&single=true&output=csv';

function csvRows(text){
  const rows=[]; let row=[], cell='', q=false; text=text.replace(/\r/g,'');
  for(let i=0;i<text.length;i++){const c=text[i];
    if(q){ if(c==='"'){ if(text[i+1]==='"'){cell+='"';i++;} else q=false; } else cell+=c; }
    else { if(c==='"')q=true; else if(c===','){row.push(cell);cell='';}
      else if(c==='\n'){row.push(cell);rows.push(row);row=[];cell='';} else cell+=c; }
  }
  if(cell!==''||row.length){row.push(cell);rows.push(row);}
  return rows;
}

const res = await fetch(CSV + '&_cb=' + Date.now());
if(!res.ok){ console.error('Fetch failed:', res.status); process.exit(1); }
const rows = csvRows(await res.text());
const log = rows.slice(1)
  .filter(r => r[0] && r[1])
  .map(r => ({ date:String(r[0]).trim(), name:String(r[1]).trim(), label:String(r[2]||'').trim() }));

const updated = new Date().toISOString();
const out = 'window.DAILY_LOG = ' + JSON.stringify(log) + ';\n' +
            'window.DAILY_LOG_UPDATED = ' + JSON.stringify(updated) + ';\n';
writeFileSync(new URL('./dailylog.js', import.meta.url), out);
const days = new Set(log.map(l=>l.date)).size;
console.log(`dailylog.js written: ${log.length} entries, ${days} days, updated ${updated}`);
