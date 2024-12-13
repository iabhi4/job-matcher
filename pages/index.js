import { useRouter } from "next/router";
import { useState, useEffect } from "react";
import PersonalDetailsForm from "../components/PersonalDetailsForm";
import RuleCreationForm from "../components/RuleCreationForm";
import axios from "../utils/api";

const IndexPage = () => {
  const router = useRouter();
  const [showDetailsForm, setShowDetailsForm] = useState(false);
  const [showRulesForm, setShowRulesForm] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkData = async () => {
      try {
        // Check if user data exists
        const userResponse = await axios.get("/api/users/names");
        const names = userResponse.data;
        const userExists = names.length > 0;

        // Check if rules exist for the user
        const rulesResponse = await axios.get("/api/rules/unique_user_id");
        const rulesExist = rulesResponse.data && rulesResponse.data.rules && rulesResponse.data.rules.length > 0;

        if (userExists && rulesExist) {
          router.push("/dashboard");
        } else if (userExists) {
          setShowRulesForm(true);
        } else {
          setShowDetailsForm(true);
        }
      } catch (error) {
        console.error("Error checking data:", error);
        setShowDetailsForm(true);
      } finally {
        setLoading(false);
      }
    };

    checkData();
  }, []);

  const handleDetailsNext = () => {
    setShowDetailsForm(false);
    setShowRulesForm(true);
  };

  const handleRulesNext = () => {
    router.push("/dashboard");
  };

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      {showDetailsForm && <PersonalDetailsForm onNext={handleDetailsNext} />}
      {showRulesForm && <RuleCreationForm onNext={handleRulesNext} />}
    </div>
  );
};

export default IndexPage;