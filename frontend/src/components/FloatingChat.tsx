import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiMessageCircle, FiX } from 'react-icons/fi';
import ChatBot from './ChatBot';
import '../styles/FloatingChat.css';

interface FloatingChatProps {
  deviceName?: string;
}

export const FloatingChat: React.FC<FloatingChatProps> = ({ deviceName }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <>
      {/* Floating Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            className="floating-chat-window"
            initial={{ opacity: 0, scale: 0.8, y: 50, x: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0, x: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 50, x: 20 }}
            transition={{ 
              type: 'spring', 
              stiffness: 350, 
              damping: 30,
              mass: 0.8
            }}
          >
            <ChatBot deviceName={deviceName} onClose={() => setIsOpen(false)} />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Floating Action Button */}
      <AnimatePresence mode="wait">
        {!isOpen ? (
          <motion.button
            key="open-btn"
            className="floating-chat-button"
            onClick={() => setIsOpen(true)}
            title="Open AI Assistant" aria-label="Open AI Assistant"
            style={{ position: 'fixed', bottom: 24, right: 24 }}
            initial={{ scale: 0, opacity: 0 }}
            animate={{ 
              scale: 1, 
              opacity: 1
            }}
            exit={{ scale: 0, opacity: 0 }}
            whileHover={{ 
              scale: 1.1,
              boxShadow: '0 12px 40px rgba(88, 166, 175, 0.5)'
            }}
            whileTap={{ scale: 0.9 }}
            transition={{ 
              type: 'spring', 
              stiffness: 400, 
              damping: 20
            }}
          >
            <FiMessageCircle className="w-7 h-7" />
            <span className="chat-badge">AI</span>
          </motion.button>
        ) : (
          <motion.button
            key="close-btn"
            className="floating-chat-button"
            onClick={() => setIsOpen(false)}
            title="Close AI Assistant" aria-label="Close AI Assistant"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            exit={{ scale: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            transition={{ type: 'spring', stiffness: 400, damping: 20 }}
            style={{ position: 'fixed', bottom: 24, right: 24, background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)' }}
          >
            <FiX className="w-7 h-7" />
          </motion.button>
        )}
      </AnimatePresence>
    </>
  );
};

export default FloatingChat;
