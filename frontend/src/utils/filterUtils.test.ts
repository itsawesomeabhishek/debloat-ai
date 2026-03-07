import test from 'node:test';
import assert from 'node:assert';
import { filterUtils } from './filterUtils.ts';

test('filterUtils.getFilterChips', () => {
  const chips = filterUtils.getFilterChips();

  assert.strictEqual(chips.length, 5);

  assert.deepStrictEqual(chips[0], { id: 'all', label: 'All', icon: 'FiList', color: 'accent' });
  assert.deepStrictEqual(chips[1], { id: 'Safe', label: 'Safe', icon: 'FiCheckCircle', color: '#10B981' });
  assert.deepStrictEqual(chips[2], { id: 'Caution', label: 'Caution', icon: 'FiAlertTriangle', color: '#F59E0B' });
  assert.deepStrictEqual(chips[3], { id: 'Expert', label: 'Expert', icon: 'FiZap', color: '#F97316' });
  assert.deepStrictEqual(chips[4], { id: 'Dangerous', label: 'Dangerous', icon: 'FiTrash2', color: '#EF4444' });
});

test('filterUtils.getSafetyColor', () => {
  assert.strictEqual(filterUtils.getSafetyColor('Safe'), '#10B981');
  assert.strictEqual(filterUtils.getSafetyColor('Caution'), '#F59E0B');
  assert.strictEqual(filterUtils.getSafetyColor('Expert'), '#F97316');
  assert.strictEqual(filterUtils.getSafetyColor('Dangerous'), '#EF4444');
});

test('filterUtils.getSafetyBg', async (t) => {
  await t.test('light mode', () => {
    assert.strictEqual(filterUtils.getSafetyBg('Safe', true), 'rgba(16, 185, 129, 0.12)');
    assert.strictEqual(filterUtils.getSafetyBg('Caution', true), 'rgba(251, 191, 36, 0.12)');
    assert.strictEqual(filterUtils.getSafetyBg('Expert', true), 'rgba(249, 115, 22, 0.12)');
    assert.strictEqual(filterUtils.getSafetyBg('Dangerous', true), 'rgba(239, 68, 68, 0.12)');
  });

  await t.test('dark mode', () => {
    assert.strictEqual(filterUtils.getSafetyBg('Safe', false), 'rgba(16, 185, 129, 0.08)');
    assert.strictEqual(filterUtils.getSafetyBg('Caution', false), 'rgba(251, 191, 36, 0.08)');
    assert.strictEqual(filterUtils.getSafetyBg('Expert', false), 'rgba(249, 115, 22, 0.08)');
    assert.strictEqual(filterUtils.getSafetyBg('Dangerous', false), 'rgba(239, 68, 68, 0.08)');
  });
});
