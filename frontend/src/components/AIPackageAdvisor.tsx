import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiX, FiAlertTriangle, FiCheckCircle, FiZap, FiXOctagon, FiRefreshCw, FiPackage, FiAlertCircle } from 'react-icons/fi';
import { usePackageAdvisor } from '../hooks/usePackageAdvisor';
import { useTheme } from '../App';
import { fadeSlideUp } from '../utils/animations';

interface AIPackageAdvisorProps {
  packageName: string | null;
  onClose: () => void;
}

const AIPackageAdvisor: React.FC<AIPackageAdvisorProps> = ({ packageName, onClose }) => {
  const { loading, error, data, refetch } = usePackageAdvisor(packageName);
  const { theme } = useTheme();
  const isLightMode = theme === 'light';
  const contentRef = React.useRef<HTMLDivElement>(null);

  // Auto-scroll to top when package changes or data loads
  React.useEffect(() => {
    if (contentRef.current) {
      contentRef.current.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }, [packageName, data]);

  const getRiskIcon = (category: string) => {
    switch (category) {
      case 'Safe':
        return <FiCheckCircle className="w-5 h-5" />;
      case 'Caution':
        return <FiAlertTriangle className="w-5 h-5" />;
      case 'Expert':
        return <FiZap className="w-5 h-5" />;
      case 'Dangerous':
        return <FiXOctagon className="w-5 h-5" />;
      default:
        return <FiAlertCircle className="w-5 h-5" />;
    }
  };

  const getRiskColor = (category: string) => {
    switch (category) {
      case 'Safe':
        return {
          bg: 'rgba(16, 185, 129, 0.12)',
          text: '#10B981',
          border: 'rgba(16, 185, 129, 0.25)',
        };
      case 'Caution':
        return {
          bg: 'rgba(251, 191, 36, 0.12)',
          text: '#F59E0B',
          border: 'rgba(251, 191, 36, 0.25)',
        };
      case 'Expert':
        return {
          bg: 'rgba(249, 115, 22, 0.12)',
          text: '#F97316',
          border: 'rgba(249, 115, 22, 0.25)',
        };
      case 'Dangerous':
        return {
          bg: 'rgba(239, 68, 68, 0.12)',
          text: '#EF4444',
          border: 'rgba(239, 68, 68, 0.25)',
        };
      default:
        return {
          bg: 'rgba(156, 163, 175, 0.12)',
          text: '#6B7280',
          border: 'rgba(156, 163, 175, 0.25)',
        };
    }
  };

  // ⚡ Bolt: Cache risk color object outside of the JSX return to avoid calling getRiskColor
  // multiple times during render, improving performance and readability.
  const riskColor = data ? getRiskColor(data.riskCategory) : null;

  return (
    <AnimatePresence>
      {packageName && (
        <motion.div
          className="fixed inset-y-0 right-0 w-full md:w-[480px] z-50 flex flex-col"
          style={{
            background: isLightMode
              ? 'linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(255, 255, 255, 0.90) 100%)'
              : 'linear-gradient(135deg, rgba(17, 17, 17, 0.95) 0%, rgba(13, 13, 13, 0.95) 100%)',
            backdropFilter: 'blur(24px) saturate(180%)',
            WebkitBackdropFilter: 'blur(24px) saturate(180%)',
            boxShadow: isLightMode
              ? '-4px 0 24px rgba(0, 0, 0, 0.08)'
              : '-4px 0 24px rgba(0, 0, 0, 0.3)',
            border: isLightMode ? '1px solid rgba(0, 0, 0, 0.05)' : 'none',
          }}
          initial={{ x: '100%' }}
          animate={{ x: 0 }}
          exit={{ x: '100%' }}
          transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
        >
          {/* Header */}
          <div
            className="flex items-center justify-between px-6 py-4"
            style={{
              borderBottom: isLightMode
                ? '1px solid rgba(0, 0, 0, 0.06)'
                : '1px solid rgba(255, 255, 255, 0.06)',
            }}
          >
            <div className="flex items-center gap-3">
              <div
                style={{
                  background: isLightMode ? 'rgba(46, 196, 182, 0.12)' : 'rgba(88, 166, 175, 0.12)',
                  borderRadius: '10px',
                  padding: '8px',
                }}
              >
                <FiPackage className="w-5 h-5" style={{ color: 'var(--theme-accent)' }} />
              </div>
              <div>
                <h3 className="text-lg font-semibold" style={{ color: 'var(--theme-text-primary)' }}>
                  AI Safety Analysis
                </h3>
                <p className="text-xs" style={{ color: 'var(--theme-text-tertiary)' }}>
                  Powered by Perplexity AI
                </p>
              </div>
            </div>
            <motion.button
              onClick={onClose}
              className="p-2 rounded-lg"
              style={{
                background: isLightMode ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.03)',
                border: isLightMode ? '1px solid rgba(0, 0, 0, 0.05)' : 'none',
              }}
              whileHover={{
                background: 'rgba(239, 68, 68, 0.15)',
                scale: 1.05,
                rotate: 90,
              }}
              whileTap={{ scale: 0.95 }}
            >
              <FiX className="w-5 h-5" style={{ color: 'var(--theme-text-secondary)' }} />
            </motion.button>
          </div>

          {/* Content */}
          <div ref={contentRef} className="flex-1 overflow-y-auto px-6 py-6">
            {/* Package Name */}
            <motion.div
              className="mb-6"
              variants={fadeSlideUp}
              initial="initial"
              animate="animate"
            >
              <div
                className="px-4 py-3 rounded-lg"
                style={{
                  background: isLightMode ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.03)',
                  border: isLightMode ? '1px solid rgba(0, 0, 0, 0.05)' : 'none',
                }}
              >
                <div className="text-xs font-medium mb-1" style={{ color: 'var(--theme-text-tertiary)' }}>
                  ANALYZING PACKAGE
                </div>
                <div className="text-sm font-mono" style={{ color: 'var(--theme-accent)' }}>
                  {packageName}
                </div>
              </div>
            </motion.div>

            {/* Loading State */}
            {loading && (
              <motion.div
                className="space-y-4"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                {[...Array(5)].map((_, i) => (
                  <div
                    key={i}
                    className="rounded-lg overflow-hidden"
                    style={{
                      background: isLightMode ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.03)',
                      height: i === 0 ? '120px' : '80px',
                    }}
                  >
                    <motion.div
                      className="h-full"
                      style={{
                        background: isLightMode
                          ? 'linear-gradient(90deg, transparent, rgba(46, 196, 182, 0.08), transparent)'
                          : 'linear-gradient(90deg, transparent, rgba(88, 166, 175, 0.08), transparent)',
                      }}
                      animate={{
                        x: ['-100%', '100%'],
                      }}
                      transition={{
                        duration: 1.5,
                        repeat: Infinity,
                        ease: 'linear',
                      }}
                    />
                  </div>
                ))}
                <div className="text-center py-4">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                    className="inline-block"
                  >
                    <FiRefreshCw className="w-6 h-6" style={{ color: 'var(--theme-accent)' }} />
                  </motion.div>
                  <p className="text-sm mt-2" style={{ color: 'var(--theme-text-secondary)' }}>
                    Analyzing package with AI...
                  </p>
                </div>
              </motion.div>
            )}

            {/* Error State */}
            {error && (
              <motion.div
                className="rounded-lg px-4 py-4"
                style={{
                  background: 'rgba(239, 68, 68, 0.12)',
                  border: '1px solid rgba(239, 68, 68, 0.25)',
                }}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
              >
                <div className="flex items-start gap-3">
                  <FiAlertCircle className="w-5 h-5 mt-0.5" style={{ color: '#EF4444' }} />
                  <div className="flex-1">
                    <div className="font-semibold text-sm mb-1" style={{ color: '#EF4444' }}>
                      Analysis Failed
                    </div>
                    <div className="text-xs" style={{ color: '#EF4444', opacity: 0.9 }}>
                      {error}
                    </div>
                    <motion.button
                      onClick={refetch}
                      className="mt-3 px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5"
                      style={{
                        background: 'rgba(239, 68, 68, 0.15)',
                        color: '#EF4444',
                      }}
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      <FiRefreshCw className="w-3.5 h-3.5" />
                      Retry
                    </motion.button>
                  </div>
                </div>
              </motion.div>
            )}

            {/* Success State */}
            {data && !loading && riskColor && (
              <motion.div
                className="space-y-4"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ staggerChildren: 0.1 }}
              >
                {/* Risk Category Badge */}
                <motion.div
                  className="rounded-lg px-4 py-4"
                  style={{
                    background: riskColor.bg,
                    border: `1px solid ${riskColor.border}`,
                  }}
                  variants={fadeSlideUp}
                >
                  <div className="flex items-center gap-3">
                    <div style={{ color: riskColor.text }}>
                      {getRiskIcon(data.riskCategory)}
                    </div>
                    <div>
                      <div className="text-xs font-medium mb-1" style={{ color: riskColor.text, opacity: 0.8 }}>
                        RISK CATEGORY
                      </div>
                      <div className="text-lg font-bold" style={{ color: riskColor.text }}>
                        {data.riskCategory}
                      </div>
                    </div>
                  </div>
                </motion.div>

                {/* Summary */}
                <motion.div
                  className="rounded-lg px-4 py-4"
                  style={{
                    background: isLightMode ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.03)',
                    border: isLightMode ? '1px solid rgba(0, 0, 0, 0.05)' : 'none',
                  }}
                  variants={fadeSlideUp}
                >
                  <div className="text-xs font-semibold mb-2 uppercase tracking-wide" style={{ color: 'var(--theme-text-tertiary)' }}>
                    Summary
                  </div>
                  <div className="text-sm leading-relaxed" style={{ color: 'var(--theme-text-primary)' }}>
                    {data.summary}
                  </div>
                </motion.div>

                {/* Safe to Remove */}
                <motion.div
                  className="rounded-lg px-4 py-3"
                  style={{
                    background: data.safeToRemove
                      ? 'rgba(16, 185, 129, 0.12)'
                      : 'rgba(239, 68, 68, 0.12)',
                    border: data.safeToRemove
                      ? '1px solid rgba(16, 185, 129, 0.25)'
                      : '1px solid rgba(239, 68, 68, 0.25)',
                  }}
                  variants={fadeSlideUp}
                >
                  <div className="flex items-center gap-2">
                    {data.safeToRemove ? (
                      <FiCheckCircle className="w-4 h-4" style={{ color: '#10B981' }} />
                    ) : (
                      <FiXOctagon className="w-4 h-4" style={{ color: '#EF4444' }} />
                    )}
                    <span className="text-sm font-medium" style={{ color: data.safeToRemove ? '#10B981' : '#EF4444' }}>
                      {data.safeToRemove ? 'Safe to remove' : 'Not recommended to remove'}
                    </span>
                  </div>
                </motion.div>

                {/* Purpose */}
                <motion.div
                  className="rounded-lg px-4 py-4"
                  style={{
                    background: isLightMode ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.03)',
                    border: isLightMode ? '1px solid rgba(0, 0, 0, 0.05)' : 'none',
                  }}
                  variants={fadeSlideUp}
                >
                  <div className="text-xs font-semibold mb-2 uppercase tracking-wide" style={{ color: 'var(--theme-text-tertiary)' }}>
                    Purpose
                  </div>
                  <div className="text-sm leading-relaxed" style={{ color: 'var(--theme-text-primary)' }}>
                    {data.purpose}
                  </div>
                </motion.div>

                {/* Consequences */}
                {data.consequences.length > 0 && (
                  <motion.div
                    className="rounded-lg px-4 py-4"
                    style={{
                      background: isLightMode ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.03)',
                      border: isLightMode ? '1px solid rgba(0, 0, 0, 0.05)' : 'none',
                    }}
                    variants={fadeSlideUp}
                  >
                    <div className="text-xs font-semibold mb-3 uppercase tracking-wide" style={{ color: 'var(--theme-text-tertiary)' }}>
                      Consequences of Removal
                    </div>
                    <ul className="space-y-2">
                      {data.consequences.map((consequence: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2 text-sm" style={{ color: 'var(--theme-text-primary)' }}>
                          <span className="mt-1.5" style={{ color: 'var(--theme-accent)' }}>•</span>
                          <span>{consequence}</span>
                        </li>
                      ))}
                    </ul>
                  </motion.div>
                )}

                {/* Dependencies */}
                {data.dependencies.length > 0 && (
                  <motion.div
                    className="rounded-lg px-4 py-4"
                    style={{
                      background: isLightMode ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.03)',
                      border: isLightMode ? '1px solid rgba(0, 0, 0, 0.05)' : 'none',
                    }}
                    variants={fadeSlideUp}
                  >
                    <div className="text-xs font-semibold mb-3 uppercase tracking-wide" style={{ color: 'var(--theme-text-tertiary)' }}>
                      Dependencies
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {data.dependencies.map((dep: string, idx: number) => (
                        <span
                          key={idx}
                          className="px-2 py-1 rounded text-xs font-mono"
                          style={{
                            background: isLightMode ? 'rgba(46, 196, 182, 0.12)' : 'rgba(88, 166, 175, 0.12)',
                            color: 'var(--theme-accent)',
                            border: isLightMode ? '1px solid rgba(46, 196, 182, 0.15)' : 'none',
                          }}
                        >
                          {dep}
                        </span>
                      ))}
                    </div>
                  </motion.div>
                )}

                {/* Best/Worst Case */}
                <motion.div className="space-y-3" variants={fadeSlideUp}>
                  <div
                    className="rounded-lg px-4 py-3"
                    style={{
                      background: 'rgba(16, 185, 129, 0.08)',
                      border: '1px solid rgba(16, 185, 129, 0.15)',
                    }}
                  >
                    <div className="text-xs font-semibold mb-1.5 uppercase tracking-wide" style={{ color: '#10B981' }}>
                      Best Case
                    </div>
                    <div className="text-xs leading-relaxed" style={{ color: '#10B981', opacity: 0.9 }}>
                      {data.bestCase}
                    </div>
                  </div>
                  <div
                    className="rounded-lg px-4 py-3"
                    style={{
                      background: 'rgba(239, 68, 68, 0.08)',
                      border: '1px solid rgba(239, 68, 68, 0.15)',
                    }}
                  >
                    <div className="text-xs font-semibold mb-1.5 uppercase tracking-wide" style={{ color: '#EF4444' }}>
                      Worst Case
                    </div>
                    <div className="text-xs leading-relaxed" style={{ color: '#EF4444', opacity: 0.9 }}>
                      {data.worstCase}
                    </div>
                  </div>
                </motion.div>

                {/* User Reports */}
                {data.userReports.length > 0 && (
                  <motion.div
                    className="rounded-lg px-4 py-4"
                    style={{
                      background: isLightMode ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.03)',
                      border: isLightMode ? '1px solid rgba(0, 0, 0, 0.05)' : 'none',
                    }}
                    variants={fadeSlideUp}
                  >
                    <div className="text-xs font-semibold mb-3 uppercase tracking-wide" style={{ color: 'var(--theme-text-tertiary)' }}>
                      Community Reports (Reddit/XDA)
                    </div>
                    <ul className="space-y-2">
                      {data.userReports.map((report: string, idx: number) => (
                        <li key={idx} className="flex items-start gap-2 text-xs" style={{ color: 'var(--theme-text-secondary)' }}>
                          <span className="mt-1" style={{ color: 'var(--theme-accent)' }}>•</span>
                          <span>{report}</span>
                        </li>
                      ))}
                    </ul>
                  </motion.div>
                )}

                {/* Technical Details */}
                <motion.div
                  className="rounded-lg px-4 py-4"
                  style={{
                    background: isLightMode ? 'rgba(0, 0, 0, 0.03)' : 'rgba(255, 255, 255, 0.03)',
                    border: isLightMode ? '1px solid rgba(0, 0, 0, 0.05)' : 'none',
                  }}
                  variants={fadeSlideUp}
                >
                  <div className="text-xs font-semibold mb-2 uppercase tracking-wide" style={{ color: 'var(--theme-text-tertiary)' }}>
                    Technical Details
                  </div>
                  <div className="text-xs leading-relaxed" style={{ color: 'var(--theme-text-secondary)' }}>
                    {data.technicalDetails}
                  </div>
                </motion.div>
              </motion.div>
            )}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

export default AIPackageAdvisor;
