# Discovery and distribution

## Public sources
- GitHub is the canonical code and evidence source. No personal host, private repository or personal agent connection is required.
- The static site under docs/ uses semantic HTML, descriptive metadata, public evidence links, a sitemap and an opt-in LLM link index. There are no analytics scripts, forms or hidden recruitment instructions.
- Pages activation: repository Settings > Pages > Deploy from a branch > main > /docs > Save. The expected project URL is https://rtl-ai.github.io/silicon-arena/ after successful deployment. Verify HTTP availability before submitting its sitemap or sharing the URL.
- The project-level robots.txt is descriptive: crawlers use the host-root robots.txt, which this project does not control. GitHub Pages host policy remains authoritative.
- llms.txt is a navigation aid, not a Google ranking factor. No indexing or citation guarantee.

## Skills and registries
The four hardware skills are standalone useful guides. Optional research links are relevant examples, not instructions to join, advertise, or spend. Inspect with the Skills CLI --list; do not simulate installs or manipulate telemetry. The public GitHub source is usable even before a third-party registry indexes it.

ClawHub requires an authorized publisher login and moderation; publishing a skill there uses MIT-0. The existing repository MIT license is unchanged. Review the separate licensing choice before release. Official MCP Registry requires a supported public package or an actually reachable remote MCP endpoint and namespace authentication. The read-only stdio adapter in this repo is not a public endpoint or registry listing. Open Challenge List review and a qualified scored leaderboard remain outstanding.

## Measuring impact
Track real unique external contributors, qualifying PRs and independent reproductions. Stars, installs and clicks are secondary; never count bots, maintainer activity or registered accounts as active external researchers. Avoid unsolicited bulk messages, fabricated engagement or keyword stuffing. Do not expose private machines, tokens or local paths. Do not send identifiable telemetry from the skills or MCP adapter.

## References
- https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://skills.sh/docs
- https://docs.openclaw.ai/clawhub/publishing
- https://registry.modelcontextprotocol.io/
