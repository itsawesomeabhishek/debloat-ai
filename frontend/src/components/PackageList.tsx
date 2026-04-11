import React, { useEffect, useState, useMemo, useCallback } from 'react';
import { api, Package } from '../utils/api';
import { motion, AnimatePresence } from 'framer-motion';
import { useDeviceMonitor } from '../hooks/useDeviceMonitor';
import { useTheme } from '../App';
import {
  FiPackage,
  FiAlertTriangle,
  FiCheckCircle,
  FiSearch,
  FiX,
  FiZap,
  FiXOctagon,
  FiInfo,
} from 'react-icons/fi';

type SafetyLevel = Package['safetyLevel'];

interface PackageStats {
  total: number;
  safe: number;
  caution: number;
  expert: number;
  dangerous: number;
  selected: number;
}

interface PackageListProps {
  selectedPackages: Set<string>;
  onSelectionChange: (selected: Set<string>) => void;
  onStatsChange: (stats: PackageStats) => void;
  filterBySafety?: string | null;
  onPackageDataChange?: (packages: Array<{ packageName: string; safetyLevel: string }>) => void;
  onAiAdvisorOpen?: (packageName: string) => void;
  refreshTrigger?: number;
}

const getSafetyStyles = (level: SafetyLevel): string => {
  switch (level) {
    case 'Safe':
      return 'badge-safe';
    case 'Caution':
      return 'badge-caution';
    case 'Expert':
      return 'badge-expert';
    case 'Dangerous':
      return 'badge-dangerous';
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-white';
  }
};

const getSafetyIcon = (level: SafetyLevel): JSX.Element => {
  switch (level) {
    case 'Safe':
      return <FiCheckCircle className="w-3.5 h-3.5" />;
    case 'Caution':
      return <FiAlertTriangle className="w-3.5 h-3.5" />;
    case 'Expert':
      return <FiZap className="w-3.5 h-3.5" />;
    case 'Dangerous':
      return <FiXOctagon className="w-3.5 h-3.5" />;
    default:
      return <FiInfo className="w-3.5 h-3.5" />;
  }
};

interface PackageListItemProps {
  pkg: Package;
  isSelected: boolean;
  isLightMode: boolean;
  toggleSelect: (packageName: string) => void;
  onAiAdvisorOpen?: (packageName: string) => void;
}

// ⚡ Bolt: Wrapped PackageListItem in React.memo to prevent unnecessary re-renders.
// Now, only the clicked item will re-render instead of the entire list.
const PackageListItem = React.memo(({ pkg, isSelected, isLightMode, toggleSelect, onAiAdvisorOpen }: PackageListItemProps) => {
  return (
    <div
      className="package-card-hover pkg-fade-in"
      style={{
        background: isSelected
          ? (isLightMode
            ? 'linear-gradient(135deg, rgba(46,196,182,0.15) 0%, rgba(46,196,182,0.10) 100%)'
            : 'linear-gradient(135deg, rgba(88,166,175,0.15) 0%, rgba(88,166,175,0.10) 100%)')
          : (isLightMode ? 'rgba(255,255,255,0.7)' : 'rgba(40,40,40,0.6)'),
        border: isLightMode ? '1px solid rgba(0,0,0,0.10)' : '1px solid rgba(255,255,255,0.10)',
        borderRadius: '12px',
        padding: '14px 16px',
        cursor: 'pointer',
        boxShadow: isSelected
          ? (isLightMode
            ? '0 0 18px rgba(46,196,182,0.20), 0 4px 14px rgba(0,0,0,0.08)'
            : '0 0 18px rgba(88,166,175,0.15), 0 4px 14px rgba(0,0,0,0.06)')
          : (isLightMode ? '0 2px 8px rgba(0,0,0,0.06)' : '0 2px 8px rgba(0,0,0,0.04)'),
        transition: 'all 0.15s ease',
      }}
      onClick={() => toggleSelect(pkg.packageName)}
    >
      <div className="flex items-center gap-3">
        {/* Checkbox */}
        <input
          type="checkbox"
          checked={isSelected}
          onChange={(e) => {
            e.stopPropagation();
            toggleSelect(pkg.packageName);
          }}
          className="flex-shrink-0"
          style={{
            width: '20px',
            height: '20px',
            accentColor: isLightMode ? '#2EC4B6' : '#58A6AF',
            cursor: 'pointer',
            border: `2px solid ${isLightMode ? '#2EC4B6' : '#58A6AF'}`,
            borderRadius: '4px',
          }}
          onClick={(e) => e.stopPropagation()}
        />

        {/* Package Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <FiPackage className="w-3.5 h-3.5 flex-shrink-0" style={{ color: isLightMode ? '#2EC4B6' : '#58A6AF' }} />
            <span className="text-sm font-semibold truncate" style={{ color: isLightMode ? '#0F0F0F' : '#FFFFFF', fontWeight: '600' }}>
              {pkg.appName}
            </span>
          </div>
          <div className="text-xs font-mono truncate" style={{ color: isLightMode ? '#525252' : '#A0A0A0' }}>
            {pkg.packageName}
          </div>
        </div>

        {/* AI Advisor Button */}
        <button
          onClick={(e) => {
            e.stopPropagation();
            onAiAdvisorOpen?.(pkg.packageName);
          }}
          className="flex-shrink-0 p-2 rounded-lg ai-advisor-btn"
          style={{
            background: isLightMode ? 'rgba(46, 196, 182, 0.15)' : 'rgba(88, 166, 175, 0.15)',
            border: isLightMode ? '1px solid rgba(46, 196, 182, 0.20)' : '1px solid rgba(88, 166, 175, 0.20)',
          }}
          title="AI Safety Analysis"
        >
          <FiZap className="w-4 h-4" style={{ color: isLightMode ? '#2EC4B6' : '#58A6AF' }} />
        </button>

        {/* Safety Badge */}
        <div className="flex-shrink-0">
          <span
            className={getSafetyStyles(pkg.safetyLevel)}
            style={{
              fontSize: '11px',
              padding: '4px 8px',
              borderRadius: '6px',
            }}
          >
            {getSafetyIcon(pkg.safetyLevel)} {pkg.safetyLevel}
          </span>
        </div>
      </div>
    </div>
  );
});

