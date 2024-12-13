import React from "react";
import { motion } from "framer-motion";
import styles from "./DetailedMatchPopup.module.css";

const DetailedMatchPopup = ({ job, onClose }) => {
  if (!job) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className={styles.popupOverlay}
      onClick={onClose}
    >
      <motion.div
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        exit={{ y: -20, opacity: 0 }}
        className={styles.popupContent}
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className={styles.popupTitle}>{job.companyName}</h2>
        <h3 className={styles.popupTitle}>{job.jobTitle}</h3>

        {/* Prolog Analysis */}
        {job.detailedAnalysis && (
          <div className={styles.popupSection}>
            <h3 className={styles.sectionHeading}>Prolog Matches</h3>
            <ul className={styles.list}>
              {job.detailedAnalysis.prolog_analysis.matched_rules.map(
                (rule, index) => (
                  <li key={index} className={styles.listItem}>
                    {rule}
                  </li>
                )
              )}
            </ul>
            <p className={styles.score}>
              Score: {job.detailedAnalysis.prolog_analysis.score}
            </p>
          </div>
        )}

        {/* Resume Analysis */}
        {job.detailedAnalysis && (
          <div className={styles.popupSection}>
            <h3 className={styles.sectionHeading}>Resume Matches</h3>
            <ul className={styles.list}>
              {job.detailedAnalysis.resume_analysis.matched_keywords.map(
                (keyword, index) => (
                  <li key={index} className={styles.listItem}>
                    {keyword}
                  </li>
                )
              )}
            </ul>
            <p className={styles.score}>
              Score: {job.detailedAnalysis.resume_analysis.score}
            </p>
          </div>
        )}

        <button className={styles.closeButton} onClick={onClose}>
          Close
        </button>
      </motion.div>
    </motion.div>
  );
};

export default DetailedMatchPopup;