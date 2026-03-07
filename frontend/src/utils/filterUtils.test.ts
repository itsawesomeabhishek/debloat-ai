import { describe, it, expect } from 'vitest';
import { filterUtils } from './filterUtils';
import { SafetyLevel } from '../types';

describe('filterUtils', () => {
  describe('getFilterChips', () => {
    it('should return exactly 5 filter chips', () => {
      const chips = filterUtils.getFilterChips();
      expect(chips).toHaveLength(5);
    });

    it('should contain the expected "all" chip at the beginning', () => {
      const chips = filterUtils.getFilterChips();
      expect(chips[0]).toEqual({
        id: 'all',
        label: 'All',
        icon: 'FiList',
        color: 'accent',
      });
    });

    it('should map safety levels to correct colors in chips', () => {
      const chips = filterUtils.getFilterChips();
      const safeChip = chips.find(c => c.id === 'Safe');
      expect(safeChip?.color).toBe('#10B981');

      const dangerousChip = chips.find(c => c.id === 'Dangerous');
      expect(dangerousChip?.color).toBe('#EF4444');
    });
  });

  describe('getSafetyColor', () => {
    it('should return correct hex colors for each SafetyLevel', () => {
      expect(filterUtils.getSafetyColor('Safe')).toBe('#10B981');
      expect(filterUtils.getSafetyColor('Caution')).toBe('#F59E0B');
      expect(filterUtils.getSafetyColor('Expert')).toBe('#F97316');
      expect(filterUtils.getSafetyColor('Dangerous')).toBe('#EF4444');
    });
  });

  describe('getSafetyBg', () => {
    it('should return correct light theme backgrounds for each SafetyLevel', () => {
      expect(filterUtils.getSafetyBg('Safe', true)).toBe('rgba(16, 185, 129, 0.12)');
      expect(filterUtils.getSafetyBg('Caution', true)).toBe('rgba(251, 191, 36, 0.12)');
      expect(filterUtils.getSafetyBg('Expert', true)).toBe('rgba(249, 115, 22, 0.12)');
      expect(filterUtils.getSafetyBg('Dangerous', true)).toBe('rgba(239, 68, 68, 0.12)');
    });

    it('should return correct dark theme backgrounds for each SafetyLevel', () => {
      expect(filterUtils.getSafetyBg('Safe', false)).toBe('rgba(16, 185, 129, 0.08)');
      expect(filterUtils.getSafetyBg('Caution', false)).toBe('rgba(251, 191, 36, 0.08)');
      expect(filterUtils.getSafetyBg('Expert', false)).toBe('rgba(249, 115, 22, 0.08)');
      expect(filterUtils.getSafetyBg('Dangerous', false)).toBe('rgba(239, 68, 68, 0.08)');
    });
  });
});
