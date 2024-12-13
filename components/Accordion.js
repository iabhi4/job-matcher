import React, { useState } from 'react';
import { motion } from 'framer-motion';
import styles from './Accordion.module.css';

const Accordion = ({ title, children }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleAccordion = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={styles.accordion}>
      <motion.div
        className={styles.accordionHeader}
        onClick={toggleAccordion}
        whileHover={{ backgroundColor: '#e0e0e0' }}
        whileTap={{ scale: 0.98 }}
      >
        <h3>{title}</h3>
        <svg
          className={`${styles.arrow} ${isOpen ? styles.down : ''}`}
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
      </motion.div>

      <motion.div
        initial={{ height: 0, opacity: 0 }}
        animate={{ height: isOpen ? 'auto' : 0, opacity: isOpen ? 1 : 0 }}
        transition={{ duration: 0.3 }}
        className={styles.accordionContent}
      >
        {children}
      </motion.div>
    </div>
  );
};

export default Accordion;