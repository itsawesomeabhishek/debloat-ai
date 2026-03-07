// Premium Ultra-Minimal Theme System
// Charcoal Black (#0F0F0F) • Pure White (#FFFFFF) • Teal Accent (#24C8D8)
export interface ThemeColors {
  name: string;
  bg: string;
  card: string;
  border: string;
  hover: string;
  textPrimary: string;
  textSecondary: string;
  accent: string;
  accentHover: string;
  glass: string;
  shadow: string;
  glow: string;
  scrollbarTrack: string;
  scrollbarThumb: string;
  scrollbarThumbHover: string;
  // Safety badge colors
  badges: Record<'safe' | 'caution' | 'expert' | 'dangerous', {
    bg: string;
    color: string;
    border: string;
  }>;
}

export const THEMES: Record<string, ThemeColors> = {
  light: {
    name: 'Light',
    bg: '#F4F4F5',
    card: 'rgba(255,255,255,0.65)',
    border: 'rgba(0, 0, 0, 0.05)',
    hover: 'rgba(46, 196, 182, 0.08)',
    textPrimary: '#1A1A1A',
    textSecondary: '#525252',
    accent: '#2EC4B6',
    accentHover: '#3DD9CA',
    glass: 'rgba(255, 255, 255, 0.65)',
    shadow: 'rgba(0, 0, 0, 0.06)',
    glow: 'rgba(46, 196, 182, 0.18)',
    scrollbarTrack: '#f1f5f9',
    scrollbarThumb: '#cbd5e1',
    scrollbarThumbHover: '#94a3b8',
    // Light mode badge colors
    badges: {
      safe: {
        bg: 'rgba(16, 185, 129, 0.08)',
        color: '#059669',
        border: 'rgba(16, 185, 129, 0.15)',
      },
      caution: {
        bg: '#fef3c7',
        color: '#92400e',
        border: '#fde68a',
      },
      expert: {
        bg: '#fed7aa',
        color: '#9a3412',
        border: '#fdba74',
      },
      dangerous: {
        bg: '#fee2e2',
        color: '#991b1b',
        border: '#fecaca',
      },
    },
  },
  dark: {
    name: 'Dark',
    bg: '#0A0A0A',
    card: '#1A1A1A',
    border: 'rgba(255, 255, 255, 0.08)',
    hover: 'rgba(88, 166, 175, 0.1)',
    textPrimary: '#FFFFFF',
    textSecondary: '#A0A0A0',
    accent: '#58A6AF',
    accentHover: '#6BB8C1',
    glass: 'rgba(26, 26, 26, 0.7)',
    shadow: 'rgba(0, 0, 0, 0.4)',
    glow: 'rgba(88, 166, 175, 0.15)',
    scrollbarTrack: '#1e293b',
    scrollbarThumb: '#475569',
    scrollbarThumbHover: '#64748b',
    // Dark mode badge colors
    badges: {
      safe: {
        bg: 'rgba(16, 185, 129, 0.15)',
        color: '#34D399',
        border: 'rgba(16, 185, 129, 0.35)',
      },
      caution: {
        bg: 'rgba(245, 158, 11, 0.2)',
        color: '#fcd34d',
        border: 'rgba(245, 158, 11, 0.5)',
      },
      expert: {
        bg: 'rgba(249, 115, 22, 0.2)',
        color: '#fb923c',
        border: 'rgba(249, 115, 22, 0.5)',
      },
      dangerous: {
        bg: 'rgba(239, 68, 68, 0.2)',
        color: '#fca5a5',
        border: 'rgba(239, 68, 68, 0.5)',
      },
    },
  },
};

export type ThemeName = keyof typeof THEMES;

export const applyTheme = (themeName: ThemeName) => {
  const theme = THEMES[themeName];
  const root = document.documentElement;

  // Apply premium design tokens
  root.style.setProperty('--theme-bg', theme.bg);
  root.style.setProperty('--theme-card', theme.card);
  root.style.setProperty('--theme-border', theme.border);
  root.style.setProperty('--theme-hover', theme.hover);
  root.style.setProperty('--theme-text-primary', theme.textPrimary);
  root.style.setProperty('--theme-text-secondary', theme.textSecondary);
  root.style.setProperty('--theme-accent', theme.accent);
  root.style.setProperty('--theme-accent-hover', theme.accentHover);
  root.style.setProperty('--theme-glass', theme.glass);
  root.style.setProperty('--theme-shadow', theme.shadow);
  root.style.setProperty('--theme-glow', theme.glow);
  root.style.setProperty('--scrollbar-track', theme.scrollbarTrack);
  root.style.setProperty('--scrollbar-thumb', theme.scrollbarThumb);
  root.style.setProperty('--scrollbar-thumb-hover', theme.scrollbarThumbHover);
  
  // Apply badge colors
  Object.entries(theme.badges).forEach(([level, colors]) => {
    root.style.setProperty(`--badge-${level}-bg`, colors.bg);
    root.style.setProperty(`--badge-${level}-color`, colors.color);
    root.style.setProperty(`--badge-${level}-border`, colors.border);
  });

  // Add/remove dark mode class for Tailwind
  if (themeName === 'light') {
    root.classList.remove('dark');
  } else {
    root.classList.add('dark');
  }
};
