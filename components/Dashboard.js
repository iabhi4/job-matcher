import React, { useState, useEffect } from "react";
import axios from "../utils/api";
import styles from "./Dashboard.module.css";
import { motion } from "framer-motion";
import Navbar from "./Navbar";
import MatchAnalysisPopup from "./MatchAnalysisPopup";
import DetailedMatchPopup from "./DetailedMatchPopup";

const Dashboard = () => {
  const [matchedJobs, setMatchedJobs] = useState([]);
  const [showAnalysisPopup, setShowAnalysisPopup] = useState(false);
  const [showDetailedMatchPopup, setShowDetailedMatchPopup] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);

  useEffect(() => {
    const fetchMatchedJobs = async () => {
      try {
        const response = await axios.get("/jobs");
        setMatchedJobs(response.data);
      } catch (error) {
        console.error("Error fetching matched jobs:", error);
      }
    };

    fetchMatchedJobs();
  }, []);

  const handleNewMatchClick = () => {
    setShowAnalysisPopup(true);
  };

  const handleCloseAnalysisPopup = () => {
    setShowAnalysisPopup(false);
  };

  const handleCardClick = async (jobId) => {
    try {
      const response = await axios.get(`/getJob/${jobId}`);
      setSelectedJob(response.data);
      setShowDetailedMatchPopup(true);
    } catch (error) {
      console.error("Error fetching job details:", error);
    }
  };

  const handleCloseDetailedMatchPopup = () => {
    setShowDetailedMatchPopup(false);
  };

  return (
    <div>
      <Navbar />
      <div className={styles.dashboardContainer}>
        <h1 className={styles.dashboardHeading}>Your Matched Jobs</h1>

        <div className={styles.buttonContainer}>
          <button
            onClick={handleNewMatchClick}
            className={styles.newMatchButton}
          >
            See a New Match
          </button>
        </div>

        <div className={styles.cardsContainer}>
          {matchedJobs.map((job) => (
            <motion.div
              key={job.id}
              className={styles.card}
              onClick={() => handleCardClick(job.id)}
              whileHover={{ scale: 1.03 }}
              whileTap={{ scale: 0.98 }}
            >
              <div className={styles.cardContent}>
                <h2 className={styles.companyName}>{job.companyName}</h2>
                <p className={styles.jobTitle}>{job.jobTitle}</p>
                <p className={styles.jobLocation}>{job.location}</p>
                <p className={styles.matchScore}>Match Score: {job.matchScore}%</p>
              </div>
            </motion.div>
          ))}
        </div>

        {showAnalysisPopup && (
          <MatchAnalysisPopup onClose={handleCloseAnalysisPopup} />
        )}

        {showDetailedMatchPopup && (
          <DetailedMatchPopup
            job={selectedJob}
            onClose={handleCloseDetailedMatchPopup}
          />
        )}
      </div>
    </div>
  );
};

export default Dashboard;