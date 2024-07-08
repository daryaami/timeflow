import{_ as x,o as s,c as o,b as a,n as H,e as p,t as u,f as w,g as m,h as E,a as T,i as D,F as v,j as h,k as S,l as B}from"./index-XHfYEdPX.js";const V={props:{isSidebarHidden:Boolean},emits:{"update:isSidebarHidden":Boolean}},N={class:"planner-header"},C={class:"planner-header__date"},F=a("span",null,"February 2024",-1),M=a("div",{class:"planner-header__date-buttons"},[a("button",{class:"planner-header__date-button planner-header__date-button--prev"}),a("button",{class:"planner-header__date-button planner-header__date-button--next"})],-1);function P(t,e,n,r,_,i){return s(),o("header",N,[a("div",C,[F,M,a("button",{class:H(["sidebar-hide",{rotated:n.isSidebarHidden}]),onClick:e[0]||(e[0]=l=>t.$emit("update:isSidebarHidden",!n.isSidebarHidden))},null,2)])])}const j=x(V,[["render",P]]),z={},I={class:"loading-container"},U=a("div",{class:"loading-progress"},null,-1),q=[U];function A(t,e){return s(),o("div",I,q)}const G=x(z,[["render",A]]),g=t=>{let e;typeof t=="string"?e=new Date(t):e=t;let n=e.getHours(),r=e.getMinutes();return n+r/60},b=t=>{let e;typeof t=="string"?e=new Date(t):e=t;const n=String(e.getHours()).padStart(2,"0"),r=String(e.getMinutes()).padStart(2,"0");return`${n}:${r}`},J={class:"event-card__name"},K={class:"event-card__time"},O={__name:"EventCard",props:["event"],setup(t){const e=t,n=p(()=>g(e.event.start.dateTime)*100/24),r=p(()=>(g(e.event.end.dateTime)-g(e.event.start.dateTime))*100/24),_=p(()=>`${b(e.event.start.dateTime)} - ${b(e.event.end.dateTime)}`);return(i,l)=>(s(),o("div",{class:"event-card",style:w({top:`${n.value}%`,height:`${r.value}%`})},[a("span",J,u(t.event.summary),1),a("span",K,u(_.value),1)],4))}},Q=async()=>{let t=await fetch(`${window.location.origin}/planner_api/get_events/`);if(t.ok)return(await t.json()).days;throw new Error("Failed to fetch events")},R={__name:"PlannerDate",props:["date"],setup(t){const e=t,[n,r,_]=e.date.split(".").map(Number),i=new Date(_,r-1,n),l=p(()=>`${i.toLocaleDateString("en-EN",{weekday:"short"})} ${i.getDate()}`),$=p(()=>new Date().getDate()===i.getDate());return(y,d)=>(s(),o("span",{class:H(["planner-date",{current:$.value}])},u(l.value),3))}},W={class:"planner"},X={key:0,class:"planner__loader-wrapper"},Y={key:1,class:"planner__grid-wrapper"},Z={class:"planner__days-header"},ee={class:"planner__grid"},te={class:"planner__line-time"},ne={class:"planner__line-time"},se={__name:"Planner",setup(t){const e=m(null),n=m({caption:"",styleTop:""}),r=()=>{const d=new Date;n.value.caption=b(d),n.value.styleTop=`${g(d)*100/24}%`},_=async()=>{r(),await B(),e.value.scrollIntoView({block:"center"});const k=(60-new Date().getSeconds())*1e3;setTimeout(()=>{r(),setInterval(r,6e4)},k)},i=m([]),l=m(!0),$=async()=>{try{i.value=await Q()}catch(d){console.error("ошибка",d)}finally{l.value=!1,_()}};E(()=>{$()});const y=[{time:"01:00",percent:100/24},{time:"02:00",percent:200/24},{time:"03:00",percent:300/24},{time:"04:00",percent:400/24},{time:"05:00",percent:500/24},{time:"06:00",percent:600/24},{time:"07:00",percent:700/24},{time:"08:00",percent:800/24},{time:"09:00",percent:900/24},{time:"10:00",percent:1e3/24},{time:"11:00",percent:1100/24},{time:"12:00",percent:1200/24},{time:"13:00",percent:1300/24},{time:"14:00",percent:1400/24},{time:"15:00",percent:1500/24},{time:"16:00",percent:1600/24},{time:"17:00",percent:1700/24},{time:"18:00",percent:1800/24},{time:"19:00",percent:1900/24},{time:"20:00",percent:2e3/24},{time:"21:00",percent:2100/24},{time:"22:00",percent:2200/24},{time:"23:00",percent:2300/24}];return(d,k)=>(s(),o("div",W,[T(j),l.value?(s(),o("div",X,[T(G)])):D("",!0),l.value?D("",!0):(s(),o("div",Y,[a("div",Z,[(s(!0),o(v,null,h(i.value,c=>(s(),S(R,{key:c.date,date:c.date},null,8,["date"]))),128))]),a("div",ee,[(s(!0),o(v,null,h(i.value,c=>(s(),o("div",{class:"planner__day-column",key:c.date},[(s(!0),o(v,null,h(c.events,(f,L)=>(s(),S(O,{key:L,event:f},null,8,["event"]))),128))]))),128)),(s(),o(v,null,h(y,(c,f)=>a("div",{class:"planner__line",key:f,style:w({top:`${c.percent}%`})},[a("div",te,u(c.time),1)],4)),64)),a("div",{class:"planner__line planner__line--now",style:w({top:`${n.value.styleTop}`}),ref_key:"timeLineEl",ref:e},[a("div",ne,u(n.value.caption),1)],4)])]))]))}};export{se as default};
