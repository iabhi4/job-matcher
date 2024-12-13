import RuleCreationForm from '../components/RuleCreationForm';
import Navbar from "../components/Navbar";

const RulesPage = () => {
  const handleRulesSubmit = () => {
  };

  return (
    <div>
      <Navbar />
      <RuleCreationForm onNext={handleRulesSubmit} />
    </div>
  );
};

export default RulesPage;