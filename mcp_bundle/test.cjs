"use strict";
const assert=require("node:assert/strict");
const path=require("node:path");
const {Client}=require("@modelcontextprotocol/sdk/client/index.js");
const {StdioClientTransport}=require("@modelcontextprotocol/sdk/client/stdio.js");
async function main(){
 const client=new Client({name:"catalog-smoke-test",version:"1.0.0"});
 const transport=new StdioClientTransport({command:process.execPath,args:[path.join(__dirname,"server","index.cjs")],env:{PATH:process.env.PATH||""}});
 await client.connect(transport);
 try{
  const {tools}=await client.listTools();
  assert.deepEqual(tools.map(t=>t.name).sort(),["get_challenge","get_research_status","list_challenges"]);
  assert.ok(tools.every(t=>t.annotations.readOnlyHint&&!t.annotations.destructiveHint&&!t.annotations.openWorldHint));
  const c=await client.callTool({name:"get_challenge",arguments:{challenge_id:"inference-002"}});
  assert.equal(c.isError||false,false);
  assert.equal(JSON.parse(c.content[0].text).baseline,4069);
  const bad=await client.callTool({name:"get_challenge",arguments:{challenge_id:"../../private"}});
  assert.equal(bad.isError,true);
  assert.equal(JSON.parse(bad.content[0].text).error,"Unknown public challenge ID");
  const l=await client.callTool({name:"list_challenges",arguments:{track:"training"}});
  assert.ok(JSON.parse(l.content[0].text).challenges.every(x=>x.track==="training"));
  const s=await client.callTool({name:"get_research_status",arguments:{}});
  assert.equal(JSON.parse(s.content[0].text).physical_ppba_ranked,false);
  console.log("MCP_BUNDLE_PROTOCOL=PASS; 3 read-only tools");
 }finally{await client.close();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
