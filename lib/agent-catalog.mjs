import { readFileSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { dirname, join } from "node:path";

const require = createRequire(import.meta.url);

export const supportedSkillsVersion = "1.5.23";
export const featuredAgentIds = [
  "codex",
  "claude-code",
  "antigravity",
  "kiro-cli",
  "zed",
];

const originalAgentFunction = `function getNonUniversalAgents() {
	return Object.entries(agents).filter(([_, config]) => config.skillsDir !== ".agents/skills").map(([type]) => type);
}`;

const originalUniversalAgentFunction = `function getVisibleUniversalAgents() {
	return Object.entries(agents).filter(([_, config]) => config.skillsDir === ".agents/skills" && config.showInUniversalList !== false && config.showInUniversalPrompt !== false).map(([type]) => type);
}`;

const featuredUniversalAgentFunction = `function getVisibleUniversalAgents() {
	return Object.entries(agents).filter(([type, config]) => config.skillsDir === ".agents/skills" && config.showInUniversalList !== false && config.showInUniversalPrompt !== false && FLUTTER_SKILLS_FEATURED_AGENT_IDS.has(type)).map(([type]) => type);
}`;

const featuredAgentFunction = `const FLUTTER_SKILLS_FEATURED_AGENT_IDS = new Set(${JSON.stringify(featuredAgentIds)});
function getNonUniversalAgents() {
	return Object.entries(agents).filter(([type, config]) => config.skillsDir !== ".agents/skills" && FLUTTER_SKILLS_FEATURED_AGENT_IDS.has(type)).map(([type]) => type);
}`;

const originalPromptStart = `async function promptForAgents(message, choices) {
	let lastSelected;`;

const featuredPromptStart = `async function promptForAgents(message, choices) {
	choices = choices.filter(({ value }) => FLUTTER_SKILLS_FEATURED_AGENT_IDS.has(value));
	let lastSelected;`;

const hiddenUniversalCount = "hiddenCount: universalAgents.length - visibleUniversalAgents.length";
const featuredAgentCountPattern = /const totalAgents = Object\.keys\(agents\)\.length;\n([ \t]*)(spinner(?:\$\d+)?)\.stop\(`\$\{totalAgents\} agents`\);/g;

const patchMarker = "const FLUTTER_SKILLS_FEATURED_AGENT_IDS =";

export function patchAgentCatalog(source) {
  if (source.includes(patchMarker)) {
    if (
      !source.includes("FLUTTER_SKILLS_FEATURED_AGENT_IDS.has(type)") ||
      !source.includes("choices = choices.filter(({ value })") ||
      !source.includes("hiddenCount: 0") ||
      !source.includes("featured agent destinations")
    ) {
      throw new Error("The featured-agent compatibility patch is incomplete.");
    }
    return source;
  }
  if (
    !source.includes(originalAgentFunction) ||
    !source.includes(originalUniversalAgentFunction) ||
    !source.includes(originalPromptStart)
  ) {
    throw new Error(
      `The skills@${supportedSkillsVersion} agent chooser changed; update the featured-agent compatibility patch.`,
    );
  }
  const hiddenCountMatches = source.split(hiddenUniversalCount).length - 1;
  const agentCountMatches = [...source.matchAll(featuredAgentCountPattern)].length;
  if (hiddenCountMatches !== 3 || agentCountMatches !== 3) {
    throw new Error(
      `The skills@${supportedSkillsVersion} agent chooser changed; expected three matching agent-picker sections.`,
    );
  }
  const featuredSource = source
    .replace(originalUniversalAgentFunction, featuredUniversalAgentFunction)
    .replace(originalAgentFunction, featuredAgentFunction)
    .replace(originalPromptStart, featuredPromptStart)
    .replaceAll(hiddenUniversalCount, "hiddenCount: 0")
    .replace(
      featuredAgentCountPattern,
      (_match, indentation, spinner) =>
        `${indentation}${spinner}.stop(\`5 featured agent destinations\`);`,
    );
  if (!featuredSource.includes("FLUTTER_SKILLS_FEATURED_AGENT_IDS.has(type)")) {
    throw new Error("Failed to filter the universal agent choices.");
  }
  return featuredSource;
}

export function applyAgentCatalogPatch() {
  const packageJsonPath = require.resolve("skills/package.json");
  const packageJson = JSON.parse(readFileSync(packageJsonPath, "utf8"));
  if (packageJson.version !== supportedSkillsVersion) {
    throw new Error(
      `Featured agent filtering supports skills@${supportedSkillsVersion}; found skills@${packageJson.version}. Update the compatibility patch before changing the pinned dependency.`,
    );
  }

  const cliPath = join(dirname(packageJsonPath), "dist", "cli.mjs");
  const source = readFileSync(cliPath, "utf8");
  const patchedSource = patchAgentCatalog(source);
  if (patchedSource !== source) writeFileSync(cliPath, patchedSource);
}
