import React, { useState } from "react";
import { motion } from "framer-motion";
import styles from "./MatchAnalysisPopup.module.css";
import axios from "../utils/api";

const MatchAnalysisPopup = ({ onClose }) => {
  const [companyName, setCompanyName] = useState("");
  const [jobDescription, setJobDescription] = useState("");

  const handleCompanyNameChange = (e) => {
    setCompanyName(e.target.value);
  };

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("/analyze", {
        companyName,
        jobDescription,
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
  
      console.log("Match analysis:", response.data); 
  
      onClose(); 
    } catch (error) {
      console.error("Error during match analysis:", error);
    }
  };
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
        <h2 className={styles.popupTitle}>Analyze New Job Match</h2>
        <form onSubmit={handleSubmit}>
          <div className={styles.inputGroup}>
            <label htmlFor="companyName">Company Name:</label>
            <input
              type="text"
              id="companyName"
              value={companyName}
              onChange={handleCompanyNameChange}
              className={styles.inputField}
            />
          </div>
          <div className={styles.inputGroup}>
            <label htmlFor="jobDescription">Job Description:</label>
            <textarea
              id="jobDescription"
              value={jobDescription}
              onChange={handleJobDescriptionChange}
              className={styles.textareaField}
            />
          </div>
          <button type="submit" className={styles.submitButton}>
            See Match Analysis
          </button>
        </form>
        <button className={styles.closeButton} onClick={onClose}>
          Close
        </button>
      </motion.div>
    </motion.div>
  );
};

export default MatchAnalysisPopup;