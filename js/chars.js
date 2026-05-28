/* ── 16종 MBTI 캐릭터 SVG 일러스트 ──
   viewBox: 0 0 100 130  /  head: cx=50 cy=53 r=22
   각 유형의 외형(헤어·의상·소품)이 성격 특성을 반영합니다
*/
const CHARS = {

/* ─── NT 분석가 그룹 (보라 계열 배경) ─── */

INTJ: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#EDE7FF"/>
<!-- suit body -->
<path d="M13,130 L13,92 Q22,84 44,79 L44,81 Q50,86 56,81 L56,79 Q78,84 87,92 L87,130Z" fill="#2D3561"/>
<!-- white shirt -->
<polygon points="44,79 50,93 56,79 50,84" fill="#F0F0F0"/>
<!-- red tie -->
<polygon points="48,84 52,84 51,102 50,104 49,102" fill="#C0392B"/>
<!-- neck -->
<rect x="44" y="69" width="12" height="12" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="55" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: neat dark short -->
<path d="M29,49 Q30,31 50,29 Q70,31 71,49 Q67,37 50,35 Q33,37 29,49Z" fill="#1A0E06"/>
<rect x="28" y="44" width="5" height="10" rx="2" fill="#1A0E06"/>
<!-- eyebrows: serious -->
<path d="M37,46 Q41,44 45,46" stroke="#1A0E06" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M55,46 Q59,44 63,46" stroke="#1A0E06" stroke-width="2" fill="none" stroke-linecap="round"/>
<!-- eyes -->
<ellipse cx="41" cy="53" rx="4.5" ry="4.5" fill="white"/>
<ellipse cx="59" cy="53" rx="4.5" ry="4.5" fill="white"/>
<circle cx="41" cy="53" r="3" fill="#1A1A2E"/>
<circle cx="59" cy="53" r="3" fill="#1A1A2E"/>
<circle cx="42.2" cy="51.5" r="1.1" fill="white"/>
<circle cx="60.2" cy="51.5" r="1.1" fill="white"/>
<!-- nose -->
<circle cx="50" cy="60" r="1.2" fill="#C9906A"/>
<!-- mouth: focused/neutral -->
<path d="M45,66 Q50,69 55,66" stroke="#BF7050" stroke-width="1.5" fill="none" stroke-linecap="round"/>
<!-- prop: chess pawn -->
<circle cx="83" cy="14" r="5" fill="#6C4AB6" opacity="0.55"/>
<rect x="79" y="18" width="8" height="4" rx="1" fill="#6C4AB6" opacity="0.55"/>
<path d="M77,22 L83,22 L84,26 L76,26Z" fill="#6C4AB6" opacity="0.55"/>
</svg>`,

INTP: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#E8E8FF"/>
<!-- sweater body -->
<path d="M13,130 L13,92 Q22,84 44,80 Q50,84 56,80 Q78,84 87,92 L87,130Z" fill="#3A7A6E"/>
<!-- collar -->
<path d="M42,80 Q50,88 58,80 Q54,84 50,86 Q46,84 42,80Z" fill="#2D6058"/>
<!-- neck -->
<rect x="44" y="69" width="12" height="12" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="55" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: messy brown -->
<path d="M29,50 Q29,31 50,28 Q71,31 71,50 Q69,36 50,34 Q31,36 29,50Z" fill="#5C3820"/>
<path d="M29,44 Q27,40 30,36" stroke="#5C3820" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M71,44 Q73,40 70,36" stroke="#5C3820" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M50,28 Q55,24 58,28" stroke="#5C3820" stroke-width="4" fill="none" stroke-linecap="round"/>
<!-- glasses frame -->
<rect x="34" y="48" width="13" height="10" rx="4" fill="none" stroke="#4A3520" stroke-width="1.8"/>
<rect x="53" y="48" width="13" height="10" rx="4" fill="none" stroke="#4A3520" stroke-width="1.8"/>
<line x1="47" y1="53" x2="53" y2="53" stroke="#4A3520" stroke-width="1.5"/>
<!-- eyebrows -->
<path d="M36,46 Q41,44 46,46" stroke="#5C3820" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<path d="M54,46 Q59,44 64,46" stroke="#5C3820" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<!-- eyes -->
<circle cx="40.5" cy="53" r="3" fill="#2C3E7A"/>
<circle cx="59.5" cy="53" r="3" fill="#2C3E7A"/>
<circle cx="41.5" cy="51.8" r="1" fill="white"/>
<circle cx="60.5" cy="51.8" r="1" fill="white"/>
<!-- nose -->
<circle cx="50" cy="60" r="1.2" fill="#C9906A"/>
<!-- mouth: slight smile -->
<path d="M45,66 Q50,70 55,66" stroke="#BF7050" stroke-width="1.5" fill="none" stroke-linecap="round"/>
<!-- prop: lightbulb -->
<circle cx="83" cy="15" r="6" fill="#FFD700" opacity="0.6"/>
<rect x="80" y="20" width="6" height="4" rx="1" fill="#FFD700" opacity="0.6"/>
<line x1="82" y1="24" x2="84" y2="24" stroke="#D4A000" stroke-width="1.2" opacity="0.6"/>
</svg>`,

ENTJ: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#DDD8FF"/>
<!-- charcoal suit -->
<path d="M13,130 L13,92 Q22,84 44,79 L44,81 Q50,86 56,81 L56,79 Q78,84 87,92 L87,130Z" fill="#3A3A4A"/>
<!-- white shirt & collar -->
<polygon points="44,79 50,93 56,79 50,84" fill="#F0F0F0"/>
<!-- blue tie -->
<polygon points="48,84 52,84 51,102 50,104 49,102" fill="#2471A3"/>
<!-- neck -->
<rect x="44" y="69" width="12" height="12" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="55" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: neat dark, strong -->
<path d="M29,48 Q30,30 50,28 Q70,30 71,48 Q68,36 50,34 Q32,36 29,48Z" fill="#1A0E06"/>
<path d="M29,48 Q28,42 30,38" fill="none" stroke="#1A0E06" stroke-width="4"/>
<!-- eyebrows: strong/confident -->
<rect x="36" y="44" width="10" height="2.2" rx="1" fill="#1A0E06"/>
<rect x="54" y="44" width="10" height="2.2" rx="1" fill="#1A0E06"/>
<!-- eyes -->
<ellipse cx="41" cy="53" rx="4.5" ry="4.5" fill="white"/>
<ellipse cx="59" cy="53" rx="4.5" ry="4.5" fill="white"/>
<circle cx="41" cy="53" r="3" fill="#1A2040"/>
<circle cx="59" cy="53" r="3" fill="#1A2040"/>
<circle cx="42.2" cy="51.5" r="1.1" fill="white"/>
<circle cx="60.2" cy="51.5" r="1.1" fill="white"/>
<!-- nose -->
<circle cx="50" cy="60" r="1.2" fill="#C9906A"/>
<!-- mouth: confident smile -->
<path d="M44,65 Q50,71 56,65" stroke="#BF7050" stroke-width="2" fill="none" stroke-linecap="round"/>
<!-- prop: flag -->
<line x1="80" y1="10" x2="80" y2="28" stroke="#E74C3C" stroke-width="1.8"/>
<polygon points="80,10 90,14 80,18" fill="#E74C3C"/>
</svg>`,

ENTP: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#E6E0FF"/>
<!-- casual jacket -->
<path d="M13,130 L13,92 Q22,84 42,80 Q50,86 58,80 Q78,84 87,92 L87,130Z" fill="#5D5F7A"/>
<!-- hoodie/shirt detail -->
<path d="M42,80 Q50,88 58,80 Q54,86 50,88 Q46,86 42,80Z" fill="#E0E0F0"/>
<!-- neck -->
<rect x="44" y="69" width="12" height="12" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="55" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: tousled light brown -->
<path d="M29,50 Q29,32 50,29 Q71,32 71,50 Q68,37 50,35 Q32,37 29,50Z" fill="#8B5E30"/>
<path d="M50,29 Q56,24 62,29" stroke="#8B5E30" stroke-width="5" fill="none" stroke-linecap="round"/>
<path d="M50,29 Q44,24 38,29" stroke="#8B5E30" stroke-width="4" fill="none" stroke-linecap="round"/>
<path d="M28,44 Q26,38 30,34" stroke="#8B5E30" stroke-width="4" fill="none" stroke-linecap="round"/>
<!-- eyebrows: raised/expressive -->
<path d="M36,45 Q41,42 45,44" stroke="#6B4820" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<path d="M55,44 Q59,42 64,45" stroke="#6B4820" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<!-- eyes: wide/energetic -->
<ellipse cx="41" cy="53" rx="5" ry="5" fill="white"/>
<ellipse cx="59" cy="53" rx="5" ry="5" fill="white"/>
<circle cx="41" cy="53" r="3.2" fill="#2C3E7A"/>
<circle cx="59" cy="53" r="3.2" fill="#2C3E7A"/>
<circle cx="42.3" cy="51.5" r="1.2" fill="white"/>
<circle cx="60.3" cy="51.5" r="1.2" fill="white"/>
<!-- nose -->
<circle cx="50" cy="60" r="1.2" fill="#C9906A"/>
<!-- mouth: big grin -->
<path d="M43,65 Q50,73 57,65" stroke="#BF7050" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M43,65 Q43,68 45,68" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<path d="M57,65 Q57,68 55,68" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<!-- prop: speech bubble -->
<ellipse cx="82" cy="15" rx="9" ry="7" fill="white" stroke="#9C6FDE" stroke-width="1.5"/>
<path d="M76,21 L73,26 L79,22" fill="white" stroke="#9C6FDE" stroke-width="1.2"/>
<circle cx="79" cy="15" r="1.5" fill="#9C6FDE"/>
<circle cx="83" cy="15" r="1.5" fill="#9C6FDE"/>
<circle cx="87" cy="15" r="1.5" fill="#9C6FDE" opacity="0.5"/>
</svg>`,

/* ─── NF 외교관 그룹 (초록 계열 배경) ─── */

INFJ: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#E6F4EA"/>
<!-- teal cardigan -->
<path d="M13,130 L13,92 Q22,85 42,82 Q50,88 58,82 Q78,85 87,92 L87,130Z" fill="#2E8B7A"/>
<!-- collar -->
<path d="M42,82 Q50,90 58,82 Q54,87 50,89 Q46,87 42,82Z" fill="#236B5E"/>
<!-- neck -->
<rect x="44" y="70" width="12" height="13" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="56" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: long dark straight -->
<ellipse cx="50" cy="38" rx="22" ry="11" fill="#1C1008"/>
<path d="M28.5,46 Q26,56 26,90 Q26,105 28,120" stroke="#1C1008" stroke-width="10" fill="none" stroke-linecap="round"/>
<path d="M71.5,46 Q74,56 74,90 Q74,105 72,120" stroke="#1C1008" stroke-width="10" fill="none" stroke-linecap="round"/>
<!-- eyebrows: gentle -->
<path d="M38,47 Q42,45 46,47" stroke="#1C1008" stroke-width="1.7" fill="none" stroke-linecap="round"/>
<path d="M54,47 Q58,45 62,47" stroke="#1C1008" stroke-width="1.7" fill="none" stroke-linecap="round"/>
<!-- eyes -->
<ellipse cx="42" cy="54" rx="4.5" ry="4.5" fill="white"/>
<ellipse cx="58" cy="54" rx="4.5" ry="4.5" fill="white"/>
<circle cx="42" cy="54" r="3" fill="#3D2010"/>
<circle cx="58" cy="54" r="3" fill="#3D2010"/>
<circle cx="43.2" cy="52.8" r="1.1" fill="white"/>
<circle cx="59.2" cy="52.8" r="1.1" fill="white"/>
<!-- nose -->
<circle cx="50" cy="61" r="1.2" fill="#C9906A"/>
<!-- mouth: gentle smile -->
<path d="M45,67 Q50,71 55,67" stroke="#BF7050" stroke-width="1.5" fill="none" stroke-linecap="round"/>
<!-- prop: open book -->
<path d="M74,10 Q83,8 87,10 L87,24 Q83,22 74,24Z" fill="white" stroke="#2E8B7A" stroke-width="1.2"/>
<path d="M74,10 Q65,8 61,10 L61,24 Q65,22 74,24Z" fill="white" stroke="#2E8B7A" stroke-width="1.2"/>
<line x1="74" y1="10" x2="74" y2="24" stroke="#2E8B7A" stroke-width="1.2"/>
</svg>`,

INFP: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#ECF8ED"/>
<!-- lavender top -->
<path d="M13,130 L13,92 Q22,85 42,82 Q50,88 58,82 Q78,85 87,92 L87,130Z" fill="#9B7CC8"/>
<!-- neck -->
<rect x="44" y="70" width="12" height="13" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="56" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: long wavy brown -->
<ellipse cx="50" cy="38" rx="22" ry="11" fill="#7A4A28"/>
<path d="M28.5,46 Q24,58 26,72 Q24,84 26,98 Q24,110 26,122" stroke="#7A4A28" stroke-width="11" fill="none" stroke-linecap="round"/>
<path d="M71.5,46 Q76,58 74,72 Q76,84 74,98 Q76,110 74,122" stroke="#7A4A28" stroke-width="11" fill="none" stroke-linecap="round"/>
<!-- centre part -->
<line x1="50" y1="34" x2="50" y2="40" stroke="#5C3820" stroke-width="2"/>
<!-- eyebrows: soft -->
<path d="M38,47 Q42,45 46,47" stroke="#5C3820" stroke-width="1.6" fill="none" stroke-linecap="round"/>
<path d="M54,47 Q58,45 62,47" stroke="#5C3820" stroke-width="1.6" fill="none" stroke-linecap="round"/>
<!-- eyes: slightly upward/dreamy -->
<ellipse cx="42" cy="54" rx="4.5" ry="4.5" fill="white"/>
<ellipse cx="58" cy="54" rx="4.5" ry="4.5" fill="white"/>
<circle cx="42" cy="53" r="3" fill="#3D2010"/>
<circle cx="58" cy="53" r="3" fill="#3D2010"/>
<circle cx="43.2" cy="51.8" r="1.1" fill="white"/>
<circle cx="59.2" cy="51.8" r="1.1" fill="white"/>
<!-- long lashes -->
<line x1="38" y1="50" x2="36" y2="48" stroke="#3D2010" stroke-width="1.2"/>
<line x1="54" y1="50" x2="52" y2="48" stroke="#3D2010" stroke-width="1.2"/>
<!-- nose -->
<circle cx="50" cy="61" r="1.2" fill="#C9906A"/>
<!-- mouth: soft smile -->
<path d="M45,67 Q50,72 55,67" stroke="#BF7050" stroke-width="1.5" fill="none" stroke-linecap="round"/>
<!-- prop: small heart + star -->
<path d="M80,10 Q80,7 83,7 Q86,7 86,10 Q86,13 83,16 Q80,13 80,10Z" fill="#FF6B9D" opacity="0.7"/>
<path d="M72,16 L74,10 L76,16 L70,12 L78,12Z" fill="#FFD700" opacity="0.7"/>
</svg>`,

ENFJ: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#E8F5E9"/>
<!-- coral top -->
<path d="M13,130 L13,92 Q22,85 42,82 Q50,88 58,82 Q78,85 87,92 L87,130Z" fill="#E05A4E"/>
<!-- collar detail -->
<path d="M42,82 Q50,90 58,82 Q54,87 50,89 Q46,87 42,82Z" fill="#C04A40"/>
<!-- neck -->
<rect x="44" y="70" width="12" height="13" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="56" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: shoulder length brown -->
<ellipse cx="50" cy="38" rx="22" ry="11" fill="#6B4020"/>
<path d="M28.5,46 Q26,58 28,72 Q26,80 28,88" stroke="#6B4020" stroke-width="10" fill="none" stroke-linecap="round"/>
<path d="M71.5,46 Q74,58 72,72 Q74,80 72,88" stroke="#6B4020" stroke-width="10" fill="none" stroke-linecap="round"/>
<!-- hair highlight -->
<path d="M36,36 Q40,34 42,37" stroke="#8B5A30" stroke-width="2" fill="none" opacity="0.5"/>
<!-- eyebrows -->
<path d="M37,47 Q42,45 46,47" stroke="#4A2A10" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<path d="M54,47 Q58,45 63,47" stroke="#4A2A10" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<!-- eyes -->
<ellipse cx="42" cy="54" rx="4.5" ry="4.5" fill="white"/>
<ellipse cx="58" cy="54" rx="4.5" ry="4.5" fill="white"/>
<circle cx="42" cy="54" r="3" fill="#3D2010"/>
<circle cx="58" cy="54" r="3" fill="#3D2010"/>
<circle cx="43.2" cy="52.5" r="1.1" fill="white"/>
<circle cx="59.2" cy="52.5" r="1.1" fill="white"/>
<!-- nose -->
<circle cx="50" cy="61" r="1.2" fill="#C9906A"/>
<!-- mouth: warm big smile -->
<path d="M44,66 Q50,73 56,66" stroke="#BF7050" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M44,66 Q44,69 46,69" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<path d="M56,66 Q56,69 54,69" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<!-- prop: megaphone -->
<path d="M76,16 L86,10 L86,24 L76,20Z" fill="#FFB830" opacity="0.8"/>
<rect x="72" y="16" width="5" height="4" rx="1" fill="#E09000" opacity="0.8"/>
<path d="M72,21 Q70,23 70,27 Q72,27 72,23Z" fill="#E09000" opacity="0.7"/>
</svg>`,

ENFP: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#F0FBF0"/>
<!-- bright yellow top -->
<path d="M13,130 L13,92 Q22,85 42,82 Q50,88 58,82 Q78,85 87,92 L87,130Z" fill="#E8B800"/>
<!-- neck -->
<rect x="44" y="70" width="12" height="13" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="56" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: wavy amber/copper -->
<ellipse cx="50" cy="37" rx="23" ry="12" fill="#C87428"/>
<path d="M27.5,46 Q24,56 26,66 Q24,78 26,90 Q24,104 27,116" stroke="#C87428" stroke-width="11" fill="none" stroke-linecap="round"/>
<path d="M72.5,46 Q76,56 74,66 Q76,78 74,90 Q76,104 73,116" stroke="#C87428" stroke-width="11" fill="none" stroke-linecap="round"/>
<!-- hair highlights -->
<path d="M36,36 Q40,33 45,35" stroke="#E8A040" stroke-width="2.5" fill="none" opacity="0.6"/>
<path d="M55,35 Q60,33 64,36" stroke="#E8A040" stroke-width="2.5" fill="none" opacity="0.6"/>
<!-- eyebrows: arched/expressive -->
<path d="M36,47 Q41,43 46,46" stroke="#8B5020" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M54,46 Q59,43 64,47" stroke="#8B5020" stroke-width="2" fill="none" stroke-linecap="round"/>
<!-- eyes: big sparkly -->
<ellipse cx="41" cy="54" rx="5.5" ry="5.5" fill="white"/>
<ellipse cx="59" cy="54" rx="5.5" ry="5.5" fill="white"/>
<circle cx="41" cy="54" r="3.5" fill="#2C5282"/>
<circle cx="59" cy="54" r="3.5" fill="#2C5282"/>
<circle cx="42.5" cy="52.2" r="1.4" fill="white"/>
<circle cx="60.5" cy="52.2" r="1.4" fill="white"/>
<!-- rosy cheeks -->
<ellipse cx="34" cy="60" rx="5" ry="3.5" fill="#FFB0B0" opacity="0.45"/>
<ellipse cx="66" cy="60" rx="5" ry="3.5" fill="#FFB0B0" opacity="0.45"/>
<!-- nose -->
<circle cx="50" cy="62" r="1.2" fill="#C9906A"/>
<!-- mouth: huge enthusiastic grin -->
<path d="M42,68 Q50,77 58,68" stroke="#BF7050" stroke-width="2.2" fill="none" stroke-linecap="round"/>
<path d="M42,68 Q41,72 44,72" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<path d="M58,68 Q59,72 56,72" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<!-- prop: sparkle star -->
<path d="M81,9 L83,5 L85,9 L89,9 L86,12 L87,16 L83,14 L79,16 L80,12 L77,9Z" fill="#FFD700" opacity="0.8"/>
<circle cx="83" cy="22" r="2" fill="#FF6B9D" opacity="0.7"/>
</svg>`,

/* ─── SJ 관리자 그룹 (파랑 계열 배경) ─── */

ISTJ: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#E3EDF8"/>
<!-- blue suit -->
<path d="M13,130 L13,92 Q22,84 44,79 L44,81 Q50,86 56,81 L56,79 Q78,84 87,92 L87,130Z" fill="#2E5F9A"/>
<!-- white shirt -->
<polygon points="44,79 50,93 56,79 50,84" fill="#F0F0F0"/>
<!-- dark tie -->
<polygon points="48,84 52,84 51,102 50,104 49,102" fill="#1A2A4A"/>
<!-- neck -->
<rect x="44" y="69" width="12" height="12" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="55" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: neat short black -->
<path d="M29,49 Q30,31 50,29 Q70,31 71,49 Q68,37 50,35 Q32,37 29,49Z" fill="#1A0E06"/>
<path d="M29,49 L29,45" stroke="#1A0E06" stroke-width="5" stroke-linecap="round"/>
<!-- glasses -->
<rect x="34" y="49" width="13" height="10" rx="4" fill="none" stroke="#2C2C2C" stroke-width="1.8"/>
<rect x="53" y="49" width="13" height="10" rx="4" fill="none" stroke="#2C2C2C" stroke-width="1.8"/>
<line x1="47" y1="54" x2="53" y2="54" stroke="#2C2C2C" stroke-width="1.5"/>
<line x1="28" y1="54" x2="34" y2="54" stroke="#2C2C2C" stroke-width="1.5"/>
<line x1="66" y1="54" x2="72" y2="54" stroke="#2C2C2C" stroke-width="1.5"/>
<!-- eyebrows -->
<rect x="36" y="46" width="9" height="2" rx="1" fill="#1A0E06"/>
<rect x="55" y="46" width="9" height="2" rx="1" fill="#1A0E06"/>
<!-- eyes -->
<circle cx="40.5" cy="54" r="2.8" fill="#1A2040"/>
<circle cx="59.5" cy="54" r="2.8" fill="#1A2040"/>
<circle cx="41.5" cy="52.8" r="1" fill="white"/>
<circle cx="60.5" cy="52.8" r="1" fill="white"/>
<!-- nose -->
<circle cx="50" cy="61" r="1.2" fill="#C9906A"/>
<!-- mouth: precise neutral -->
<path d="M45,66 Q50,69 55,66" stroke="#BF7050" stroke-width="1.5" fill="none" stroke-linecap="round"/>
<!-- prop: clipboard -->
<rect x="74" y="8" width="16" height="20" rx="2" fill="white" stroke="#2E5F9A" stroke-width="1.5"/>
<rect x="79" y="6" width="6" height="4" rx="1" fill="#2E5F9A"/>
<line x1="77" y1="15" x2="87" y2="15" stroke="#2E5F9A" stroke-width="1.2"/>
<line x1="77" y1="18" x2="87" y2="18" stroke="#2E5F9A" stroke-width="1.2"/>
<line x1="77" y1="21" x2="84" y2="21" stroke="#2E5F9A" stroke-width="1.2"/>
</svg>`,

ISFJ: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#EBF4FD"/>
<!-- light blue/white top -->
<path d="M13,130 L13,92 Q22,85 42,82 Q50,88 58,82 Q78,85 87,92 L87,130Z" fill="#4A9ED4"/>
<!-- white collar -->
<path d="M40,82 Q50,92 60,82 Q54,88 50,90 Q46,88 40,82Z" fill="white"/>
<!-- neck -->
<rect x="44" y="70" width="12" height="13" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="56" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: brown, neatly pulled back -->
<ellipse cx="50" cy="38" rx="22" ry="11" fill="#6B4020"/>
<path d="M28.5,46 Q27,56 28,68" stroke="#6B4020" stroke-width="9" fill="none" stroke-linecap="round"/>
<path d="M71.5,46 Q73,56 72,68" stroke="#6B4020" stroke-width="9" fill="none" stroke-linecap="round"/>
<!-- bun at back (implied top) -->
<circle cx="50" cy="34" r="7" fill="#6B4020" opacity="0.4"/>
<!-- eyebrows: gentle arched -->
<path d="M37,47 Q42,45 46,47" stroke="#4A2A10" stroke-width="1.7" fill="none" stroke-linecap="round"/>
<path d="M54,47 Q58,45 63,47" stroke="#4A2A10" stroke-width="1.7" fill="none" stroke-linecap="round"/>
<!-- eyes -->
<ellipse cx="42" cy="54" rx="4.5" ry="4.5" fill="white"/>
<ellipse cx="58" cy="54" rx="4.5" ry="4.5" fill="white"/>
<circle cx="42" cy="54" r="3" fill="#5C3010"/>
<circle cx="58" cy="54" r="3" fill="#5C3010"/>
<circle cx="43.2" cy="52.8" r="1.1" fill="white"/>
<circle cx="59.2" cy="52.8" r="1.1" fill="white"/>
<!-- rosy cheeks -->
<ellipse cx="34" cy="60" rx="5" ry="3" fill="#FFB0B0" opacity="0.4"/>
<ellipse cx="66" cy="60" rx="5" ry="3" fill="#FFB0B0" opacity="0.4"/>
<!-- nose -->
<circle cx="50" cy="61" r="1.2" fill="#C9906A"/>
<!-- mouth: kind smile -->
<path d="M44,67 Q50,73 56,67" stroke="#BF7050" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<!-- prop: heart -->
<path d="M80,10 Q80,7 83,7 Q86,7 86,10 Q86,14 83,17 Q80,14 80,10Z" fill="#FF6B9D" opacity="0.7"/>
<path d="M76,10 Q76,7 79,7 Q80,8 80,10 Q80,14 77,17 Q76,14 76,10Z" fill="#FF6B9D" opacity="0.7"/>
</svg>`,

ESTJ: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#D8E8F8"/>
<!-- formal charcoal suit -->
<path d="M13,130 L13,92 Q22,84 44,79 L44,81 Q50,86 56,81 L56,79 Q78,84 87,92 L87,130Z" fill="#3A3A4A"/>
<!-- white shirt -->
<polygon points="44,79 50,93 56,79 50,84" fill="#F0F0F0"/>
<!-- grey tie -->
<polygon points="48,84 52,84 51,102 50,104 49,102" fill="#8A8AA0"/>
<!-- neck -->
<rect x="44" y="69" width="12" height="12" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="55" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: slicked back dark -->
<path d="M29,48 Q30,30 50,28 Q70,30 71,48 Q68,36 50,34 Q32,36 29,48Z" fill="#1A0E06"/>
<path d="M29,48 Q28,40 32,35 Q40,31 50,31" stroke="#1A0E06" stroke-width="3" fill="none"/>
<!-- eyebrows: strong/authoritative -->
<rect x="35" y="44" width="12" height="2.5" rx="1" fill="#1A0E06"/>
<rect x="53" y="44" width="12" height="2.5" rx="1" fill="#1A0E06"/>
<!-- eyes -->
<ellipse cx="41" cy="53" rx="4.5" ry="4.5" fill="white"/>
<ellipse cx="59" cy="53" rx="4.5" ry="4.5" fill="white"/>
<circle cx="41" cy="53" r="3" fill="#1A1A30"/>
<circle cx="59" cy="53" r="3" fill="#1A1A30"/>
<circle cx="42.2" cy="51.5" r="1.1" fill="white"/>
<circle cx="60.2" cy="51.5" r="1.1" fill="white"/>
<!-- nose -->
<circle cx="50" cy="60" r="1.2" fill="#C9906A"/>
<!-- mouth: authoritative neutral -->
<path d="M44,65 Q50,68 56,65" stroke="#BF7050" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<!-- prop: checkmark -->
<path d="M76,14 L80,20 L88,9" stroke="#27AE60" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="82" cy="14" r="8" fill="none" stroke="#27AE60" stroke-width="1.5" opacity="0.4"/>
</svg>`,

ESFJ: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#E0EFF8"/>
<!-- warm beige top -->
<path d="M13,130 L13,92 Q22,85 42,82 Q50,88 58,82 Q78,85 87,92 L87,130Z" fill="#C8956A"/>
<!-- neck -->
<rect x="44" y="70" width="12" height="13" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="56" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: curly/wavy brown -->
<ellipse cx="50" cy="37" rx="23" ry="12" fill="#7A4A28"/>
<circle cx="29" cy="50" r="9" fill="#7A4A28"/>
<circle cx="71" cy="50" r="9" fill="#7A4A28"/>
<circle cx="33" cy="62" r="8" fill="#7A4A28"/>
<circle cx="67" cy="62" r="8" fill="#7A4A28"/>
<!-- eyebrows -->
<path d="M37,47 Q42,45 46,47" stroke="#4A2A10" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<path d="M54,47 Q58,45 63,47" stroke="#4A2A10" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<!-- eyes -->
<ellipse cx="42" cy="54" rx="4.5" ry="4.5" fill="white"/>
<ellipse cx="58" cy="54" rx="4.5" ry="4.5" fill="white"/>
<circle cx="42" cy="54" r="3" fill="#5C3010"/>
<circle cx="58" cy="54" r="3" fill="#5C3010"/>
<circle cx="43.2" cy="52.5" r="1.1" fill="white"/>
<circle cx="59.2" cy="52.5" r="1.1" fill="white"/>
<!-- rosy cheeks -->
<ellipse cx="34" cy="60" rx="5" ry="3.5" fill="#FFB0B0" opacity="0.5"/>
<ellipse cx="66" cy="60" rx="5" ry="3.5" fill="#FFB0B0" opacity="0.5"/>
<!-- nose -->
<circle cx="50" cy="61" r="1.2" fill="#C9906A"/>
<!-- mouth: big friendly smile -->
<path d="M43,67 Q50,75 57,67" stroke="#BF7050" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M43,67 Q43,71 45,71" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<path d="M57,67 Q57,71 55,71" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<!-- prop: small hearts -->
<path d="M78,9 Q78,7 80,7 Q82,7 82,9 Q82,12 80,14 Q78,12 78,9Z" fill="#FF6B9D" opacity="0.7"/>
<path d="M75,9 Q75,7 77,7 Q78,8 78,9 Q78,12 76,14 Q75,12 75,9Z" fill="#FF6B9D" opacity="0.7"/>
<path d="M83,14 Q83,12 85,12 Q87,12 87,14 Q87,16 85,18 Q83,16 83,14Z" fill="#FF6B9D" opacity="0.5"/>
</svg>`,

/* ─── SP 탐험가 그룹 (따뜻한 계열 배경) ─── */

ISTP: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#FFEBEE"/>
<!-- dark hoodie -->
<path d="M13,130 L13,92 Q22,84 42,80 Q50,88 58,80 Q78,84 87,92 L87,130Z" fill="#484858"/>
<!-- hoodie pocket/detail -->
<path d="M42,80 Q50,86 58,80 Q54,84 50,86 Q46,84 42,80Z" fill="#383848"/>
<path d="M38,100 Q50,100 62,100 Q62,110 50,110 Q38,110 38,100Z" fill="#383848" opacity="0.5"/>
<!-- neck -->
<rect x="44" y="70" width="12" height="12" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="56" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: casual dark, slightly messy -->
<path d="M29,50 Q30,32 50,30 Q70,32 71,50 Q68,38 50,36 Q32,38 29,50Z" fill="#1A0E06"/>
<path d="M71,44 Q74,38 72,34" stroke="#1A0E06" stroke-width="4" fill="none" stroke-linecap="round"/>
<!-- eyebrows: relaxed/cool -->
<path d="M37,46 Q42,44 46,46" stroke="#1A0E06" stroke-width="1.7" fill="none" stroke-linecap="round"/>
<path d="M54,46 Q58,44 63,46" stroke="#1A0E06" stroke-width="1.7" fill="none" stroke-linecap="round"/>
<!-- eyes: calm/cool -->
<ellipse cx="42" cy="54" rx="4.5" ry="4" fill="white"/>
<ellipse cx="58" cy="54" rx="4.5" ry="4" fill="white"/>
<circle cx="42" cy="54" r="2.8" fill="#2C3E7A"/>
<circle cx="58" cy="54" r="2.8" fill="#2C3E7A"/>
<circle cx="43.2" cy="52.8" r="1" fill="white"/>
<circle cx="59.2" cy="52.8" r="1" fill="white"/>
<!-- nose -->
<circle cx="50" cy="61" r="1.2" fill="#C9906A"/>
<!-- mouth: relaxed neutral -->
<path d="M45,66 Q50,69 55,66" stroke="#BF7050" stroke-width="1.5" fill="none" stroke-linecap="round"/>
<!-- prop: wrench -->
<path d="M76,10 Q80,8 83,10 L82,12 Q84,14 82,16 L78,20 Q76,18 77,16 L73,12 Z" fill="#8A8A9A" opacity="0.7"/>
<circle cx="83" cy="10" r="3" fill="#6A6A7A" opacity="0.7"/>
</svg>`,

ISFP: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#FFE5E5"/>
<!-- artistic apron -->
<path d="M13,130 L13,92 Q22,85 42,82 Q50,88 58,82 Q78,85 87,92 L87,130Z" fill="#6B9E78"/>
<!-- apron bib -->
<path d="M42,82 Q50,90 58,82 Q58,96 50,98 Q42,96 42,82Z" fill="#5A8A66"/>
<!-- neck -->
<rect x="44" y="70" width="12" height="13" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="56" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: brown with beret -->
<ellipse cx="50" cy="38" rx="22" ry="11" fill="#7A4A28"/>
<path d="M28.5,46 Q26,56 27,70" stroke="#7A4A28" stroke-width="9" fill="none" stroke-linecap="round"/>
<path d="M71.5,46 Q74,56 73,70" stroke="#7A4A28" stroke-width="9" fill="none" stroke-linecap="round"/>
<!-- beret! -->
<ellipse cx="48" cy="34" rx="26" ry="9" fill="#D4623A"/>
<ellipse cx="50" cy="27" rx="18" ry="7" fill="#D4623A"/>
<circle cx="63" cy="31" r="3" fill="#C04820"/>
<!-- eyebrows: soft -->
<path d="M37,47 Q42,45 46,47" stroke="#4A2A10" stroke-width="1.6" fill="none" stroke-linecap="round"/>
<path d="M54,47 Q58,45 62,47" stroke="#4A2A10" stroke-width="1.6" fill="none" stroke-linecap="round"/>
<!-- eyes -->
<ellipse cx="42" cy="54" rx="4.5" ry="4.5" fill="white"/>
<ellipse cx="58" cy="54" rx="4.5" ry="4.5" fill="white"/>
<circle cx="42" cy="54" r="3" fill="#5C3010"/>
<circle cx="58" cy="54" r="3" fill="#5C3010"/>
<circle cx="43.2" cy="52.8" r="1.1" fill="white"/>
<circle cx="59.2" cy="52.8" r="1.1" fill="white"/>
<!-- nose -->
<circle cx="50" cy="61" r="1.2" fill="#C9906A"/>
<!-- mouth: gentle creative smile -->
<path d="M45,67 Q50,72 55,67" stroke="#BF7050" stroke-width="1.6" fill="none" stroke-linecap="round"/>
<!-- prop: paint palette -->
<ellipse cx="81" cy="15" rx="9" ry="7" fill="#F0E0D0" opacity="0.85"/>
<ellipse cx="83" cy="19" rx="3" ry="2" fill="#F0E0D0" opacity="0.85"/>
<circle cx="77" cy="13" r="2" fill="#E74C3C" opacity="0.8"/>
<circle cx="81" cy="11" r="2" fill="#3498DB" opacity="0.8"/>
<circle cx="85" cy="12" r="2" fill="#F1C40F" opacity="0.8"/>
<circle cx="86" cy="16" r="2" fill="#2ECC71" opacity="0.8"/>
</svg>`,

ESTP: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#FFDADA"/>
<!-- olive casual jacket -->
<path d="M13,130 L13,92 Q22,84 44,80 L44,82 Q50,87 56,82 L56,80 Q78,84 87,92 L87,130Z" fill="#6B7A3A"/>
<!-- inner shirt -->
<polygon points="44,80 50,94 56,80 50,85" fill="#E8D0A0"/>
<!-- neck -->
<rect x="44" y="69" width="12" height="12" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="55" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="55" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: casual brown -->
<path d="M29,49 Q30,32 50,30 Q70,32 71,49 Q68,37 50,35 Q32,37 29,49Z" fill="#6B4020"/>
<path d="M29,46 Q27,40 31,36" stroke="#6B4020" stroke-width="4" fill="none" stroke-linecap="round"/>
<!-- eyebrows: confident raised -->
<path d="M36,46 Q41,43 46,46" stroke="#4A2A10" stroke-width="2" fill="none" stroke-linecap="round"/>
<path d="M54,46 Q59,43 64,46" stroke="#4A2A10" stroke-width="2" fill="none" stroke-linecap="round"/>
<!-- eyes: confident wide -->
<ellipse cx="41" cy="53" rx="5" ry="5" fill="white"/>
<ellipse cx="59" cy="53" rx="5" ry="5" fill="white"/>
<circle cx="41" cy="53" r="3.2" fill="#2C3E7A"/>
<circle cx="59" cy="53" r="3.2" fill="#2C3E7A"/>
<circle cx="42.5" cy="51.5" r="1.2" fill="white"/>
<circle cx="60.5" cy="51.5" r="1.2" fill="white"/>
<!-- rosy cheeks -->
<ellipse cx="33" cy="59" rx="5" ry="3.5" fill="#FFB0B0" opacity="0.4"/>
<ellipse cx="67" cy="59" rx="5" ry="3.5" fill="#FFB0B0" opacity="0.4"/>
<!-- nose -->
<circle cx="50" cy="60" r="1.2" fill="#C9906A"/>
<!-- mouth: big energetic grin -->
<path d="M43,66 Q50,75 57,66" stroke="#BF7050" stroke-width="2.2" fill="none" stroke-linecap="round"/>
<path d="M43,66 Q42,70 45,71" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<path d="M57,66 Q58,70 55,71" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<!-- prop: thumbs up symbol -->
<path d="M76,20 Q76,16 79,14 L82,14 L82,10 Q82,8 84,8 Q86,8 86,10 L86,14 L88,14 Q90,14 90,16 L90,22 Q90,24 88,24 L78,24 Q76,24 76,22Z" fill="#FFB830" opacity="0.75"/>
<rect x="74" y="20" width="4" height="6" rx="1" fill="#E09000" opacity="0.75"/>
</svg>`,

ESFP: `<svg viewBox="0 0 100 130" xmlns="http://www.w3.org/2000/svg">
<rect width="100" height="130" rx="14" fill="#FFCDD2"/>
<!-- bright teal/turquoise top -->
<path d="M13,130 L13,92 Q22,85 42,82 Q50,88 58,82 Q78,85 87,92 L87,130Z" fill="#26B8B0"/>
<!-- collar detail -->
<path d="M42,82 Q50,90 58,82 Q54,87 50,89 Q46,87 42,82Z" fill="#1E9890"/>
<!-- neck -->
<rect x="44" y="70" width="12" height="13" rx="2" fill="#FFDBB5"/>
<!-- head -->
<circle cx="50" cy="56" r="22" fill="#FFDBB5"/>
<!-- ears -->
<ellipse cx="28.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<ellipse cx="71.5" cy="56" rx="3.5" ry="5" fill="#FFDBB5"/>
<!-- hair: long flowing auburn -->
<ellipse cx="50" cy="37" rx="23" ry="12" fill="#A04A1A"/>
<path d="M27.5,46 Q24,58 26,74 Q24,90 26,108 Q24,118 26,126" stroke="#A04A1A" stroke-width="12" fill="none" stroke-linecap="round"/>
<path d="M72.5,46 Q76,58 74,74 Q76,90 74,108 Q76,118 74,126" stroke="#A04A1A" stroke-width="12" fill="none" stroke-linecap="round"/>
<!-- hair highlights -->
<path d="M35,36 Q40,33 46,35" stroke="#D07030" stroke-width="2.5" fill="none" opacity="0.5"/>
<!-- eyebrows -->
<path d="M37,47 Q42,45 46,47" stroke="#6A2A08" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<path d="M54,47 Q58,45 63,47" stroke="#6A2A08" stroke-width="1.8" fill="none" stroke-linecap="round"/>
<!-- eyes: big sparkly -->
<ellipse cx="41" cy="54" rx="5.5" ry="5.5" fill="white"/>
<ellipse cx="59" cy="54" rx="5.5" ry="5.5" fill="white"/>
<circle cx="41" cy="54" r="3.5" fill="#1A1A2E"/>
<circle cx="59" cy="54" r="3.5" fill="#1A1A2E"/>
<circle cx="42.5" cy="52.2" r="1.5" fill="white"/>
<circle cx="60.5" cy="52.2" r="1.5" fill="white"/>
<!-- rosy cheeks -->
<ellipse cx="33" cy="60" rx="5.5" ry="3.5" fill="#FFB0B0" opacity="0.5"/>
<ellipse cx="67" cy="60" rx="5.5" ry="3.5" fill="#FFB0B0" opacity="0.5"/>
<!-- nose -->
<circle cx="50" cy="62" r="1.2" fill="#C9906A"/>
<!-- mouth: big sparkly grin -->
<path d="M42,68 Q50,78 58,68" stroke="#BF7050" stroke-width="2.2" fill="none" stroke-linecap="round"/>
<path d="M42,68 Q41,73 44,74" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<path d="M58,68 Q59,73 56,74" stroke="#BF7050" stroke-width="1.2" fill="none"/>
<!-- prop: microphone + sparkles -->
<rect x="74" y="14" width="7" height="10" rx="3" fill="#E0E0E0" stroke="#9A9A9A" stroke-width="1"/>
<rect x="76" y="24" width="3" height="6" fill="#9A9A9A"/>
<path d="M73,30 L79,30" stroke="#9A9A9A" stroke-width="1.5" stroke-linecap="round"/>
<!-- sparkles -->
<path d="M84,9 L85,5 L86,9 L90,8 L87,11 L89,15 L85,13 L82,15 L83,11 L80,8Z" fill="#FFD700" opacity="0.75"/>
<circle cx="83" cy="22" r="1.5" fill="#FF6B9D" opacity="0.7"/>
<circle cx="88" cy="18" r="1" fill="#FF6B9D" opacity="0.6"/>
</svg>`,
};
