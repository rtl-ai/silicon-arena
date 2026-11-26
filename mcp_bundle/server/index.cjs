"use strict";
// Only fixed bundled public data. No network, arbitrary paths, shell, or credentials.
const fs = require("node:fs");
const path = require("node:path");
const {McpServer} = require("@modelcontextprotocol/sdk/server/mcp.js");
const {StdioServerTransport} = require("@modelcontextprotocol/sdk/server/stdio.js");
const {z} = require("zod");
const catalog = JSON.parse(fs.readFileSync(path.join(__dirname,"challenges.json"),"utf8"));
const server = new McpServer({name:"siliconarena-catalog",version:"0.1.0"});
const annotations = {readOnlyHint:true,destructiveHint:false,idempotentHint:true,openWorldHint:false};
const result = value => ({content:[{type:"text",text:JSON.stringify(value,null,2)}]});
server.registerTool("list_challenges",{
  description:"Read dated public RTL research tasks by track. No enrollment, execution or external calls.",
  inputSchema:{track:z.enum(["all","training","inference"]).optional()},annotations
},async ({track="all"})=>result({
  project:catalog.project,updated:catalog.updated,stage:catalog.stage,
  physical_ppba_ranked:catalog.physical_ppba_ranked,
  challenges:catalog.challenges.filter(c=>track==="all"||c.track===track),limitations:catalog.limitations
}));
server.registerTool("get_challenge",{
  description:"Read one challenge by public catalog ID. Input is never interpreted as a path.",
  inputSchema:{challenge_id:z.string().max(128)},annotations
},async ({challenge_id})=>{
  const c=catalog.challenges.find(x=>x.id===challenge_id);
  return c?result(c):{...result({error:"Unknown public challenge ID",available:catalog.challenges.map(x=>x.id)}),isError:true};
});
server.registerTool("get_research_status",{
  description:"Read the bundled dated project snapshot and evidence links, not a live participant census.",
  inputSchema:{},annotations
},async ()=>result(Object.fromEntries(["project","updated","repository","stage","physical_ppba_ranked","external_agents","fabricated_silicon","links","limitations"].map(k=>[k,catalog[k]]))));
server.connect(new StdioServerTransport()).catch(()=>{console.error("SiliconArena stdio initialization failed.");process.exitCode=1;});
