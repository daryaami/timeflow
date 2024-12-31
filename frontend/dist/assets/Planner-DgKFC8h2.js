import{e as k,f,g as M,h as O,r as A,o as s,i as C,w as G,c as o,b as e,t as g,j as $,n as L,k as H,l as N,m as W,F as E,p as S,u as P,q as Y,s as Z,v as R,x as F,y as J,z as K,A as Q,_ as U,a as z,B as j,C as I,D as ee}from"./index-BlSklm8P.js";const te={key:0,class:"event-card__short-wrapper"},ne={class:"event-card__name"},ae={class:"event-card__time"},se={class:"event-card__name-wrapper"},re={key:1,class:"event-card__time"},le={__name:"EventCard",props:["card","gridHeight"],setup(r){const n=r,l=k(()=>(new Date(n.card.end)-new Date(n.card.start))/(1e3*60*60)),p=f(M(n.card.event.start.dateTime)),c=k(()=>O(n.card.start)*100/24),m=k(()=>Math.max(l.value,.25)*100/24),_=k(()=>`${p.value} - ${M(n.card.event.end.dateTime)}`),a=k(()=>new Date(n.card.event.end.dateTime)<new Date),i=k(()=>n.gridHeight?[10,n.gridHeight/96]:[0,0]),u=k(()=>n.card.overlapLevel?n.card.overlapLevel+1:1);return(v,T)=>{const x=A("vue-draggable-resizable");return r.gridHeight?(s(),C(x,{key:0,class:L(["event-card",{"no-padding":l.value<=.25,"no-right-padding":l.value<=.5,past:a.value,overlap:r.card.overlapLevel}]),axis:"y",grid:i.value,handles:["tm","bm"],active:!0,style:H({top:`${c.value}%`,height:`calc(${m.value}% - 2px)`,backgroundColor:`${r.card.event.background_color}`,color:`${r.card.event.foreground_color}`,width:`calc(100% - ${u.value*.75}rem)`})},{default:G(()=>[l.value<.75?(s(),o("div",te,[e("span",ne,g(r.card.event.summary)+", ",1),e("span",ae,g(p.value),1)])):$("",!0),e("div",se,[l.value>=.75?(s(),o("span",{key:0,class:L(["event-card__name",{"one-string":l.value<=1}])},g(r.card.event.summary),3)):$("",!0)]),l.value>=.75?(s(),o("span",re,g(_.value),1)):$("",!0)]),_:1},8,["grid","style","class"])):$("",!0)}}},oe=[{time:"01:00",percent:100/24},{time:"02:00",percent:200/24},{time:"03:00",percent:300/24},{time:"04:00",percent:400/24},{time:"05:00",percent:500/24},{time:"06:00",percent:600/24},{time:"07:00",percent:700/24},{time:"08:00",percent:800/24},{time:"09:00",percent:900/24},{time:"10:00",percent:1e3/24},{time:"11:00",percent:1100/24},{time:"12:00",percent:1200/24},{time:"13:00",percent:1300/24},{time:"14:00",percent:1400/24},{time:"15:00",percent:1500/24},{time:"16:00",percent:1600/24},{time:"17:00",percent:1700/24},{time:"18:00",percent:1800/24},{time:"19:00",percent:1900/24},{time:"20:00",percent:2e3/24},{time:"21:00",percent:2100/24},{time:"22:00",percent:2200/24},{time:"23:00",percent:2300/24}],ce={class:"planner-date__weekday"},ie={class:"planner-date__day"},de={__name:"PlannerDate",props:["day"],setup(r){return(n,l)=>(s(),o("div",{class:L(["planner-date",{current:r.day.isToday}])},[e("span",ce,g(r.day.weekday),1),e("div",ie,[e("span",null,g(r.day.date),1)])],2))}},ue={class:"planner__grid-wrapper"},ve={class:"planner__days-header"},_e={class:"planner__line-time"},pe={class:"planner__line-time"},me={__name:"PlannerGrid",props:["events","currentDate","selectedEvent"],emits:["cardClick"],setup(r,{emit:n}){const l=r,p=n,c=y=>{const h=y.sort((t,d)=>new Date(t.start)-new Date(d.start));for(let t=1;t<h.length;t++){const d=h[t],b=new Date(d.start);for(let D=t-1;D>=0;D--){const w=h[D];if(b>new Date(w.start)&&b<new Date(w.end)){w.overlapLevel?d.overlapLevel=w.overlapLevel+1:d.overlapLevel=1;break}}}return h},m=k(()=>{const y=Y(l.currentDate),h=[];for(let t=0;t<7;t++){const d=new Date(y);d.setDate(y.getDate()+t),h.push({weekday:d.toLocaleDateString("en-EN",{weekday:"short"}),date:d.getDate(),isToday:Z(d,new Date),day:d,cards:[]})}return l.events.forEach(t=>{if(!t.start.dateTime)return;const d=new Date(t.start.dateTime),b=new Date(t.end.dateTime);if(d.getDate()===b.getDate()){const D=h.find(V=>V.date===d.getDate());if(!D)return;const w={event:t,start:t.start.dateTime,end:t.end.dateTime};D.cards.push(w)}else{const D={event:t,start:t.start.dateTime,end:t.start.dateTime.replace(/T\d{2}:\d{2}:\d{2}/,"T23:59:00")},w=h.find(B=>B.date===d.getDate());w&&w.cards.push(D);const V={event:t,start:t.end.dateTime.replace(/T\d{2}:\d{2}:\d{2}/,"T00:00:00"),end:t.end.dateTime},X=h.find(B=>B.date===b.getDate());w&&X.cards.push(V)}}),h.forEach(t=>t.cards=c(t.cards)),h}),_=f(null),a=f(),i=f(null),u=f(null),v=f({caption:"",styleTop:""}),T=()=>{u.value.style.display="none";const y=document.querySelector(".planner-date.current");if(!y)return;const h=(y.getBoundingClientRect().left-i.value.getBoundingClientRect().left)/i.value.offsetWidth*100,t=y.offsetWidth*.9/i.value.offsetWidth*100;u.value.style.left=`${h}%`,u.value.style.width=`${t}%`,u.value.style.display="block"},x=()=>{const y=new Date;v.value.caption=M(y),v.value.styleTop=`${O(y)*100/24}%`},q=async()=>{x(),await W(),T(),i.value.scrollIntoView({block:"center"});const h=(60-new Date().getSeconds())*1e3;setTimeout(()=>{x(),setInterval(x,6e4)},h)};return N(async()=>{await W(),q(),a.value=_.value.offsetHeight}),(y,h)=>(s(),o("div",ue,[e("div",ve,[(s(!0),o(E,null,S(m.value,t=>(s(),C(de,{key:t.date,day:t},null,8,["day"]))),128))]),e("div",{class:"planner__grid",ref_key:"grid",ref:_},[(s(!0),o(E,null,S(m.value,t=>(s(),o("div",{class:"planner__day-column",key:t.date},[(s(!0),o(E,null,S(t.cards,(d,b)=>(s(),C(le,{key:b,card:d,gridHeight:a.value,onClick:D=>p("cardClick",d.event),class:L({selected:r.selectedEvent===d.event})},null,8,["card","gridHeight","onClick","class"]))),128))]))),128)),(s(!0),o(E,null,S(P(oe),(t,d)=>(s(),o("div",{class:"planner__line",key:d,style:H({top:`${t.percent}%`})},[e("div",_e,g(t.time),1)],4))),128)),e("div",{class:"planner__line planner__line--now",style:H({top:`${v.value.styleTop}`}),ref_key:"timeLineEl",ref:i},[e("div",pe,g(v.value.caption),1),e("div",{class:"planner__line-today-line",ref_key:"todayLine",ref:u},null,512)],4)],512)]))}},he={class:"planner-header"},fe={class:"planner-header__date"},ge={__name:"PlannerHeader",props:R(["isSidebarOpened","isLoading"],{modelValue:{},modelModifiers:{}}),emits:R(["prevWeek","nextWeek"],["update:modelValue"]),setup(r,{emit:n}){const l=F(),p=r,c=J(r,"modelValue"),m=k(()=>{if(l.date){const i=l.date;return`${i.toLocaleString("default",{month:"long"})} ${i.getFullYear()}`}else return""}),_=async()=>{p.isLoading||l.toNextWeek()},a=async()=>{p.isLoading||l.toPrevWeek()};return(i,u)=>(s(),o("header",he,[e("span",fe,g(m.value),1),e("div",{class:"planner-header__buttons"},[e("button",{class:"planner-header__date-button planner-header__date-button--prev icon-button",onClick:a}),e("button",{class:"planner-header__date-button planner-header__date-button--next icon-button",onClick:_})]),e("label",{class:L(["sidebar-hide icon-button",{rotated:!c.value}])},[K(e("input",{type:"checkbox",class:"visually-hidden","onUpdate:modelValue":u[0]||(u[0]=v=>c.value=v)},null,512),[[Q,c.value]])],2)]))}},ye={},ke={class:"loading-container"};function $e(r,n){return s(),o("div",ke,n[0]||(n[0]=[e("div",{class:"loading-progress"},null,-1)]))}const we=U(ye,[["render",$e]]),De={},be={width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg"};function Ce(r,n){return s(),o("svg",be,n[0]||(n[0]=[e("path",{d:"M20.7457 3.32854C20.3552 2.93801 19.722 2.93801 19.3315 3.32854L12.0371 10.6229L4.74275 3.32854C4.35223 2.93801 3.71906 2.93801 3.32854 3.32854C2.93801 3.71906 2.93801 4.35223 3.32854 4.74275L10.6229 12.0371L3.32856 19.3314C2.93803 19.722 2.93803 20.3551 3.32856 20.7457C3.71908 21.1362 4.35225 21.1362 4.74277 20.7457L12.0371 13.4513L19.3315 20.7457C19.722 21.1362 20.3552 21.1362 20.7457 20.7457C21.1362 20.3551 21.1362 19.722 20.7457 19.3315L13.4513 12.0371L20.7457 4.74275C21.1362 4.35223 21.1362 3.71906 20.7457 3.32854Z",fill:"currentColor"},null,-1)]))}const Le=U(De,[["render",Ce]]),Te={class:"event-info-sidebar"},xe={class:"event-info-sidebar__buttons-wrapper"},Ee={class:"event-info-sidebar__event-title"},Se={class:"event-characteristics"},Me={class:"event-characteristics__value"},He={class:"event-characteristics__value"},Ve={key:0},Be={class:"event-characteristics__value"},We={__name:"EventInfoSidebar",props:["event"],emits:["close"],setup(r,{emit:n}){const l=r,p=n,c=k(()=>{const _=new Date(l.event.start.dateTime),i=new Date(l.event.end.dateTime)-_,u=Math.floor(i/(1e3*60*60)),v=Math.floor(i%(1e3*60*60)/(1e3*60));return`${u} hr${u>1?"s":""}${v>0?` ${v} min`:""}`}),m=k(()=>{const _=new Date(l.event.start.dateTime),a=new Date(l.event.end.dateTime);return`${_.getDate()}/${_.getMonth()} ${M(_)} - ${M(a)}`});return(_,a)=>(s(),o("div",Te,[e("div",xe,[e("button",{class:"event-info-sidebar__button icon-button",onClick:a[0]||(a[0]=i=>p("close"))},[z(Le)])]),e("span",Ee,g(r.event.summary),1),e("ul",Se,[e("li",null,[a[1]||(a[1]=e("span",{class:"event-characteristics__name"},"Duration",-1)),e("span",Me,g(c.value),1)]),e("li",null,[a[2]||(a[2]=e("span",{class:"event-characteristics__name"},"Dates",-1)),e("span",He,g(m.value),1)]),r.event.calendar?(s(),o("li",Ve,[a[3]||(a[3]=e("span",{class:"event-characteristics__name"},"Calendar",-1)),e("span",Be,g(r.event.calendar),1)])):$("",!0)])]))}},Pe={class:"task"},ze=["for"],Ie=["id"],Ne={__name:"TaskItem",props:["task"],setup(r){return(n,l)=>(s(),o("div",Pe,[e("span",{class:"task__color",style:H({backgroundColor:r.task.color})},null,4),e("label",{class:"task__checkbox-label",for:n.title},[e("input",{class:"visually-hidden",id:n.title,type:"checkbox"},null,8,Ie)],8,ze),e("span",null,g(r.task.name),1)]))}},Re={class:"right-sidebar"},Oe={class:"right-sidebar__tabs"},Fe={class:"underline"},Ue={key:0,class:"tasks"},je={__name:"RightSidebar",setup(r){const n=f(),l=f();f(null);const p=f(null),c=f(null),m=f(j.value.tasks);return N(()=>{c.value=p.value}),I(c,()=>{n.value.style.transform=`translateX(${c.value.offsetLeft}px)`,l.value.style.transform=`translateX(${c.value.offsetLeft}px)`}),(_,a)=>(s(),o("div",Re,[e("div",Oe,[e("button",{ref_key:"tasksButton",ref:p,class:"right-sidebar__tab",onClick:a[0]||(a[0]=i=>c.value=p.value)},a[1]||(a[1]=[e("span",null,"Tasks",-1)]),512),e("div",Fe,[e("div",{ref_key:"underlineRight",ref:n,class:"underline__closer underline__closer--right"},null,512),e("div",{ref_key:"underlineLeft",ref:l,class:"underline__closer underline__closer--left"},null,512)])]),c.value===p.value?(s(),o("div",Ue,[(s(!0),o(E,null,S(m.value,i=>(s(),C(Ne,{key:i.id,task:i},null,8,["task"]))),128))])):$("",!0)]))}},qe={class:"planner-wrapper"},Xe={class:"planner"},Ae={key:0,class:"planner__loader-wrapper"},Ye={__name:"Planner",setup(r){const n=f(!0),l=f(),p=ee(),c=F(),m=f(!0),_=async u=>{m.value=!0;try{const v=await p.getEvents(u);l.value=v}catch(v){console.error("ошибка",v)}finally{m.value=!1,await W()}};I(c,u=>{_(u.date)}),I(p,()=>{_(c.date)}),N(()=>{_(c.date)});const a=f(null),i=u=>{a.value=u};return(u,v)=>(s(),o("div",qe,[e("div",Xe,[z(ge,{modelValue:n.value,"onUpdate:modelValue":v[0]||(v[0]=T=>n.value=T),isLoading:m.value},null,8,["modelValue","isLoading"]),m.value?(s(),o("div",Ae,[z(we)])):$("",!0),m.value?$("",!0):(s(),C(me,{key:1,events:l.value,"current-date":P(c).date,selectedEvent:a.value,onCardClick:i},null,8,["events","current-date","selectedEvent"]))]),P(j)?(s(),o("div",{key:0,class:L(["planner__right-sidebar",{hidden:!n.value}])},[a.value?$("",!0):(s(),C(je,{key:0})),a.value?(s(),C(We,{key:1,event:a.value,onClose:v[1]||(v[1]=T=>a.value=null)},null,8,["event"])):$("",!0)],2)):$("",!0)]))}};export{Ye as default};
