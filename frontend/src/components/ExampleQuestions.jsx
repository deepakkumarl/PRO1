import React from 'react';

const SAMPLES = [
  "What should be checked when an EV reports repeated battery overheating?",
  "What precautions and PPE apply before working on the high-voltage system?",
  "How is the 3-Point Voltage-Free Verification Test performed on BMW HV systems?",
  "What symptoms indicate a cooling-system issue on electric drive vehicles?",
  "What does diagnostic trouble code 21F004 indicate in ISTA?",
];

const ExampleQuestions = ({ onSelectQuestion }) => {
  return (
    <div className="example-questions-container">
      <h4 className="example-title">Suggested Technician Queries:</h4>
      <div className="example-chips">
        {SAMPLES.map((q, idx) => (
          <button
            key={idx}
            className="example-chip"
            onClick={() => onSelectQuestion(q)}
          >
            <span className="chip-icon">💡</span>
            {q}
          </button>
        ))}
      </div>
    </div>
  );
};

export default ExampleQuestions;
