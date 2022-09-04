module.exports=(O,o) => (Object.entries(O).forEach(([K,V])=>Object.entries(V).forEach(([k,v])=>(o[K]=o[K]||{},o[K][k]=v))), o);
