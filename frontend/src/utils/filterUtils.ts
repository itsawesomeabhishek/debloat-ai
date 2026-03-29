import type { SafetyLevel } from '../types';

// Shared filter utilities
export const filterUtils = {
  // Filter chips data
  getFilterChips: () => [
    { id: 'all', label: 'All', icon: 'FiList', color: 'accent' },
    { id: 'Safe', label: 'Safe', icon: 'FiCheckCircle', color: '#10B981' },
    { id: 'Caution', label: 'Caution', icon: 'FiAlertTriangle', color: '#F59E0B' },
    { id: 'Expert', label: 'Expert', icon: 'FiZap', color: '#F97316' },
    { id: 'Dangerous', label: 'Dangerous', icon: 'FiTrash2', color: '#EF4444' },
  ] as const,

  // Get color for safety level
  getSafetyColor: (level: SafetyLevel): string => {
    const colors: Record<SafetyLevel, string> = {
      Safe: '#10B981',
      Caution: '#F59E0B',
      Expert: '#F97316',
      Dangerous: '#EF4444',
    };
    return colors[level];
  },

  // Get background for safety level
  getSafetyBg: (level: SafetyLevel, isLight: boolean): string => {
    const light: Record<SafetyLevel, string> = {
      Safe: 'rgba(16, 185, 129, 0.12)',
      Caution: 'rgba(251, 191, 36, 0.12)',
      Expert: 'rgba(249, 115, 22, 0.12)',
      Dangerous: 'rgba(239, 68, 68, 0.12)',
    };
    const dark: Record<SafetyLevel, string> = {
      Safe: 'rgba(16, 185, 129, 0.08)',
      Caution: 'rgba(251, 191, 36, 0.08)',
      Expert: 'rgba(249, 115, 22, 0.08)',
      Dangerous: 'rgba(239, 68, 68, 0.08)',
    };
    return isLight ? light[level] : dark[level];
  },
};
