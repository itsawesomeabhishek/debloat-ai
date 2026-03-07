import test from 'node:test';
import assert from 'node:assert';
import { storage, storageKeys } from './storage.ts';

test('storage utils', async (t) => {
  // Mock localStorage
  const store = new Map<string, string>();
  const originalLocalStorage = globalThis.localStorage;

  t.beforeEach(() => {
    store.clear();
    globalThis.localStorage = {
      getItem: (key: string) => store.get(key) || null,
      setItem: (key: string, value: string) => store.set(key, value),
      removeItem: (key: string) => store.delete(key),
      clear: () => store.clear(),
      length: store.size,
      key: (index: number) => Array.from(store.keys())[index] || null,
    } as Storage;
  });

  t.afterEach(() => {
    globalThis.localStorage = originalLocalStorage;
  });

  await t.test('storageKeys should have correct keys', () => {
    assert.strictEqual(storageKeys.THEME, 'theme-preference');
    assert.strictEqual(storageKeys.CHAT_MESSAGES, 'chatbot_messages');
    assert.strictEqual(storageKeys.APP_SETTINGS, 'app-settings');
  });

  await t.test('storage.get should return default value if item is not present', () => {
    const val = storage.get('non-existent', 'default');
    assert.strictEqual(val, 'default');
  });

  await t.test('storage.get should return null if item is not present and no default', () => {
    const val = storage.get('non-existent');
    assert.strictEqual(val, null);
  });

  await t.test('storage.set should serialize and store value', () => {
    const obj = { foo: 'bar' };
    storage.set('my-key', obj);
    assert.strictEqual(store.get('my-key'), JSON.stringify(obj));
  });

  await t.test('storage.get should retrieve and deserialize value', () => {
    const obj = { foo: 'bar' };
    store.set('my-key', JSON.stringify(obj));
    const val = storage.get('my-key');
    assert.deepStrictEqual(val, obj);
  });

  await t.test('storage.get should handle parse errors and return default value', () => {
    store.set('my-key', 'invalid-json');
    const val = storage.get('my-key', 'default');
    assert.strictEqual(val, 'default');
  });

  await t.test('storage.remove should remove item', () => {
    store.set('my-key', 'value');
    storage.remove('my-key');
    assert.strictEqual(store.has('my-key'), false);
  });

  await t.test('storage.set should handle errors gracefully', () => {
    const originalConsoleError = console.error;
    let loggedError: unknown = null;
    let loggedMsg: string = '';
    console.error = (msg: string, e: unknown) => {
      loggedMsg = msg;
      loggedError = e;
    };

    // Override setItem to throw
    const originalSetItem = globalThis.localStorage.setItem;
    globalThis.localStorage.setItem = () => { throw new Error('Quota Exceeded'); };

    storage.set('my-key', 'value'); // Shouldn't throw
    assert.strictEqual(loggedMsg, 'Storage error:');
    assert.ok(loggedError instanceof Error);
    assert.strictEqual((loggedError as Error).message, 'Quota Exceeded');

    // Restore
    console.error = originalConsoleError;
    globalThis.localStorage.setItem = originalSetItem;
  });

  await t.test('storage.remove should handle errors gracefully', () => {
    const originalConsoleError = console.error;
    let loggedError: unknown = null;
    let loggedMsg: string = '';
    console.error = (msg: string, e: unknown) => {
      loggedMsg = msg;
      loggedError = e;
    };

    // Override removeItem to throw
    const originalRemoveItem = globalThis.localStorage.removeItem;
    globalThis.localStorage.removeItem = () => { throw new Error('Remove Failed'); };

    storage.remove('my-key'); // Shouldn't throw
    assert.strictEqual(loggedMsg, 'Storage error:');
    assert.ok(loggedError instanceof Error);
    assert.strictEqual((loggedError as Error).message, 'Remove Failed');

    // Restore
    console.error = originalConsoleError;
    globalThis.localStorage.removeItem = originalRemoveItem;
  });
});
