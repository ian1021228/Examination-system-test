with open("src/features.tsx", "r") as f:
    content = f.read()

badge_map = """
const BADGE_LABELS: Record<string, string> = {
  perfect_100: '滿分達人',
  speed_demon: '極速傳說',
  survival_expert: '生存大師',
  honest_player: '誠信守護者'
};
"""

if "BADGE_LABELS" not in content:
    content = content.replace("export function GamificationProfile", badge_map + "\nexport function GamificationProfile")
    
    content = content.replace(
        '<span className="text-[10px] text-[#8C7A6B] font-bold">{b}</span>',
        '<span className="text-[10px] text-[#8C7A6B] font-bold text-center leading-tight whitespace-pre-wrap w-16">{BADGE_LABELS[b] || b}</span>'
    )

with open("src/features.tsx", "w") as f:
    f.write(content)
