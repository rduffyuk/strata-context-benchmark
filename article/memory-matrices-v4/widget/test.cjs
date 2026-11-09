const assert=require('node:assert/strict');
const m=require('./model.js');
const ram=m.pool('ram'); assert.equal(ram.observed,34.00482177734375); assert.notEqual(ram.observed,38); assert.equal(ram.outside,28.55224609375); assert.equal(ram.outsideFree,false);
for(const [name,count,extent] of [['gpu',16,15.9921875],['ram',63,62.55706787109375],['ssd',64,63.35423609614372]]) {const p=m.pool(name);const cells=m.cells(p);assert.equal(cells.length,count);assert.ok(Math.abs(cells.reduce((a,c)=>a+c.extent,0)-extent)<1e-9);assert.ok(cells.at(-1).extent>0&&cells.at(-1).extent<1)}
assert.equal(m.pool('ssd').extent,63.35423609614372); assert.equal(m.pool('gpu').extent,15.9921875); assert.equal(m.pool('ram').extent,62.55706787109375); // copies overlap, file size is independent
assert.equal(m.theme('light',true),'light');assert.equal(m.theme('dark',false),'dark');assert.equal(m.theme(null,true),'dark');assert.equal(m.theme(null,false),'light');
const c=m.controller(true); c.setPool('ssd');c.setView(2); c.setToken(3);c.setContext(131072);c.setPlaying(true);assert.equal(c.state().pool,'ssd');assert.equal(c.state().view,2);assert.equal(c.state().playing,false);assert.equal(c.state().snapshot.contextFraction,.5); c.setPool('bogus');assert.equal(c.state().pool,'ssd');
for(let i=0;i<4;i++) assert.equal(new Set(m.experts(i)).size,10);
const x=m.snapshot(2048),y=m.snapshot(262144);assert.deepEqual(x.gpu,y.gpu);assert.deepEqual(x.ram,y.ram);assert.equal(x.contextFraction,1/128);assert.equal(y.contextFraction,1);
console.log('PASS: sampled RAM, non-free outside, pool cells and partial extents, independent copies, view/pool/theme/reduced-motion state, experts and fixed context allocation');
const fs=require('node:fs');const html=fs.readFileSync(__dirname+'/index.html','utf8');const js=fs.readFileSync(__dirname+'/widget.js','utf8');assert.match(html,/not a matched speed comparison/);assert.doesNotMatch(html,/8 GiB weights|12 GiB weights/);assert.match(js,/38 GiB was the configured ceiling/);console.log('PASS: no illustrative head-to-head and ceiling distinguished from use');