const PackageList: React.FC<PackageListProps> = ({
  selectedPackages,
  onSelectionChange,
  onStatsChange,
  filterBySafety,
  onPackageDataChange,
  onAiAdvisorOpen,
  refreshTrigger,
}) => {
  const { theme } = useTheme();
  const isLightMode = theme === 'light';
  const [packages, setPackages] = useState<Package[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [search, setSearch] = useState<string>('');
  const [detailPackage, setDetailPackage] = useState<Package | null>(null);
  const { isConnected, deviceId } = useDeviceMonitor();

  const fetchPackages = useCallback(async (retryCount = 0) => {
    setLoading(true);
    try {
      const res = await api.listPackages();
      const pkgs = res ?? [];
      setPackages(pkgs);

      // Pass package data to parent for safety checking
      if (onPackageDataChange) {
        onPackageDataChange(pkgs.map(p => ({ packageName: p.packageName, safetyLevel: p.safetyLevel })));
      }

      // If device is connected but packages came back empty, retry (ADB may not be ready yet)
      if (pkgs.length === 0 && retryCount < 6) {
        setTimeout(() => {
          fetchPackages(retryCount + 1);
        }, 2000);
      }
    } catch (err) {
      console.error('list_packages failed', err);
      setPackages([]);
      if (onPackageDataChange) {
        onPackageDataChange([]);
      }
      // Retry on error too (device may still be initializing)
      if (retryCount < 6) {
        setTimeout(() => {
          fetchPackages(retryCount + 1);
        }, 2000);
      }
    } finally {
      setLoading(false);
    }
  }, [onPackageDataChange]);

  // Fetch packages when device connects or changes
  useEffect(() => {
    if (isConnected && deviceId) {
      // Fetch immediately
      fetchPackages();
      // Also retry after a short delay in case ADB isn't fully ready yet
      const retryTimer = setTimeout(() => {
        if (packages.length === 0) {
          fetchPackages();
        }
      }, 3000);
      // Clear selection when device changes
      onSelectionChange(new Set());
      return () => clearTimeout(retryTimer);
    } else {
      // Clear packages when device disconnects
      setPackages([]);
      onSelectionChange(new Set());
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isConnected, deviceId, fetchPackages]);

  // Refresh packages when refreshTrigger changes (manual refresh from DevicePanel)
  useEffect(() => {
    if (refreshTrigger && refreshTrigger > 0) {
      // Force refresh regardless of connection state (user explicitly requested it)
      setLoading(true);
      // Small delay to ensure device state is updated
      const refreshTimer = setTimeout(() => {
        fetchPackages(0); // Start fresh with retry count 0
      }, 500);
      return () => clearTimeout(refreshTimer);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [refreshTrigger]);

  // ⚡ Bolt: Cache base package stats to avoid O(4N) recalculation on every selection toggle.
  // Single-pass loop replaces four separate .filter() calls.
  const baseStats = useMemo(() => {
    let safe = 0, caution = 0, expert = 0, dangerous = 0;
    for (let i = 0; i < packages.length; i++) {
      const level = packages[i].safetyLevel;
      if (level === 'Safe') safe++;
      else if (level === 'Caution') caution++;
      else if (level === 'Expert') expert++;
      else if (level === 'Dangerous') dangerous++;
    }
    return { total: packages.length, safe, caution, expert, dangerous };
  }, [packages]);

  // Update stats whenever base stats or selection changes
  useEffect(() => {
    const stats: PackageStats = {
      ...baseStats,
      selected: selectedPackages.size,
    };
    onStatsChange(stats);
  }, [baseStats, selectedPackages.size, onStatsChange]);

  const filtered = useMemo(() => {
    const searchLower = search.toLowerCase();
    return packages.filter((pkg) => {
      // Search filter
      const matchesSearch =
        pkg.packageName.toLowerCase().includes(searchLower) ||
        pkg.appName.toLowerCase().includes(searchLower);

      if (!matchesSearch) return false;

      // Safety level filter
      if (filterBySafety) {
        return pkg.safetyLevel === filterBySafety;
      }

      return true;
    });
  }, [packages, search, filterBySafety]);

  // ⚡ Bolt: Use a ref to store the latest selectedPackages to avoid
  // re-creating the toggleSelect function every time selection changes.
  // This allows the child PackageListItem components to remain memoized.
  const selectedPackagesRef = React.useRef(selectedPackages);
  useEffect(() => {
    selectedPackagesRef.current = selectedPackages;
  }, [selectedPackages]);

  const toggleSelect = useCallback((packageName: string) => {
    const newSet = new Set(selectedPackagesRef.current);
    if (newSet.has(packageName)) {
      newSet.delete(packageName);
    } else {
      newSet.add(packageName);
    }
    onSelectionChange(newSet);
  }, [onSelectionChange]);

  return (
    <div className="w-full p-5 md:p-6" style={{
      background: isLightMode
        ? 'linear-gradient(135deg, rgba(255,255,255,0.85) 0%, rgba(255,255,255,0.75) 100%)'
        : 'linear-gradient(135deg, rgba(26,26,26,0.85) 0%, rgba(20,20,20,0.85) 100%)',
      backdropFilter: 'blur(20px)',
      borderRadius: '16px',
      border: isLightMode ? '1px solid rgba(0,0,0,0.08)' : '1px solid rgba(255,255,255,0.08)',
      boxShadow: isLightMode ? '0 4px 16px rgba(0,0,0,0.06)' : '0 4px 16px rgba(0,0,0,0.3)',
    }}>
      {/* Minimal Header */}
      <div className="mb-5">
        <h3 className="text-base font-semibold flex items-center gap-2.5" style={{ color: isLightMode ? '#1A1A1A' : '#FFFFFF' }}>
          <FiPackage className="w-4 h-4" style={{ color: isLightMode ? '#2EC4B6' : '#58A6AF' }} />
          Packages
        </h3>
        <p className="text-xs mt-1.5" style={{ color: isLightMode ? '#666666' : '#A0A0A0' }}>
          {filtered.length} of {packages.length} shown
        </p>
      </div>

      {/* Minimal Search Bar */}
      <div className="relative mb-5 group">
        <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
          <FiSearch className="w-4 h-4" style={{ color: isLightMode ? '#999999' : '#A0A0A0' }} />
        </div>
        <input
          type="text"
          placeholder="Search packages..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{
            backgroundColor: isLightMode ? 'rgba(0,0,0,0.03)' : 'rgba(255,255,255,0.05)',
            border: isLightMode ? '1px solid rgba(0,0,0,0.08)' : '1px solid rgba(255,255,255,0.10)',
            borderRadius: '10px',
            padding: '10px 40px 10px 38px',
            width: '100%',
            fontSize: '14px',
            color: isLightMode ? '#1A1A1A' : '#FFFFFF',
            outline: 'none',
            transition: 'all 250ms ease',
          }}
          onFocus={(e) => {
            e.target.style.backgroundColor = isLightMode ? 'rgba(0,0,0,0.04)' : 'rgba(255,255,255,0.06)';
            e.target.style.borderColor = isLightMode ? 'rgba(46,196,182,0.25)' : 'rgba(88,166,175,0.25)';
            e.target.style.boxShadow = isLightMode ? '0 0 12px rgba(46,196,182,0.12)' : '0 0 12px rgba(88,166,175,0.12)';
          }}
          onBlur={(e) => {
            e.target.style.backgroundColor = isLightMode ? 'rgba(0,0,0,0.02)' : 'rgba(255,255,255,0.03)';
            e.target.style.borderColor = isLightMode ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.08)';
            e.target.style.boxShadow = 'none';
          }}
        />
        {search && (
          <button
            onClick={() => setSearch('')}
            className="absolute inset-y-0 right-0 pr-3.5 flex items-center transition-all duration-250"
            style={{ color: isLightMode ? '#999999' : '#A0A0A0', transform: 'scale(1)' }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.1)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
            aria-label="Clear search"
          >
            <FiX className="w-4 h-4" />
          </button>
        )}
      </div>      {loading ? (
        <div className="space-y-2.5">
          {[1, 2, 3, 4, 5].map((i) => (
            <div
              key={i}
              className="h-14 rounded-xl animate-pulse"
              style={{
                background: isLightMode ? 'rgba(0,0,0,0.05)' : 'rgba(255,255,255,0.05)',
                animationDelay: `${i * 80}ms`
              }}
            />
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          {filtered.length === 0 ? (
            <div className="px-4 py-12 text-center">
              <FiPackage className="w-12 h-12 mx-auto mb-3 opacity-50" style={{ color: isLightMode ? '#999999' : '#A0A0A0' }} />
              {packages.length === 0 && isConnected ? (
                <>
                  <p className="text-sm font-medium mb-2" style={{ color: isLightMode ? '#666666' : '#A0A0A0' }}>Device connected but no packages loaded</p>
                  <div className="text-xs space-y-1" style={{ color: isLightMode ? '#999999' : '#888888' }}>
                    <p>This usually means ADB cannot access your device.</p>
                    <p className="font-semibold mt-3" style={{ color: isLightMode ? '#2EC4B6' : '#58A6AF' }}>Quick Fix:</p>
                    <ol className="text-left inline-block mt-2 space-y-1">
                      <li>1. Check USB debugging is enabled on your phone</li>
                      <li>2. Accept the USB debugging popup on your device</li>
                      <li>3. Try a different USB port or cable</li>
                      <li>4. Click "Refresh Device Info" button above</li>
                    </ol>
                  </div>
                </>
              ) : (
                <>
                  <p className="text-sm font-medium" style={{ color: isLightMode ? '#666666' : '#A0A0A0' }}>No packages found</p>
                  <p className="text-xs mt-1" style={{ color: isLightMode ? '#999999' : '#888888' }}>Try adjusting your search</p>
                </>
              )}
            </div>
          ) : (
            <div className="space-y-2">
              {filtered.map((pkg) => (
                <PackageListItem
                  key={pkg.packageName}
                  pkg={pkg}
                  isSelected={selectedPackages.has(pkg.packageName)}
                  isLightMode={isLightMode}
                  toggleSelect={toggleSelect}
                  onAiAdvisorOpen={onAiAdvisorOpen}
                />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Glassmorphic Modal */}
      <AnimatePresence>
        {detailPackage && (
          <motion.div
            className="fixed inset-0 flex items-center justify-center z-50 p-4"
            style={{
              background: isLightMode ? 'rgba(0,0,0,0.40)' : 'rgba(0,0,0,0.75)',
              backdropFilter: 'blur(12px)',
            }}
            onClick={() => setDetailPackage(null)}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          >
            <motion.div
              className="w-full max-w-lg max-h-[90vh] overflow-y-auto"
              style={{
                background: isLightMode
                  ? 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.90) 100%)'
                  : 'linear-gradient(135deg, rgba(17,17,17,0.95) 0%, rgba(13,13,13,0.95) 100%)',
                backdropFilter: 'blur(24px) saturate(180%)',
                border: isLightMode ? '1px solid rgba(0,0,0,0.06)' : 'none',
                borderRadius: '16px',
                padding: '28px',
                boxShadow: isLightMode
                  ? '0 20px 60px rgba(0,0,0,0.15), 0 0 40px rgba(46,196,182,0.12)'
                  : '0 20px 60px rgba(0,0,0,0.5), 0 0 40px rgba(88,166,175,0.12)',
              }}
              onClick={(e) => e.stopPropagation()}
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              transition={{ duration: 0.2, ease: [0.22, 1, 0.36, 1] }}
            >
              {/* Modal Header */}
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2.5">
                  <div
                    style={{
                      background: isLightMode ? 'rgba(46,196,182,0.12)' : 'rgba(88,166,175,0.12)',
                      borderRadius: '10px',
                      padding: '8px',
                    }}
                  >
                    <FiInfo className="w-5 h-5 text-accent" />
                  </div>
                  <h4 className="text-lg font-semibold text-text-primary">
                    Package Details
                  </h4>
                </div>
                <motion.button
                  onClick={() => setDetailPackage(null)}
                  style={{
                    background: isLightMode ? 'rgba(0,0,0,0.02)' : 'rgba(255,255,255,0.02)',
                    border: isLightMode ? '1px solid rgba(0,0,0,0.05)' : 'none',
                    borderRadius: '8px',
                    padding: '8px',
                    cursor: 'pointer',
                  }}
                  whileHover={{
                    background: 'rgba(239,68,68,0.15)',
                    scale: 1.05,
                    rotate: 90,
                    transition: { duration: 0.2 }
                  }}
                  whileTap={{ scale: 0.95 }}
                  aria-label="Close dialog"
                >
                  <FiX className="w-5 h-5 text-text-secondary" />
                </motion.button>
              </div>

              {/* Modal Content */}
              <div className="space-y-4">
                {/* Package Name */}
                <div
                  style={{
                    background: isLightMode ? 'rgba(0,0,0,0.02)' : 'rgba(255,255,255,0.03)',
                    border: isLightMode ? '1px solid rgba(0,0,0,0.05)' : 'none',
                    borderRadius: '12px',
                    padding: '16px',
                  }}
                >
                  <div className="flex items-center gap-2 text-xs font-semibold text-text-tertiary uppercase tracking-wide mb-2.5">
                    <FiPackage className="w-3.5 h-3.5" />
                    Package Name
                  </div>
                  <div
                    className="font-mono text-sm text-text-primary break-all"
                    style={{
                      background: isLightMode ? 'rgba(0,0,0,0.02)' : 'rgba(255,255,255,0.02)',
                      borderRadius: '8px',
                      padding: '10px 12px',
                    }}
                  >
                    {detailPackage.packageName}
                  </div>
                </div>

                {/* App Name */}
                <div
                  style={{
                    background: isLightMode ? 'rgba(46,196,182,0.10)' : 'rgba(88,166,175,0.08)',
                    border: isLightMode ? '1px solid rgba(46,196,182,0.15)' : 'none',
                    borderRadius: '12px',
                    padding: '16px',
                  }}
                >
                  <div className="flex items-center gap-2 text-xs font-semibold text-accent uppercase tracking-wide mb-2.5">
                    <FiPackage className="w-3.5 h-3.5" />
                    Application Name
                  </div>
                  <div className="text-base font-semibold text-text-primary">
                    {detailPackage.appName}
                  </div>
                </div>

                {/* Safety Level */}
                <div
                  style={{
                    background: isLightMode ? 'rgba(0,0,0,0.02)' : 'rgba(255,255,255,0.03)',
                    border: isLightMode ? '1px solid rgba(0,0,0,0.05)' : 'none',
                    borderRadius: '12px',
                    padding: '16px',
                  }}
                >
                  <div className="flex items-center gap-2 text-xs font-semibold text-text-tertiary uppercase tracking-wide mb-2.5">
                    {getSafetyIcon(detailPackage.safetyLevel)}
                    Safety Level
                  </div>
                  <span className={getSafetyStyles(detailPackage.safetyLevel)}>
                    {getSafetyIcon(detailPackage.safetyLevel)} {detailPackage.safetyLevel}
                  </span>
                </div>
              </div>

              {/* Modal Footer */}
              <motion.button
                type="button"
                onClick={() => setDetailPackage(null)}
                className="mt-6 w-full btn-ghost text-sm font-semibold"
                style={{
                  padding: '12px',
                  borderRadius: '10px',
                }}
                whileHover={{ scale: 1.02, y: -1 }}
                whileTap={{ scale: 0.98 }}
              >
                Close
              </motion.button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default PackageList;