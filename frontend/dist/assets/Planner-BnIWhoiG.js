import{e as _,g as T,f as S,h as $,r as I,o as l,i as D,w as N,c,b as t,t as m,j as f,n as x,k as L,l as B,m as C,F as b,p as w,u as P,q as E,s as R,v as F,x as U,_ as q,y as z,z as X,a as M,A as V,B as O,C as H}from"./index-Btb7Gxzh.js";const j={key:0,class:"event-card__short-wrapper"},A={class:"event-card__name"},G={class:"event-card__time"},Y={class:"event-card__name-wrapper"},J={key:1,class:"event-card__time"},K={__name:"EventCard",props:["event","gridHeight"],setup(i){const a=i,n=_(T(a.event.end.dateTime)-T(a.event.start.dateTime)),s=_(S(a.event.start.dateTime)),d=$(()=>T(a.event.start.dateTime)*100/24),o=$(()=>Math.max(n.value,.25)*100/24),v=$(()=>`${s.value} - ${S(a.event.end.dateTime)}`),h=$(()=>new Date(a.event.end.dateTime)<new Date),p=$(()=>a.gridHeight?[10,a.gridHeight/96]:[0,0]);return(e,u)=>{const r=I("vue-draggable-resizable");return i.gridHeight?(l(),D(r,{key:0,class:x(["event-card",{"no-padding":n.value<=.25,"no-right-padding":n.value<=.5,past:h.value}]),axis:"y",grid:p.value,handles:["tm","bm"],active:!0,style:L({top:`${d.value}%`,height:`calc(${o.value}% - 2px)`,backgroundColor:`${i.event.background_color}`,color:`${i.event.foreground_color}`})},{default:N(()=>[n.value<=.5?(l(),c("div",j,[t("span",A,m(i.event.summary)+", ",1),t("span",G,m(s.value),1)])):f("",!0),t("div",Y,[n.value>.5?(l(),c("span",{key:0,class:x(["event-card__name",{"one-string":n.value<=1}])},m(i.event.summary),3)):f("",!0)]),n.value>.5?(l(),c("span",J,m(v.value),1)):f("",!0)]),_:1},8,["grid","style","class"])):f("",!0)}}},Q=[{time:"01:00",percent:100/24},{time:"02:00",percent:200/24},{time:"03:00",percent:300/24},{time:"04:00",percent:400/24},{time:"05:00",percent:500/24},{time:"06:00",percent:600/24},{time:"07:00",percent:700/24},{time:"08:00",percent:800/24},{time:"09:00",percent:900/24},{time:"10:00",percent:1e3/24},{time:"11:00",percent:1100/24},{time:"12:00",percent:1200/24},{time:"13:00",percent:1300/24},{time:"14:00",percent:1400/24},{time:"15:00",percent:1500/24},{time:"16:00",percent:1600/24},{time:"17:00",percent:1700/24},{time:"18:00",percent:1800/24},{time:"19:00",percent:1900/24},{time:"20:00",percent:2e3/24},{time:"21:00",percent:2100/24},{time:"22:00",percent:2200/24},{time:"23:00",percent:2300/24}],Z={class:"planner__line-time"},ee={class:"planner__line-time"},te={__name:"PlannerGrid",props:["days"],setup(i){const a=_(null),n=_(),s=_(null),d=_(null),o=_({caption:"",styleTop:""}),v=()=>{d.value.style.display="none";const e=document.querySelector(".planner-date.current");if(!e)return;const u=(e.getBoundingClientRect().left-s.value.getBoundingClientRect().left)/s.value.offsetWidth*100,r=e.offsetWidth*.9/s.value.offsetWidth*100;d.value.style.left=`${u}%`,d.value.style.width=`${r}%`,d.value.style.display="block"},h=()=>{const e=new Date;o.value.caption=S(e),o.value.styleTop=`${T(e)*100/24}%`},p=async()=>{h(),await C(),v(),s.value.scrollIntoView({block:"center"});const u=(60-new Date().getSeconds())*1e3;setTimeout(()=>{h(),setInterval(h,6e4)},u)};return B(async()=>{await C(),p(),n.value=a.value.offsetHeight}),(e,u)=>(l(),c("div",{class:"planner__grid",ref_key:"grid",ref:a},[(l(!0),c(b,null,w(i.days,r=>(l(),c("div",{class:"planner__day-column",key:r.date},[(l(!0),c(b,null,w(r.events,(k,y)=>(l(),D(K,{key:y,event:k,gridHeight:n.value},null,8,["event","gridHeight"]))),128))]))),128)),(l(!0),c(b,null,w(P(Q),(r,k)=>(l(),c("div",{class:"planner__line",key:k,style:L({top:`${r.percent}%`})},[t("div",Z,m(r.time),1)],4))),128)),t("div",{class:"planner__line planner__line--now",style:L({top:`${o.value.styleTop}`}),ref_key:"timeLineEl",ref:s},[t("div",ee,m(o.value.caption),1),t("div",{class:"planner__line-today-line",ref_key:"todayLine",ref:d},null,512)],4)],512))}},ne={class:"planner-header"},ae={class:"planner-header__date"},se={class:"planner-header__buttons"},le={__name:"PlannerHeader",props:E(["isSidebarOpened","currentMonth"],{modelValue:{},modelModifiers:{}}),emits:E(["prevWeek","nextWeek"],["update:modelValue"]),setup(i,{emit:a}){const n=a,s=R(i,"modelValue");return(d,o)=>(l(),c("header",ne,[t("span",ae,m(i.currentMonth),1),t("div",se,[t("button",{class:"planner-header__date-button planner-header__date-button--prev icon-button",onClick:o[0]||(o[0]=v=>n("prevWeek"))}),t("button",{class:"planner-header__date-button planner-header__date-button--next icon-button",onClick:o[1]||(o[1]=v=>n("nextWeek"))})]),t("label",{class:x(["sidebar-hide icon-button",{rotated:!s.value}])},[F(t("input",{type:"checkbox",class:"visually-hidden","onUpdate:modelValue":o[2]||(o[2]=v=>s.value=v)},null,512),[[U,s.value]])],2)]))}},re={},oe={class:"loading-container"},ie=t("div",{class:"loading-progress"},null,-1),ce=[ie];function de(i,a){return l(),c("div",oe,ce)}const ue=q(re,[["render",de]]),_e={class:"planner-date__weekday"},ve={class:"planner-date__day"},pe={__name:"PlannerDate",props:["day"],setup(i){return(a,n)=>(l(),c("div",{class:x(["planner-date",{current:i.day.isToday}])},[t("span",_e,m(i.day.weekday),1),t("div",ve,[t("span",null,m(i.day.date),1)])],2))}},me={class:"task"},ye=["for"],he=["id"],fe={__name:"TaskItem",props:["task"],setup(i){return(a,n)=>(l(),c("div",me,[t("span",{class:"task__color",style:L({backgroundColor:i.task.color})},null,4),t("label",{class:"task__checkbox-label",for:a.title},[t("input",{class:"visually-hidden",id:a.title,type:"checkbox"},null,8,he)],8,ye),t("span",null,m(i.task.name),1)]))}},ge={class:"right-sidebar__tabs"},ke=t("span",null,"Habits",-1),$e=[ke],be=t("span",null,"Tasks",-1),we=[be],De={class:"underline"},xe={key:0,class:"tasks"},Te={__name:"RightSidebar",props:["isOpened"],setup(i){const a=_(),n=_(),s=_(null),d=_(null),o=_(null),v=_(z.value.tasks);return B(()=>{o.value=d.value}),X(o,()=>{a.value.style.transform=`translateX(${o.value.offsetLeft}px)`,n.value.style.transform=`translateX(${o.value.offsetLeft}px)`}),(h,p)=>(l(),c("div",{class:x(["right-sidebar",{hidden:!i.isOpened}])},[t("div",ge,[t("button",{ref_key:"habitsButton",ref:s,class:"right-sidebar__tab",onClick:p[0]||(p[0]=e=>o.value=s.value)},$e,512),t("button",{ref_key:"tasksButton",ref:d,class:"right-sidebar__tab",onClick:p[1]||(p[1]=e=>o.value=d.value)},we,512),t("div",De,[t("div",{ref_key:"underlineRight",ref:a,class:"underline__closer underline__closer--right"},null,512),t("div",{ref_key:"underlineLeft",ref:n,class:"underline__closer underline__closer--left"},null,512)])]),o.value===d.value?(l(),c("div",xe,[(l(!0),c(b,null,w(v.value,e=>(l(),D(fe,{key:e.id,task:e},null,8,["task"]))),128))])):f("",!0)],2))}},Le={class:"planner-wrapper"},Ce={class:"planner"},Me={key:0,class:"planner__loader-wrapper"},Ve={key:1,class:"planner__grid-wrapper"},He={class:"planner__days-header"},Be={__name:"Planner",setup(i){const a=_(!0),n=_([]),s=_(!0),d=(e,u)=>{const r=e.getDay(),k=new Date(e.setDate(e.getDate()-r+1));n.value=[];for(let y=0;y<7;y++){const g=new Date(k);g.setDate(k.getDate()+y),n.value.push({weekday:g.toLocaleDateString("en-EN",{weekday:"short"}),date:g.getDate(),isToday:H(g,new Date),day:g,events:[]})}n.value.forEach(y=>{const g=u.filter(W=>H(y.day,new Date(W.start.dateTime))||H(y.day,new Date(W.end.dateTime)));y.events=g}),console.log(n.value)},o=async()=>{try{const e=await V();d(new Date,e)}catch(e){console.error("ошибка",e)}finally{s.value=!1}},v=async()=>{if(s.value)return;s.value=!0;const e=n.value[0].day,u=new Date(e.setDate(e.getDate()+7));try{const r=await V(O(u));d(u,r)}catch(r){console.error("ошибка",r)}finally{s.value=!1,await C(),timeLineEl.value.scrollIntoView({block:"center"})}},h=async()=>{if(s.value)return;s.value=!0;const e=n.value[0].day,u=new Date(e.setDate(e.getDate()-7));try{const r=await V(O(u));d(u,r)}catch(r){console.error("ошибка",r)}finally{s.value=!1,await C(),timeLineEl.value.scrollIntoView({block:"center"})}},p=$(()=>{if(n.value.length){const e=n.value[0].day;return`${e.toLocaleString("default",{month:"long"})} ${e.getFullYear()}`}else return""});return B(()=>{o()}),(e,u)=>(l(),c("div",Le,[t("div",Ce,[M(le,{modelValue:a.value,"onUpdate:modelValue":u[0]||(u[0]=r=>a.value=r),currentMonth:p.value,onPrevWeek:h,onNextWeek:v},null,8,["modelValue","currentMonth"]),s.value?(l(),c("div",Me,[M(ue)])):f("",!0),s.value?f("",!0):(l(),c("div",Ve,[t("div",He,[(l(!0),c(b,null,w(n.value,r=>(l(),D(pe,{key:r.date,day:r},null,8,["day"]))),128))]),M(te,{days:n.value},null,8,["days"])]))]),P(z)?(l(),D(Te,{key:0,isOpened:a.value},null,8,["isOpened"])):f("",!0)]))}};export{Be as default};
