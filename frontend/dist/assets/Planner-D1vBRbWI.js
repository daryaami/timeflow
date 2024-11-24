import{e as w,f as m,g as H,h as F,r as G,o as n,i as x,w as Y,c,b as e,t as f,j as D,n as M,k as W,l as V,m as Z,p as R,q as z,F as E,s as S,u as I,v as O,x as J,y as K,z as Q,_ as U,a as N,A as j,B as q,C as ee,D as T}from"./index-CzXVkN2P.js";const te={key:0,class:"event-card__short-wrapper"},ne={class:"event-card__name"},ae={class:"event-card__time"},se={class:"event-card__name-wrapper"},re={key:1,class:"event-card__time"},le={__name:"EventCard",props:["card","gridHeight"],setup(a){const s=a,r=w(()=>(new Date(s.card.end)-new Date(s.card.start))/(1e3*60*60)),o=m(H(s.card.event.start.dateTime)),v=w(()=>F(s.card.start)*100/24),_=w(()=>Math.max(r.value,.25)*100/24),u=w(()=>`${o.value} - ${H(s.card.event.end.dateTime)}`),h=w(()=>new Date(s.card.event.end.dateTime)<new Date),i=w(()=>s.gridHeight?[10,s.gridHeight/96]:[0,0]),k=w(()=>s.card.overlapLevel?s.card.overlapLevel+1:1);return(l,y)=>{const $=G("vue-draggable-resizable");return a.gridHeight?(n(),x($,{key:0,class:M(["event-card",{"no-padding":r.value<=.25,"no-right-padding":r.value<=.5,past:h.value,overlap:a.card.overlapLevel}]),axis:"y",grid:i.value,handles:["tm","bm"],active:!0,style:W({top:`${v.value}%`,height:`calc(${_.value}% - 2px)`,backgroundColor:`${a.card.event.background_color}`,color:`${a.card.event.foreground_color}`,width:`calc(100% - ${k.value*.75}rem)`})},{default:Y(()=>[r.value<.75?(n(),c("div",te,[e("span",ne,f(a.card.event.summary)+", ",1),e("span",ae,f(o.value),1)])):D("",!0),e("div",se,[r.value>=.75?(n(),c("span",{key:0,class:M(["event-card__name",{"one-string":r.value<=1}])},f(a.card.event.summary),3)):D("",!0)]),r.value>=.75?(n(),c("span",re,f(u.value),1)):D("",!0)]),_:1},8,["grid","style","class"])):D("",!0)}}},ce=[{time:"01:00",percent:100/24},{time:"02:00",percent:200/24},{time:"03:00",percent:300/24},{time:"04:00",percent:400/24},{time:"05:00",percent:500/24},{time:"06:00",percent:600/24},{time:"07:00",percent:700/24},{time:"08:00",percent:800/24},{time:"09:00",percent:900/24},{time:"10:00",percent:1e3/24},{time:"11:00",percent:1100/24},{time:"12:00",percent:1200/24},{time:"13:00",percent:1300/24},{time:"14:00",percent:1400/24},{time:"15:00",percent:1500/24},{time:"16:00",percent:1600/24},{time:"17:00",percent:1700/24},{time:"18:00",percent:1800/24},{time:"19:00",percent:1900/24},{time:"20:00",percent:2e3/24},{time:"21:00",percent:2100/24},{time:"22:00",percent:2200/24},{time:"23:00",percent:2300/24}],oe={class:"planner-date__weekday"},ie={class:"planner-date__day"},de={__name:"PlannerDate",props:["day"],setup(a){return(s,r)=>(n(),c("div",{class:M(["planner-date",{current:a.day.isToday}])},[e("span",oe,f(a.day.weekday),1),e("div",ie,[e("span",null,f(a.day.date),1)])],2))}},ue={class:"planner__grid-wrapper"},_e={class:"planner__days-header"},ve={class:"planner__line-time"},pe={class:"planner__line-time"},me={__name:"PlannerGrid",props:["events","currentDate","selectedEvent"],emits:["cardClick"],setup(a,{emit:s}){const r=a,o=s,v=g=>{const p=g.sort((t,d)=>new Date(t.start)-new Date(d.start));for(let t=1;t<p.length;t++){const d=p[t],L=new Date(d.start);for(let C=t-1;C>=0;C--){const b=p[C];if(L>new Date(b.start)&&L<new Date(b.end)){b.overlapLevel?d.overlapLevel=b.overlapLevel+1:d.overlapLevel=1;break}}}return p},_=w(()=>{const g=V(r.currentDate),p=[];for(let t=0;t<7;t++){const d=new Date(g);d.setDate(g.getDate()+t),p.push({weekday:d.toLocaleDateString("en-EN",{weekday:"short"}),date:d.getDate(),isToday:Z(d,new Date),day:d,cards:[]})}return r.events.forEach(t=>{if(!t.start.dateTime)return;const d=new Date(t.start.dateTime),L=new Date(t.end.dateTime);if(d.getDate()===L.getDate()){const C=p.find(B=>B.date===d.getDate());if(!C)return;const b={event:t,start:t.start.dateTime,end:t.end.dateTime};C.cards.push(b)}else{const C={event:t,start:t.start.dateTime,end:t.start.dateTime.replace(/T\d{2}:\d{2}:\d{2}/,"T23:59:00")},b=p.find(P=>P.date===d.getDate());b&&b.cards.push(C);const B={event:t,start:t.end.dateTime.replace(/T\d{2}:\d{2}:\d{2}/,"T00:00:00"),end:t.end.dateTime},A=p.find(P=>P.date===L.getDate());b&&A.cards.push(B)}}),p.forEach(t=>t.cards=v(t.cards)),p}),u=m(null),h=m(),i=m(null),k=m(null),l=m({caption:"",styleTop:""}),y=()=>{k.value.style.display="none";const g=document.querySelector(".planner-date.current");if(!g)return;const p=(g.getBoundingClientRect().left-i.value.getBoundingClientRect().left)/i.value.offsetWidth*100,t=g.offsetWidth*.9/i.value.offsetWidth*100;k.value.style.left=`${p}%`,k.value.style.width=`${t}%`,k.value.style.display="block"},$=()=>{const g=new Date;l.value.caption=H(g),l.value.styleTop=`${F(g)*100/24}%`},X=async()=>{$(),await z(),y(),i.value.scrollIntoView({block:"center"});const p=(60-new Date().getSeconds())*1e3;setTimeout(()=>{$(),setInterval($,6e4)},p)};return R(async()=>{await z(),X(),h.value=u.value.offsetHeight}),(g,p)=>(n(),c("div",ue,[e("div",_e,[(n(!0),c(E,null,S(_.value,t=>(n(),x(de,{key:t.date,day:t},null,8,["day"]))),128))]),e("div",{class:"planner__grid",ref_key:"grid",ref:u},[(n(!0),c(E,null,S(_.value,t=>(n(),c("div",{class:"planner__day-column",key:t.date},[(n(!0),c(E,null,S(t.cards,(d,L)=>(n(),x(le,{key:L,card:d,gridHeight:h.value,onClick:C=>o("cardClick",d.event),class:M({selected:a.selectedEvent===d.event})},null,8,["card","gridHeight","onClick","class"]))),128))]))),128)),(n(!0),c(E,null,S(I(ce),(t,d)=>(n(),c("div",{class:"planner__line",key:d,style:W({top:`${t.percent}%`})},[e("div",ve,f(t.time),1)],4))),128)),e("div",{class:"planner__line planner__line--now",style:W({top:`${l.value.styleTop}`}),ref_key:"timeLineEl",ref:i},[e("div",pe,f(l.value.caption),1),e("div",{class:"planner__line-today-line",ref_key:"todayLine",ref:k},null,512)],4)],512)]))}},he={class:"planner-header"},fe={class:"planner-header__date"},ye={class:"planner-header__buttons"},ge={__name:"PlannerHeader",props:O(["isSidebarOpened","currentMonth"],{modelValue:{},modelModifiers:{}}),emits:O(["prevWeek","nextWeek","updateEvents"],["update:modelValue"]),setup(a,{emit:s}){const r=s,o=J(a,"modelValue");return(v,_)=>(n(),c("header",he,[e("span",fe,f(a.currentMonth),1),e("div",ye,[e("button",{class:"planner-header__date-button planner-header__date-button--prev icon-button",onClick:_[0]||(_[0]=u=>r("prevWeek"))}),e("button",{class:"planner-header__date-button planner-header__date-button--next icon-button",onClick:_[1]||(_[1]=u=>r("nextWeek"))})]),e("label",{class:M(["sidebar-hide icon-button",{rotated:!o.value}])},[K(e("input",{type:"checkbox",class:"visually-hidden","onUpdate:modelValue":_[2]||(_[2]=u=>o.value=u)},null,512),[[Q,o.value]])],2)]))}},ke={},$e={class:"loading-container"},we=e("div",{class:"loading-progress"},null,-1),De=[we];function be(a,s){return n(),c("div",$e,De)}const Ce=U(ke,[["render",be]]),Te={},Le={width:"24",height:"24",viewBox:"0 0 24 24",fill:"none",xmlns:"http://www.w3.org/2000/svg"},xe=e("path",{d:"M20.7457 3.32854C20.3552 2.93801 19.722 2.93801 19.3315 3.32854L12.0371 10.6229L4.74275 3.32854C4.35223 2.93801 3.71906 2.93801 3.32854 3.32854C2.93801 3.71906 2.93801 4.35223 3.32854 4.74275L10.6229 12.0371L3.32856 19.3314C2.93803 19.722 2.93803 20.3551 3.32856 20.7457C3.71908 21.1362 4.35225 21.1362 4.74277 20.7457L12.0371 13.4513L19.3315 20.7457C19.722 21.1362 20.3552 21.1362 20.7457 20.7457C21.1362 20.3551 21.1362 19.722 20.7457 19.3315L13.4513 12.0371L20.7457 4.74275C21.1362 4.35223 21.1362 3.71906 20.7457 3.32854Z",fill:"currentColor"},null,-1),Me=[xe];function Ee(a,s){return n(),c("svg",Le,Me)}const Se=U(Te,[["render",Ee]]),He={class:"event-info-sidebar"},Ve={class:"event-info-sidebar__buttons-wrapper"},We={class:"event-info-sidebar__event-title"},Be={class:"event-characteristics"},Pe=e("span",{class:"event-characteristics__name"},"Duration",-1),ze={class:"event-characteristics__value"},Ie=e("span",{class:"event-characteristics__name"},"Dates",-1),Ne={class:"event-characteristics__value"},Re={key:0},Oe=e("span",{class:"event-characteristics__name"},"Calendar",-1),Fe={class:"event-characteristics__value"},Ue={__name:"EventInfoSidebar",props:["event"],emits:["close"],setup(a,{emit:s}){const r=a,o=s,v=w(()=>{const u=new Date(r.event.start.dateTime),i=new Date(r.event.end.dateTime)-u,k=Math.floor(i/(1e3*60*60)),l=Math.floor(i%(1e3*60*60)/(1e3*60));return`${k} hr${k>1?"s":""}${l>0?` ${l} min`:""}`}),_=w(()=>{const u=new Date(r.event.start.dateTime),h=new Date(r.event.end.dateTime);return`${u.getDate()}/${u.getMonth()} ${H(u)} - ${H(h)}`});return(u,h)=>(n(),c("div",He,[e("div",Ve,[e("button",{class:"event-info-sidebar__button icon-button",onClick:h[0]||(h[0]=i=>o("close"))},[N(Se)])]),e("span",We,f(a.event.summary),1),e("ul",Be,[e("li",null,[Pe,e("span",ze,f(v.value),1)]),e("li",null,[Ie,e("span",Ne,f(_.value),1)]),a.event.calendar?(n(),c("li",Re,[Oe,e("span",Fe,f(a.event.calendar),1)])):D("",!0)])]))}},je={class:"task"},qe=["for"],Xe=["id"],Ae={__name:"TaskItem",props:["task"],setup(a){return(s,r)=>(n(),c("div",je,[e("span",{class:"task__color",style:W({backgroundColor:a.task.color})},null,4),e("label",{class:"task__checkbox-label",for:s.title},[e("input",{class:"visually-hidden",id:s.title,type:"checkbox"},null,8,Xe)],8,qe),e("span",null,f(a.task.name),1)]))}},Ge={class:"right-sidebar"},Ye={class:"right-sidebar__tabs"},Ze=e("span",null,"Tasks",-1),Je=[Ze],Ke={class:"underline"},Qe={key:0,class:"tasks"},et={__name:"RightSidebar",setup(a){const s=m(),r=m();m(null);const o=m(null),v=m(null),_=m(j.value.tasks);return R(()=>{v.value=o.value}),q(v,()=>{s.value.style.transform=`translateX(${v.value.offsetLeft}px)`,r.value.style.transform=`translateX(${v.value.offsetLeft}px)`}),(u,h)=>(n(),c("div",Ge,[e("div",Ye,[e("button",{ref_key:"tasksButton",ref:o,class:"right-sidebar__tab",onClick:h[0]||(h[0]=i=>v.value=o.value)},Je,512),e("div",Ke,[e("div",{ref_key:"underlineRight",ref:s,class:"underline__closer underline__closer--right"},null,512),e("div",{ref_key:"underlineLeft",ref:r,class:"underline__closer underline__closer--left"},null,512)])]),v.value===o.value?(n(),c("div",Qe,[(n(!0),c(E,null,S(_.value,i=>(n(),x(Ae,{key:i.id,task:i},null,8,["task"]))),128))])):D("",!0)]))}},tt={class:"planner-wrapper"},nt={class:"planner"},at={key:0,class:"planner__loader-wrapper"},rt={__name:"Planner",setup(a){const s=m(!0),r=m(),o=m(!0),v=async(l=new Date)=>{o.value=!0;const y=V(l);try{const $=await ee.get(y);r.value=$}catch($){console.error("ошибка",$)}finally{o.value=!1,await z()}},_=async()=>{if(o.value)return;const l=T.value,y=V(new Date(l.setDate(l.getDate()+7)));T.value=y},u=async()=>{if(o.value)return;const l=T.value,y=V(new Date(l.setDate(l.getDate()-7)));T.value=y};q(T,l=>{l&&v(T.value)});const h=w(()=>{if(T.value){const l=T.value;return`${l.toLocaleString("default",{month:"long"})} ${l.getFullYear()}`}else return""});R(()=>{v()});const i=m(null),k=l=>{i.value=l};return(l,y)=>(n(),c("div",tt,[e("div",nt,[N(ge,{modelValue:s.value,"onUpdate:modelValue":y[0]||(y[0]=$=>s.value=$),currentMonth:h.value,onPrevWeek:u,onNextWeek:_},null,8,["modelValue","currentMonth"]),o.value?(n(),c("div",at,[N(Ce)])):D("",!0),o.value?D("",!0):(n(),x(me,{key:1,events:r.value,"current-date":I(T),selectedEvent:i.value,onCardClick:k},null,8,["events","current-date","selectedEvent"]))]),I(j)?(n(),c("div",{key:0,class:M(["planner__right-sidebar",{hidden:!s.value}])},[i.value?D("",!0):(n(),x(et,{key:0})),i.value?(n(),x(Ue,{key:1,event:i.value,onClose:y[1]||(y[1]=$=>i.value=null)},null,8,["event"])):D("",!0)],2)):D("",!0)]))}};export{rt as default};
