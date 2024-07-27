import{_ as S,o as n,c as a,b as t,n as L,e as p,t as u,f as w,g as $,h as b,i as m,j as H,a as T,k as x,F as v,l as h,m as D,p as B}from"./index-BSA1WZ6y.js";const V={props:{isSidebarHidden:Boolean},emits:{"update:isSidebarHidden":Boolean}},N={class:"planner-header"},C={class:"planner-header__date"},F=t("span",null,"February 2024",-1),P=t("div",{class:"planner-header__date-buttons"},[t("button",{class:"planner-header__date-button planner-header__date-button--prev"}),t("button",{class:"planner-header__date-button planner-header__date-button--next"})],-1);function j(s,e,r,i,_,o){return n(),a("header",N,[t("div",C,[F,P,t("button",{class:L(["sidebar-hide",{rotated:r.isSidebarHidden}]),onClick:e[0]||(e[0]=l=>s.$emit("update:isSidebarHidden",!r.isSidebarHidden))},null,2)])])}const z=S(V,[["render",j]]),I={},M={class:"loading-container"},U=t("div",{class:"loading-progress"},null,-1),q=[U];function A(s,e){return n(),a("div",M,q)}const G=S(I,[["render",A]]),J={class:"event-card__name"},K={class:"event-card__time"},O={__name:"EventCard",props:["event"],setup(s){const e=s,r=p(()=>$(e.event.start.dateTime)*100/24),i=p(()=>($(e.event.end.dateTime)-$(e.event.start.dateTime))*100/24),_=p(()=>`${b(e.event.start.dateTime)} - ${b(e.event.end.dateTime)}`);return(o,l)=>(n(),a("div",{class:"event-card",style:w({top:`${r.value}%`,height:`${i.value}%`})},[t("span",J,u(s.event.summary),1),t("span",K,u(_.value),1)],4))}},Q=async()=>{let s=await fetch(`${window.location.origin}/planner_api/get_events/`);if(s.ok)return(await s.json()).days;throw new Error("Failed to fetch events")},R={__name:"PlannerDate",props:["date"],setup(s){const e=s,[r,i,_]=e.date.split(".").map(Number),o=new Date(_,i-1,r),l=p(()=>`${o.toLocaleDateString("en-EN",{weekday:"short"})} ${o.getDate()}`),y=p(()=>new Date().getDate()===o.getDate());return(f,d)=>(n(),a("span",{class:L(["planner-date",{current:y.value}])},u(l.value),3))}},W={class:"planner"},X={key:0,class:"planner__loader-wrapper"},Y={key:1,class:"planner__grid-wrapper"},Z={class:"planner__days-header"},ee={class:"planner__grid"},te={class:"planner__line-time"},ne={class:"planner__line-time"},se={__name:"Planner",setup(s){const e=m(null),r=m({caption:"",styleTop:""}),i=()=>{const d=new Date;r.value.caption=b(d),r.value.styleTop=`${$(d)*100/24}%`},_=async()=>{i(),await B(),e.value.scrollIntoView({block:"center"});const k=(60-new Date().getSeconds())*1e3;setTimeout(()=>{i(),setInterval(i,6e4)},k)},o=m([]),l=m(!0),y=async()=>{try{o.value=await Q()}catch(d){console.error("ошибка",d)}finally{l.value=!1,_()}};H(()=>{y()});const f=[{time:"01:00",percent:100/24},{time:"02:00",percent:200/24},{time:"03:00",percent:300/24},{time:"04:00",percent:400/24},{time:"05:00",percent:500/24},{time:"06:00",percent:600/24},{time:"07:00",percent:700/24},{time:"08:00",percent:800/24},{time:"09:00",percent:900/24},{time:"10:00",percent:1e3/24},{time:"11:00",percent:1100/24},{time:"12:00",percent:1200/24},{time:"13:00",percent:1300/24},{time:"14:00",percent:1400/24},{time:"15:00",percent:1500/24},{time:"16:00",percent:1600/24},{time:"17:00",percent:1700/24},{time:"18:00",percent:1800/24},{time:"19:00",percent:1900/24},{time:"20:00",percent:2e3/24},{time:"21:00",percent:2100/24},{time:"22:00",percent:2200/24},{time:"23:00",percent:2300/24}];return(d,k)=>(n(),a("div",W,[T(z),l.value?(n(),a("div",X,[T(G)])):x("",!0),l.value?x("",!0):(n(),a("div",Y,[t("div",Z,[(n(!0),a(v,null,h(o.value,c=>(n(),D(R,{key:c.date,date:c.date},null,8,["date"]))),128))]),t("div",ee,[(n(!0),a(v,null,h(o.value,c=>(n(),a("div",{class:"planner__day-column",key:c.date},[(n(!0),a(v,null,h(c.events,(g,E)=>(n(),D(O,{key:E,event:g},null,8,["event"]))),128))]))),128)),(n(),a(v,null,h(f,(c,g)=>t("div",{class:"planner__line",key:g,style:w({top:`${c.percent}%`})},[t("div",te,u(c.time),1)],4)),64)),t("div",{class:"planner__line planner__line--now",style:w({top:`${r.value.styleTop}`}),ref_key:"timeLineEl",ref:e},[t("div",ne,u(r.value.caption),1)],4)])]))]))}};export{se as default};
