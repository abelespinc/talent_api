import{R as l,T as m}from"./vendor-535dae5b.js";function d(o){let r={};for(const[t,s]of Object.entries(o))typeof s=="object"?r={...r,...d(s)}:r[t]=s;return r}function v(o){return Object.fromEntries(Object.entries(o).filter(([r,t])=>![void 0,null,"",NaN].includes(t)))}const i=100,u=0,I={isLoading:!1,isError:!1,isSuccess:!1,moreDataAvailable:!0,data:[],error:void 0,totalCount:void 0,params:{limit:i,offset:u}};function L(o,r={}){const t=l({...structuredClone(I),params:{limit:i,offset:u,...r}}),s=(a=!1)=>(t.isLoading=!0,a&&(t.params.offset=r.offset||0),o(t.params).then(e=>{if(a&&(t.data.length=0),t.isSuccess=!0,t.data.push(...e.results),t.moreDataAvailable=!!e.next,t.totalCount=e.count,e.next){const f=Number.parseInt(new URL(e.next).searchParams.get("offset"));t.params.offset=f||t.params.offset}return Promise.resolve(e)}).catch(e=>(t.isError=!0,t.error=e,Promise.reject(e))).finally(()=>{t.isLoading=!1})),c=a=>new Promise(e=>{const f=()=>{s().then(n=>{a==null||a(n.results),n.next?f():e(t.data)})};f()});return{...m(t),fetchNextPage:s,fetchAllPages:c}}export{d as f,v as p,L as u};