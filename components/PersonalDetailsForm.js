import React, { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import axios from "../utils/api";
import styles from "./PersonalDetailsForm.module.css";
import Accordion from "./Accordion";

const PersonalDetailsForm = ({ onNext }) => {
  const [allUserNames, setAllUserNames] = useState([]);
  const [filteredNames, setFilteredNames] = useState([]);
  const [personalDetails, setPersonalDetails] = useState({
    name: "",
    email: "",
    phone: "",
    linkedin: "",
    github: "",
  });
  const [experience, setExperience] = useState([
    {
      company: "",
      role: "",
      location: "",
      startDate: "",
      endDate: "",
      responsibilities: "",
    },
  ]);
  const [projects, setProjects] = useState([
    { name: "", description: "", technologies: "", startDate: "", endDate: "" },
  ]);
  const [skills, setSkills] = useState({
    languages: "",
    frameworks: "",
    developerTools: "",
    libraries: "",
  });
  const [education, setEducation] = useState([
    {
      institution: "",
      degree: "",
      location: "",
      startYear: "",
      endYear: "",
    },
  ]);

  useEffect(() => {
    const fetchAllUserNames = async () => {
      try {
        const response = await axios.get("/users/names");
        setAllUserNames(response.data);
      } catch (error) {
        console.error("Error fetching user names:", error);
      }
    };
    fetchAllUserNames();
  }, []);

  const handleNameChange = (value) => {
    setPersonalDetails({ ...personalDetails, name: value });
    const filtered = allUserNames.filter((name) =>
      name.toLowerCase().includes(value.toLowerCase())
    );
    setFilteredNames(filtered);
  };

  const fetchData = useCallback(async (name) => {
    try {
      const response = await axios.get(`/users/${name}`); // Change this to user id later
      if (response.status === 200) {
        const userData = response.data;
        const userResume = userData.resume;
        setPersonalDetails({
          name: userData.name,
          email: userResume.personalDetails.email,
          phone: userResume.personalDetails.phone,
          linkedin: userResume.personalDetails.linkedin,
          github: userResume.personalDetails.github,
        });
        setExperience(userResume.experience);
        setProjects(userResume.projects);
        setSkills(userResume.skills);
        setEducation(userResume.education);
      } else {
        console.error("User not found");
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  }, []);

  useEffect(() => {
    if (
      filteredNames.length > 0 &&
      filteredNames.includes(personalDetails.name)
    ) {
      fetchData(personalDetails.name);
    }
  }, [fetchData, filteredNames, personalDetails.name]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const dataToSend = {
      name: personalDetails.name,
      resume: {
        personalDetails,
        experience,
        projects,
        skills,
        education,
      },
    };

    try {
      const response = await axios.post("/save_user", dataToSend, {
        // Updated endpoint
        headers: {
          "Content-Type": "application/json",
        },
      });
      console.log("Data saved:", response.data);
      onNext();
    } catch (error) {
      console.error("Error submitting the form:", error);
    }
  };

  const addExperience = () =>
    setExperience([
      ...experience,
      {
        company: "",
        role: "",
        location: "",
        startDate: "",
        endDate: "",
        responsibilities: "",
      },
    ]);
  const addProject = () =>
    setProjects([
      ...projects,
      { name: "", description: "", technologies: "", startDate: "", endDate: "" },
    ]);
  const addEducation = () =>
    setEducation([
      ...education,
      {
        institution: "",
        degree: "",
        location: "",
        startYear: "",
        endYear: "",
      },
    ]);

  const handlePersonalDetailsChange = (field, value) => {
    setPersonalDetails({ ...personalDetails, [field]: value });
  };

  const handleExperienceChange = (index, field, value) => {
    const updatedExperience = [...experience];
    updatedExperience[index][field] = value;
    setExperience(updatedExperience);
  };

  const handleProjectChange = (index, field, value) => {
    const updatedProjects = [...projects];
    updatedProjects[index][field] = value;
    setProjects(updatedProjects);
  };

  const handleSkillsChange = (field, value) => {
    setSkills({ ...skills, [field]: value });
  };

  const handleEducationChange = (index, field, value) => {
    const updatedEducation = [...education];
    updatedEducation[index][field] = value;
    setEducation(updatedEducation);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={styles["resume-form-container"]}
    >
      <h1 className={styles["form-heading"]}>Enter Your Details</h1>
      <form onSubmit={handleSubmit} className={styles["form-body"]}>
        <Accordion title="Personal Details">
          <div className={styles["form-section"]}>
            <div className={styles["input-group"]}>
              <input
                type="text"
                placeholder="Name"
                value={personalDetails.name}
                onChange={(e) => handleNameChange(e.target.value)}
                className={styles["form-input"]}
              />
              <input
                type="text"
                placeholder="Email"
                value={personalDetails.email}
                onChange={(e) =>
                  handlePersonalDetailsChange("email", e.target.value)
                }
                className={styles["form-input"]}
              />
            </div>
            <div className={styles["input-group"]}>
              <input
                type="text"
                placeholder="Phone"
                value={personalDetails.phone}
                onChange={(e) =>
                  handlePersonalDetailsChange("phone", e.target.value)
                }
                className={styles["form-input"]}
              />
              <input
                type="text"
                placeholder="LinkedIn"
                value={personalDetails.linkedin}
                onChange={(e) =>
                  handlePersonalDetailsChange("linkedin", e.target.value)
                }
                className={styles["form-input"]}
              />
              <input
                type="text"
                placeholder="GitHub"
                value={personalDetails.github}
                onChange={(e) =>
                  handlePersonalDetailsChange("github", e.target.value)
                }
                className={styles["form-input"]}
              />
            </div>
          </div>
        </Accordion>

        {/* Experience */}
        <Accordion title="Experience">
          <div className={styles["form-section"]}>
            {experience.map((exp, index) => (
              <div key={index} className={styles["form-group"]}>
                <div className={styles["input-group"]}>
                  <input
                    type="text"
                    placeholder="Company"
                    value={exp.company}
                    onChange={(e) =>
                      handleExperienceChange(index, "company", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                  <input
                    type="text"
                    placeholder="Role"
                    value={exp.role}
                    onChange={(e) =>
                      handleExperienceChange(index, "role", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                </div>
                <div className={styles["input-group"]}>
                  <input
                    type="text"
                    placeholder="Location"
                    value={exp.location}
                    onChange={(e) =>
                      handleExperienceChange(index, "location", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                  <input
                    type="text"
                    placeholder="Start Date"
                    value={exp.startDate}
                    onChange={(e) =>
                      handleExperienceChange(index, "startDate", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                  <input
                    type="text"
                    placeholder="End Date"
                    value={exp.endDate}
                    onChange={(e) =>
                      handleExperienceChange(index, "endDate", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                </div>
                <textarea
                  placeholder="Responsibilities"
                  value={exp.responsibilities}
                  onChange={(e) =>
                    handleExperienceChange(
                      index,
                      "responsibilities",
                      e.target.value
                    )
                  }
                  className={styles["form-textarea"]}
                />
              </div>
            ))}
            <button
              type="button"
              onClick={addExperience}
              className={styles["add-button"]}
            >
              Add Experience
            </button>
          </div>
        </Accordion>

        {/* Projects */}
        <Accordion title="Projects">
          <div className={styles["form-section"]}>
            {projects.map((proj, index) => (
              <div key={index} className={styles["form-group"]}>
                <input
                  type="text"
                  placeholder="Project Name"
                  value={proj.name}
                  onChange={(e) =>
                    handleProjectChange(index, "name", e.target.value)
                  }
                  className={styles["form-input"]}
                />
                <textarea
                  placeholder="Description"
                  value={proj.description}
                  onChange={(e) =>
                    handleProjectChange(index, "description", e.target.value)
                  }
                  className={styles["form-textarea"]}
                />
                <input
                  type="text"
                  placeholder="Technologies Used"
                  value={proj.technologies}
                  onChange={(e) =>
                    handleProjectChange(index, "technologies", e.target.value)
                  }
                  className={styles["form-input"]}
                />
                <div className={styles["input-group"]}>
                  <input
                    type="text"
                    placeholder="Start Date"
                    value={proj.startDate}
                    onChange={(e) =>
                      handleProjectChange(index, "startDate", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                  <input
                    type="text"
                    placeholder="End Date"
                    value={proj.endDate}
                    onChange={(e) =>
                      handleProjectChange(index, "endDate", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                </div>
              </div>
            ))}
            <button
              type="button"
              onClick={addProject}
              className={styles["add-button"]}
            >
              Add Project
            </button>
          </div>
        </Accordion>

        {/* Skills */}
        <Accordion title="Technical Skills">
          <div className={styles["form-section"]}>
            <div className={styles["input-group"]}>
              <input
                type="text"
                placeholder="Languages"
                value={skills.languages}
                onChange={(e) =>
                  handleSkillsChange("languages", e.target.value)
                }
                className={styles["form-input"]}
              />
              <input
                type="text"
                placeholder="Frameworks"
                value={skills.frameworks}
                onChange={(e) =>
                  handleSkillsChange("frameworks", e.target.value)
                }
                className={styles["form-input"]}
              />
              <input
                type="text"
                placeholder="Developer Tools"
                value={skills.developerTools}
                onChange={(e) =>
                  handleSkillsChange("developerTools", e.target.value)
                }
                className={styles["form-input"]}
              />
              <input
                type="text"
                placeholder="Libraries"
                value={skills.libraries}
                onChange={(e) =>
                  handleSkillsChange("libraries", e.target.value)
                }
                className={styles["form-input"]}
              />
            </div>
          </div>
        </Accordion>

        {/* Education */}
        <Accordion title="Education">
          <div className={styles["form-section"]}>
            {education.map((edu, index) => (
              <div key={index} className={styles["form-group"]}>
                <input
                  type="text"
                  placeholder="Institution"
                  value={edu.institution}
                  onChange={(e) =>
                    handleEducationChange(index, "institution", e.target.value)
                  }
                  className={styles["form-input"]}
                />
                <div className={styles["input-group"]}>
                  <input
                    type="text"
                    placeholder="Degree"
                    value={edu.degree}
                    onChange={(e) =>
                      handleEducationChange(index, "degree", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                  <input
                    type="text"
                    placeholder="Location"
                    value={edu.location}
                    onChange={(e) =>
                      handleEducationChange(index, "location", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                </div>
                <div className={styles["input-group"]}>
                  <input
                    type="text"
                    placeholder="Start Year"
                    value={edu.startYear}
                    onChange={(e) =>
                      handleEducationChange(index, "startYear", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                  <input
                    type="text"
                    placeholder="End Year"
                    value={edu.endYear}
                    onChange={(e) =>
                      handleEducationChange(index, "endYear", e.target.value)
                    }
                    className={styles["form-input"]}
                  />
                </div>
              </div>
            ))}
            <button
              type="button"
              onClick={addEducation}
              className={styles["add-button"]}
            >
              Add Education
            </button>
          </div>
        </Accordion>

        <button type="submit" className={styles["submit-button"]}>
          Submit
        </button>
      </form>
    </motion.div>
  );
};

export default PersonalDetailsForm;