(function(){
  const endpoint = "REPLACE_WITH_API_URL"; // https://.../prod/events
  function uid(){ try{ let u=localStorage.getItem("uid"); if(!u){u=crypto.randomUUID(); localStorage.setItem("uid",u);} return u; }catch{ return "anon-"+Math.random().toString(36).slice(2);} }
  function send(ev){ return fetch(endpoint,{ method:"POST", headers:{ "Content-Type":"application/json" }, body: JSON.stringify(ev) }).catch(()=>{}); }
  window.Clickstream = { track: (name, props={}) => send({ event_name: name, user_id: props.user_id||uid(), created_at: new Date().toISOString(), ...props }) };
})();