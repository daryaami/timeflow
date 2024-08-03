import{_ as S,o as n,c as r,b as e,n as B,e as f,t as v,f as g,g as k,h as D,i as d,j as C,k as H,l as V,F as m,m as h,p as b,q as y,a as L,u as T,s as x,v as N}from"./index-BPgzdxJw.js";const F={props:{isSidebarHidden:Boolean},emits:{"update:isSidebarHidden":Boolean}},I={class:"planner-header"},P={class:"planner-header__date"},R=e("span",null,"February 2024",-1),j=e("div",{class:"planner-header__date-buttons"},[e("button",{class:"planner-header__date-button planner-header__date-button--prev"}),e("button",{class:"planner-header__date-button planner-header__date-button--next"})],-1);function z(a,t,o,i,c,s){return n(),r("header",I,[e("div",P,[R,j,e("button",{class:B(["sidebar-hide",{rotated:o.isSidebarHidden}]),onClick:t[0]||(t[0]=p=>a.$emit("update:isSidebarHidden",!o.isSidebarHidden))},null,2)])])}const M=S(F,[["render",z]]),X={},q={class:"loading-container"},U=e("div",{class:"loading-progress"},null,-1),A=[U];function G(a,t){return n(),r("div",q,A)}const J=S(X,[["render",G]]),K={class:"event-card__name"},O={class:"event-card__time"},Q={__name:"EventCard",props:["event"],setup(a){const t=a,o=f(()=>k(t.event.start.dateTime)*100/24),i=f(()=>(k(t.event.end.dateTime)-k(t.event.start.dateTime))*100/24),c=f(()=>`${D(t.event.start.dateTime)} - ${D(t.event.end.dateTime)}`);return(s,p)=>(n(),r("div",{class:"event-card",style:g({top:`${o.value}%`,height:`calc(${i.value}% - 2px)`,backgroundColor:`${a.event.background_color}`,color:`${a.event.foreground_color}`})},[e("span",K,v(a.event.summary),1),e("span",O,v(c.value),1)],4))}},W=async()=>{let a=await fetch(`${window.location.origin}/planner_api/get_events/`);if(a.ok)return(await a.json()).days;throw new Error("Failed to fetch events")},Y={__name:"PlannerDate",props:["date"],setup(a){const t=a,[o,i,c]=t.date.split(".").map(Number),s=new Date(c,i-1,o),p=f(()=>`${s.toLocaleDateString("en-EN",{weekday:"short"})} ${s.getDate()}`),$=f(()=>new Date().getDate()===s.getDate());return(l,_)=>(n(),r("span",{class:B(["planner-date",{current:$.value}])},v(p.value),3))}},Z={class:"task"},ee=["for"],te=["id"],ne={__name:"TaskItem",props:["task"],setup(a){return(t,o)=>(n(),r("div",Z,[e("span",{class:"task__color",style:g({backgroundColor:a.task.color})},null,4),e("label",{class:"task__checkbox-label",for:t.title},[e("input",{class:"visually-hidden",id:t.title,type:"checkbox"},null,8,te)],8,ee),e("span",null,v(a.task.name),1)]))}},se={class:"right-sidebar"},ae={class:"right-sidebar__tabs"},re=e("span",null,"Habits",-1),oe=[re],le=e("span",null,"Tasks",-1),ie=[le],ce={class:"underline"},de={key:0,class:"tasks"},_e={__name:"RightSidebar",setup(a){const t=d(),o=d(),i=d(null),c=d(null),s=d(null),p=d(C.value.tasks);return H(()=>{console.log(i)}),V(s,()=>{t.value.style.transform=`translateX(${s.value.offsetLeft}px)`,o.value.style.transform=`translateX(${s.value.offsetLeft}px)`}),s.value=c.value,($,l)=>(n(),r("div",se,[e("div",ae,[e("button",{ref_key:"habitsButton",ref:i,class:"right-sidebar__tab",onClick:l[0]||(l[0]=_=>s.value=i.value)},oe,512),e("button",{ref_key:"tasksButton",ref:c,class:"right-sidebar__tab",onClick:l[1]||(l[1]=_=>s.value=c.value)},ie,512),e("div",ce,[e("div",{ref_key:"underlineRight",ref:t,class:"underline__closer underline__closer--right"},null,512),e("div",{ref_key:"underlineLeft",ref:o,class:"underline__closer underline__closer--left"},null,512)])]),s.value===c.value?(n(),r("div",de,[(n(!0),r(m,null,h(p.value,_=>(n(),b(ne,{key:_.id,task:_},null,8,["task"]))),128))])):y("",!0)]))}},ue={class:"planner-wrapper"},pe={class:"planner"},ve={key:0,class:"planner__loader-wrapper"},me={key:1,class:"planner__grid-wrapper"},he={class:"planner__days-header"},fe={class:"planner__grid"},$e={class:"planner__line-time"},ke={class:"planner__line-time"},ye={__name:"Planner",setup(a){const t=d(null),o=d({caption:"",styleTop:""}),i=()=>{const l=new Date;o.value.caption=D(l),o.value.styleTop=`${k(l)*100/24}%`},c=async()=>{i(),await N(),t.value.scrollIntoView({block:"center"});const _=(60-new Date().getSeconds())*1e3;setTimeout(()=>{i(),setInterval(i,6e4)},_)},s=d(!0),p=async()=>{try{x.value=await W()}catch(l){console.error("ошибка",l)}finally{s.value=!1,c()}};H(()=>{p()});const $=[{time:"01:00",percent:100/24},{time:"02:00",percent:200/24},{time:"03:00",percent:300/24},{time:"04:00",percent:400/24},{time:"05:00",percent:500/24},{time:"06:00",percent:600/24},{time:"07:00",percent:700/24},{time:"08:00",percent:800/24},{time:"09:00",percent:900/24},{time:"10:00",percent:1e3/24},{time:"11:00",percent:1100/24},{time:"12:00",percent:1200/24},{time:"13:00",percent:1300/24},{time:"14:00",percent:1400/24},{time:"15:00",percent:1500/24},{time:"16:00",percent:1600/24},{time:"17:00",percent:1700/24},{time:"18:00",percent:1800/24},{time:"19:00",percent:1900/24},{time:"20:00",percent:2e3/24},{time:"21:00",percent:2100/24},{time:"22:00",percent:2200/24},{time:"23:00",percent:2300/24}];return(l,_)=>(n(),r("div",ue,[e("div",pe,[L(M),s.value?(n(),r("div",ve,[L(J)])):y("",!0),s.value?y("",!0):(n(),r("div",me,[e("div",he,[(n(!0),r(m,null,h(T(x),u=>(n(),b(Y,{key:u.date,date:u.date},null,8,["date"]))),128))]),e("div",fe,[(n(!0),r(m,null,h(T(x),u=>(n(),r("div",{class:"planner__day-column",key:u.date},[(n(!0),r(m,null,h(u.events,(w,E)=>(n(),b(Q,{key:E,event:w},null,8,["event"]))),128))]))),128)),(n(),r(m,null,h($,(u,w)=>e("div",{class:"planner__line",key:w,style:g({top:`${u.percent}%`})},[e("div",$e,v(u.time),1)],4)),64)),e("div",{class:"planner__line planner__line--now",style:g({top:`${o.value.styleTop}`}),ref_key:"timeLineEl",ref:t},[e("div",ke,v(o.value.caption),1)],4)])]))]),T(C)?(n(),b(_e,{key:0})):y("",!0)]))}};export{ye as default};
