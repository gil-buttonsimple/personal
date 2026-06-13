// Shared apex-key drawer. Renders the property outline north-up with the four
// outer tips labelled, into an <svg> using a viewBox so it scales crisply to any
// size (standalone page or embedded floating panel). drawApexKey(svgEl).
(function(global){
 var PTS=[
  [34.6495527,-81.1523474],[34.6536156,-81.1568293],[34.6601593,-81.1640557],
  [34.6602285,-81.1639634],[34.6614509,-81.1623321],[34.6627292,-81.1637436],
  [34.6677877,-81.1569951],[34.6726967,-81.1534565],[34.6701087,-81.1513568],
  [34.6697552,-81.1504037],[34.6679685,-81.1507564],[34.6676831,-81.1494846],
  [34.6669591,-81.1494366],[34.6662387,-81.1495769],[34.6661748,-81.1495278],
  [34.6661226,-81.1494438],[34.6659990,-81.1494844],[34.6657248,-81.1494687],
  [34.6656399,-81.1495002],[34.6655156,-81.1494813],[34.6654462,-81.1495285],
  [34.6653266,-81.1495547],[34.6651742,-81.1494303],[34.6649675,-81.1492525],
  [34.6649649,-81.1491757],[34.6633606,-81.1493578],[34.6629126,-81.1492898],
  [34.6618783,-81.1489730],[34.6621229,-81.1499263],[34.6625455,-81.1515752],
  [34.6610315,-81.1521945],[34.6579598,-81.1534454],[34.6546086,-81.1548209],
  [34.6530302,-81.1493460],[34.6530003,-81.1492423],[34.6529604,-81.1492812],
  [34.6528464,-81.1494119],[34.6525019,-81.1498402],[34.6522948,-81.1500943],
  [34.6520949,-81.1503260],[34.6510338,-81.1514756],[34.6508461,-81.1516602],
  [34.6508878,-81.1518282],[34.6495527,-81.1523474]
 ];
 var APEX={7:{c:'#d62828',t:'NORTH'},0:{c:'#1f6f3d',t:'SOUTH'},27:{c:'#1d6fb8',t:'EAST'},2:{c:'#b8860b',t:'WEST'}};
 var WEST_INNER=3;
 var NS='http://www.w3.org/2000/svg';
 function el(tag,at){var e=document.createElementNS(NS,tag);for(var k in at)e.setAttribute(k,at[k]);return e;}

 global.drawApexKey=function(svg){
  while(svg.firstChild)svg.removeChild(svg.firstChild);
  var BW=360, M=42;
  var latMid=PTS.reduce(function(s,p){return s+p[0];},0)/PTS.length;
  var mLon=Math.cos(latMid*Math.PI/180)*111320, mLat=111320;
  var xs=PTS.map(function(p){return p[1]*mLon;}), ys=PTS.map(function(p){return p[0]*mLat;});
  var x0=Math.min.apply(null,xs),x1=Math.max.apply(null,xs),y0=Math.min.apply(null,ys),y1=Math.max.apply(null,ys);
  var sc=(BW-2*M)/(x1-x0), BH=(y1-y0)*sc+2*M;
  svg.setAttribute('viewBox','0 0 '+BW.toFixed(0)+' '+BH.toFixed(0));
  function X(p){return M+(p[1]*mLon-x0)*sc;}
  function Y(p){return BH-M-(p[0]*mLat-y0)*sc;}      // flip: north up

  // outline
  var d=PTS.map(function(p,i){return (i?'L':'M')+X(p).toFixed(1)+' '+Y(p).toFixed(1);}).join(' ')+' Z';
  svg.appendChild(el('path',{d:d,fill:'#e7e2d4',stroke:'#333','stroke-width':2,'stroke-linejoin':'round'}));

  // north arrow
  var ax=BW-26, ay=34;
  svg.appendChild(el('line',{x1:ax,y1:ay+22,x2:ax,y2:ay-12,stroke:'#333','stroke-width':2}));
  svg.appendChild(el('path',{d:'M'+(ax-5)+' '+(ay-6)+' L'+ax+' '+(ay-16)+' L'+(ax+5)+' '+(ay-6)+' Z',fill:'#333'}));
  var nt=el('text',{x:ax,y:ay+36,'text-anchor':'middle','font-size':12,'font-weight':'bold',fill:'#333'});nt.textContent='N';svg.appendChild(nt);

  // 500 m scale bar
  var sb=500*sc, sx=M, sy=BH-16;
  svg.appendChild(el('line',{x1:sx,y1:sy,x2:sx+sb,y2:sy,stroke:'#333','stroke-width':2}));
  svg.appendChild(el('line',{x1:sx,y1:sy-3,x2:sx,y2:sy+3,stroke:'#333','stroke-width':2}));
  svg.appendChild(el('line',{x1:sx+sb,y1:sy-3,x2:sx+sb,y2:sy+3,stroke:'#333','stroke-width':2}));
  var st=el('text',{x:sx+sb/2,y:sy-6,'text-anchor':'middle','font-size':11,fill:'#333'});st.textContent='500 m';svg.appendChild(st);

  // west second-point hint
  var wi=PTS[WEST_INNER];
  svg.appendChild(el('circle',{cx:X(wi),cy:Y(wi),r:4,fill:'none',stroke:'#b8860b','stroke-width':1.5,'stroke-dasharray':'2,2'}));

  // apex markers + labels
  Object.keys(APEX).forEach(function(i){
   var p=PTS[i],a=APEX[i];
   svg.appendChild(el('circle',{cx:X(p),cy:Y(p),r:7,fill:a.c,stroke:'#fff','stroke-width':2}));
   var dx=(a.t[0]==='E')?-12:(a.t[0]==='W'?12:0);
   var anchor=(a.t[0]==='E')?'end':(a.t[0]==='W'?'start':'middle');
   var dy=(a.t[0]==='N')?-13:(a.t[0]==='S'?22:4);
   var tx=el('text',{x:X(p)+dx,y:Y(p)+dy,'text-anchor':anchor,'font-size':13,'font-weight':'bold',fill:a.c});
   tx.textContent=a.t;svg.appendChild(tx);
  });
  var wp=PTS[2];
  var cap=el('text',{x:X(wp)+12,y:Y(wp)+18,'font-size':10,fill:'#7a5c08'});
  cap.textContent='(pick outer of two)';svg.appendChild(cap);
 };
})(window);
