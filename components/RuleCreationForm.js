import React, { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import axios from "../utils/api";
import styles from "./RuleCreationForm.module.css";
import Accordion from "./Accordion";
import { useRouter } from 'next/router';

const RuleCreationForm = ({ onNext }) => {
  const router = useRouter();
  const availableCategories = [
    "Location",
    "Compensation",
    "Education Level",
    "Pay",
    "Skills",
    "Tools",
    "Certifications",
    "Years of Experience",
    "Number of Papers published",
    "Sponsorship",
    "Work Authorization",
  ];

  const [rules, setRules] = useState([{ category: "", rule: "" }]);
  const [usedCategories, setUsedCategories] = useState([]);

  const handleRuleChange = (index, field, value) => {
    const updatedRules = [...rules];
    updatedRules[index][field] = value;
    setRules(updatedRules);
  };

  const handleCategoryChange = (index, value) => {
    const updatedUsedCategories = [...usedCategories];
    updatedUsedCategories[index] = value;
    setUsedCategories(updatedUsedCategories);
    handleRuleChange(index, "category", value);
  };

  const addRule = () => {
    setRules([...rules, { category: "", rule: "" }]);
  };

  const getAvailableCategories = (index) => {
    return availableCategories.filter(
      (category) =>
        !usedCategories.includes(category) ||
        category === rules[index].category
    );
  };

  const fetchRules = useCallback(async () => {
    try {
      name = "Abhinav Sin";
      const response = await axios.get(`/rules/${name}`);
      if (response.status === 200 && response.data.rules) {
        setRules(response.data.rules);
        const fetchedUsedCategories = response.data.rules.map(
          (rule) => rule.category
        );
        setUsedCategories(fetchedUsedCategories);
      } else {
        // If no rules, reset to default empty state
        setRules([{ category: "", rule: "" }]);
        setUsedCategories([]);
      }
    } catch (error) {
      console.error("Error fetching rules:", error);
      setRules([{ category: "", rule: "" }]);
      setUsedCategories([]);
    }
  }, []);

  useEffect(() => {
    fetchRules();
  }, [fetchRules]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const rulesData = {
      user_id: "Abhinav Sin",
      rules: rules.map((rule) => ({
        category: rule.category,
        rule: rule.rule,
      })),
    };

    try {
      const response = await axios.post(
        "/rules",
        rulesData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      console.log("Rules saved:", response.data);
      router.push("/dashboard");
    } catch (error) {
      console.error("Error saving rules:", error);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={styles["resume-form-container"]}
    >
      <h1 className={styles["form-heading"]}>Create Matching Rules</h1>
      <form onSubmit={handleSubmit} className={styles["form-body"]}>
        <Accordion title="Rules">
          <div className={styles["form-section"]}>
            {rules.map((rule, index) => (
              <div key={index} className={styles["form-group"]}>
                <div className={styles["input-group"]}>
                  <select
                    value={rule.category}
                    onChange={(e) => handleCategoryChange(index, e.target.value)}
                    className={styles["form-input"]}
                  >
                    <option value="">Select Category</option>
                    {getAvailableCategories(index).map((category) => (
                      <option key={category} value={category}>
                        {category}
                      </option>
                    ))}
                  </select>
                  <input
                    type="text"
                    placeholder="Enter comma-separated rules"
                    value={rule.rule}
                    onChange={(e) =>
                      handleRuleChange(index, "rule", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                </div>
              </div>
            ))}
            <button
              type="button"
              onClick={addRule}
              className={styles["add-button"]}
            >
              Add Rule
            </button>
          </div>
        </Accordion>
        <button type="submit" className={styles["submit-button"]}>
          Save Rules
        </button>
      </form>
    </motion.div>
  );
};

export default RuleCreationForm;